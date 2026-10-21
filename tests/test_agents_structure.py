"""Every agent definition has valid frontmatter (name + description)."""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AGENTS = os.path.join(ROOT, "agents")

def agent_files():
    return sorted(f for f in os.listdir(AGENTS) if f.endswith(".md"))

def test_agents_exist():
    assert len(agent_files()) >= 60, f"only {len(agent_files())} agents"

def test_agent_frontmatter():
    bad = []
    for f in agent_files():
        text = open(os.path.join(AGENTS, f), encoding="utf-8", errors="ignore").read()
        m = re.match(r"^---\n(.*?)\n---", text, re.S)
        if not m:
            bad.append((f, "no frontmatter"))
            continue
        fm = m.group(1)
        if not re.search(r"^name:\s*\S", fm, re.M):
            bad.append((f, "no name"))
        if not re.search(r"^description:\s*\S", fm, re.M):
            bad.append((f, "no description"))
    assert not bad, f"agent problems: {bad}"

def test_agent_body_nonempty():
    for f in agent_files():
        text = open(os.path.join(AGENTS, f), encoding="utf-8", errors="ignore").read()
        body = re.sub(r"^---\n.*?\n---", "", text, flags=re.S).strip()
        assert len(body) > 50, f"{f}: agent has no body content"
