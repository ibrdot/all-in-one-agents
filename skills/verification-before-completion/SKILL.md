---
name: verification-before-completion
description: Hard gate before any task is claimed done — the agent must show real command output proving tests pass, build succeeds, and the plan's success criteria are met. Use at every task boundary, before every "done", "fixed", or "finished" claim.
---

# Verification Before Completion

Claims are free. Evidence is the currency.

## The gate

Before saying any task is complete, you MUST present:

1. **Test output** — the actual command and its actual output (exit code 0)
2. **Build proof** — if the project builds/compiles, show it succeeding
3. **Criteria check** — map each success criterion from the plan to its evidence

```
Verify: pytest tests/test_parser.py -x
Output: 3 passed in 0.42s        ← real, just ran
Criterion "handles empty input": test_empty_input PASSED
```

## What does NOT count

- "It should work now"
- Output from a run 20 minutes ago
- Tests you wrote to pass by weakening assertions
- Green subset runs when the task required the full suite

## If verification fails

Say so plainly: "Task not done — verification failed at X." Then loop back through `systematic-debugging`. A reported failure is progress; a hidden one is debt.

## If you cannot verify

(e.g. no test harness exists) — say what you checked instead (manual run, type-check, diff review) and flag the residual risk explicitly. Never silently downgrade the standard.
