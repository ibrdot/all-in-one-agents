"""Objective task grading. Python subprocess resource limits are NOT a sandbox.

Run untrusted candidates only in a disposable isolated environment with no secrets
or network. Explicit allow_code_execution is required; JSON grading runs no code.
"""
import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import signal
import subprocess
import sys
import tempfile
import time


def load_tasks(path):
    tasks=_json(Path(path).read_text())['tasks']
    if not isinstance(tasks,list) or not 1<=len(tasks)<=200:raise ValueError('nonempty tasks required')
    ids=set()
    for t in tasks:
        if not isinstance(t,dict):raise ValueError('task object required')
        if not isinstance(t['id'],str) or not t['id'] or t['id'] in ids:raise ValueError('unique ids required')
        ids.add(t['id'])
        if t['kind'] not in ('json','python') or not isinstance(t['checks'],list) or not 1<=len(t['checks'])<=20 or not isinstance(t['prompt'],str) or not 1<=len(t['prompt'])<=20000:raise ValueError('invalid task')
        for check in t['checks']:
            if not isinstance(check,dict):raise ValueError('check object required')
            if t['kind']=='python' and (not isinstance(check.get('args'),list) or 'expected' not in check):raise ValueError('Python args/expected required')
            if t['kind']=='json' and (not isinstance(check.get('path'),list) or 'equals' not in check):raise ValueError('JSON path/equals required')
    return tasks


def _same(a,b):
    # Avoid Python bool == int and permit integer/float numeric equivalents.
    if isinstance(a,bool) or isinstance(b,bool):return type(a) is type(b) and a==b
    if isinstance(a,(int,float)) and isinstance(b,(int,float)):
        return math.isfinite(a) and math.isfinite(b) and math.isclose(a,b,rel_tol=1e-9,abs_tol=1e-9)
    if type(a) is not type(b):return False
    if isinstance(a,dict):return a.keys()==b.keys() and all(_same(a[k],b[k]) for k in a)
    if isinstance(a,list):return len(a)==len(b) and all(_same(x,y) for x,y in zip(a,b))
    return a==b


def _json(raw):
    def unique(pairs):
        result={}
        for key,value in pairs:
            if key in result:raise ValueError('duplicate JSON key')
            result[key]=value
        return result
    return json.loads(raw,object_pairs_hook=unique,parse_constant=lambda x:(_ for _ in ()).throw(ValueError('nonfinite JSON')))


_RUNNER='''import json,runpy,sys,resource
resource.setrlimit(resource.RLIMIT_CPU,(2,2))
resource.setrlimit(resource.RLIMIT_AS,(256*1024*1024,256*1024*1024))
resource.setrlimit(resource.RLIMIT_FSIZE,(1024*1024,1024*1024))
namespace=runpy.run_path('candidate.py')
args=json.loads(sys.stdin.read())
result=namespace['solve'](*args)
print(json.dumps(result,allow_nan=False))
'''


def grade(task,response,allow_code_execution=False,timeout=3):
    if not isinstance(response,str) or not response.strip() or len(response.encode())>200000:
        return dict(passed=False,reason='missing, empty or oversized response',checks=[])
    if task['kind']=='python' and not allow_code_execution:
        raise ValueError('Python grading requires explicit allow_code_execution; limits are NOT a sandbox')
    if not isinstance(timeout,(int,float)) or not math.isfinite(timeout) or not 0<timeout<=60:raise ValueError('invalid timeout')
    results=[]
    if task['kind']=='json':
        try:
            value=_json(response)
            for check in task['checks']:
                item=value
                for key in check['path']:item=item[key]
                results.append(_same(item,check['equals']))
        except (ValueError,TypeError,KeyError,IndexError,RecursionError):
            return dict(passed=False,reason='invalid or structurally incorrect JSON',checks=[])
    elif task['kind']=='python':
        if os.name!='posix':raise ValueError('Python grader requires POSIX resource limits')
        for check in task['checks']:
            with tempfile.TemporaryDirectory() as directory:
                Path(directory,'candidate.py').write_text(response)
                Path(directory,'runner.py').write_text(_RUNNER)
                # Secret environment variables are not inherited. Files/network
                # remain accessible: use a real sandbox for untrusted candidates.
                with tempfile.TemporaryFile() as out, tempfile.TemporaryFile() as err:
                    proc=subprocess.Popen([sys.executable,'-I','runner.py'],cwd=directory,stdin=subprocess.PIPE,
                                          stdout=out,stderr=err,start_new_session=True,
                                          env={'PATH':os.defpath,'LC_ALL':'C.UTF-8'})
                    try:
                        proc.communicate(json.dumps(check['args']).encode(),timeout=timeout)
                        out.seek(0);raw=out.read(1048577)
                        result=proc.returncode==0 and len(raw)<=1048576 and _same(_json(raw),check['expected'])
                    except (subprocess.TimeoutExpired,ValueError,UnicodeError,RecursionError):result=False
                    finally:
                        try:os.killpg(proc.pid,signal.SIGKILL)
                        except ProcessLookupError:pass
                        proc.wait()
                    results.append(result)
    else:raise ValueError('unknown task kind')
    return dict(passed=bool(results) and all(results),reason=None if results and all(results) else 'objective checks failed',checks=results)


