"""Docs and manifests must agree with the filesystem."""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))

from counts import counts  # noqa: E402


def test_readme_counts_match_filesystem():
    c = counts()
    readme = open(os.path.join(ROOT, "README.md"), encoding="utf-8").read()
    assert f"{c['skills']} skills" in readme
    assert f"{c['agents']} agent" in readme
    assert f"{c['commands']} slash commands" in readme or f"{c['commands']} commands" in readme


def test_manifest_counts_match_filesystem():
    c = counts()
    manifest = json.load(open(os.path.join(ROOT, ".claude-plugin", "plugin.json")))
    for key in ("skills", "agents", "commands"):
        assert f"{c[key]} {key}" in manifest["description"], (
            f"manifest description missing {c[key]} {key}"
        )


def test_hooks_json_is_valid_and_points_at_a_real_script():
    path = os.path.join(ROOT, "hooks", "hooks.json")
    data = json.load(open(path))
    commands = [
        hook["command"]
        for entry in data["hooks"]["SessionStart"]
        for hook in entry["hooks"]
    ]
    assert commands, "no SessionStart commands configured"
    assert any("session-start.sh" in c for c in commands)
    assert os.path.isfile(os.path.join(ROOT, "hooks", "session-start.sh"))


def test_plugin_manifests_do_not_list_markdown_as_hooks():
    import glob
    for p in glob.glob(os.path.join(ROOT, ".*-plugin", "*.json")) + glob.glob(
        os.path.join(ROOT, ".pi", "*.json")
    ):
        data = json.load(open(p))
        hooks = data.get("hooks")
        if isinstance(hooks, list):
            assert not any(h.endswith(".md") for h in hooks), f"{p}: markdown listed as hook"
        elif isinstance(hooks, str):
            assert hooks.endswith(".json"), f"{p}: hooks must point at JSON config"
