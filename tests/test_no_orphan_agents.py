"""Every agent in agents/ is referenced somewhere in the pack (skills, commands, docs, or INDEX)."""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def haystack():
    text = []
    for sub in ("skills", "commands", "docs"):
        for dirpath, dirnames, files in os.walk(os.path.join(ROOT, sub)):
            dirnames[:] = [d for d in dirnames if d not in ("node_modules", "__pycache__")]
            for fn in files:
                if fn.endswith((".md", ".yaml", ".yml")):
                    text.append(open(os.path.join(dirpath, fn), encoding="utf-8", errors="ignore").read())
    text.append(open(os.path.join(ROOT, "INDEX.md"), encoding="utf-8").read())
    return "\n".join(text)

def test_no_orphan_agents():
    corpus = haystack()
    orphans = []
    for f in sorted(os.listdir(os.path.join(ROOT, "agents"))):
        if f.endswith(".md"):
            name = f[:-3]
            if name not in corpus:
                orphans.append(name)
    assert not orphans, f"orphan agents: {orphans}"
