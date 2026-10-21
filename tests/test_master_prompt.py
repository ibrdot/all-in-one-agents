"""MASTER-PROMPT.md integrity: routing table covers every skill and references only real skills."""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROMPT = os.path.join(ROOT, "MASTER-PROMPT.md")

def real_skills():
    return {d for d in os.listdir(os.path.join(ROOT, "skills"))
            if os.path.isdir(os.path.join(ROOT, "skills", d))}

def prompt_text():
    return open(PROMPT, encoding="utf-8").read()

def test_master_prompt_exists():
    assert os.path.isfile(PROMPT)
    assert os.path.getsize(PROMPT) > 15000, "master prompt too small for v2 spec"

def test_routing_covers_all_skills():
    covered = set(re.findall(r"`([a-z0-9][a-z0-9-]+)`", prompt_text()))
    missing = real_skills() - covered
    assert not missing, f"skills missing from routing table: {sorted(missing)}"

def test_no_phantom_skill_refs():
    text = prompt_text()
    # pull the routing section only (between the routing header and anti-patterns)
    m = re.search(r"Skill routing table(.*?)anti-patterns", text, re.S | re.I)
    assert m, "routing section not found"
    refs = set(re.findall(r"`([a-z0-9][a-z0-9-]+)`", m.group(1)))
    phantoms = refs - real_skills()
    assert not phantoms, f"routing table references nonexistent skills: {sorted(phantoms)}"

def test_required_sections():
    text = prompt_text().lower()
    for section in ("rule zero", "understand", "anti-pattern", "compaction", "oath", "evidence"):
        assert section in text, f"missing section: {section}"

def test_min_version_kept():
    assert os.path.isfile(os.path.join(ROOT, "MASTER-PROMPT.min.md"))
