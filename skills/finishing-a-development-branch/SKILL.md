---
name: finishing-a-development-branch
description: Close out a feature branch properly — full verification, then merge / PR / keep / discard with worktree cleanup. Use when all plan tasks are complete and the work needs to land or be abandoned cleanly.
---

# Finishing a Development Branch

Tasks done ≠ branch done. Land it deliberately.

## Step 1 — Full verification (blocking)

```bash
# from the worktree root, run the ENTIRE suite — not just your task's tests
```

Whole suite green = proceed. Anything red = back to execution. No exceptions, no "pre-existing failure" claims without baseline evidence.

## Step 2 — Present options

Give the human the choice, with a recommendation:

| Option | When |
|---|---|
| **Merge locally** | solo project, suite green, no review needed |
| **Open a PR** | shared repo, review valuable, CI should gate |
| **Keep branch** | work paused, not abandoned |
| **Discard** | experiment failed — say so honestly |

## Step 3 — Execute the choice

- **Merge:** fast-forward or merge-commit per repo convention, then delete the branch
- **PR:** push, open with a summary that states what/why/how-verified
- **Discard:** confirm once, then delete branch

## Step 4 — Cleanup

```bash
git worktree remove ../<project>-<feature>
```

Remove scratch files, kill stray processes, close the loop. A finished branch leaves no trace except its commits.
