---
name: using-git-worktrees
description: Isolate feature work in a git worktree with a verified clean baseline. Use after design approval, before writing any implementation code — especially in dirty repos, shared checkouts, or when parallel workstreams exist.
---

# Using Git Worktrees

Never implement on a dirty checkout. Isolation first.

## Setup sequence

1. **Confirm design approval** — no worktree before brainstorming + plan exist
2. **Create the worktree:**

```bash
git worktree add ../<project>-<feature> -b <feature-branch>
cd ../<project>-<feature>
```

3. **Run project setup** — install deps, apply env, whatever the project needs
4. **Verify clean baseline:**

```bash
# run the project's own test suite
# MUST be green BEFORE you write a single line of implementation
```

**A red baseline means stop.** Fix or document pre-existing failures first — otherwise you'll never know if you broke it or it was already broken.

## During work

- Commit early, commit per task
- Keep the worktree dedicated to this feature only

## When done

Hand off to `finishing-a-development-branch` — it handles merge/PR/discard and worktree cleanup. Never `rm -rf` a worktree; use `git worktree remove`.

## Done when

- The procedure's stated outcome is observable and checked
- The user can verify the result without trusting the agent's word
