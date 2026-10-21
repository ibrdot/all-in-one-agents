---
name: codebase-context
description: Use when entering an unfamiliar repository, locating a feature across modules, recovering context for a coding task, or narrowing a large codebase into an evidence-backed edit plan.
---

# Build a precise working map before editing

## Workflow

1. Read repository instructions, manifests, entrypoints, CI configuration, and the current diff before following assumptions from memory.
2. Trace the user-visible behavior from entrypoint to implementation, data contracts, tests, and persistence. Prefer symbol references and `git grep` over reading every file.
3. Create a compact map: path, symbol, responsibility, relevant test, and why it matters. Distinguish source code from generated output, vendored code, fixtures, and archived examples.
4. Inspect recent history only for affected files: `git log -5 -- path/to/file`. Do not assume the most recent commit explains unrelated behavior.
5. Record unknowns and resolve them with a minimal reproduction or focused test. Treat comments, issues, and old docs as leads, not authoritative runtime behavior.
6. Propose the smallest owned edit set with verification commands and known consumers. Hand off a bounded context packet rather than dumping the repository into every subagent.

## Context packet

Include the task and acceptance criteria; exact revision; relevant paths/symbols; current worktree state; constraints; test commands with baseline results; unresolved questions; and source pointers. Never include credentials, private user data, or hidden reasoning.

## Completion gate

Another agent can find the same code and reproduce the baseline without relying on guesses. Proceed to `writing-plans` only after the behavior and ownership boundary are clear.
