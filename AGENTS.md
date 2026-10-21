# Repository guide for coding agents

## Load in order

1. Read `skills/using-all-in-one-agents/SKILL.md` for bootstrap instructions.
2. Read `skills/pack-kernel/SKILL.md` for the engineering loop.
3. Use `INDEX.md` to load only task-relevant skills.
4. For coordinated code changes, consult `docs/CODING-WORKFLOWS.md`.

## Map

| Path | Responsibility |
|---|---|
| `skills/` | 79 skills; instructions and optional resources |
| `agents/` | 73 role definitions |
| `commands/` | 97 command definitions |
| `hooks/` | Executable SessionStart hook; other Markdown is guidance |
| `scripts/` | Validation, inventory, installation, routing generation |
| `tests/` | Regression tests; run before committing |
| `docs/` | Installation, workflows, provenance |

## Change rules

- Preserve unrelated work; avoid destructive cleanup and forced pushes.
- Prefer original skills. Import third-party content only with reviewed license,
  retained copyright/notice, pinned revision, and an attribution record.
- Never remove legally required attribution or claim imported work as original.
- Reconcile API producers, consumers, tests, and docs in one reviewed plan.
- After inventory changes run `python3 scripts/sync_catalog.py` and
  `python3 scripts/gen_routing.py`; inspect both generated diffs.
- Run validation, smoke tests, pytest, catalog check, and `git diff --check`.
- Use conventional commits. Describe AI-assisted authorship accurately; a Git
  author name alone does not attest to autonomy or verification.
