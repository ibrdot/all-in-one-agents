#!/usr/bin/env python3
"""Token spend report from JSONL usage logs.

Reads lines like {"model":"gpt-4o","input":1200,"output":300,"route":"chat"}
(one JSON object per line, extra keys ignored) and prints spend by model and
route plus the top cost centers. Prices in $/1M tokens - edit PRICING for your
providers. Exit code 0 always; designed for cron + CI.

Usage: token_cost_report.py [logfile.jsonl ...]   (default: stdin)
"""
import json, sys
from collections import defaultdict

# $ per 1M tokens. Update to match your provider price sheet.
PRICING = {
    "gpt-4o": (2.50, 10.00), "gpt-4o-mini": (0.15, 0.60),
    "claude-sonnet-4-5": (3.00, 15.00), "claude-haiku-4": (0.80, 4.00),
    "claude-opus-4": (15.00, 75.00), "gemini-2.0-flash": (0.10, 0.40),
}
DEFAULT = (1.00, 4.00)  # unknown model: conservative estimate

def main():
    in_tok, out_tok, calls = defaultdict(int), defaultdict(int), defaultdict(int)
    route_cost = defaultdict(float)
    for path in ([sys.argv[1]] if len(sys.argv) > 1 else ["-"]):
        fh = sys.stdin if path == "-" else open(path)
        for line in fh:
            line = line.strip()
            if not line: continue
            try: rec = json.loads(line)
            except json.JSONDecodeError: continue
            model = rec.get("model", "unknown")
            inp, out = int(rec.get("input", 0)), int(rec.get("output", 0))
            pin, pout = PRICING.get(model, DEFAULT)
            cost = inp / 1e6 * pin + out / 1e6 * pout
            in_tok[model] += inp; out_tok[model] += out; calls[model] += 1
            route_cost[rec.get("route", "unrouted")] += cost
    if not calls:
        print("no usage records found"); return
    print(f"{'model':24}{'calls':>8}{'in tok':>12}{'out tok':>12}{'cost $':>10}")
    total = 0.0
    for m in sorted(calls, key=lambda m: calls[m] * sum(PRICING.get(m, DEFAULT)), reverse=True):
        pin, pout = PRICING.get(m, DEFAULT)
        c = in_tok[m] / 1e6 * pin + out_tok[m] / 1e6 * pout
        total += c
        print(f"{m:24}{calls[m]:>8}{in_tok[m]:>12}{out_tok[m]:>12}{c:>10.2f}")
    print(f"{'TOTAL':24}{sum(calls.values()):>8}{sum(in_tok.values()):>12}{sum(out_tok.values()):>12}{total:>10.2f}")
    print("\ncost by route:")
    for r, c in sorted(route_cost.items(), key=lambda kv: -kv[1]):
        pct = 100 * c / total if total else 0
        flag = "  <-- top lever" if pct >= 40 else ""
        print(f"  {r:30}${c:10.2f}  {pct:5.1f}%{flag}")

if __name__ == "__main__":
    main()
