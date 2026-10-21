#!/usr/bin/env python3
"""Hotspot map for an inherited codebase: churn x complexity.

Ranks files by git-change frequency (churn) weighted by size and an
indentation-depth heuristic (nesting ~ complexity). The top of the list is
where characterization tests go first, and where you change nothing else.

Usage: repo_map.py [since-date]   e.g. repo_map.py 2025-01-01
"""
import subprocess, sys, os

SKIP = ("/test", "/tests/", "/vendor/", "/dist/", "/build/", ".min.", "/migrations/", "/locale/")

def complexity(path):
    try:
        lines = open(path, errors="replace").read().splitlines()
    except OSError:
        return 0
    depth = 0
    for ln in lines:
        ind = len(ln) - len(ln.lstrip(" \t"))
        depth += ind + (2 if ln.rstrip().endswith((":", "{", "(")) else 0)
    return depth // max(len(lines) or 1, 1) + len(lines) // 100

def main():
    since = sys.argv[1] if len(sys.argv) > 1 else "1 year ago"
    log = subprocess.run(
        ["git", "log", f"--since={since}", "--name-only", "--pretty=format:"],
        capture_output=True, text=True).stdout.splitlines()
    churn = {}
    for f in log:
        f = f.strip()
        if f: churn[f] = churn.get(f, 0) + 1
    rows = []
    for f, c in churn.items():
        if not os.path.isfile(f) or any(s in f for s in SKIP): continue
        sz = os.path.getsize(f)
        rows.append((c * complexity(f), c, complexity(f), sz, f))
    rows.sort(reverse=True)
    print(f"{'score':>8}{'commits':>9}{'cx':>5}{'bytes':>9}  file   <- test first, touch last")
    for score, c, cx, sz, f in rows[:20]:
        print(f"{score:>8}{c:>9}{cx:>5}{sz:>9}  {f}")

if __name__ == "__main__":
    main()
