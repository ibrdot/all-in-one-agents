# Task dispatch and independent review protocol

Original all-in-one-agents playbook. This is a procedure, not an assertion that
any particular host can create subagents. Inspect host tools first.

## Decide execution topology

Use parallel workers only when their write sets and prerequisites are disjoint.
Shared package lockfiles, generated catalogues, database schemas and common API
contracts make apparently separate tasks coupled. Serialize those tasks or agree
on the producer/consumer contract before dispatch. Do not give two workers the
same checkout and hope merge will discover the dependency for you.

If the host has no worker tool, execute serially and mark the independent review
unavailable. A single model role-playing reviewer is not an independent agent.
Platform restrictions outrank this playbook: delegate read-only review when
writes must remain in the orchestrator. Do not claim a worker implemented work
that the parent actually wrote.

## Implementation brief

Record these fields in the plan, then send the complete task, not a pointer to
conversation context a worker cannot read:

```
Task ID and outcome:
Repository and exact base commit:
Allowed write paths:
Read-only dependency paths:
Inputs/outputs and invariants:
Acceptance cases (normal, boundary, failure):
Commands for RED, targeted GREEN, and neighboring regression:
Forbidden operations (network, credentials, destructive git):
Expected handoff: patch or commit, actual outputs, limitations:
Stop conditions: missing dependency, ambiguous contract, scope expansion:
```

Worker reads current files, reproduces baseline and reports mismatches. The
worker does not redesign the task to fit an easy implementation. Missing access
is a blocker, not permission to invent results.

## Two review passes

### Pass A: specification compliance

Reviewer receives the request, accepted plan, base/head revisions, changed paths,
and raw verification outputs. Do not substitute the implementer's summary for
the diff. Map every requirement to a changed behavior and an executable check.

- Missing requirement: cite the requirement and missing behavior.
- Extra scope: identify why the addition is unrelated or dangerous.
- Misstated evidence: distinguish test-double wiring, local execution, native
  host verification and actual remote provider results.
- Acceptance criteria met: list which checks establish it, not "looks good".

### Pass B: implementation quality

A separate pass asks whether a compliant implementation is robust. Review error
paths, cancellation, partial writes, types, trust boundaries, compatibility and
operational limits. Read both callers and callees. Review tests for assertions
that always pass, assertions copied from implementation, missing negative cases,
and mocks replacing the very boundary the test claims to validate.

A finding needs severity, file/function, reproducer, expected/actual behavior and
minimal remedy. A style preference is not critical. Secret leakage, silent data
loss, broken acceptance or an unbounded paid call are blocking.

## Remediation loop

1. Reproduce a concrete finding as a failing check.
2. Send the finding to the original implementer with the same scope boundary.
3. Verify the fix against the reproducer and neighboring consumers.
4. Re-review the changed diff; do not treat a worker's "fixed" as evidence.
5. After repeated failed fixes, stop and revisit the contract. Do not accumulate
   speculative patches or lower the acceptance bar.

## Handoff receipt

Record base/head SHA, files touched, requirement-to-test map, command results,
review findings and dispositions, remaining external gates, and rollback path.
No fabricated clean-review claim when a reviewer tool was unavailable. A clean
local test suite does not establish production readiness or marketplace approval.
