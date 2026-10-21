"""Every skill named in the entrypoints or hooks must exist under skills/.

The kernel is a router: if it dispatches to a skill that is not installed, the
agent burns a turn discovering the dead end and then improvises. This test is
the regression guard for that failure mode.

Scope is deliberately narrow: the two entrypoint skills and hooks/. Skills
referencing each other are audited separately by ``scripts/audit_skills.py``
because the existing pack has known cross-skill references that need editorial
review, not a blanket assertion.
"""
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILLS = os.path.join(ROOT, "skills")
HOOKS = os.path.join(ROOT, "hooks")

ENTRYPOINTS = (
    "skills/pack-kernel/SKILL.md",
    "skills/using-all-in-one-agents/SKILL.md",
)

# Backticked kebab-case tokens that are not skill names. Keep this list short
# and justified: every entry here is a hole in the guard.
NON_SKILL_TERMS = {
    "startup",          # hook matcher value
    "clear",            # hook matcher value
    "compact",          # hook matcher value
    "dry-run",          # installer flag
    "text",             # generic prose
}

TOKEN_RE = re.compile(r"`([a-z][a-z0-9-]+)`")


def existing_skills():
    return {d for d in os.listdir(SKILLS) if os.path.isdir(os.path.join(SKILLS, d))}


def source_files():
    paths = [os.path.join(ROOT, p) for p in ENTRYPOINTS]
    paths += [
        os.path.join(HOOKS, f)
        for f in sorted(os.listdir(HOOKS))
        if f.endswith(".md")
    ]
    return [p for p in paths if os.path.isfile(p)]


def references(path):
    text = open(path, encoding="utf-8", errors="ignore").read()
    return set(TOKEN_RE.findall(text))


def test_entrypoints_and_hooks_reference_real_skills():
    skills = existing_skills()
    unresolved = []
    for path in source_files():
        rel = os.path.relpath(path, ROOT)
        for token in sorted(references(path)):
            if token in NON_SKILL_TERMS:
                continue
            if token not in skills:
                unresolved.append(f"{rel}: `{token}`")
    assert not unresolved, "unresolved skill references:\n" + "\n".join(unresolved)


def test_allowlist_entries_are_not_skills():
    """A term that later becomes a skill should leave the allowlist."""
    skills = existing_skills()
    stale = sorted(NON_SKILL_TERMS & skills)
    assert not stale, f"allowlisted term now exists as a skill: {stale}"


def test_guard_catches_a_planted_reference(tmp_path):
    """Negative control: the detector must actually fail on a dead reference."""
    fake = tmp_path / "fake.md"
    fake.write_text("Load `definitely-not-a-real-skill` now.\n", encoding="utf-8")
    skills = existing_skills()
    bad = [t for t in references(str(fake)) if t not in skills and t not in NON_SKILL_TERMS]
    assert bad == ["definitely-not-a-real-skill"]
