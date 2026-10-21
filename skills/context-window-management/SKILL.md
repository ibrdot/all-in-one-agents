---
name: context-window-management
description: "Keep an AI agent effective in long sessions: what to load into context, when to compact or summarize, how to persist state to disk, and how to avoid context poisoning from stale or bloated context. Use when sessions run long, the agent forgets earlier decisions, or token usage balloons."
---

# Context Window Management

The context window is the agent's only working memory. Manage it like RAM: load what serves the current task, spill the rest to disk.

## Priorities when context is scarce

1. **Current task and its constraints** - the plan, the acceptance criteria, the failing test output.
2. **Decisions made and why** - one line each. A decision without its reason gets re-litigated and re-broken.
3. **The minimal code surface** - signatures, not bodies; the function under change, not its whole file.

Everything else can be re-fetched on demand. Retrieval beats retention: knowing where the answer lives is worth more than carrying the answer around.

## Compaction discipline

- Summarize state to a durable artifact (plan file, notes file) *before* the window fills, not after it is lost. Structure: goal, decisions log, done list, next step, open questions.
- On resume, reload from the artifact, not from the transcript. Transcripts drift; artifacts are the source of truth.
- Cut stale context aggressively: superseded diffs, resolved errors, finished subtask details. Old context is not free; it biases every new answer.

## Poisoning and drift

- Watch for the agent repeating its own earlier mistake (self-conditioning). If an artifact now says something wrong, correct the artifact immediately or every later step inherits the error.
- Large retrieved chunks crowd out instructions. When behavior degrades, check first what got pushed out of the window, not what got added to the prompt.

## In this pack

- [checkpoint-recovery](../checkpoint-recovery/SKILL.md) resumes interrupted work from on-disk evidence
- [pack-kernel](../pack-kernel/SKILL.md) structures the loop so long sessions stay phase-disciplined
- [using-git-worktrees](../using-git-worktrees/SKILL.md) moves physical state out of the conversation entirely

## Anti-patterns

- Pasting whole files when a signature and a line range would do
- Trusting the transcript to remember decisions instead of writing them down
- Summarizing only when the window is already full (too late - the middle is already gone)
