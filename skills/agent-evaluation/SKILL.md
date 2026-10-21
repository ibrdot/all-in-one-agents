---
name: agent-evaluation
description: Use when comparing coding-agent prompts, evaluating a new skill, testing multi-edit reliability, or checking whether an agent workflow improves correctness rather than just producing persuasive output.
---

# Measure agent changes against reproducible tasks

## Workflow

1. Define the capability and an observable success criterion before tuning prompts. Keep this separate from `agent-self-evaluation`, which is a subjective per-task reflection.
2. Build fixtures with an input repository revision, task prompt, expected invariants, allowed tools, timeout, and independent acceptance tests. Include ambiguous requests, stale context, failing baselines, and cross-file edits.
3. Split development fixtures from held-out fixtures. Never copy acceptance answers into the agent prompt or tune against the held-out set.
4. Run baseline and candidate in separate clean worktrees with identical tool permissions and budgets. Do not reuse modified files or cached answers across runs.
5. Score functional checks, unintended edits, security boundaries, patch size, tool cost, and elapsed time. Record failed runs and flaky tests instead of dropping them.
6. Repeat enough runs to report variability. State sample size, environment, model/version, tool settings, and any unavailable metadata; do not invent precision.
7. Promote only when the measured improvement justifies regressions and cost. Keep the old skill version and regression fixtures for rollback.

## Run record

Store fixture ID, revision, baseline/candidate IDs, timestamps, test commands/exit codes, changed files, budget, and reviewer findings. Keep logs free of credentials and personal data.

## Completion gate

A different reviewer can reproduce the scores. Label syntax tests, behavioral tests, and subjective assessments separately; successful prompt loading is not proof of better coding.
