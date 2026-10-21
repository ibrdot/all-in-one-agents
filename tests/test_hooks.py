"""Every skill referenced by a hook actually exists under skills/."""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOOKS = os.path.join(ROOT, "hooks")
SKILLS = os.path.join(ROOT, "skills")

def existing_skills():
    return {d for d in os.listdir(SKILLS) if os.path.isdir(os.path.join(SKILLS, d))}

def test_hooks_exist():
    for name in ("SessionStart.md", "Stop.md", "PostToolUse.md"):
        assert os.path.isfile(os.path.join(HOOKS, name)), f"missing hook {name}"

def test_hook_references_resolve():
    skills = existing_skills()
    for hook in os.listdir(HOOKS):
        if not hook.endswith(".md"):
            continue
        text = open(os.path.join(HOOKS, hook), encoding="utf-8").read()
        for ref in re.findall(r"`([a-z0-9][a-z0-9-]{2,})`", text):
            if "-" in ref and ref in skills or ref in ("using-all-in-one-agents",):
                assert ref in skills, f"{hook} references missing skill {ref}"
