---
name: dispatching-parallel-agents
description: Run independent tasks concurrently in isolated subagents with a deterministic merge strategy. Use when a plan contains 2+ tasks that touch disjoint files and share no ordering constraints — never for tasks that edit the same files.
---

# Dispatching Parallel Agents

Parallelism is for independent work only. Speed never outranks correctness.

## Qualification test (all must be YES)

- [ ] Tasks touch **disjoint files** (zero overlap)
- [ ] No task depends on another's output
- [ ] Each task has its own verification command
- [ ] The plan already exists (from `writing-plans`)

Any NO → execute sequentially with `executing-plans` instead.

## Dispatch

Launch one subagent per qualified task. Each subagent receives:

1. The task block from the plan (files, complete code, verify command)
2. Its scope boundary: "touch only these files"
3. The evidence requirement: return command output, not claims

## Isolation rules

- Subagents never see each other's uncommitted work
- One subagent per worktree if tasks are heavy; shared checkout is fine only for truly disjoint small files
- A subagent that hits an unexpected dependency STOPS and reports — it does not improvise into another task's scope

## Merge strategy

1. Collect results; verify each task's acceptance check independently
2. Merge in plan order, one at a time
3. After EACH merge, run the combined verification — catching interaction bugs early
4. All merges green → proceed to `requesting-code-review`

## Failure handling

One failed branch never blocks the others from landing. Merge the green ones, loop the failed one back through `systematic-debugging`.
