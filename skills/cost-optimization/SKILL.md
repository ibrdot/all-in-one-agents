---
name: cost-optimization
description: "Use when cloud, database, or LLM spend is too high or growing faster than usage - measure, find the top 3 levers, apply architectural fixes before cosmetic ones, and keep savings from regressing."
---

# Cost Optimization

Cost problems are almost never diffuse. One query, one loop, one misconfigured cache, one chatty integration is usually 60% of the bill. Find that one thing before touching anything else.

## Step 1: Make spend attributable (never skip)

- Break the bill to the smallest unit you can: per service, per endpoint, per tenant, per model call. A bill you cannot attribute is a bill you cannot reduce.
- One week of data minimum. Optimizing off a daily spike is how teams "save" money and break peak traffic.

## Step 2: Attack in leverage order

Work this list top-down; each level typically beats everything below it:

1. **Architecture:** fix N+1 queries, add/repair caching (with explicit invalidation), stop polling when events exist, move fan-out work off the request path.
2. **Right-sizing:** the 16GB instance serving 2GB of traffic; the SSD holding cold logs; the region nobody's users live in.
3. **Commitments:** reserved instances / savings plans / committed-use once usage is stable - only after 1 and 2, or you commit to waste.
4. **Cosmetics:** log retention, image sizes, zombie resources. Real but small; do not lead with a press release about deleting unattached volumes.

## Step 3: LLM/AI spend specifics

- Log every call's token counts. Route cheap tasks to small models, escalate only on failure; a cascade (small first, large on retry) often cuts spend 5-10x with no quality loss.
- Cache aggressively: exact-match for deterministic prompts, semantic cache where freshness allows.
- Kill the debug loop's silent burn: a retry loop with no cap on a 100k-token context is an invoice generator.

## Step 4: Make it stick

- Budget alerts per service, not just account-wide, so regressions page the owner of the code, not the owner of the credit card.
- Add a cost check to review for anything that multiplies work with user count ([thinking-margin-of-safety](../thinking-margin-of-safety/SKILL.md)).
- Re-measure after each change and write down what moved. Savings that cannot be shown are savings that did not happen.

## Tooling

Run `python3 skills/cost-optimization/scripts/token_cost_report.py usage.jsonl` for an instant per-model, per-route spend report with the top lever flagged. Point it at your LLM gateway's JSONL logs (see the script header for the format).
