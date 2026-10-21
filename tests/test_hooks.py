"""Every skill referenced by a hook actually exists under skills/."""
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOOKS = os.path.join(ROOT, "hooks")
SKILLS = os.path.join(ROOT, "skills")

# Backticked tokens in hooks that are commands or concepts, not skills.
NON_SKILL_TERMS = {"dry-run", "startup", "clear", "compact"}


def existing_skills():
    return {d for d in os.listdir(SKILLS) if os.path.isdir(os.path.join(SKILLS, d))}


def test_hooks_exist():
    for name in ("SessionStart.md", "Stop.md", "PostToolUse.md"):
        assert os.path.isfile(os.path.join(HOOKS, name)), f"missing hook {name}"


def test_hook_references_resolve():
    skills = existing_skills()
    unresolved = []
    for hook in sorted(os.listdir(HOOKS)):
        if not hook.endswith(".md"):
            continue
        text = open(os.path.join(HOOKS, hook), encoding="utf-8").read()
        for ref in set(re.findall(r"`([a-z][a-z0-9-]+)`", text)):
            if ref in NON_SKILL_TERMS:
                continue
            if ref not in skills:
                unresolved.append(f"{hook}: `{ref}`")
    assert not unresolved, "hooks reference missing skills:\n" + "\n".join(unresolved)


def test_hook_reference_guard_is_not_vacuous():
    """The guard must be able to fail; assert the detection logic directly."""
    skills = existing_skills()
    planted = ["definitely-not-a-skill"]
    detected = [r for r in planted if r not in skills and r not in NON_SKILL_TERMS]
    assert detected == planted
