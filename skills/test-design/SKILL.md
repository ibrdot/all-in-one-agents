---
name: test-design
description: Use when writing a test plan, reviewing coverage, flaky tests keep appearing, or a bug escaped to production and similar regressions must be caught next time.
---

# Design tests that catch real regressions

## Workflow

1. From the changed behavior, list inputs, boundaries, error paths, concurrency, and external contracts. Derive cases from the specification and from failure history, not from the implementation.
2. Cover each requirement at the cheapest level that gives real confidence: unit for logic, integration for contracts, end-to-end only for critical user paths.
3. Write assertions on observable behavior. Asserting on internal calls or private state makes refactoring painful and tests brittle; assert on outputs, state, and side effects that consumers see.
4. For every bug fix, first write the failing test that reproduces it. Add the missing case that let the bug escape.
5. Remove flakiness at the cause: fixed clocks, seeded randomness, isolated network and filesystem, no inter-test ordering. Mark genuinely unavoidable cases and track them, never blanket-skip silently.
6. Keep fixtures explicit and minimal; shared mutable fixtures hide coupling. Prefer factories or builders over giant setup blocks.
7. Check the suite itself: runtime, coverage of critical paths, assertion strength. A suite that cannot fail is not a suite. Mutation-style spot checks (break the code, watch tests fail) verify strength on critical modules.

## Review questions

Would this test fail if the feature broke? Does it test the requirement or the implementation? Can it pass with the feature deleted? Does it duplicate an existing case? Name the test after the behavior, not the method.
