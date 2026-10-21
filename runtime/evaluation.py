"""Deterministic golden-response scoring and non-destructive improvement proposals.
Exact-output checks are narrow acceptance tests, not reasoning-quality judges.
"""
import hashlib
import json
from pathlib import Path


def evaluate(cases,responses,baseline=None):
    if not isinstance(cases,list) or not cases:raise ValueError('nonempty cases required')
    if not isinstance(responses,dict):raise ValueError('response mapping required')
    results=[];seen=set()
    for case in cases:
        key=case['id']
        if not isinstance(key,str) or not key or key in seen:raise ValueError('case ids must be unique')
        seen.add(key)
        # No regex execution or model-based judgment hidden in this scorer.
        if not ('exact' in case or case.get('contains') or case.get('forbidden')):
            raise ValueError('case requires an assertion')
        if 'exact' in case and not isinstance(case['exact'],str):
            raise ValueError('exact assertion must be text')
        for field in ('contains','forbidden'):
            if field in case and (not isinstance(case[field],list) or any(not isinstance(v,str) or not v for v in case[field])):
                raise ValueError('assertions must be nonempty strings')
        response=responses.get(key); reasons=[]
        if not isinstance(response,str): reasons.append('missing text response')
        else:
            if 'exact' in case and response!=case['exact']:reasons.append('exact mismatch')
            if any(s not in response for s in case.get('contains',[])):reasons.append('required text missing')
            if any(s in response for s in case.get('forbidden',[])):reasons.append('forbidden text present')
        results.append(dict(id=key,passed=not reasons,reasons=reasons,skill=case.get('skill')))
    regressions=[]
    if baseline:
        previous={r['id']:r['passed'] for r in baseline['results']}
        regressions=[r['id'] for r in results if previous.get(r['id']) is True and not r['passed']]
    return dict(total=len(results),passed=sum(r['passed'] for r in results),results=results,regressions=regressions)


def propose_improvement(skill_path,report,candidate):
    """Return a reviewable candidate only; never overwrite skill content."""
    path=Path(skill_path)
    if not isinstance(candidate,str) or not candidate.strip():raise ValueError('nonempty candidate required')
    failed=[r['id'] for r in report['results'] if not r['passed'] and r.get('skill')==path.parent.name]
    if not failed:raise ValueError('no failed evaluations attributed to this skill')
    return dict(skill=str(path),original_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                failing_cases=failed,candidate=candidate,status='needs_review_and_re_evaluation')


def main():
    import argparse
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('cases',type=Path);parser.add_argument('responses',type=Path)
    parser.add_argument('--baseline',type=Path)
    args=parser.parse_args()
    try:
        load=lambda p:json.loads(p.read_text(encoding='utf-8'))
        result=evaluate(load(args.cases),load(args.responses),load(args.baseline) if args.baseline else None)
    except (OSError,ValueError,KeyError,TypeError) as exc:
        print(f'evaluation error: {exc}',file=__import__('sys').stderr);return 2
    print(json.dumps(result,indent=2))
    return int(result['passed']!=result['total'] or bool(result['regressions']))


if __name__=='__main__':raise SystemExit(main())
