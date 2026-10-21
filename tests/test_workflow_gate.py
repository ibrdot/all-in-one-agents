import importlib.util
from pathlib import Path
import sys
import pytest

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('gate',ROOT/'scripts/workflow_gate.py')
gate=importlib.util.module_from_spec(spec); spec.loader.exec_module(gate)


def check(code,**kw):
    return dict(id='test',command=[sys.executable,'-c',code],**kw)


def test_pass_and_capture(tmp_path):
    r=gate.run_checks([check('print("evidence")')],tmp_path)
    assert r['passed'] and r['checks'][0]['stdout_tail']=='evidence\n'


def test_failure(tmp_path):
    assert not gate.run_checks([check('raise SystemExit(3)')],tmp_path)['passed']


def test_expected_red_then_green(tmp_path):
    # A regression demonstration, not a claim to evaluate a model's TDD behavior.
    checks=[dict(id='red',command=[sys.executable,'-c','assert 1 == 2'],expect_exit=1),
            dict(id='green',command=[sys.executable,'-c','assert 1 == 1'])]
    assert gate.run_checks(gate.validate({'checks':checks}),tmp_path)['passed']


def test_timeout(tmp_path):
    r=gate.run_checks([check('import time; time.sleep(2)',timeout=.05)],tmp_path)
    assert not r['passed'] and r['checks'][0]['error']=='timeout'


def test_missing_binary(tmp_path):
    assert not gate.run_checks([dict(id='missing',command=['/nonexistent/binary'])],tmp_path)['passed']


def test_bounded_report(tmp_path):
    r=gate.run_checks([check('print("x"*10000)')],tmp_path)
    assert len(r['checks'][0]['stdout_tail'])==4096


@pytest.mark.parametrize('plan',[{}, {'checks':[]}, {'checks':[dict(id='x',command='echo x')]},
    {'checks':[check('pass'),check('pass')]}, {'checks':[check('pass',timeout=0)]},
    {'checks':[check('pass',timeout=float('nan'))]}, {'checks':[check('pass',expect_exit=True)]}])
def test_bad_plans(plan):
    with pytest.raises(ValueError): gate.validate(plan)
