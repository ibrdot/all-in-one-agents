#!/usr/bin/env python3
"""Smoke test: syntax-check every script shipped inside skills/.

Checks:
- .py   -> python compile
- .sh   -> bash -n
- .js/.cjs/.mjs -> node --check (skipped if node is unavailable)
- .json -> JSON parse
"""
import json, os, py_compile, shutil, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILLS = os.path.join(ROOT, "skills")
SKIP = {"node_modules", "__pycache__", ".git"}

errors = []
stats = {"py": 0, "sh": 0, "js": 0, "json": 0}
has_node = shutil.which("node") is not None

for dirpath, dirnames, files in os.walk(SKILLS):
    dirnames[:] = [d for d in dirnames if d not in SKIP]
    for fn in files:
        p = os.path.join(dirpath, fn)
        rel = os.path.relpath(p, ROOT)
        ext = os.path.splitext(fn)[1].lower()
        try:
            if ext == ".py":
                py_compile.compile(p, doraise=True)
                stats["py"] += 1
            elif ext == ".sh":
                subprocess.run(["bash", "-n", p], check=True, capture_output=True)
                stats["sh"] += 1
            elif ext in (".js", ".cjs", ".mjs") and has_node:
                subprocess.run(["node", "--check", p], check=True, capture_output=True)
                stats["js"] += 1
            elif ext == ".json":
                with open(p, encoding="utf-8", errors="ignore") as f:
                    json.load(f)
                stats["json"] += 1
        except Exception as e:
            errors.append(f"{rel}: {e}")

print(f"checked: {stats['py']} py, {stats['sh']} sh, {stats['js']} js, {stats['json']} json")
if errors:
    print("\n".join(errors))
    sys.exit(1)
print("smoke test passed ✔")
