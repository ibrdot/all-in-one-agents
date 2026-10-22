<div align="center">

<img src="https://raw.githubusercontent.com/ibrorg/all-in-one-agents/main/docs/assets/favicon.svg" width="90" height="90" alt="All-in-One Agents logo" />

# ⚡ All-in-One Agents

**The complete engineering workflow for AI coding agents.**

*Understand the task. Plan the change. Edit with care. Verify with evidence.*

[![Tests](https://github.com/ibrorg/all-in-one-agents/actions/workflows/validate.yml/badge.svg)](https://github.com/ibrorg/all-in-one-agents/actions/workflows/validate.yml)
[![Release](https://img.shields.io/github/v/release/ibrorg/all-in-one-agents?style=flat-square&color=8b5cf6)](https://github.com/ibrorg/all-in-one-agents/releases)
[![License](https://img.shields.io/badge/license-MIT-16a34a?style=flat-square)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-ff69b4?style=flat-square)](CONTRIBUTING.md)

[![Skills](https://img.shields.io/badge/skills-141-2563eb?style=flat-square)](INDEX.md)
[![Agents](https://img.shields.io/badge/agents-73-0ea5e9?style=flat-square)](INDEX.md)
[![Commands](https://img.shields.io/badge/commands-97-64748b?style=flat-square)](INDEX.md)
[![Tests passing](https://img.shields.io/badge/tests-272-22c55e?style=flat-square)](tests/)
[![Python](https://img.shields.io/badge/python-3.10+-3776ab?style=flat-square)](https://www.python.org/)

</div>

---

<div align="center">

<h3>📊 By the numbers</h3>

| Skills | Agents | Commands | Tests | Runtime contracts | Objective microtasks |
|:------:|:------:|:--------:|:-----:|:------------------:|:--------------------:|
| **141** | **73** | **97** | **272** | **50** | **50** |

</div>

---

## 📑 Table of contents

- [Overview](#overview)
- [What it solves](#-what-it-solves)
- [Quick start](#quick-start)
- [The engineering loop](#-the-engineering-loop)
- [Engineering and reasoning toolkit](#-engineering-and-reasoning-toolkit)
- [Configuration and usage](#configuration-and-usage)
- [Technology stack](#technology-stack)
- [Repository structure](#repository-structure)
- [Validation](#validation)
- [Documentation](#documentation)
- [Community](#community)
- [Executable runtime foundation](#executable-runtime-foundation)

---

## Overview

A practical toolkit for AI-assisted engineering: **141 skills, 73 agent definitions,
97 command definitions**, executable workflow helpers and an optional Python runtime.
Start with a bounded task, load only relevant skills, and verify the result.

The pack includes semantic retrieval, peer-critique councils, objective evaluation
and native document generation. Instructions and adapter files do not create
host permissions or prove compatibility. See [tested boundaries](docs/COMPATIBILITY-EVIDENCE.md).

> 💡 **Philosophy in one line** — *A test that has never been seen failing proves nothing.
> "Done" is a claim about reality, and reality is checked with commands.* See
> [Philosophy](docs/PHILOSOPHY.md) for the four commitments everything follows from.

---

## 🧭 What it solves

> Pick the need on the left, start with the skill in the middle, ship what the right column promises.

| Need | Start with | What it adds |
|---|---|---|
| 🔍 Understand an unfamiliar repo | [codebase-context](skills/codebase-context/SKILL.md) | Bounded map of source, tests, contracts, unknowns |
| ✏️ Change several files safely | [multi-file-editing](skills/multi-file-editing/SKILL.md) | Hash-checked previews, exact match counts, explicit apply |
| 🔁 Rename symbols or APIs | [ast-aware-refactoring](skills/ast-aware-refactoring/SKILL.md) | Syntax-aware tools, fixtures, consumer checks |
| 🚚 Migrate contracts | [api-migration](skills/api-migration/SKILL.md) | Compatibility, deployment order, rollback evidence |
| ⬆️ Upgrade dependencies | [dependency-upgrades](skills/dependency-upgrades/SKILL.md) | Controlled lockfile and runtime changes |
| 🚀 Speed up a slow path | [performance-profiling](skills/performance-profiling/SKILL.md) | Profiled, measured, revertible optimization |
| 🧪 Make tests bite | [test-design](skills/test-design/SKILL.md) | Behavior-asserted, non-flaky regression coverage |
| 📦 Cut a release | [release-engineering](skills/release-engineering/SKILL.md) | Clean build, staged rollout, rollback path |
| 📚 Trust the docs | [docs-accuracy](skills/docs-accuracy/SKILL.md) | Every documented command actually runs |
| 🧠 Reason on purpose | [thinking-first-principles](skills/thinking-first-principles/SKILL.md) + 27 more `thinking-*` | OODA, pre-mortem, red-team, systems, TRIZ on demand |
| 🗺️ Wayfind a codebase | [wayfinder](skills/wayfinder/SKILL.md) | Guided orientation in unfamiliar code |
| 🔀 Review a diff properly | [code-review](skills/code-review/SKILL.md) | Standards + spec axes, parallel sub-agents |
| 🤝 Act on review feedback | [receiving-code-review](skills/receiving-code-review/SKILL.md) | Verify suggestions before implementing |
| 👥 Compare agents | [agent-evaluation](skills/agent-evaluation/SKILL.md) | Reproducible fixtures, independent scoring |
| ♻️ Resume interrupted work | [checkpoint-recovery](skills/checkpoint-recovery/SKILL.md) | Reconcile files with recorded evidence |

---

## Quick start

Requires **Git**, **Bash**, **Python 3.10+** (for the edit helper). Review scripts before running them.

```bash
git clone https://github.com/ibrorg/all-in-one-agents.git
cd all-in-one-agents
./install.sh claude --dry-run   # preview
./install.sh claude             # install
```

<details>
<summary><b>📦 Other harnesses and custom paths</b></summary>

```bash
./install.sh opencode           # ~/.config/opencode
./install.sh /your/custom/path # skills/, agents/, commands/
```

The installer copies files into the selected destination; it is **not** an isolated
package manager. Claude installs merge the `SessionStart` configuration without
replacing unrelated settings. Back up local customizations before upgrades.
Replacing changed installed files requires an explicit `--force`; preview with
`--dry-run` first.

</details>

<details>
<summary><b>✅ Validate the install</b></summary>

```bash
python3 -m pip install pytest
python3 scripts/validate.py
python3 scripts/smoke_test.py
python3 -m pytest tests/ -q
```

Loaded instructions do not prove compliance; Markdown gates do not mechanically
block a tool call. Inspect the diff and actual test output after every run.

</details>

<details>
<summary><b>🎯 Give the agent a bounded task</b></summary>

> Add input validation to this API. Reproduce the invalid-input failure first,
> preserve unrelated changes, implement the smallest fix, then show test results.

The intended loop is **understand → plan → execute → verify → deliver**.
Ask questions only when a material unknown cannot be resolved from the project.

</details>

---

## 🔁 The engineering loop

```
  ┌────────────┐    ┌────────┐    ┌──────────┐    ┌──────────┐    ┌───────────┐
  │ UNDERSTAND │──▶ │  PLAN  │──▶ │ EXECUTE  │──▶ │  VERIFY  │──▶ │  DELIVER  │
  └────────────┘    └────────┘    └──────────┘    └──────────┘    └───────────┘
        │               │               │               │               │
        ▼               ▼               ▼               ▼               ▼
   brainstorming   writing-plans   test-driven-    verification-  finishing-a-
   + codebase-     + using-git-    development     before-         development-
     context         worktrees                     completion       branch
```

| # | Stage | Skill |
|---|---|---|
| 1 | Map the requirement | [brainstorming](skills/brainstorming/SKILL.md) |
| 2 | Isolate approved work | [using-git-worktrees](skills/using-git-worktrees/SKILL.md) |
| 3 | Create atomic tasks | [writing-plans](skills/writing-plans/SKILL.md) |
| 4 | Implement | [test-driven-development](skills/test-driven-development/SKILL.md) |
| 5 | Inspect the diff | [requesting-code-review](skills/requesting-code-review/SKILL.md) |
| 6 | Show real results | [verification-before-completion](skills/verification-before-completion/SKILL.md) |
| 7 | Ship | [finishing-a-development-branch](skills/finishing-a-development-branch/SKILL.md) |

---

## 🧩 Engineering and reasoning toolkit

<details>
<summary><b>🏗️ Engineering workflow</b> — 20 skills for spec-to-PR discipline</summary>

`code-review` · `codebase-design` · `diagnosing-bugs` · `domain-modeling` · `grill-with-docs` · `implement` · `implement-spec` · `improve-codebase-architecture` · `pr` · `prototype` · `research` · `retro` · `to-spec` · `to-tickets` · `triage` · `wayfinder` · `wizard` · `tdd` · `git-guardrails` · `setup-pre-commit`

Spec-to-ticket-to-PR discipline, refactoring plans, bug reproduction, repo wayfinding.

</details>

<details>
<summary><b>🧠 Decision & reasoning toolkit</b> — 28 on-demand reasoning models</summary>

28 `thinking-*` skills: `first-principles`, `ooda`, `pre-mortem`, `red-team`, `second-order`, `systems`, `cynefin`, `triz`, `probabilistic`, `socratic`, `steel-manning`, `theory-of-constraints`, and more.

</details>

<details>
<summary><b>📄 Documents & judgment</b></summary>

`doc-coauthoring` · `discernment-nudge` — collaborative drafting and judgment checks.

</details>

> 💡 **Try a focused task** — *Rename a shared configuration key across source and
> tests. Inventory consumers, preview the exact edit plan, preserve unrelated
> changes, and show the test results.*
> Concrete multi-edit commands and migration scenarios: [coding workflow guide](docs/CODING-WORKFLOWS.md).

---

## Configuration and usage

The installer copies into the selected destination; Claude installs merge the
SessionStart configuration without replacing unrelated settings. **Back up local
customizations before upgrades.** Replacing changed installed files requires an
explicit `--force`; preview with `--dry-run` first.

Give the agent a concrete outcome and acceptance checks, for example:

> Add input validation to this API. Reproduce the invalid-input failure first,
> preserve unrelated changes, implement the smallest fix, then show test results.

Optional runtime configuration uses explicit provider/model settings and an
environment-based credential, **not a key committed to the repository**. Follow the
[runtime guide](docs/RUNTIME.md) before enabling potentially billed requests.

---

## Technology stack

| Component | Implementation |
|---|---|
| Skill/agent/command definitions | Markdown with skill metadata |
| Runtime, validators and regression tests | Python 3.10+; pytest |
| Installation and hook helpers | Bash and host configuration JSON |
| Selected skill helpers | Python, JavaScript and shell; inspect per-skill dependencies |
| Optional native reports | python-docx, openpyxl, ReportLab, python-pptx, pypdf |
| Automation | GitHub Actions; remote execution status reported separately |

---

## Repository structure

| Path | Contents |
|---|---|
| [`skills/`](skills/) | 141 skills, each with a `SKILL.md` entrypoint |
| [`agents/`](agents/) | 73 agent definitions |
| [`commands/`](commands/) | 97 slash commands |
| [`hooks/`](hooks/) | Executable SessionStart hook and written guidance |
| [`runtime/`](runtime/) | Optional semantic routing, council, evaluation and document pipeline |
| [`scripts/`](scripts/) | Install, validation, release metadata and documentation checks |
| [`docs/`](docs/) | Setup, workflows, methodology, provenance |
| [`tests/`](tests/) | 272 passing local regression checks |
| [`evals/`](evals/) | Behavioral scenarios, 50 runtime contracts and 50 objective microtasks |
| [`examples/experimental/`](examples/experimental/) | Opt-in experimental skills |

---

## Validation

```bash
python3 scripts/validate.py
python3 scripts/smoke_test.py
python3 -m pytest tests/ -q
python3 scripts/sync_catalog.py --check
python3 scripts/release_metadata.py --check
python3 scripts/check_docs.py
git diff --check
```

Original material is under [LICENSE](LICENSE).

---

<div align="center">

### 🌟 Community

[Contributing](CONTRIBUTING.md) · [Security](SECURITY.md) · [Changelog](CHANGELOG.md) · [Philosophy](docs/PHILOSOPHY.md) · [Command catalog](docs/COMMANDS.md) · [Code of Conduct](CODE_OF_CONDUCT.md)

**⭐ If this pack makes your agent measurably better, star the repo.**

</div>

---

## Documentation

| Goal | Guide |
|---|---|
| First installation | [Getting started](docs/GETTING-STARTED.md) |
| Host-specific setup | [Installation and compatibility](docs/INSTALL.md) |
| Fix common setup problems | [Troubleshooting](docs/TROUBLESHOOTING.md) |
| Run semantic routing and councils | [Runtime](docs/RUNTIME.md) |
| Evaluate tasks or generate documents | [Objective evaluation](docs/OBJECTIVE-EVALUATION.md) |
| Check implemented vs remaining work | [Blueprint status](docs/BLUEPRINT-STATUS.md) |
| Prepare a release | [Release procedure](docs/RELEASING.md) |

---

## Community

Use the [issue templates](.github/ISSUE_TEMPLATE) for reproducible bugs and focused
skill requests. Follow [CONTRIBUTING.md](CONTRIBUTING.md) for tests, licensing and
review expectations. Report security concerns privately using [SECURITY.md](SECURITY.md).

---

## Executable runtime foundation

Persistent vector retrieval, budgeted skill routing, evidence hashes, capability-based model selection, peer-critique councils, and regression scoring: see [runtime contracts and runnable demo](docs/RUNTIME.md). Real provider integration and live-model benchmarks remain separate validation work.

### Executable blueprint progress

The [connected runtime](docs/RUNTIME.md) now includes explicit HTTP chat/embedding
adapters, semantic indexing, memory retrieval, budgeted debate and reviewed skill
improvement. [Blueprint status](docs/BLUEPRINT-STATUS.md) separates executable
contracts from unproven model-quality and marketplace claims. The weekly benchmark
runs 50 distinct offline runtime contracts, not a live intelligence leaderboard.

### Objective tasks and executable documents

[50 coding/infra microtasks](docs/OBJECTIVE-EVALUATION.md) now support explicit
provider generation, separate replay grading, and source-labeled calibration.
The document pipeline generates and reopens DOCX/XLSX/PDF/PPTX in CI. Neither
reference calibration nor offline contract tests are advertised as live model
performance. See the [measured inventory](docs/MEASURED-INVENTORY.md) for counts.
