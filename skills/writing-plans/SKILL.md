---
name: writing-plans
description: Turn an approved design into an executable plan of atomic tasks. Use after brainstorming, before any implementation — when work has more than one step, touches more than one file, or will be executed by subagents.
---

# Writing Plans

A plan is a contract: precise enough that a fresh agent with zero context can execute it.

## Task anatomy

Every task MUST specify:

1. **Exact file paths** — what to create, what to modify
2. **Complete code** — not "add validation" but the actual diff/content
3. **Verification steps** — the exact command that proves it works
4. **Success criteria** — observable, binary, checkable
5. **Rollback plan** — how to undo this task if it breaks neighbors

## Sizing

- Target **2–5 minutes per task**. If a task is bigger, split it.
- If you can't split it, you don't understand it yet — go back to brainstorming.

## Format

```markdown
## Task N: <verb> <thing>
Files: path/to/file.py (create), path/to/other.py (modify lines 40-55)
Code: <complete implementation>
Verify: pytest tests/test_thing.py -x
Done when: exit code 0, output contains "1 passed"
Rollback: git checkout -- path/to/other.py
```

## Rules

- Order tasks so the project stays runnable after each one
- Never write "etc." or "similar changes" — enumerate
- The plan file lives on disk; it is the shared memory across agents and compactions
