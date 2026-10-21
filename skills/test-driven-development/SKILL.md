---
name: test-driven-development
description: Write the failing test first, watch it fail, then implement until it passes. Use for any behavior change, bug fix, or new function in a project with a test runner — and especially when tempted to "just write the code" because the change looks small.
---

# Test-Driven Development

A test you never watched fail might be testing nothing. The red comes first.

## Why the order matters

Writing code first feels faster. It isn't — it just moves the cost. When the
test comes second, you unconsciously write tests that confirm what you built
instead of tests that pin down what was required. The red-first loop exists to
keep the specification honest: if the test can't fail, it can't protect you.

## The loop

```
RED    → write a test that expresses the requirement; run it; WATCH IT FAIL
GREEN  → write the minimum implementation that passes; run it; watch it pass
REFACTOR → clean up with the test suite standing guard; stay green
```

### RED — the most skipped step

- The test must express the *requirement*, not your planned implementation
- Run it before implementing. If it passes immediately, one of these is true:
  the feature already exists (check for duplication!), or the test is broken
- A never-red test is deleted on sight in disciplined teams — treat it as suspect

### GREEN — minimum, not masterpiece

- Write the least code that turns the test green
- Hard-code the return value if that's all the test demands — the next test
  will force the generalization. This feels silly; it is the mechanism that
  keeps implementations from outrunning their evidence

### REFACTOR — only on green

- Rename, extract, deduplicate — behavior frozen, tests green throughout
- If you break something while refactoring, undo — don't "fix forward" by
  editing tests

## Bug fixes

A bug is a missing test. Reproduce it as a failing test FIRST, then fix.
The test stays forever as the guard that the bug can never return silently.

## Anti-patterns this skill blocks

- "I'll add tests after" — you won't, and even if you do they'll be confirmation tests
- Weakening an assertion to make a run green — that deletes the alarm, not the fire
- Testing implementation details (private helpers, call counts) instead of behavior
- Committing code whose only evidence is "I read it carefully"

## Done when

- Every new behavior has a test that was observed failing before it passed
- The full suite runs green — output shown, exit code 0
- No assertion was weakened to get there
