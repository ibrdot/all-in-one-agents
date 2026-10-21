# Coding workflows

[Home](../README.md) | [Catalog](../INDEX.md) | [Install](INSTALL.md)

## Pick the right workflow

| Situation | Skill | Do not substitute |
|---|---|---|
| Unfamiliar project | [codebase-context](../skills/codebase-context/SKILL.md) | A repository-wide text dump |
| Literal changes across files | [multi-file-editing](../skills/multi-file-editing/SKILL.md) | Unbounded global replacement |
| Symbols, imports, call signatures | [ast-aware-refactoring](../skills/ast-aware-refactoring/SKILL.md) | Text replacement across unrelated scopes |
| Shared contract change | [api-migration](../skills/api-migration/SKILL.md) | Removing an API before consumers migrate |
| Package version changes | [dependency-upgrades](../skills/dependency-upgrades/SKILL.md) | Lockfile deletion and blind reinstall |
| Reviewer suggestions | [receiving-code-review](../skills/receiving-code-review/SKILL.md) | Automatic agreement |
| Prompt/skill comparison | [agent-evaluation](../skills/agent-evaluation/SKILL.md) | A self-reported quality score |
| Interrupted session | [checkpoint-recovery](../skills/checkpoint-recovery/SKILL.md) | Blind replay of old commands |

## Exact-text multi-edit: preview first

The helper uses Python 3.10+ and only the standard library. Run it from the
pack checkout, or use an absolute path to the script when working elsewhere.

1. Capture `git status --short` and inspect the existing diff.
2. Build a JSON plan using the [plan contract](../skills/multi-file-editing/references/plan-format.md).
   Compute each hash from the actual current file, not from an old summary:

```bash
python3 -c 'import hashlib,pathlib; print(hashlib.sha256(pathlib.Path("src/config.py").read_bytes()).hexdigest())'
```

3. Preview and inspect all diffs:

```bash
python3 skills/multi-file-editing/scripts/multi_edit.py plan.json --root /path/to/project
```

4. After reviewing the preview, apply explicitly:

```bash
python3 skills/multi-file-editing/scripts/multi_edit.py plan.json --root /path/to/project --apply
```

5. Run the project's focused tests, type checks, relevant full suite, and
   `git diff --check`. Search for old references and explain intentional leftovers.

The helper refuses stale hashes, wrong match counts, symlinks, binary content,
invalid paths, duplicate paths, and no-op edits. It validates the batch before
writing, then atomically replaces **one file at a time**. It does not offer
multi-file transactional rollback. Stop concurrent writers; inspect a partially
applied batch and regenerate the plan rather than replaying it.

## A safe contract migration

Map consumers -> add compatibility tests -> add an adapter -> migrate owned
callers -> verify integrations -> observe the agreed rollout -> remove old code
only after the compatibility window and consumer owners permit it.

Production deployments, destructive migrations, publishing, and force pushes
remain separate authorization decisions. A skill does not grant those permissions.

## Evidence to deliver

Record the revision, changed paths, approved intent, commands and exit codes,
remaining compatibility concerns, skipped checks, and rollback approach.
Do not include access tokens or private data in plans, commits, or logs.
