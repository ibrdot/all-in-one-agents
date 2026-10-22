"""Inventory counts stay consistent across all published surfaces.

Prevents the silent drift class where skills/agents/commands counts change in
the directory tree but not in the README badges, catalog header, site stats or
measured inventory. Update ALL of these together, always in the same change.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def actual_counts():
    skills = sum(1 for p in (ROOT / "skills").iterdir() if p.is_dir())
    agents = sum(1 for p in (ROOT / "agents").glob("*.md"))
    commands = sum(1 for p in (ROOT / "commands").glob("*.md"))
    return skills, agents, commands


def test_readme_badges_match_actual():
    skills, agents, commands = actual_counts()
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert f"skills-{skills}-" in readme, "README skills badge out of sync"
    assert f"agents-{agents}-" in readme, "README agents badge out of sync"
    assert f"commands-{commands}-" in readme, "README commands badge out of sync"


def test_index_header_matches_actual():
    skills, _, _ = actual_counts()
    index = (ROOT / "INDEX.md").read_text(encoding="utf-8")
    assert f"## Skills ({skills})" in index, "INDEX.md skills count out of sync"


def test_site_stats_match_actual():
    skills, agents, commands = actual_counts()
    html = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")
    nums = re.findall(r'stat-num mono">(\d+)<', html)
    assert nums[:3] == [str(skills), str(agents), str(commands)], "site stats out of sync"


def test_measured_inventory_matches_actual():
    skills, _, _ = actual_counts()
    inv = (ROOT / "docs" / "MEASURED-INVENTORY.md").read_text(encoding="utf-8")
    assert f"| Skills | {skills} |" in inv, "MEASURED-INVENTORY skills count out of sync"
