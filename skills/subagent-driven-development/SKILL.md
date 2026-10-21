---
name: subagent-driven-development
description: Drive implementation by dispatching a fresh subagent per plan task, with review between tasks. Use for multi-task plans where tasks are mostly independent, sessions will be long, or context budget matters — each subagent starts clean with only its task.
---

# Subagent-Driven Development

The orchestrator keeps the map; subagents walk one step each.

## Roles

- **You (orchestrator):** hold the plan, dispatch tasks, review results, never implement in the main context
- **Subagent:** receives ONE task block + scope boundary, implements, verifies, returns evidence

## Dispatch template

```
Task: <paste exact task block from the plan>
Scope: touch ONLY these files: <list>
Rules: implement as specified; run the verify command; return the
       command output verbatim. If the task is impossible as written,
       STOP and explain — do not improvise a redesign.
```

## Between tasks

1. Check the subagent's evidence (real output, exit code)
2. Run `requesting-code-review` on the diff
3. Critical issues → dispatch a fix subagent for the same task
4. Green → check off the task, dispatch the next

## Why fresh subagents

- No accumulated confusion from a long context
- Review of task N isn't biased by having written task N
- Context budget stays flat regardless of plan length

## Never

- Two subagents on overlapping files at once (use `dispatching-parallel-agents` qualification first)
- Accepting "done" without the verify output

## Done when

- The skill's scripts run without errors on their documented inputs
- The output matches the format the skill promises
