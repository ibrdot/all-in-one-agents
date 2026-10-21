#!/usr/bin/env python3
"""Validate every skill: folder must contain SKILL.md with name + description frontmatter."""
import os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILLS = os.path.join(ROOT, "skills")

errors = []
count = 0
for name in sorted(os.listdir(SKILLS)):
    path = os.path.join(SKILLS, name)
    if not os.path.isdir(path):
        continue
    count += 1
    skill_md = os.path.join(path, "SKILL.md")
    if not os.path.isfile(skill_md):
        errors.append(f"{name}: missing SKILL.md")
        continue
    text = open(skill_md, encoding="utf-8", errors="ignore").read()
    m = re.match(r"^---\n(.*?)\n---", text, re.S)
    if not m:
        errors.append(f"{name}: SKILL.md has no frontmatter")
        continue
    fm = m.group(1)
    if not re.search(r"^name:\s*\S", fm, re.M):
        errors.append(f"{name}: frontmatter missing 'name'")
    if not re.search(r"^description:\s*\S", fm, re.M):
        errors.append(f"{name}: frontmatter missing 'description'")

print(f"validated {count} skills")
if errors:
    print("\n".join(errors))
    sys.exit(1)
print("all skills valid ✔")
