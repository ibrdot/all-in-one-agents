---
name: concurrency-debugging
description: "Hunt race conditions, deadlocks, and flaky tests: reproducing intermittent failures, reasoning about shared state, locking, idempotency, and async ordering. Use when bugs appear only sometimes, under load, in parallel tests, or in async/timeout code."
---

# Concurrency Debugging

Intermittent bugs are deterministic bugs whose inputs you cannot see yet.

## Reproduce first

- Never fix from a stack trace alone. Build the smallest loop that reproduces: fewer threads, controlled ordering, injected delays at the suspicious boundary.
- Stress in CI with a dedicated job (hundreds of iterations) so the repro pays rent. A race you cannot trigger on demand cannot be verified fixed.
- Flaky test? Quarantine with a tracking ticket, never delete. See [test-design](../test-design/SKILL.md).

## Reason about the invariant

1. Name the shared state and its invariant in one sentence ("the balance is never negative", "this map is only mutated while holding the lock").
2. For each access, ask who else can run between this line and that one. Interleavings are the bug; the code is just the map.
3. Classify: **race** (ordering), **deadlock** (cyclic waiting), **lost update** (read-modify-write), **visibility** (stale reads), **reentrancy**.
4. Fix the invariant, not the symptom: use the language's primitive that makes the invariant hold by construction (atomic types, transactions, message queues, single-owner data) instead of sprinkling locks.

## Verify

- The repro loop now runs clean for the original stress count.
- The fix does not regress throughput on the hot path; measure, see [performance-profiling](../performance-profiling/SKILL.md).
- Look for the same pattern elsewhere in the codebase before closing. Races, like cockroaches, are rarely alone.

## Anti-patterns

- Adding `time.sleep` until the flake disappears
- Believing "it passed 100 times locally" as evidence
- Fixing a deadlock with a timeout instead of removing the cycle
