"""Black-box regressions for the shipped command line tools."""
import json
from pathlib import Path
import subprocess
import sys
import pytest

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / 'skills/ai-code-audit/scripts/audit_diff.py'
COST = ROOT / 'skills/cost-optimization/scripts/token_cost_report.py'


def cli(script, *args, stdin=''):
    return subprocess.run([sys.executable, str(script), *map(str, args)], input=stdin, capture_output=True, text=True)


def test_audit_multiline_except(tmp_path):
    p = tmp_path / 'bad.py'
    p.write_text('try:\n    work()\nexcept Exception:\n    pass\n')
    r = cli(AUDIT, '--format', 'json', p)
    assert r.returncode == 1
    assert json.loads(r.stdout)['findings'][0]['line'] == 3


def test_audit_comments_and_strings_are_not_code(tmp_path):
    p = tmp_path / 'ok.py'
    p.write_text('# eval(user)\nx = "eval(user)"\nassert x is not None\n')
    assert cli(AUDIT, p).returncode == 0


def test_audit_diff_line_numbers():
    diff = '--- a/a.py\n+++ b/a.py\n@@ -40,0 +41,2 @@\n+eval(user)\n+print(1)\n'
    r = cli(AUDIT, '--format', 'json', stdin=diff)
    assert r.returncode == 1
    assert json.loads(r.stdout)['findings'][0]['line'] == 41


def test_audit_removed_lines_ignored():
    r = cli(AUDIT, stdin='--- a/a.py\n+++ b/a.py\n@@ -1 +1 @@\n-eval(user)\n+print(1)\n')
    assert r.returncode == 0


def test_audit_missing_file_fails_closed(tmp_path):
    assert cli(AUDIT, tmp_path / 'missing.py').returncode == 2


def test_audit_syntax_error_fails_closed(tmp_path):
    p = tmp_path / 'bad.py'
    p.write_text('def broken(:\n')
    assert cli(AUDIT, p).returncode == 2


def test_audit_sarif(tmp_path):
    p = tmp_path / 'a.py'
    p.write_text('exec(user)\n')
    r = cli(AUDIT, '--format', 'sarif', p)
    data = json.loads(r.stdout)
    assert data['version'] == '2.1.0'
    assert data['runs'][0]['results'][0]['ruleId'] == 'dynamic-exec'


def test_audit_parameterized_sql_is_safe(tmp_path):
    p = tmp_path / 'a.py'
    p.write_text('cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))\n')
    assert cli(AUDIT, p).returncode == 0


@pytest.mark.parametrize('expression', ['f"SELECT * FROM users WHERE id={user}"', '"SELECT * FROM users WHERE id=" + user', '"SELECT * FROM users WHERE id=%s" % user'])
def test_audit_dynamic_sql(tmp_path, expression):
    p = tmp_path / 'a.py'
    p.write_text(f'cursor.execute({expression})\n')
    r = cli(AUDIT, '--format', 'json', p)
    assert r.returncode == 1
    assert any(f['rule'] == 'sql-interp' for f in json.loads(r.stdout)['findings'])


@pytest.fixture
def prices(tmp_path):
    p = tmp_path / 'prices.json'
    p.write_text(json.dumps({'test-model': {'input': '2', 'output': '6'}}))
    return p


def record(**kw):
    return json.dumps(dict(model='test-model', input=1000000, output=500000, route='chat', **kw))


def test_cost_multiple_files_and_exact_decimal(tmp_path, prices):
    a, b = tmp_path/'a.jsonl', tmp_path/'b.jsonl'
    a.write_text(record()+'\n')
    b.write_text(record()+'\n')
    r = cli(COST, '--pricing', prices, '--format', 'json', a, b)
    assert r.returncode == 0
    d = json.loads(r.stdout)
    assert d['calls'] == 2
    assert d['total_usd'] == '10.000000'
    assert d['routes'][0]['route'] == 'chat'


def test_cost_budget_exit(prices):
    r = cli(COST, '--pricing', prices, '--budget', '4.99', stdin=record())
    assert r.returncode == 1


def test_cost_budget_equal_is_ok(prices):
    assert cli(COST, '--pricing', prices, '--budget', '5', stdin=record()).returncode == 0


