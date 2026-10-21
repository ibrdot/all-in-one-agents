#!/usr/bin/env python3
"""Advisory health report for the skill pack.

Not a gate: the pack has known cross-skill references that need editorial
review. This surfaces them so each one can be fixed or explicitly accepted.

Usage:
    python3 scripts/audit_skills.py            # human report
    python3 scripts/audit_skills.py --json     # machine report
    python3 scripts/audit_skills.py --strict   # exit 1 on any finding (CI opt-in)
"""
import argparse
import hashlib
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILLS = os.path.join(ROOT, "skills")

FILE_REF_RE = re.compile(r"`([A-Za-z0-9_./-]+\.(?:md|json|py|sh|js|ts|yaml))`")
CODE_EXT = (".py", ".sh", ".js", ".mjs", ".cjs")


def skill_dirs():
    return sorted(d for d in os.listdir(SKILLS) if os.path.isdir(os.path.join(SKILLS, d)))


def read(path):
    with open(path, encoding="utf-8", errors="ignore") as f:
        return f.read()


def block_value(fm, key):
    """Return a frontmatter value, expanding YAML block scalars."""
    m = re.search(rf"^{key}:\s*(.*)$", fm, re.M)
    if not m:
        return None
    val = m.group(1).strip()
    if val in ("|", ">", "|-", ">-", "|+", ">+"):
        block = re.search(rf"^{key}:.*\n((?:[ \t]+\S.*\n?)+)", fm, re.M)
        return block.group(1).strip() if block else ""
    return val.strip('"').strip("'")


def has_children(fm, key):
    """True when a key is followed by an indented block."""
    m = re.search(rf"^{key}:\s*$", fm, re.M)
    if not m:
        return False
    rest = fm[m.end():].split("\n")[1:]
    for line in rest:
        if not line.strip():
            continue
        return line.startswith((" ", "\t"))
    return False


def frontmatter_problems(text, name):
    problems = []
    m = re.match(r"^---\n(.*?)\n---", text, re.S)
    if not m:
        return ["no frontmatter"]
    fm = m.group(1)
    if not re.search(r"^name:\s*\S", fm, re.M):
        problems.append("missing name")
    if has_children(fm, "metadata") is False and re.search(r"^metadata:\s*$", fm, re.M):
        problems.append("empty metadata key")
    desc = block_value(fm, "description")
    if not desc or len(desc) < 40:
        problems.append("description missing or <40 chars")
    return problems


def skill_basenames(skill):
    names = set()
    for dirpath, _dirnames, files in os.walk(os.path.join(SKILLS, skill)):
        names.update(files)
    return names


def dead_file_refs(skill, text):
    """A ref is dead only if neither the literal path nor the basename exists."""
    base = os.path.join(SKILLS, skill)
    present = skill_basenames(skill)
    dead = []
    for ref in sorted(set(FILE_REF_RE.findall(text))):
        candidates = [
            os.path.join(base, ref),
            os.path.join(ROOT, ref),
            os.path.join(base, "references", ref),
            os.path.join(base, "templates", ref),
        ]
        if any(os.path.exists(c) for c in candidates):
            continue
        if os.path.basename(ref) in present:
            continue
        dead.append(ref)
    return dead


def code_lines(skill):
    total = 0
    for dirpath, _dirnames, files in os.walk(os.path.join(SKILLS, skill)):
        for f in files:
            if f.endswith(CODE_EXT):
                try:
                    with open(os.path.join(dirpath, f), encoding="utf-8", errors="ignore") as fh:
                        total += sum(1 for _ in fh)
                except OSError:
                    pass
    return total


def duplicate_groups():
    seen = {}
    for dirpath, _dirnames, files in os.walk(SKILLS):
        for f in files:
            p = os.path.join(dirpath, f)
            try:
                digest = hashlib.md5(open(p, "rb").read()).hexdigest()
            except OSError:
                continue
            seen.setdefault(digest, []).append(os.path.relpath(p, ROOT))
    return {k: v for k, v in seen.items() if len(v) > 1}


def build_report():
    report = {"skills": {}, "dead_refs": {}, "no_code": [], "duplicates": []}
    for skill in skill_dirs():
        path = os.path.join(SKILLS, skill, "SKILL.md")
        if not os.path.isfile(path):
            report["skills"][skill] = ["missing SKILL.md"]
            continue
        text = read(path)
        problems = frontmatter_problems(text, skill)
        if problems:
            report["skills"][skill] = problems

        dead = dead_file_refs(skill, text)
        if dead:
            report["dead_refs"][skill] = dead

        if code_lines(skill) == 0:
            report["no_code"].append(skill)

    dups = duplicate_groups()
    report["duplicates"] = [
        {"count": len(v), "sample": v[0], "wasted_bytes": os.path.getsize(os.path.join(ROOT, v[0])) * (len(v) - 1)}
        for v in dups.values()
    ]
    report["duplicates"].sort(key=lambda d: -d["wasted_bytes"])
    return report


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--strict", action="store_true")
    args = ap.parse_args()

    r = build_report()
    findings = (
        len(r["skills"]) + len(r["dead_refs"]) + len(r["duplicates"])
    )

    if args.json:
        print(json.dumps(r, indent=2))
    else:
        print(f"skills: {len(skill_dirs())}")
        print(f"frontmatter problems: {len(r['skills'])}")
        for s, p in r["skills"].items():
            print(f"  - {s}: {', '.join(p)}")
        print(f"refs to files not shipped (may be created at runtime): {len(r['dead_refs'])}")
        for s, refs in r["dead_refs"].items():
            print(f"  - {s}: {', '.join(refs)}")
        print(f"skills with no executable code: {len(r['no_code'])}")
        print(f"duplicate file groups: {len(r['duplicates'])}")
        for d in r["duplicates"][:5]:
            print(f"  - {d['count']}x {d['sample']} ({d['wasted_bytes']} wasted bytes)")
        print(f"\nfindings: {findings}")

    if args.strict and findings:
        sys.exit(1)


if __name__ == "__main__":
    main()
