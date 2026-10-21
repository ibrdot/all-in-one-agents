"""Safety and behavior checks for the exact-text editing helper."""
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys

import pytest

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / 'skills/multi-file-editing/scripts/multi_edit.py'
spec = importlib.util.spec_from_file_location('multi_edit', SCRIPT)
helper = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helper)


def entry(path, text=b'old\n', **changes):
    result = dict(sha256=hashlib.sha256(text).hexdigest(), old='old', new='new', count=1)
    result['path'] = path
    result.update(changes)
    return result


def test_preview_is_read_only(tmp_path, capsys):
    target = tmp_path/'a.txt'
    target.write_bytes(b'old\n')
    assert helper.run(tmp_path, [entry('a.txt')]) == 1
    assert target.read_bytes() == b'old\n'
    assert '-old' in capsys.readouterr().out


def test_apply_preserves_crlf_and_mode(tmp_path):
    target = tmp_path/'a.txt'
    before = b'old\r\n'
    target.write_bytes(before)
    target.chmod(0o750)
    helper.run(tmp_path, [entry('a.txt', before)], apply=True)
    assert target.read_bytes() == b'new\r\n'
    assert target.stat().st_mode & 0o777 == 0o750
    assert not list(tmp_path.glob('.multi-edit-*'))


@pytest.mark.parametrize('changes', [
    {'sha256': '0'*64}, {'count': 2}, {'count': True}, {'count': 0},
    {'old': ''}, {'new': 'old'}, {'path': '../outside.txt'},
    {'path': '/etc/passwd'}, {'path': ''}, {'new': 'bad\x00text'},
])
def test_invalid_plans_write_nothing(tmp_path, changes):
    target = tmp_path/'a.txt'
    target.write_bytes(b'old\n')
    plan = entry('a.txt')
    plan.update(changes)
    with pytest.raises((ValueError, OSError)):
        helper.run(tmp_path, [plan], apply=True)
    assert target.read_bytes() == b'old\n'


def test_later_failure_does_not_apply_earlier_entry(tmp_path):
    for name in ('a.txt', 'b.txt'):
        (tmp_path/name).write_bytes(b'old\n')
    with pytest.raises(ValueError):
        helper.run(tmp_path, [entry('a.txt'), entry('b.txt', count=99)], apply=True)
    assert (tmp_path/'a.txt').read_bytes() == b'old\n'


def test_duplicate_paths_rejected(tmp_path):
    (tmp_path/'a.txt').write_bytes(b'old\n')
    with pytest.raises(ValueError):
        helper.run(tmp_path, [entry('a.txt'), entry('./a.txt')], apply=True)


def test_symlink_file_rejected(tmp_path):
    (tmp_path/'a.txt').write_bytes(b'old\n')
    (tmp_path/'link.txt').symlink_to(tmp_path/'a.txt')
    with pytest.raises(ValueError):
        helper.run(tmp_path, [entry('link.txt')], apply=True)


def test_symlink_parent_rejected(tmp_path):
    (tmp_path/'real').mkdir()
    (tmp_path/'real/a.txt').write_bytes(b'old\n')
    (tmp_path/'link').symlink_to(tmp_path/'real', target_is_directory=True)
    with pytest.raises(ValueError):
        helper.run(tmp_path, [entry('link/a.txt')], apply=True)


@pytest.mark.parametrize('before', [b'old\x00', b'\xffold'])
def test_binary_or_invalid_utf8_rejected(tmp_path, before):
    (tmp_path/'a.txt').write_bytes(before)
    with pytest.raises((ValueError, UnicodeError)):
        helper.run(tmp_path, [entry('a.txt', before)], apply=True)


@pytest.mark.parametrize('plan', [None, {}, [], [None]])
def test_malformed_plan_rejected(tmp_path, plan):
    with pytest.raises(ValueError):
        helper.run(tmp_path, plan)


def test_cli_defaults_to_preview_then_applies(tmp_path):
    target = tmp_path/'a.txt'
    target.write_bytes(b'old\n')
    plan = tmp_path/'plan.json'
    plan.write_text(json.dumps([entry('a.txt')]))
    command = [sys.executable, str(SCRIPT), str(plan), '--root', str(tmp_path)]
    preview = subprocess.run(command, capture_output=True, text=True)
    assert preview.returncode == 0
    assert 'no files written' in preview.stdout
    assert target.read_bytes() == b'old\n'
    applied = subprocess.run(command+['--apply'], capture_output=True, text=True)
    assert applied.returncode == 0
    assert target.read_bytes() == b'new\n'
    stale = subprocess.run(command+['--apply'], capture_output=True, text=True)
    assert stale.returncode == 1
    assert 'stale hash' in stale.stderr
