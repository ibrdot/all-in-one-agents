## [1.1.0] - 2026-10-21

### Added
- 20 new engineering-workflow skills: code-review, codebase-design, diagnosing-bugs, domain-modeling, grill-with-docs, implement, implement-spec, improve-codebase-architecture, pr, prototype, research, retro, to-spec, to-tickets, triage, wayfinder, wizard, tdd, git-guardrails, setup-pre-commit
- 28 new thinking-* reasoning skills (first-principles, ooda, pre-mortem, red-team, and more)
- doc-coauthoring and discernment-nudge for collaborative drafting and judgment checks

### Changed
- Skill count 83 -> 133; routing map, INDEX catalog, and README regenerated
- README redesigned with badge row, collapsible catalogs, and per-harness details
- Upstream attribution recorded in ATTRIBUTION.md and NOTICE
# Changelog

## Unreleased

- Add four engineering skills: performance profiling, test design, release
  engineering, and documentation accuracy (83 skills total).
- Add multi-edit-safety and escaped-bug-regression behavioral scenarios.
- Refresh README with inventory badges and workflow table coverage.

## Unreleased

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
