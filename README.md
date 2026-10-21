<div align="center">

# All-in-One Agents

**A practical engineering workflow for AI coding agents.**

Understand the task. Plan the change. Edit with care. Verify with evidence.

[![Tests](https://github.com/ibrdot/all-in-one-agents/actions/workflows/ci.yml/badge.svg)](https://github.com/ibrdot/all-in-one-agents/actions/workflows/ci.yml)
![Skills](https://img.shields.io/badge/skills-83-2563eb) ![Agents](https://img.shields.io/badge/agents-73-0ea5e9) ![Commands](https://img.shields.io/badge/commands-97-64748b) ![License](https://img.shields.io/badge/license-MIT-16a34a)

[Start here](docs/GETTING-STARTED.md) | [Skill catalog](INDEX.md) | [Installation](docs/INSTALL.md) | [Coding workflows](docs/CODING-WORKFLOWS.md) | [Evals](evals/README.md) | [Contributing](CONTRIBUTING.md)

</div>

---

## Built for real repository work

A reusable library of **83 skills, 73 agents, 97 commands** with an orchestration
kernel, safe multi-file editing, test-first workflows, and explicit verification.
Use the parts your harness supports; a manifest alone does not guarantee runtime compatibility.

| Need | Start with | What it adds |
|---|---|---|
| Understand an unfamiliar repo | [codebase-context](skills/codebase-context/SKILL.md) | A bounded map of source, tests, contracts, and unknowns |
| Change several files safely | [multi-file-editing](skills/multi-file-editing/SKILL.md) | Hash-checked previews, exact match counts, explicit apply |
| Rename symbols or APIs | [ast-aware-refactoring](skills/ast-aware-refactoring/SKILL.md) | Syntax-aware tools, fixtures, and consumer checks |
| Migrate contracts | [api-migration](skills/api-migration/SKILL.md) | Compatibility, deployment order, rollback evidence |
| Upgrade dependencies | [dependency-upgrades](skills/dependency-upgrades/SKILL.md) | Controlled lockfile and runtime changes |
| Speed up a slow path | [performance-profiling](skills/performance-profiling/SKILL.md) | Profiled, measured, revertible optimization |
| Make tests bite | [test-design](skills/test-design/SKILL.md) | Behavior-asserted, non-flaky regression coverage |
| Cut a release | [release-engineering](skills/release-engineering/SKILL.md) | Clean build, staged rollout, rollback path |
| Trust the docs | [docs-accuracy](skills/docs-accuracy/SKILL.md) | Every documented command actually runs |
| Act on review feedback | [receiving-code-review](skills/receiving-code-review/SKILL.md) | Verify suggestions before implementing them |
| Compare agent behavior | [agent-evaluation](skills/agent-evaluation/SKILL.md) | Reproducible fixtures and independent scoring |
| Resume interrupted work | [checkpoint-recovery](skills/checkpoint-recovery/SKILL.md) | Reconcile current files with recorded evidence |

## Install in a minute

Requires Git, Bash, and Python 3.10+ for the new edit helper. Individual domain
skills may need additional tools. Review repository scripts before execution.

```bash
git clone https://github.com/ibrdot/all-in-one-agents.git
cd all-in-one-agents
./install.sh claude --dry-run
./install.sh claude
```

Claude installation copies the pack and merges a SessionStart hook into
`~/.claude/settings.json`, preserving unrelated settings. Back up any existing
same-name skills before installing: skill files are copied into the target.

```bash
./install.sh opencode           # ~/.config/opencode
./install.sh /your/custom/path  # skills/, agents/, commands/
```

See [per-harness setup](docs/INSTALL.md) for the 12 included manifest targets.
**No installer?** Use [MASTER-PROMPT.md](MASTER-PROMPT.md) as portable guidance,
or [MASTER-PROMPT.min.md](MASTER-PROMPT.min.md) for a smaller prompt.
Neither prompt-only setup nor a manifest creates tool permissions or executable gates.

## The engineering loop

```text
UNDERSTAND -> PLAN -> EXECUTE -> VERIFY -> DELIVER
```

1. Map the requirement and constraints with [brainstorming](skills/brainstorming/SKILL.md).
2. Isolate approved work with [Git worktrees](skills/using-git-worktrees/SKILL.md).
3. Create atomic tasks with [writing-plans](skills/writing-plans/SKILL.md).
4. Implement with [test-driven-development](skills/test-driven-development/SKILL.md).
5. Inspect the diff with [requesting-code-review](skills/requesting-code-review/SKILL.md).
6. Show actual results with [verification-before-completion](skills/verification-before-completion/SKILL.md).
7. Finish through [finishing-a-development-branch](skills/finishing-a-development-branch/SKILL.md).

The SessionStart hook emits the kernel and bootstrap text for supported Claude
sessions. Stop/PostToolUse Markdown files are **guidance**, not executable
blocking. The optional [delivery gate](skills/delivery-gate/SKILL.md) requires
separate hook configuration. Skills guide an agent; they do not guarantee compliance.

## Try a focused task

> Rename a shared configuration key across source and tests. Inventory consumers,
> preview the exact edit plan, preserve unrelated changes, and show the test results.

For concrete multi-edit commands and migration scenarios, follow
[the coding workflow guide](docs/CODING-WORKFLOWS.md).

## Repository map

| Path | Contents |
|---|---|
| [skills/](skills/) | 83 skills, each with a `SKILL.md` entrypoint |
| [agents/](agents/) | 73 agent definitions |
| [commands/](commands/) | 97 slash commands |
| [hooks/](hooks/) | Executable SessionStart hook and written guidance |
| [docs/](docs/) | Setup, workflows, methodology, and provenance |
| [tests/](tests/) | Structural and behavioral regression tests |
| [evals/](evals/) | 7 behavioral evaluation scenarios |
| [examples/experimental/](examples/experimental/) | 11 opt-in experimental skills |

## Validate a checkout

```bash
python3 -m pip install pytest
python3 scripts/validate.py
python3 scripts/smoke_test.py
python3 -m pytest tests/ -q
python3 scripts/sync_catalog.py --check
git diff --check
```

Counts come from [scripts/counts.py](scripts/counts.py); regenerate the catalog
with `python3 scripts/sync_catalog.py` after changing the inventory.

## Ownership and provenance

Repository commits may use the project automation identity **IBRaiagent**.
That is a Git author label, not proof that every change was autonomous or independently reviewed.

Original pack material is under [LICENSE](LICENSE). Third-party material retains
its own notices: see [ATTRIBUTION.md](ATTRIBUTION.md), [NOTICE](NOTICE), and
[the pinned import manifest](docs/import-manifest.json). Unresolved pre-existing
provenance is documented, not silently relabeled as original work.

[Contribution guide](CONTRIBUTING.md) | [Security policy](SECURITY.md) | [Changelog](CHANGELOG.md)
