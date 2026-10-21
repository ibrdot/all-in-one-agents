---
name: executing-plans
description: Execute a written plan task-by-task with evidence at each step. Use when a plan file exists and work should proceed sequentially — the default executor when tasks are dependent or too entangled for parallel dispatch.
---

# Executing Plans

The plan is law. Execute it exactly; flag it when reality disagrees.

## Loop

For each task in the plan, in order:

1. **Read** the task block fully — files, code, verify command
2. **Implement** exactly what is specified
3. **Verify** — run the task's verification, capture the output
4. **Report** — one line: task N, pass/fail, evidence
5. **Check off** the task in the plan file (the plan on disk is the memory)

## Deviation protocol

When the plan is wrong (missing file, changed API, better route discovered):

- **Trivial deviation** (renamed import, moved file): fix, note it in the plan
- **Design-level deviation**: STOP. Surface it. The human decides — you don't redesign mid-execution

## Discipline

- One task at a time — never batch multiple tasks into one edit
- Never skip a verification "because it's obviously fine"
- If a task fails twice, stop the loop and load `systematic-debugging`

## Finish

All tasks checked → hand off to `requesting-code-review`, then `finishing-a-development-branch`.
