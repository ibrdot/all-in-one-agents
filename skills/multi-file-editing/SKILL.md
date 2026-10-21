---
name: multi-file-editing
description: Use when changing multiple files together, applying repeated edits, renaming interfaces across modules, or needing a safe multi-edit workflow with exact-match checks and verification.
---

# Coordinated edits without collateral damage

## Workflow

1. Capture `git status --short` and `git diff`. Keep user changes intact; do not reset or stash without permission.
2. Enumerate producers, consumers, tests, fixtures, generated outputs, and docs with `git grep -n 'symbol'` and language tooling. Define explicit file ownership if delegating.
3. Choose exact-text editing only for unambiguous literal changes. For identifiers, imports, scopes, or syntax use `ast-aware-refactoring` instead.
4. Write a JSON edit plan using [the plan contract](references/plan-format.md). Include the current SHA-256 and exact expected match count for every file. One literal replacement per file; use a language-aware tool for complex edits.
5. Preview with `python3 skills/multi-file-editing/scripts/multi_edit.py plan.json --root .`. Review every unified diff. Preview writes nothing.
6. Apply with the same command plus `--apply` only after approving the diff. The helper validates the whole plan before starting writes, then replaces files individually. It is NOT a multi-file transaction: an I/O failure may leave a partial batch. Inspect the diff before retrying.
7. Run focused tests, type checks, full relevant tests, and `git diff --check`. Search for obsolete references. Report changed files, commands, results, and any skipped checks.

## Stop conditions

Stop on stale hashes, unexpected match counts, symlinks, paths outside the root, binary files, overlapping ownership, or unclear behavior. Never broaden a search-and-replace to force a plan through. Preserve file permissions and line endings; do not edit generated files directly.

## Completion evidence

Show the reviewed diff, successful checks, remaining references, and any public contract changes. Pair with `verification-before-completion` and `requesting-code-review`.
