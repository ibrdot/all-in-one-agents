"""Run reviewed offline golden contracts through pytest, detect baseline regressions.

The suite contains executable node IDs. Review before running: tests are code.
No live provider calls, canned model-quality scores, or invented responses.
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]


def run_suite(suite, baseline=None):
    raw = Path(suite).read_bytes()
    fingerprint = hashlib.sha256(raw).hexdigest()
    cases = json.loads(raw)['cases']
    if not isinstance(cases, list) or not cases: raise ValueError('nonempty suite required')
    ids = [c['id'] for c in cases]; nodes = [c['node'] for c in cases]
    if len(set(ids)) != len(ids) or len(set(nodes)) != len(nodes):
        raise ValueError('duplicate suite ids or test nodes')
    if baseline and baseline.get('suite_sha256') != fingerprint:
        raise ValueError('baseline suite mismatch; explicit rebaseline required')
    for node in nodes:
        if not isinstance(node, str) or '::test_' not in node or not node.startswith('tests/') or '..' in Path(node.split('::')[0]).parts:
            raise ValueError('invalid test node')
    results = []
    # Run one contract per subprocess: failures cannot silently hide another node.
    for case in cases:
        started = time.monotonic()
        with tempfile.TemporaryDirectory() as directory:
            xml = Path(directory) / 'result.xml'
            try:
                with tempfile.TemporaryFile() as log:
                    p = subprocess.run([sys.executable, '-m', 'pytest', case['node'], '-q',
                                        '--junitxml', str(xml)], cwd=ROOT, stdout=log,
                                       stderr=subprocess.STDOUT, timeout=60)
                root = ET.parse(xml).getroot()
                testcases = list(root.iter('testcase'))
                # Skips/xfails are not successful acceptance evidence.
                passed = p.returncode == 0 and len(testcases) == 1 and not any(child.tag in ('failure', 'error', 'skipped') for child in testcases[0])
                reason = None if passed else 'test failed, skipped, missing or unexpectedly expanded'
            except (OSError, ET.ParseError, subprocess.TimeoutExpired):
                passed, reason = False, 'execution timeout or report failure'
        results.append(dict(id=case['id'], node=case['node'], passed=passed,
                            reason=reason, seconds=round(time.monotonic()-started, 3)))
    if baseline and (len({r['id'] for r in baseline['results']}) != len(baseline['results']) or any(type(r['passed']) is not bool for r in baseline['results'])):
        raise ValueError('baseline ids must be unique and statuses boolean')
    previous = {r['id']: r['passed'] for r in baseline['results']} if baseline else {}
    regressions = [r['id'] for r in results if previous.get(r['id']) is True and not r['passed']]
    return dict(kind='offline runtime contract benchmark', suite_sha256=fingerprint,
                total=len(results), passed=sum(r['passed'] for r in results),
                regressions=regressions, results=results)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--suite', type=Path, default=ROOT/'evals/golden/runtime-contracts.json')
    parser.add_argument('--baseline', type=Path)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    try:
        baseline = json.loads(args.baseline.read_text()) if args.baseline else None
        report = run_suite(args.suite, baseline)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, indent=2)+'\n')
    except (ValueError, OSError, KeyError, TypeError) as exc:
        print(f'benchmark configuration/baseline error: {exc}', file=sys.stderr)
        return 2
    print(json.dumps({k: v for k, v in report.items() if k != 'results'}, indent=2))
    return int(report['passed'] != report['total'] or bool(report['regressions']))


if __name__ == '__main__': raise SystemExit(main())
