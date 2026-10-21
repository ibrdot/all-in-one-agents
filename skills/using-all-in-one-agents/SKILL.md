---
name: using-all-in-one-agents
description: Bootstrap entrypoint of the all-in-one-agents framework — loaded automatically at session start and after compaction. Establishes the core workflow, the skill-check rule, and the no-code-before-brainstorming rule. Every session begins here.
---

# Using All-in-One Agents

You are running with the all-in-one-agents framework. This skill is your constitution.

## Rule Zero — check before you act

Before ANY task, ask: *is there a skill for this?* Check `skills/` (see INDEX.md). If yes — load it and follow it. Skills override improvisation.

## The Core Workflow (non-trivial work)

For anything beyond a one-line answer, run this pipeline:

1. **brainstorming** — understand before building. Ask the questions whose answers change the design. **Refuse to write code before this on non-trivial work.**
2. **using-git-worktrees** — isolate the work: fresh branch, clean baseline, tests green before touching anything.
3. **writing-plans** — break the design into atomic tasks, each with exact files, complete code, and verification.
4. **subagent-driven-development** OR **executing-plans** — execute task by task. Dispatch isolated subagents for independent tasks.
5. **test-driven-development** — failing test first, then code, then green.
6. **requesting-code-review** — independent eyes on the diff before merge.
7. **finishing-a-development-branch** — full suite green, then merge / PR / discard with cleanup.

Shallow work (typos, one-liners, direct questions) may skip the pipeline — but never skip verification.

## Enforcement

- **verification-before-completion** gates every "done" claim — evidence or it didn't happen.
- **delivery-gate** blocks shipping unverified work.
- **pack-kernel** holds the phase loop and routing table when you need deeper guidance.

## After compaction

This skill reloads via the SessionStart hook. Find the plan file, resume the first unchecked task. The plan on disk outranks your memory.

## Done when

- The procedure's stated outcome is observable and checked
- The user can verify the result without trusting the agent's word
