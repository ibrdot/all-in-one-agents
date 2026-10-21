"""Every slash command has a description and a usable body."""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COMMANDS = os.path.join(ROOT, "commands")

def command_files():
    return sorted(f for f in os.listdir(COMMANDS) if f.endswith(".md"))

def test_commands_exist():
    assert len(command_files()) >= 90, f"only {len(command_files())} commands"

def test_command_descriptions():
    bad = []
    for f in command_files():
        text = open(os.path.join(COMMANDS, f), encoding="utf-8", errors="ignore").read()
        m = re.match(r"^---\n(.*?)\n---", text, re.S)
        if not m:
            bad.append((f, "no frontmatter"))
            continue
        if not re.search(r"^description:\s*\S", m.group(1), re.M):
            bad.append((f, "no description"))
    assert not bad, f"command problems: {bad}"

def test_command_bodies():
    for f in command_files():
        text = open(os.path.join(COMMANDS, f), encoding="utf-8", errors="ignore").read()
        body = re.sub(r"^---\n.*?\n---", "", text, flags=re.S).strip()
        assert len(body) > 30, f"{f}: command has no body"
