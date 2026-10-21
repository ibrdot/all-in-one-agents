---
name: checkpoint-recovery
description: Use when a coding session is interrupted, context is compacted, a task changes agents, or a multi-file edit must resume without losing user changes or repeating completed work.
---

# Resume work from evidence, not stale memory

## Workflow

1. Before a risky batch or handoff, record repository revision, branch, `git status --short`, changed file list, approved plan, and last verified test commands/results.
2. Store the checkpoint in an agreed local task file. Do not auto-commit secrets, unrelated work, or task notes to the repository.
3. On resume, compare current HEAD and worktree with the checkpoint. Re-read repository instructions and affected files; the filesystem wins over old summaries.
4. Classify each planned step as not started, partially applied, applied but unverified, or verified. Do not infer completion solely from a checked box.
5. Re-run targeted verification for partially applied or changed steps. Recompute edit hashes and preview any resumed `multi-file-editing` plan; never replay stale replacements.
6. Reconcile user edits explicitly. Never run `git reset --hard`, `git clean`, forced checkout, or blanket stash to make the worktree match a checkpoint.
7. Continue from the earliest unverified dependency. Report recovered work, new changes since the checkpoint, and remaining verification.

## Checkpoint template

Record task/acceptance criteria; revision/branch; dirty paths and ownership; completed steps with evidence; active step; exact next command; blockers; rollback approach; and approval boundaries. Exclude tokens, passwords, and hidden reasoning.

## Completion gate

The resumed run preserves all pre-existing changes, revalidates assumptions, and never claims an old test result applies to a new diff.
