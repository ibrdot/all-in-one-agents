---
name: pack-kernel
description: The orchestration core of the all-in-one pack. Always-on methodology that routes every task through understand-plan-execute-verify-deliver phases, dispatches the right skill at the right phase, blocks unverified delivery, and recovers context after compaction. Load this first; it drives everything else.
---

# Pack Kernel — Orchestration Core

This is not a reference sheet. This is the **operating loop**. Every non-trivial task runs through it.

## The Loop

```
UNDERSTAND → PLAN → EXECUTE → VERIFY → DELIVER
     ↑__________| (any gate failure loops back)
```

No phase may be skipped. Each phase names the skill that drives it.

### Phase 1 — UNDERSTAND
Before writing anything: restate the goal, ask the 3–6 questions whose answers change the design, list constraints.
→ drivers: `brainstorming`, `context-and-decisions`
**Gate:** you can say in one sentence what "done" looks like. If not — keep asking.

### Phase 2 — PLAN
Break the approved design into tasks of 2–10 minutes each, with exact file paths and acceptance checks per task.
→ drivers: `writing-plans`, `pr-design-doc`
**Gate:** every task has a verifiable acceptance check. No check, no task.

### Phase 3 — EXECUTE
One task at a time. Prefer isolated execution (worktree/subagent) per task. Test-first where code is involved.
→ drivers: `test-driven-development`, `subagent-driven-development`, plus a matching domain skill (`frontend-development`, `angular-developer`, `desktop-electron`) when one applies
**Gate:** the task's acceptance check passes locally.

### Phase 4 — VERIFY
Independent review of the diff against the plan. Hunt for: scope creep, untested paths, broken neighbors.
→ drivers: `requesting-code-review`, `security-review`, `module-regression`
**Gate:** reviewer finds zero critical issues. Critical issue found → back to EXECUTE.

### Phase 5 — DELIVER
Run the full verification suite, clean up scaffolding, present merge/PR options with evidence.
→ drivers: `verification-before-completion`, `delivery-gate`, `finishing-a-development-branch`
**Gate:** full suite green + evidence attached. **Unverified work is never delivered.**

## Routing table (task smell → skill)

| You notice... | Load |
|---|---|
| vague request | `brainstorming` |
| multi-step build | `writing-plans` + `executing-plans` |
| bug with unknown cause | `systematic-debugging` |
| "just a quick fix" urge | `delivery-gate` (slow down) |
| long session / compaction | re-read this file, resume current phase |
| repeated domain terms | `context-and-decisions` |
| regression fear in big repo | `module-regression` |
| document deliverable | `docx` / `pdf` / `pptx` / `xlsx` |
| security-sensitive change | `security-review` |

## Compaction recovery

If context was compacted: re-read this SKILL.md, check the plan file for the first unchecked task, resume from that phase. The plan on disk is the memory.

## Hard rules

1. Never deliver unverified work
2. Never skip UNDERSTAND on a vague request
3. One task at a time — no parallel edits to the same file
4. The plan file is source of truth, not memory

## Done when

- The procedure's stated outcome is observable and checked
- The user can verify the result without trusting the agent's word
