---
name: zero-to-production
description: "Use when starting from an empty repo or raw idea and the goal is a deployed, monitored, production service - not a demo. Orchestrates spec, scaffold, TDD, hardening, deploy, and on-call readiness in one guided flow."
---

# Zero to Production

Most AI builds stop at "it runs on my machine." This skill exists to cross the gap between *works locally* and *sleep-well-at-night production*. That gap is where real engineering lives.

## The five gates

Do not advance a gate until the previous one is verifiably closed. Each gate has an artifact and a check.

### Gate 1: Spec frozen (30 min, not zero)

- One-page spec: users, top 3 user journeys, non-goals, SLOs (latency, availability), data model sketch.
- Hard rule: no production code before this page exists. Revisit it at every later gate; drift between spec and code is the first smell of a doomed project.

### Gate 2: Walking skeleton deployed on day one

- Deploy the thinnest possible slice - one endpoint, one page, empty DB - to real infrastructure **the first day**. "We'll add deploys later" is how month-long integration hell starts.
- Automated deploy on every push to main from that moment on.

### Gate 3: Tests pay rent

- TDD for all business logic ([test-driven-development](../test-driven-development/SKILL.md)).
- One end-to-end test per critical journey, not per page.
- Coverage target is journey coverage, not a line percentage.

### Gate 4: Production hardening

- Structured logs with request IDs; errors tracked with alerts that page a human.
- Migrations are reversible ([database-migrations](../database-migrations/SKILL.md)); secrets come from a vault, never the repo.
- Load test the top journey to 3x expected peak; fix what falls over.

### Gate 5: On-call ready

- Runbook per alert: symptom, likely causes, first three commands to run ([incident-response](../incident-response/SKILL.md)).
- Rollback rehearsed once for real. An untested rollback is a rumor.
- Dashboards answer: is it up, is it fast, is it losing data, is it costing too much ([production-observability](../production-observability/SKILL.md)).

## Anti-patterns

- Building features before gates 1-2 close.
- "Temporary" manual deploy steps that live for a year.
- Alerts with no runbook - paging noise trains humans to ignore pages.
