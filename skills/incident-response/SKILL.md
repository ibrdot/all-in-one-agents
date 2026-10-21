---
name: incident-response
description: "Production is broken: errors, outage, or data corruption. Stabilize first, diagnose second, communicate in parallel. Use when a live system is failing, an alert fired, or users report breakage, and every minute costs money or trust."
---

# Incident Response

Live incidents punish investigation order. Work the loop: **stabilize, diagnose, communicate, fix, learn.**

## Phase 1 - Stabilize (minutes)

In priority order:

1. **Stop the bleeding.** Roll back the last deploy, flip the feature flag off, or shed load. Prefer reverting a bad change over hot-fixing it in place.
2. **Protect data.** If writes are corrupting data, disable the write path before anything else. Backups beat cleverness.
3. **Capture evidence.** Before restarts wipe state, snapshot logs, heap dumps, metrics, and the exact error signatures.

State the stabilization bet out loud: "We deployed commit X at T, reverting because it is the only change in the window." Revert is a hypothesis too; watch whether the symptom actually stops.

## Phase 2 - Diagnose (parallel)

- **Timeline first:** last deploy, config change, traffic spike, dependency outage. Correlate clock times, not feelings.
- **Narrow the blast radius:** which users, which regions, which request shapes? Failure patterns localize the bug faster than code reading.
- **One hypothesis at a time,** each with a falsifiable prediction. Cross hypotheses off with evidence, not discussion.
- Use [systematic-debugging](../systematic-debugging/SKILL.md) once the system is stable; never debug a moving incident.

## Phase 3 - Communicate

- One owner posts updates on a fixed cadence (every 15-30 min), even when the update is "no change."
- Format: current impact, actions in flight, next update time. No blame, no speculation presented as fact.
- Internal notes go in a live incident doc; decisions and timestamps land there, not in chat scrollback.

## Phase 4 - Fix and verify

- Fix forward only when the fix is smaller than the revert. Apply [multi-file-editing](../multi-file-editing/SKILL.md) discipline.
- Verify against the captured symptom signatures from Phase 1, plus [verification-before-completion](../verification-before-completion/SKILL.md).
- Watch the fix through at least one full traffic cycle (peak included) before declaring resolution.

## Phase 5 - Learn

Within a week, write the postmortem:

1. Timeline of facts with timestamps
2. Root cause chain (the five-whys; see [thinking-five-whys-plus](../thinking-five-whys-plus/SKILL.md))
3. What made detection slow; what made recovery slow
4. Exactly one owner and due date per action item

An incident without a follow-up action item is a scheduled repeat.

## Anti-patterns

- Debugging while the fire spreads instead of reverting
- "Fix" pushes during peak traffic without a rollback plan
- Postmortems that end at "human error" (the error was the system that let the human)
