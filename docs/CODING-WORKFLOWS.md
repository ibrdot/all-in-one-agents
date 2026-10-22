# Coding workflows

[Home](../README.md) | [Catalog](../INDEX.md) | [Install](INSTALL.md)

## ⏱️ 30-second TL;DR

Three patterns cover most engineering work in this pack:

1. **Pick the right skill** from the [workflow table](#pick-the-right-workflow) — each row has a "do not substitute" anti-pattern that tells you when you are reaching for the wrong tool.
2. **Preview multi-file edits before applying** — the helper computes hashes from the actual current file, validates the batch, then atomically replaces one file at a time. Never replay a stale plan.
3. **Migrate contracts safely** — map consumers → add compatibility tests → add adapter → migrate owned callers → verify → observe rollout → remove old code only after the compatibility window and consumer owners permit it.

> **Evidence over vibes**: every workflow ends with a delivery record — revision,
> changed paths, approved intent, commands and exit codes, remaining concerns,
> skipped checks, rollback approach. No tokens or private data in plans, commits,
> or logs.

---

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

---

## Exact-text multi-edit: preview first

The helper uses Python 3.10+ and only the standard library. Run it from the
pack checkout, or use an absolute path to the script when working elsewhere.

<details>
<summary><b>Step 1 — Capture the current state</b></summary>

```bash
git status --short
```

Inspect the existing diff so you know what is already changed before you plan
more edits.

</details>

<details>
<summary><b>Step 2 — Build a JSON plan</b></summary>

Use the [plan contract](../skills/multi-file-editing/references/plan-format.md).
Compute each hash from the actual current file, not from an old summary:

```bash
python3 -c 'import hashlib,pathlib; print(hashlib.sha256(pathlib.Path("src/config.py").read_bytes()).hexdigest())'
```

</details>

<details>
<summary><b>Step 3 — Preview and inspect all diffs</b></summary>

```bash
python3 skills/multi-file-editing/scripts/multi_edit.py plan.json --root /path/to/project
```

Review every diff in the preview output before applying anything.

</details>

<details>
<summary><b>Step 4 — Apply explicitly</b></summary>

```bash
python3 skills/multi-file-editing/scripts/multi_edit.py plan.json --root /path/to/project --apply
```

Only after step 3 has been reviewed.

</details>

<details>
<summary><b>Step 5 — Verify and clean up</b></summary>

Run the project's focused tests, type checks, relevant full suite, and
`git diff --check`. Search for old references and explain intentional leftovers.

</details>

### What the helper refuses and why

The helper refuses stale hashes, wrong match counts, symlinks, binary content,
invalid paths, duplicate paths, and no-op edits. It validates the batch before
writing, then atomically replaces **one file at a time**. It does not offer
multi-file transactional rollback. Stop concurrent writers; inspect a partially
applied batch and regenerate the plan rather than replaying it.

---

## A safe contract migration

Map consumers → add compatibility tests → add an adapter → migrate owned
callers → verify integrations → observe the agreed rollout → remove old code
only after the compatibility window and consumer owners permit it.

Production deployments, destructive migrations, publishing, and force pushes
remain separate authorization decisions. A skill does not grant those permissions.

---

## Evidence to deliver

Record the revision, changed paths, approved intent, commands and exit codes,
remaining compatibility concerns, skipped checks, and rollback approach.
Do not include access tokens or private data in plans, commits, or logs.

---

## Next

- [Installation by harness](INSTALL.md) — per-harness setup and adapter manifests
- [Getting started](GETTING-STARTED.md) — first-time path and post-install checklist
- [Runtime](RUNTIME.md) — semantic routing, council, evaluation pipeline
- [Skill catalog](../INDEX.md) — full 141-skill index with trigger conditions
