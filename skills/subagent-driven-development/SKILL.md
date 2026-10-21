---
name: subagent-driven-development
description: Drive implementation by dispatching a fresh subagent per plan task, with review between tasks. Use for multi-task plans where tasks are mostly independent, sessions will be long, or context budget matters — each subagent starts clean with only its task.
---

# Subagent-Driven Development

The orchestrator keeps the map; subagents walk one step each.

## Why this pattern exists

Long implementations fail in predictable ways: the agent's context fills with
yesterday's decisions, it starts pattern-matching to its own earlier mistakes,
and review quality collapses because the reviewer wrote the code. Fresh
subagents per task solve all three: clean context, no sunk-cost attachment,
and genuine independent review.

## Roles

- **You (orchestrator):** hold the plan, dispatch tasks, review evidence,
  decide go/no-go between tasks. You NEVER implement in the main context —
  your context is the scarcest resource in the system.
- **Subagent:** receives ONE task block + scope boundary, implements,
  verifies, returns evidence. Disposable by design.

## Dispatch template

```
Task: <paste the exact task block from the plan — files, code, verify, rollback>
Scope: touch ONLY these files: <list>
Rules:
- Implement exactly as specified
- Run the verify command; return the output verbatim
- If the task is impossible as written, STOP and explain —
  do not improvise a redesign, do not expand scope
```

## Between every task

1. **Evidence check** — real output? exit code 0? criteria mapped?
2. **Review** — load `requesting-code-review` on the diff
3. **Decide:**
   - Green + clean review → check off, dispatch next
   - Green + critical review issue → fix subagent for the SAME task
   - Red → loop through `systematic-debugging`, then retry the task

## Context economics

- Each subagent prompt is self-contained — never "continue from where we were"
- The plan file is the shared state; subagents read tasks from it, write
  results back through you
- Your own context should hold: the plan, task statuses, and open issues —
  nothing else

## Never

- Two subagents on overlapping files simultaneously (qualify parallelism with
  `dispatching-parallel-agents` first)
- Accepting "done" without verify output
- Implementing "just this small task" yourself — that road ends with you
  holding ten tasks of context and reviewing your own work
- Letting a subagent redefine the task to match what it built

## Done when

- Every task has evidence + review on record
- The plan file shows all tasks checked
- The final diff has passed independent review
