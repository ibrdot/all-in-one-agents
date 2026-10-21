# Changelog

## Unreleased

- Explicit local memory CLI with validated put, read-only semantic search and
  delete. New databases use private permissions; no network or automatic capture.
- Published v1.5.0 assets downloaded again and all three SHA256 checks passed.

## [1.5.0] - 2026-10-21

### Added
- Connected Python runtime: semantic skill indexing, persistent memory retrieval,
  explicit HTTP chat/embedding adapters, capability/cost routing and budgeted
  proposal/critique/judge council with run evidence manifests.
- Reviewed skill improvement: stable repeated evaluations, optional held-out
  checks, hash-guarded promotion and rollback receipts.
- Fifty executable runtime contracts plus fifty objective coding/infrastructure
  microtasks with separate provider generation and replay grading.
- DOCX/XLSX/PDF/PPTX generation and native-file readback tests; optional pinned
  document dependencies and mandatory offline-quality CI workflow.
- Deeper dispatch/review, debugging experiment and behavioral testing playbooks.
- Release metadata synchronization checks covering all plugin/extension versions.

### Changed
- Issue #5: README navigation, technology stack and usage refreshed; added
  troubleshooting and maintained Markdown link/anchor/SVG regression checks.
- Inventory is 140 skills, 73 agents and 97 commands; local suite has 272 passing
  checks. Generated inventory, routing and compatibility documentation refreshed.
- Installer rejects symlink destinations and requires --force to replace modified
  installed content; identical reinstalls remain supported.
- Version helper updates metadata locally only, never stages unrelated work,
  commits, tags or pushes automatically.
- README workflow badge repaired and release notes brought up to date.

### Evidence and limits
- Runtime contracts and author-reference calibration are separate from actual
  model quality. No live-provider score, native-host compatibility, marketplace
  approval or enterprise service is claimed.
- Python grading requires separate execution consent; resource limits are not a
  security sandbox. Embedding charges are excluded from estimated chat budgets.

## Release history note

v1.2.0 was the last published GitHub release. Version 1.4.0 existed in main's
metadata but was not published as a GitHub release; v1.5.0 packages the accumulated
runtime and safety changes. Historical entries below retain their release-time
counts; they are not current inventory.

## [1.1.0] - 2026-10-21

### Added
- 20 new engineering-workflow skills: code-review, codebase-design, diagnosing-bugs, domain-modeling, grill-with-docs, implement, implement-spec, improve-codebase-architecture, pr, prototype, research, retro, to-spec, to-tickets, triage, wayfinder, wizard, tdd, git-guardrails, setup-pre-commit
- 28 new thinking-* reasoning skills (first-principles, ooda, pre-mortem, red-team, and more)
- doc-coauthoring and discernment-nudge for collaborative drafting and judgment checks

### Changed
- Skill count 83 -> 133; routing map, INDEX catalog, and README regenerated
- README redesigned with badge row, collapsible catalogs, and per-harness details
- Upstream attribution recorded in ATTRIBUTION.md and NOTICE

### Earlier foundation work

- Add four engineering skills: performance profiling, test design, release
  engineering, and documentation accuracy (83 skills total).
- Add multi-edit-safety and escaped-bug-regression behavioral scenarios.
- Refresh README with inventory badges and workflow table coverage.

### Earlier workflow work

- Add seven original coding workflows: multi-file editing, AST-aware refactoring,
  API migration, dependency upgrades, codebase context, agent evaluation, and recovery.
- Import receiving-code-review from a pinned MIT-licensed upstream with notices.
- Add a dry-run-first, hash-checked exact-text edit helper and regression coverage.
- Refresh README, contributor and agent guidance, installation, and getting started.
- Add deterministic catalog synchronization and import-integrity checks.

## [1.0.0] — 2026-10-21

First stable release. The pack is now an installable framework, not a catalog.

### Added
- **Orchestration core**: `using-all-in-one-agents` bootstrap + `pack-kernel` phase loop (UNDERSTAND → PLAN → EXECUTE → VERIFY → DELIVER)
- **Enforcement hooks**: SessionStart (compaction recovery), Stop (delivery gate), PostToolUse (verification gate)
- **Core workflow skills**: writing-plans, using-git-worktrees, finishing-a-development-branch, dispatching-parallel-agents, verification-before-completion
- **Plugin manifests** for 15 harnesses (+ any custom install target): Claude Code, Cursor, Codex, Gemini, OpenCode, Copilot CLI, Devin, Hermes, Muse, Kimi Code, Pi, Antigravity, Grok, Qwen, Factory Droid, and any custom target
- **Test suite** (11 tests) + behavioral evals (3 scenarios) + CodeQL
- One-command installer (`install.sh`) with hook wiring
- Versioning infra: package.json, bump script, pre-commit config
- Docs: PHILOSOPHY, GETTING-STARTED, TELEMETRY, per-harness INSTALL

### Changed
- Core workflow skills rewritten as original content
- Company-internal/niche skills moved to `examples/experimental/` (11 skills)

### Numbers
- 70 skills in default path, 73 agents, 97 commands, 11 experimental
