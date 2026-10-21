---
name: writing-plans
description: Turn an approved design into an executable plan of atomic tasks. Use after brainstorming, before any implementation — when work has more than one step, touches more than one file, or will be executed by subagents.
---

# Writing Plans

A plan is a contract: precise enough that a fresh agent — or a tired you at
midnight — can execute it without re-deriving a single decision.

## Overview

Design tells you *what* to build. The plan tells you *in what order, touching
which files, proven by which commands*. A good plan converts an intimidating
feature into a queue of boring, obvious, verifiable tasks. When execution
feels scary, the plan wasn't finished.

## Scope check first

Before writing tasks, draw the boundary:

- **In scope:** exactly what the approved design covers
- **Out of scope:** the adjacent improvements you'll be tempted to sneak in
  (write them at the bottom as "future ideas" — naming them frees you from
  doing them now)
- **Unknowns:** anything you still can't specify — each unknown becomes a
  task of the form "investigate X, produce answer Y", never a silent gap

## Task anatomy

Every task MUST specify all five:

1. **Exact file paths** — what to create, what to modify (with line anchors where useful)
2. **Complete code** — not "add validation" but the actual implementation or diff
3. **Verification steps** — the exact command that proves it works
4. **Success criteria** — observable, binary, checkable
5. **Rollback plan** — how to undo this task if it breaks neighbors

Missing any of the five means the task isn't written yet — you're hoping,
not planning.

## Sizing

- Target **2–5 minutes of execution per task**
- Bigger than that → split. The split points usually reveal hidden structure
- Can't split it? You don't understand it yet → back to `brainstorming`

## Task format

```markdown
## Task N: <verb> <thing>
Files: path/to/file.py (create), path/to/other.py (modify lines 40-55)
Code: <complete implementation>
Verify: pytest tests/test_thing.py -x
Done when: exit code 0, output contains "1 passed"
Rollback: git checkout -- path/to/other.py
```

## Ordering rules

- **The project stays runnable after every task** — never leave a task whose
  completion requires the next task
- **Risky tasks early** — the scariest unknown goes near the front; discovering
  a fatal flaw at task 2 of 20 is cheap, at task 19 it's a disaster
- **Shared files cluster** — tasks touching the same file go adjacent, so
  context (and merge conflicts) stay local

## Commit cadence

One commit per task, conventional message, after the task's verification
passes. The commit history then *is* the progress report — reviewers read
the plan executed in order.

## The plan is shared memory

- The plan file lives on disk (e.g. `.plan/<feature>.md`) — it survives
  compaction, subagent boundaries, and your own forgetting
- Check tasks off as they complete; the first unchecked task is always the
  resume point
- Deviations get written INTO the plan when they happen — a stale plan is
  worse than no plan because it lies confidently

## Never

- "etc." or "similar changes" — enumerate everything
- Tasks whose verification is "looks right"
- Planning in your head because the feature "isn't that big" — that phrase
  is the leading indicator of features that are exactly that big

## Done when

- Every task has all five anatomy elements
- A stranger could execute task 1 with zero questions
- The risky unknowns sit at the front, each with an investigation task
