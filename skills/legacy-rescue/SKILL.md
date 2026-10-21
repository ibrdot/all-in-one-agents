---
name: legacy-rescue
description: "Use when inheriting an old, undocumented, possibly abandoned codebase that must be changed safely - mapping, characterization tests, seam-cutting, and strangler-pattern migration before any feature work."
---

# Legacy Rescue

Inherited a codebase with no docs, no tests, and three departed authors? The mistake almost everyone makes is starting with a rewrite. The second mistake is making feature changes with no safety net. This skill does neither.

## Phase 1: Map the territory (first day)

- Run it locally first; a codebase you cannot run, you cannot understand.
- Build a map: entry points, data stores, external calls, cron jobs, and the 3 flows that make money. Draw it; do not memorize it.
- Find the load-bearing files with `git log` churn + incident history. Change nothing there yet.

## Phase 2: Buy safety with characterization tests

- Before refactoring, pin current behavior with tests that assert what the code *does*, not what it *should* do. Bugs pinned now are documentation; bugs fixed blind are regressions.
- Cover the money flows first. 60% coverage of critical paths beats 20% coverage of everything.
- Every test green before touching a line. This is your only honest safety net.

## Phase 3: Cut seams

- Identify natural boundaries: the places where data crosses a network, a queue, or a module edge.
- At each seam, add an interface or adapter so tests can substitute fakes. Seams turn "cannot test" into "trivially testable."
- Isolate the horror: wrap the worst module in an anti-corruption layer instead of reading all of it.

## Phase 4: Strangle, do not rewrite

- New features go in new code that talks to old code only through seams.
- Migrate one route/flow at a time; old and new run side by side behind a flag. Delete old paths the moment traffic moves - dead code is a liability, not a keepsake.
- Track migration in tickets, one flow per ticket, so progress is visible and resumable.

## Rules of engagement

- Never mix "understand" commits with "change" commits.
- Leave the campground cleaner: any file you touch gets one small improvement (test, name, comment removal) - one, not fifty.
- Write down everything you learn in [context-and-decisions](../context-and-decisions/SKILL.md). The next inheritor is future you.