def fingerprint(tasks):
    return hashlib.sha256(json.dumps(tasks,sort_keys=True,separators=(',',':')).encode()).hexdigest()


def evaluate(tasks,responses,output,source='replay',allow_code_execution=False,metadata=None):
    if source not in ('replay','live','reference-calibration'):raise ValueError('explicit result source required')
    if any(t['kind']=='python' and t['id'] in responses for t in tasks) and not allow_code_execution:
        raise ValueError('Python candidates require explicit execution consent')
    output=Path(output);output.mkdir(parents=True,exist_ok=False,mode=0o700)
    results=[]
    for task in tasks:
        start=time.monotonic()
        result=grade(task,responses[task['id']],allow_code_execution) if task['id'] in responses else dict(passed=False,reason='missing response',checks=[])
        results.append(dict(id=task['id'],kind=task['kind'],seconds=round(time.monotonic()-start,4),**result))
    report=dict(suite_sha256=fingerprint(tasks),source=source,total=len(tasks),passed=sum(r['passed'] for r in results),
                results=results,metadata=metadata or {},grader_isolation='resource limits only; NOT a sandbox; checks not secret from same-user code',scope='objective microtasks, not unrestricted agent autonomy')
    raw=json.dumps(responses,indent=2).encode();(output/'responses.json').write_bytes(raw)
    report['responses_sha256']=hashlib.sha256(raw).hexdigest()
    (output/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    return report


def compare(report,baseline):
    if report.get('source') and baseline.get('source') and report['source']!=baseline['source']:
        raise ValueError('cross-source baseline comparison refused')
    if report['suite_sha256']!=baseline['suite_sha256']:raise ValueError('suite mismatch; explicit rebaseline required')
    def statuses(r):
        rows=r['results']
        if len({x['id'] for x in rows})!=len(rows) or any(type(x['passed']) is not bool for x in rows):raise ValueError('invalid result rows')
        return {x['id']:x['passed'] for x in rows}
    now,old=statuses(report),statuses(baseline)
    if now.keys()!=old.keys():raise ValueError('task id mismatch')
    return sorted(k for k,v in old.items() if v and not now[k])


def generate(tasks,provider,model,max_calls):
    """Generate from public prompts only; grading is a separate operation."""
    if type(max_calls) is not int or max_calls<1 or len(tasks)>max_calls:
        raise ValueError('explicit call cap too small or invalid')
    if not isinstance(model,str) or not model.strip():raise ValueError('explicit model required')
    responses={};errors={}
    for task in tasks:
        try:
            response=provider(model,[{'role':'system','content':'Follow the task output format exactly.'},
                                     {'role':'user','content':task['prompt']}])
            if not isinstance(response,str) or not response.strip():raise ValueError('empty response')
            responses[task['id']]=response
        except Exception as exc:
            errors[task['id']]=type(exc).__name__
    return dict(source='live',model=model,responses=responses,errors=errors,
                suite_sha256=fingerprint(tasks),call_cap=max_calls)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--tasks',type=Path,default=Path(__file__).resolve().parents[1]/'evals/tasks/tasks.json')
    parser.add_argument('--responses',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--baseline',type=Path)
    parser.add_argument('--source',choices=['replay','reference-calibration'],default='replay',help='Operator label, not authenticated provenance')
    parser.add_argument('--allow-code-execution',action='store_true')
    args=parser.parse_args()
    try:
        payload=json.loads(args.responses.read_text())
        source=args.source
        tasks=load_tasks(args.tasks)
        if payload.get('suite_sha256') and payload['suite_sha256']!=fingerprint(tasks):raise ValueError('response suite mismatch')
        report=evaluate(tasks,payload['responses'],args.output,source,args.allow_code_execution,metadata=dict(model=payload.get('model'),reported_generation_source=payload.get('source'),provenance='operator label; unauthenticated'))
        regressions=compare(report,json.loads(args.baseline.read_text())) if args.baseline else []
        print(json.dumps(dict(passed=report['passed'],total=report['total'],source=source,regressions=regressions)))
        return int(report['passed']!=report['total'] or bool(regressions))
    except (ValueError,OSError,KeyError,TypeError,RecursionError) as exc:
        print(f'taskbench failed: {type(exc).__name__}',file=sys.stderr);return 2


if __name__=='__main__':raise SystemExit(main())
