#!/usr/bin/env python3
"""Run explicit local acceptance checks and emit machine-readable evidence.
Only execute a plan you have reviewed: its commands run with your permissions.
No shell expansion, no remote upload, no model calls. Not an agent benchmark.
Exit 0: all checks pass; 1: failed check/timeout; 2: invalid plan.
"""
import argparse
import json
import math
from pathlib import Path
import subprocess
import sys
import tempfile
import time


def validate(plan):
    if not isinstance(plan, dict) or not isinstance(plan.get('checks'), list) or not plan['checks']:
        raise ValueError('plan requires a nonempty checks list')
    seen = set()
    for check in plan['checks']:
        if not isinstance(check, dict):
            raise ValueError('each check must be an object')
        name, command = check.get('id'), check.get('command')
        if not isinstance(name, str) or not name or name in seen:
            raise ValueError('check ids must be nonempty and unique')
        seen.add(name)
        if not isinstance(command, list) or not command or any(not isinstance(s, str) or '\0' in s for s in command) or not command[0]:
            raise ValueError(f'{name}: command must be an argv array')
        timeout = check.get('timeout', 30)
        if isinstance(timeout, bool) or not isinstance(timeout, (int,float)) or not math.isfinite(timeout) or timeout <= 0 or timeout > 3600:
            raise ValueError(f'{name}: timeout must be 0 < seconds <= 3600')
        expected = check.get('expect_exit', 0)
        if type(expected) is not int or expected < 0 or expected > 255:
            raise ValueError(f'{name}: invalid expected exit code')
    return plan['checks']


def run_checks(checks, root):
    results = []
    for check in checks:
        started = time.monotonic()
        # Bound memory use. Output stays in temporary files; reports include a
        # short tail only. Disk usage remains dependent on the reviewed command.
        with tempfile.TemporaryFile() as out, tempfile.TemporaryFile() as err:
            status, code, error = 'passed', None, None
            try:
                proc = subprocess.run(check['command'], cwd=root, stdout=out, stderr=err,
                                      timeout=check.get('timeout',30), shell=False)
                code = proc.returncode
                if code != check.get('expect_exit',0):
                    status = 'failed'
            except subprocess.TimeoutExpired:
                status, error = 'failed', 'timeout'
            except OSError as exc:
                status, error = 'failed', str(exc)
            tails = {}
            for key, stream in [('stdout_tail',out),('stderr_tail',err)]:
                size=stream.tell()
                stream.seek(max(0,size-4096))
                tails[key]=stream.read().decode('utf-8',errors='replace')
            results.append(dict(id=check['id'],command=check['command'],status=status,
                                exit_code=code,error=error,seconds=round(time.monotonic()-started,3),**tails))
    return dict(passed=all(r['status']=='passed' for r in results),checks=results)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('plan',type=Path)
    parser.add_argument('--root',type=Path,default=Path.cwd())
    args=parser.parse_args()
    try:
        checks=validate(json.loads(args.plan.read_text(encoding='utf-8')))
        if not args.root.is_dir():
            raise ValueError('root is not a directory')
    except (ValueError,OSError) as exc:
        print(f'plan error: {exc}',file=sys.stderr)
        return 2
    result=run_checks(checks,args.root.resolve())
    print(json.dumps(result,indent=2))
    return 0 if result['passed'] else 1


if __name__=='__main__':
    sys.exit(main())
