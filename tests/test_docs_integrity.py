"""Markdown links in README and INDEX resolve to real files."""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def md_links(path):
    text = open(path, encoding="utf-8").read()
    for target in re.findall(r"\]\(([^)]+)\)", text):
        if target.startswith(("http://", "https://", "#")):
            continue
        yield target

def test_readme_links_resolve():
    bad = [t for t in md_links(os.path.join(ROOT, "README.md"))
           if not os.path.exists(os.path.join(ROOT, t))]
    assert not bad, f"README dead links: {bad}"

def test_index_links_resolve():
    bad = [t for t in md_links(os.path.join(ROOT, "INDEX.md"))
           if not os.path.exists(os.path.join(ROOT, t))]
    assert not bad, f"INDEX dead links: {bad}"

def test_index_count_matches_reality():
    text = open(os.path.join(ROOT, "INDEX.md"), encoding="utf-8").read()
    m = re.search(r"## Skills \((\d+)\)", text)
    assert m, "INDEX missing skill count header"
    real = sum(1 for d in os.listdir(os.path.join(ROOT, "skills"))
               if os.path.isdir(os.path.join(ROOT, "skills", d)))
    assert int(m.group(1)) == real, f"INDEX says {m.group(1)} but {real} skills exist"
