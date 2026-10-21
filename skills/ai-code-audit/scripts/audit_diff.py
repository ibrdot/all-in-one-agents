#!/usr/bin/env python3
"""Static tells-scanner for AI-generated code (the audit checklist, automated).

Scans files or `git diff -U0 main` output for the highest-signal tells:
swallowed exceptions, test-gaming asserts, eval/exec, string-built SQL,
empty catches with side-effect defaults. Heuristics, not proof - each hit
gets human eyes. Exit 1 if findings, so CI can block.

Usage: audit_diff.py [files...]    or: git diff -U0 main | audit_diff.py
"""
import re, sys

PATTERNS = [
    (r"except[^:]*:\s*pass\b", "swallowed-exception", "except: pass hides failures - log or re-raise"),
    (r"catch\s*\([^)]*\)\s*\{\s*\}", "swallowed-exception", "empty catch block"),
    (r"except[^:]*:\s*continue\b", "swallowed-exception", "except: continue hides failures in loops"),
    (r"assert\s+\w+\s+is\s+not\s+None\b", "test-gaming", "assert is-not-None asserts nothing meaningful"),
    (r"expect\(\s*mock[^)]*\)", "test-gaming", "test asserts the mock, not behavior"),
    (r"\beval\s*\(|\bexec\s*\(", "dynamic-exec", "eval/exec on possibly-attacker data"),
    (r"(SELECT|INSERT|UPDATE|DELETE)[^\n]*[\"\']\s*\+\s*|\%\s*\w+[\"\']\s*[\),]", "sql-interp", "string-concatenated SQL - use parameters"),
    (r"==\s*True\b|==\s*False\b", "logic-smell", "comparison to bool literal; likely meant is or truthiness"),
    (r"\.json\(\)\s*\[", "unchecked-parse", "json parse indexed directly - key may be missing"),
    (r"-\s*1\]\s*;|\[0\]\s*\.", "boundary-risk", "indexing without emptiness check nearby"),
    (r"TODO\s*[:\s]|FIXME\b", "loose-end", "unresolved TODO left in generated code"),
]

def scan(lines, source):
    findings = 0
    for i, line in enumerate(lines, 1):
        if len(line) > 400: continue
        for pat, kind, why in PATTERNS:
            if re.search(pat, line):
                print(f"{source}:{i}: [{kind}] {why}\n    {line.strip()[:120]}")
                findings += 1
    return findings

def main():
    args = sys.argv[1:]
    total = 0
    if not args:  # read diff from stdin
        cur = None
        for line in sys.stdin:
            if line.startswith("+++ b/"):
                cur = line.split("b/", 1)[1].strip()
            elif cur and line.startswith("+") and not line.startswith("+++"):
                total += scan([line[1:]], f"{cur}")
    else:
        for path in args:
            try:
                total += scan(open(path, errors="replace").read().splitlines(), path)
            except OSError as e:
                print(f"skip {path}: {e}")
    print(f"\n{total} finding(s)" + ("" if total == 0 else " - review each; heuristics only"))
    sys.exit(1 if total else 0)

if __name__ == "__main__":
    main()
