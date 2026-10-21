---
name: microservices-design
description: "Use when splitting a system into services, or deciding whether to - boundaries, data ownership, communication patterns, and the honest tests for whether you need this at all."
---

# Microservices Design

Microservices trade code complexity for operational complexity. Make the trade deliberately, with the team and tooling to pay for it.

## Should you? The honest test

- Do you have independent teams hitting deploy contention on one codebase? Painful org scaling is the real driver. Technology boredom is not a reason.
- Can you operate 10 services (on-call, tracing, deploys) before building them? If not, a modular monolith with clean module boundaries gives you 80% of the benefit at 20% of the cost - and boundaries make the future split cheap.

## Boundaries

- Cut along business capabilities (billing, catalog), not technical layers (a "data service" everyone calls is a distributed monolith).
- One service, one owner, one database. Shared databases are shared couplings with a network hop added.
- If two services always deploy together, they are one service. Merge them.

## Communication

- Sync (REST/gRPC) for read-your-write paths where the caller needs the answer; async (events/queues) for everything the caller does not need to block on.
- Events are contracts: version them, keep them backward-compatible, and never let one team's refactor silently change a payload.
- Every cross-service call needs a timeout, a retry budget with jitter, and a circuit breaker. Retrying without all three is how one slow service becomes a fleet-wide outage (retry storm).

## Data consistency

- Design for eventual consistency: sagas or outbox patterns for multi-service workflows, not distributed transactions.
- Idempotent consumers mandatory; duplicate delivery is normal, not exceptional.
- Correlation IDs through every hop, or tracing is fiction.

## The standing rule

Every service earns its operational cost: own runbook, own dashboards, own deploy pipeline. A service nobody can operate is a liability wearing a nice architecture diagram.
