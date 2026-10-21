---
name: executing-plans
description: Execute a written plan task-by-task with evidence at each step. Use when a plan file exists and work should proceed sequentially — the default executor when tasks are dependent or too entangled for parallel dispatch.
---

# Executing Plans

The plan is law. Execute it exactly; flag it when reality disagrees.

## Why strict execution matters

A plan you follow 90% is worse than no plan — it gives the *feeling* of
discipline with none of the guarantees. The value of the plan is that every
task was sized, sequenced, and given a verification when your understanding
was freshest. Improvising mid-execution spends that investment.

## The loop

For each task in the plan, in order:

1. **Read** the task block fully — files, code, verify command, rollback
2. **Implement** exactly what is specified — no more, no less
3. **Verify** — run the task's verification command, capture the real output
4. **Report** — one line: task N, pass/fail, evidence
5. **Check off** the task in the plan file — the plan on disk is the memory

## Reading the plan correctly

- **Files:** touch exactly these. A task that "also needs" another file is a
  plan defect — note it, don't absorb it silently
- **Code:** the plan's code was written when context was full. Prefer it over
  your mid-execution re-derivation unless reality contradicts it
- **Verify:** run it even when the change looks obviously right. *Especially*
  then — obviousness is where bugs hide

## Deviation protocol

When the plan is wrong (missing file, changed API, better route discovered):

| Deviation size | Action |
|---|---|
| Trivial (renamed import, moved file) | Fix it, note the correction IN the plan |
| Structural (task needs splitting, order wrong) | Rewrite that section of the plan, then continue |
| Design-level (approach itself is wrong) | **STOP.** Surface it. The human decides |

A stale plan lies confidently — every deviation goes into the plan file the
moment it happens.

## Failure handling

- Task fails verification → fix forward within the task's scope once
- Fails twice → stop the loop, load `systematic-debugging`
- Failure outside the task's scope → that's a plan defect; document and escalate

## Discipline rules

- One task at a time — never batch multiple tasks into one edit
- Never skip a verification "because it's obviously fine"
- Never check off a task whose evidence you haven't seen
- Commit per task after green — history becomes the progress report

## Finish

All tasks checked → hand off to `requesting-code-review`, then
`finishing-a-development-branch`. Do not skip review because "each task was
already verified" — review catches what task-level verification can't:
interaction bugs, scope drift, and plan-vs-reality mismatch.

## Done when

- Every task checked off with real evidence
- The plan file reflects reality (deviations recorded)
- Review has been requested
