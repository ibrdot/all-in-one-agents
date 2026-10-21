"""Every skill under skills/ has a SKILL.md with required frontmatter."""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILLS = os.path.join(ROOT, "skills")

def skill_dirs():
    return [d for d in sorted(os.listdir(SKILLS)) if os.path.isdir(os.path.join(SKILLS, d))]

def frontmatter(path):
    text = open(path, encoding="utf-8", errors="ignore").read()
    m = re.match(r"^---\n(.*?)\n---", text, re.S)
    return m.group(1) if m else None

def test_every_skill_has_skill_md():
    missing = [d for d in skill_dirs() if not os.path.isfile(os.path.join(SKILLS, d, "SKILL.md"))]
    assert not missing, f"missing SKILL.md: {missing}"

def test_frontmatter_present():
    bad = [d for d in skill_dirs() if frontmatter(os.path.join(SKILLS, d, "SKILL.md")) is None]
    assert not bad, f"no frontmatter: {bad}"

def test_name_and_description():
    bad = []
    for d in skill_dirs():
        fm = frontmatter(os.path.join(SKILLS, d, "SKILL.md")) or ""
        if not re.search(r"^name:\s*\S", fm, re.M):
            bad.append((d, "name"))
        dm = re.search(r"^description:\s*(.*)$", fm, re.M)
        val = dm.group(1).strip() if dm else ""
        if val in ("|", ">", "|-", ">-", "|+", ">+"):
            block = re.search(r"^description:.*\n((?:[ \t]+\S.*\n?)+)", fm, re.M)
            val = block.group(1) if block else ""
        if len(val.strip().strip('"')) < 40:
            bad.append((d, "description"))
    assert not bad, f"frontmatter problems: {bad}"

def test_skill_count_minimum():
    assert len(skill_dirs()) >= 70, f"only {len(skill_dirs())} skills"
