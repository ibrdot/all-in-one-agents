---
name: commit-craft
description: Write clean conventional commits and review git history quality. Use when the user asks to commit changes, split work into commits, write commit messages, or clean up a messy branch before pushing.
---

# Commit Craft

Great repos are read through their history. Every commit must answer: *what changed and why*.

## Rules

1. **Conventional format**: `type: subject` — types: `feat`, `fix`, `docs`, `test`, `ci`, `refactor`, `chore`
2. **One idea per commit** — never mix a fix with a feature
3. **Subject ≤ 72 chars**, imperative mood ("add", not "added")
4. **Commit working states only** — run the tests/validator first

## Workflow

```bash
git status                 # what changed?
git diff --stat            # how much?
# group related changes, stage per group
git add <files>
git commit -m "type: subject"
```

## Splitting big work

Chunk it: land a working slice, push, continue. Five honest small commits beat one giant dump — reviewers trust granular history.

## Never
- Fake or backdated history
- Committing secrets, tokens, or generated junk
- `git add -A` without checking what got staged

## Done when

- The procedure's stated outcome is observable and checked
- The user can verify the result without trusting the agent's word