@pytest.mark.parametrize('bad', ['not json', '[]', 'null', '{"model":"unknown","input":1,"output":2}', '{"model":"test-model","input":-1,"output":2}', '{"model":"test-model","input":true,"output":2}', '{"model":"test-model","input":1.5,"output":2}', '{"model":"test-model","input":1}', '{"model":"test-model","input":1,"output":2,"route":[]}'])
def test_cost_rejects_invalid_records(prices, bad):
    r = cli(COST, '--pricing', prices, stdin=bad)
    assert r.returncode == 2
    assert 'line 1' in r.stderr


def test_cost_no_pricing_never_guesses():
    r = cli(COST, stdin=record())
    assert r.returncode == 2
    assert 'pricing' in r.stderr.lower()


def test_cost_empty_input(prices):
    r = cli(COST, '--pricing', prices, '--format', 'json')
    assert r.returncode == 0
    assert json.loads(r.stdout)['calls'] == 0


@pytest.mark.parametrize('value', ['NaN', '-1', 'Infinity', 'oops'])
def test_cost_invalid_budget(prices, value):
    assert cli(COST, '--pricing', prices, '--budget', value, stdin=record()).returncode == 2


def test_cost_invalid_price_file(tmp_path):
    p = tmp_path/'prices.json'
    p.write_text('{"test-model":{"input":-1,"output":2}}')
    assert cli(COST, '--pricing', p, stdin=record()).returncode == 2


def test_audit_multiple_hunks_context_and_removed():
    diff = ('--- a/a.py\n+++ b/a.py\n@@ -10,2 +10,3 @@\n keep\n-old\n+exec(user)\n+new\n'
            '@@ -100 +101 @@\n-before\n+eval(user)\n')
    r = cli(AUDIT, '--format', 'json', stdin=diff)
    assert [f['line'] for f in json.loads(r.stdout)['findings']] == [11, 101]


def test_audit_multiple_diff_files():
    diff = ('--- a/a.py\n+++ b/a.py\n@@ -0,0 +1 @@\n+eval(a)\n'
            '--- a/b.py\n+++ b/b.py\n@@ -0,0 +9 @@\n+exec(b)\n')
    r = cli(AUDIT, '--format', 'json', stdin=diff)
    assert [(f['path'], f['line']) for f in json.loads(r.stdout)['findings']] == [('a.py', 1), ('b.py', 9)]


def test_audit_handler_logging_not_swallowed(tmp_path):
    p = tmp_path/'a.py'
    p.write_text('try:\n    work()\nexcept Exception:\n    log.exception("failed")\n    raise\n')
    assert cli(AUDIT, p).returncode == 0


def test_audit_sql_format(tmp_path):
    p = tmp_path/'a.py'
    p.write_text('cursor.execute("SELECT * FROM users WHERE id={}".format(user))\n')
    assert cli(AUDIT, p).returncode == 1


def test_audit_long_line_not_silently_skipped(tmp_path):
    p = tmp_path/'a.py'
    p.write_text('x = ' + ' '*500 + 'eval(user)\n')
    assert cli(AUDIT, p).returncode == 1


def test_cost_missing_file(prices, tmp_path):
    assert cli(COST, '--pricing', prices, tmp_path/'missing').returncode == 2


def test_cost_blank_lines_and_missing_route(prices):
    r = cli(COST, '--pricing', prices, '--format', 'json', stdin='\n{"model":"test-model","input":0,"output":0}\n\n')
    assert r.returncode == 0
    assert json.loads(r.stdout)['routes'] == [{'route': 'unrouted', 'cost_usd': '0.000000'}]


def test_cost_invalid_record_does_not_emit_partial_success(prices):
    r = cli(COST, '--pricing', prices, '--format', 'json', stdin=record()+'\n[]\n')
    assert r.returncode == 2
    assert r.stdout == ''
    assert 'line 2' in r.stderr


def test_cost_repeated_stdin_rejected(prices):
    assert cli(COST, '--pricing', prices, '-', '-', stdin=record()).returncode == 2


def test_cost_real_decimal_fraction(prices):
    r = cli(COST, '--pricing', prices, '--format', 'json', stdin='{"model":"test-model","input":1,"output":1}')
    assert json.loads(r.stdout)['total_usd'] == '0.000008'
