"""Installer: hooks component is covered by --force conflict protection.

Regression test for the finding that scripts/install.sh copied the
SessionStart hook unconditionally, silently replacing user modifications,
while skills/agents/commands required --force. The documented behavior
("replacing changed installed files requires an explicit --force") now
applies to the hooks component too.
"""
import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INSTALLER = ROOT / "scripts" / "install.sh"


def run_install(home, *args):
    env = os.environ.copy()
    env["HOME"] = str(home)
    return subprocess.run(
        ["bash", str(INSTALLER), *args],
        env=env, capture_output=True, text=True,
    )


def test_hooks_component_requires_force_after_modification(tmp_path):
    home = tmp_path / "home"
    home.mkdir()

    first = run_install(home, "claude")
    assert first.returncode == 0, first.stderr

    hook = home / ".claude" / "hooks" / "session-start.sh"
    assert hook.is_file()
    hook.write_text(hook.read_text() + "\n# user customization\n")

    refused = run_install(home, "claude")
    assert refused.returncode != 0
    assert "refusing modified installed files" in refused.stderr
    # modification preserved on refusal
    assert "user customization" in hook.read_text()

    forced = run_install(home, "claude", "--force")
    assert forced.returncode == 0, forced.stderr
    # replacement happened on explicit --force
    assert "user customization" not in hook.read_text()
