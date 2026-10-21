"""The golden contract suite must execute assertions, not canned responses."""
import json
from pathlib import Path
import subprocess
import sys


def test_benchmark_has_distinct_executable_contracts():
    cases=json.loads(Path('evals/golden/runtime-contracts.json').read_text())['cases']
    assert len(cases)>=50
    assert len({c['id'] for c in cases})==len(cases)
    assert len({c['node'] for c in cases})==len(cases)
    assert all(c['description'] and c['category'] for c in cases)


def test_benchmark_cli_rejects_stale_baseline(tmp_path):
    baseline=tmp_path/'baseline.json';baseline.write_text(json.dumps({'suite_sha256':'stale','results':[]}))
    p=subprocess.run([sys.executable,'-m','runtime.benchmark','--baseline',str(baseline),'--output',str(tmp_path/'report.json')],capture_output=True,text=True)
    assert p.returncode==2 and 'baseline' in p.stderr.lower()
