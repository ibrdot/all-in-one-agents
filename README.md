# ⚡ All-in-One Agents

**The complete engineering workflow for AI coding agents.**

*Understand the task. Plan the change. Edit with care. Verify with evidence.*

[![Tests](https://github.com/ibrorg/all-in-one-agents/actions/workflows/validate.yml/badge.svg)](https://github.com/ibrorg/all-in-one-agents/actions/workflows/validate.yml)
[![Release](https://img.shields.io/github/v/release/ibrorg/all-in-one-agents?style=flat-square&color=8b5cf6)](https://github.com/ibrorg/all-in-one-agents/releases)
[![Skills](https://img.shields.io/badge/skills-140-2563eb?style=flat-square)](INDEX.md)
[![Agents](https://img.shields.io/badge/agents-73-0ea5e9?style=flat-square)](INDEX.md)
[![Commands](https://img.shields.io/badge/commands-97-64748b?style=flat-square)](INDEX.md)
[![License](https://img.shields.io/badge/license-MIT-16a34a?style=flat-square)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-ff69b4?style=flat-square)](CONTRIBUTING.md)

[Get started](#quick-start) · [Skill catalog](INDEX.md) · [Installation](docs/INSTALL.md) · [Workflows](docs/CODING-WORKFLOWS.md) · [Release notes](RELEASE-NOTES.md) · [Runtime](docs/RUNTIME.md) · [Objective evaluations](docs/OBJECTIVE-EVALUATION.md)

</div>

---

## Overview

**All-in-One Agents** is a practical toolkit for AI-assisted engineering. It brings together **140 skills, 73 agent definitions, 97 command definitions**, executable workflow helpers, and an optional Python runtime.

Start with a well-defined task, load only the skills relevant to that task, and verify the outcome with evidence.

The toolkit includes semantic retrieval, peer-critique councils, objective evaluation, and native document generation. Instructions and adapter files do not grant host permissions or, by themselves, prove compatibility. See the [tested compatibility boundaries](docs/COMPATIBILITY-EVIDENCE.md).

## Contents

- [What it solves](#-what-it-solves)
- [Quick start](#quick-start)
- [Configuration and usage](#configuration-and-usage)
- [Technology stack](#technology-stack)
- [The engineering loop](#-the-engineering-loop)
- [Engineering and reasoning toolkit](#-engineering-and-reasoning-toolkit)
- [Try a focused task](#-try-a-focused-task)
- [Repository structure](#repository-structure)
- [Validation](#validation)
- [Ownership and provenance](#-ownership-and-provenance)
- [Documentation](#documentation)
- [Community](#community)
- [Executable runtime foundation](#executable-runtime-foundation)
- [Executable blueprint progress](#executable-blueprint-progress)
- [Objective tasks and executable documents](#objective-tasks-and-executable-documents)

## 🧭 What it solves

| Need | Start with | What it adds |
|---|---|---|
| 🔍 Understand an unfamiliar repository | [codebase-context](skills/codebase-context/SKILL.md) | A bounded map of source code, tests, contracts, and unknowns |
| ✏️ Change several files safely | [multi-file-editing](skills/multi-file-editing/SKILL.md) | Hash-checked previews, exact match counts, and explicit apply steps |
| 🔁 Rename symbols or APIs | [ast-aware-refactoring](skills/ast-aware-refactoring/SKILL.md) | Syntax-aware tools, fixtures, and consumer checks |
| 🚚 Migrate contracts | [api-migration](skills/api-migration/SKILL.md) | Compatibility planning, deployment order, and rollback evidence |
| ⬆️ Upgrade dependencies | [dependency-upgrades](skills/dependency-upgrades/SKILL.md) | Controlled lockfile and runtime changes |
| 🚀 Improve a slow path | [performance-profiling](skills/performance-profiling/SKILL.md) | Profiled, measured, and reversible optimization |
| 🧪 Strengthen tests | [test-design](skills/test-design/SKILL.md) | Behavior-focused regression coverage designed to avoid flakiness |
| 📦 Prepare a release | [release-engineering](skills/release-engineering/SKILL.md) | A clean build, staged rollout, and rollback path |
| 📚 Keep documentation trustworthy | [docs-accuracy](skills/docs-accuracy/SKILL.md) | Checks that documented commands actually run |
| 🧠 Reason deliberately | [thinking-first-principles](skills/thinking-first-principles/SKILL.md) and 27 more `thinking-*` skills | OODA, pre-mortems, red-teaming, systems thinking, TRIZ, and more on demand |
| 🗺️ Navigate a codebase | [wayfinder](skills/wayfinder/SKILL.md) | Guided orientation in an unfamiliar codebase |
| 🔀 Review a diff thoroughly | [code-review](skills/code-review/SKILL.md) | Standards-based review, specification axes, and parallel sub-agents |
| 🤝 Respond to review feedback | [receiving-code-review](skills/receiving-code-review/SKILL.md) | A process for verifying suggestions before implementing them |
| 👥 Compare agents | [agent-evaluation](skills/agent-evaluation/SKILL.md) | Reproducible fixtures and independent scoring |
| ♻️ Resume interrupted work | [checkpoint-recovery](skills/checkpoint-recovery/SKILL.md) | Reconciliation of files with recorded evidence |

## Quick start

### Requirements

- Git
- Bash
- Python 3.10 or later for the edit helper

Review scripts before running them.

### Install

```bash
git clone https://github.com/ibrorg/all-in-one-agents.git
cd all-in-one-agents

# Preview the installation
./install.sh claude --dry-run

# Install for Claude
./install.sh claude
```

<details>
<summary><strong>Install for other harnesses or a custom path</strong></summary>

```bash
# OpenCode: installs to ~/.config/opencode
./install.sh opencode

# Custom destination: installs skills/, agents/, and commands/
./install.sh /your/custom/path
```

</details>

## Configuration and usage

The installer copies files to the selected destination. For Claude, it merges the SessionStart configuration without replacing unrelated settings.

Before upgrading, back up local customizations. Replacing changed installed files requires the explicit `--force` flag; use `--dry-run` to preview changes first.

Give the agent a concrete outcome and clear acceptance checks. For example:

> Add input validation to this API. Reproduce the invalid-input failure first, preserve unrelated changes, implement the smallest fix, and show the test results.

The optional runtime uses explicit provider and model settings, with credentials supplied through the environment rather than committed to the repository. Read the [runtime guide](docs/RUNTIME.md) before enabling requests that may incur charges.

## Technology stack

| Component | Implementation |
|---|---|
| Skill, agent, and command definitions | Markdown with skill metadata |
| Runtime, validators, and regression tests | Python 3.10+ and pytest |
| Installation and hook helpers | Bash and host configuration JSON |
| Selected skill helpers | Python, JavaScript, and shell; dependencies vary by skill |
| Optional native reports | `python-docx`, `openpyxl`, ReportLab, `python-pptx`, and `pypdf` |
| Automation | GitHub Actions; remote execution status is reported separately |

## 🔁 The engineering loop

```text
UNDERSTAND ──▶ PLAN ──▶ EXECUTE ──▶ VERIFY ──▶ DELIVER
```

A typical workflow is:

1. Map the requirement with [brainstorming](skills/brainstorming/SKILL.md).
2. Isolate approved work in [Git worktrees](skills/using-git-worktrees/SKILL.md).
3. Break the work into atomic tasks with [writing-plans](skills/writing-plans/SKILL.md).
4. Implement using [test-driven development](skills/test-driven-development/SKILL.md).
5. Inspect the diff with [requesting-code-review](skills/requesting-code-review/SKILL.md).
6. Report actual results using [verification-before-completion](skills/verification-before-completion/SKILL.md).
7. Ship through [finishing-a-development-branch](skills/finishing-a-development-branch/SKILL.md).

## 🧩 Engineering and reasoning toolkit

<details>
<summary><strong>Engineering workflow</strong> — 20 skills for spec-to-PR discipline</summary>

`code-review` · `codebase-design` · `diagnosing-bugs` · `domain-modeling` · `grill-with-docs` · `implement` · `implement-spec` · `improve-codebase-architecture` · `pr` · `prototype` · `research` · `retro` · `to-spec` · `to-tickets` · `triage` · `wayfinder` · `wizard` · `tdd` · `git-guardrails` · `setup-pre-commit`

Supports spec-to-ticket-to-PR workflows, refactoring plans, bug reproduction, and codebase navigation.

</details>

<details>
<summary><strong>Decision and reasoning toolkit</strong> — 28 on-demand reasoning models</summary>

The 28 `thinking-*` skills include `first-principles`, `ooda`, `pre-mortem`, `red-team`, `second-order`, `systems`, `cynefin`, `triz`, `probabilistic`, `socratic`, `steel-manning`, and `theory-of-constraints`, among others.

</details>

<details>
<summary><strong>Documents and judgment</strong></summary>

`doc-coauthoring` · `discernment-nudge` — collaborative drafting and judgment checks.

</details>

## 💡 Try a focused task

Use a bounded task to explore the workflow:

> Rename a shared configuration key across source and tests. Inventory its consumers, preview the exact edit plan, preserve unrelated changes, and show the test results.

For concrete multi-file editing commands and migration scenarios, see the [coding workflow guide](docs/CODING-WORKFLOWS.md).

## Repository structure

| Path | Contents |
|---|---|
| [`skills/`](skills/) | 140 skills, each with a `SKILL.md` entry point |
| [`agents/`](agents/) | 73 agent definitions |
| [`commands/`](commands/) | 97 slash commands |
| [`hooks/`](hooks/) | Executable SessionStart hook and written guidance |
| [`runtime/`](runtime/) | Optional semantic routing, council, evaluation, and document pipeline |
| [`scripts/`](scripts/) | Installation, validation, release metadata, and documentation checks |
| [`docs/`](docs/) | Setup, workflows, methodology, and provenance |
| [`tests/`](tests/) | 272 passing local regression checks |
| [`evals/`](evals/) | Behavioral scenarios, 50 runtime contracts, and 50 objective microtasks |
| [`examples/experimental/`](examples/experimental/) | Opt-in experimental skills |

## Validation

Run the repository's validation commands from the project root:

```bash
python3 scripts/validate.py
python3 scripts/smoke_test.py
python3 -m pytest tests/ -q
python3 scripts/sync_catalog.py --check
python3 scripts/release_metadata.py --check
python3 scripts/check_docs.py
git diff --check
```

## 🛡️ Ownership and provenance

Original material is available under the [MIT license](LICENSE).

---

## Documentation

| Goal | Guide |
|---|---|
| First installation | [Getting started](docs/GETTING-STARTED.md) |
| Host-specific setup | [Installation and compatibility](docs/INSTALL.md) |
| Resolve common setup problems | [Troubleshooting](docs/TROUBLESHOOTING.md) |
| Run semantic routing and councils | [Runtime](docs/RUNTIME.md) |
| Evaluate tasks or generate documents | [Objective evaluation](docs/OBJECTIVE-EVALUATION.md) |
| Review implemented and remaining work | [Blueprint status](docs/BLUEPRINT-STATUS.md) |
| Prepare a release | [Release procedure](docs/RELEASING.md) |

## Community

Use the [issue templates](.github/ISSUE_TEMPLATE) to report reproducible bugs or request focused skill improvements.

Before contributing, review [CONTRIBUTING.md](CONTRIBUTING.md) for testing, licensing, and review expectations. Report security concerns privately through [SECURITY.md](SECURITY.md).

## Executable runtime foundation

The runtime foundation includes persistent vector retrieval, budgeted skill routing, evidence hashes, capability-based model selection, peer-critique councils, and regression scoring. See the [runtime contracts and runnable demo](docs/RUNTIME.md).

Real provider integration and live-model benchmarks remain separate validation work.

### Executable blueprint progress

The [connected runtime](docs/RUNTIME.md) includes explicit HTTP chat and embedding adapters, semantic indexing, memory retrieval, budgeted debate, and reviewed skill improvement.

The [blueprint status](docs/BLUEPRINT-STATUS.md) distinguishes executable contracts from unproven model-quality and marketplace claims. The weekly benchmark runs 50 distinct offline runtime contracts; it is not a live intelligence leaderboard.

### Objective tasks and executable documents

The [50 coding and infrastructure microtasks](docs/OBJECTIVE-EVALUATION.md) support explicit provider generation, separate replay grading, and source-labeled calibration.

The document pipeline generates and reopens DOCX, XLSX, PDF, and PPTX files in CI. Neither reference calibration nor offline contract tests are presented as live model-performance results.

See the [measured inventory](docs/MEASURED-INVENTORY.md) for counts.

---

<div align="center">

[Contributing](CONTRIBUTING.md) · [Security](SECURITY.md) · [Changelog](CHANGELOG.md) · [Philosophy](docs/PHILOSOPHY.md) · [Command catalog](docs/COMMANDS.md) · [Code of Conduct](CODE_OF_CONDUCT.md)

**⭐ If this pack makes your agent measurably better, star the repository.**

</div>
