"""The SessionStart hook must emit a real Claude Code payload, not a status line."""
import json
import os
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOOK = os.path.join(ROOT, "hooks", "session-start.sh")


def run_hook(env=None):
    e = dict(os.environ)
    e.pop("PACK_DIR", None)
    if env:
        e.update(env)
    return subprocess.run(
        ["bash", HOOK],
        capture_output=True,
        text=True,
        env=e,
        timeout=30,
    )


def test_emits_valid_json():
    proc = run_hook()
    assert proc.returncode == 0, proc.stderr
    payload = json.loads(proc.stdout)
    assert payload["hookSpecificOutput"]["hookEventName"] == "SessionStart"


def test_injects_actual_kernel_text():
    proc = run_hook()
    context = json.loads(proc.stdout)["hookSpecificOutput"]["additionalContext"]
    # Phase names and the entrypoint rule prove the body was read, not just a path.
    assert "UNDERSTAND" in context
    assert "Rule Zero" in context
    assert len(context) > 2000


def test_no_partial_json_when_pack_missing():
    proc = run_hook({"PACK_DIR": "/nonexistent", "HOME": "/nonexistent"})
    assert proc.returncode == 0, proc.stderr
    # Either silence or valid JSON - never a truncated payload.
    if proc.stdout.strip():
        json.loads(proc.stdout)


def test_installed_layout_resolves():
    """A user install puts skills at ~/.claude/skills; the hook must find them."""
    import shutil
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        dest = os.path.join(tmp, ".claude", "skills")
        shutil.copytree(os.path.join(ROOT, "skills"), dest)
        proc = run_hook({"HOME": tmp})
        context = json.loads(proc.stdout)["hookSpecificOutput"]["additionalContext"]
        assert "UNDERSTAND" in context
