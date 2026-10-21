---
name: ci-cd-pipelines
description: "Use when building or fixing CI/CD - pipeline stages that catch bugs early, fast feedback loops, safe deploy strategies, and keeping the pipeline trusted and green."
---

# CI/CD Pipelines

A pipeline has one job: make main deployable at any moment and prove it. Everything else is negotiable.

## Stage order that works

1. **Fast checks first** (<2 min): lint, typecheck, unit tests. Fail fast, save minutes on every commit.
2. **Build once** - artifact built in one stage, promoted through the rest. Rebuilding per stage means you deploy something you never tested.
3. **Integration/e2e** against a real dependency stack (containers, not mocks, for anything with queries or queues).
4. **Deploy** behind your strategy (below), then **smoke test in prod** and auto-rollback on failure signals.

## Speed is a feature

- Parallelize; cache dependencies and build outputs keyed on lockfiles.
- Target: under 10 minutes total, under 2 to first signal. Slower pipelines train people to batch merges, and batches are how rollbacks become surgery.
- Flaky tests are quarantined same-day with a ticket - a red pipeline everyone reruns is a pipeline nobody reads.

## Deploy strategies

- Blue/green or canary for user-facing services: shift a slice of traffic, watch error rate and latency, roll forward or back automatically.
- Feature flags decouple deploy from release; the flag removal ticket is part of the PR, not "later."
- Migrations deploy before code that needs them and must be backward-compatible for one release cycle (expand → migrate → contract).

## Trust rules

- Main is protected; every change via PR with the pipeline green - including yours, especially under deadline.
- Pipeline-as-code reviewed like code; secrets from the platform's vault, never in logs or YAML.
- Rollback is a documented, rehearsed one-command action, not a wiki page from 2023.
