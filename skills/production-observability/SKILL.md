---
name: production-observability
description: "Instrument systems so incidents answer themselves: structured logging, metrics, traces, SLOs, and actionable alerting. Use when adding monitoring to a service, digging into slow or failing production behavior, or drowning in useless alerts."
---

# Production Observability

Observability is the difference between "the service is slow" and "p99 of checkout for EU users regressed 40% after the 14:00 deploy."

## The three pillars, done right

1. **Structured logs.** One JSON object per event, stable field names (`service`, `request_id`, `user_id`, `duration_ms`, `error_kind`). Never log secrets or PII. Logs you cannot filter are noise with extra steps.
2. **Metrics.** The four golden signals per service: latency, traffic, errors, saturation. Always with dimensions that support slicing (route, region, dependency), never unbounded (no user IDs as labels).
3. **Traces.** One trace per request across service boundaries; propagate the `request_id` everywhere. The trace that stops at a queue boundary is the investigation that stops at a queue boundary.

## SLOs before alerts

- Define SLOs on user-facing outcomes (success rate, p99 latency), not CPU.
- Alert on **symptoms that page a human** (SLO burn rate) and **causes that ticket a human** (disk filling in 6 hours). Everything else is a dashboard, not an alert.
- Every alert must answer in one sentence: "what is broken, what does it cost the user, what should I check first." Alerts that fail this test get deleted.

## Instrument new code by default

- New endpoint -> latency + error metrics per route, structured logs with the request ID, trace spans for external calls.
- New background job -> resumability, progress metric, dead-letter handling. Silent job failure is how data quietly rots.
- Apply [release-engineering](../release-engineering/SKILL.md) so the deploy itself is observable, and [incident-response](../incident-response/SKILL.md) when the alerts fire.

## Anti-patterns

- `console.log("here")` shipped to production
- Dashboards nobody opens and alerts everybody ignores (they are the same failure)
- Mean latency as the headline metric (the tail is where users live)
