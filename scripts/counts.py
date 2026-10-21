#!/usr/bin/env python3
"""Print the pack's real inventory; used by tests and release docs."""
import argparse
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def counts():
    skills = len([d for d in os.listdir(os.path.join(ROOT, "skills"))
                  if os.path.isdir(os.path.join(ROOT, "skills", d))])
    agents = len([f for f in os.listdir(os.path.join(ROOT, "agents"))
                  if f.endswith(".md")])
    commands = len([f for f in os.listdir(os.path.join(ROOT, "commands"))
                    if f.endswith(".md")])
    return {"skills": skills, "agents": agents, "commands": commands}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    c = counts()
    if args.json:
        print(json.dumps(c))
    else:
        print(f"skills={c['skills']} agents={c['agents']} commands={c['commands']}")


if __name__ == "__main__":
    main()
