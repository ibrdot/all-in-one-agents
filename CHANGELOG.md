# Changelog

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
- **Plugin manifests** for 12 harnesses: Claude Code, Cursor, Codex, Gemini, OpenCode, Copilot CLI, Devin, Hermes, Muse, Kimi Code, Pi, Antigravity
- **Test suite** (11 tests) + behavioral evals (3 scenarios) + CodeQL
- One-command installer (`install.sh`) with hook wiring
- Versioning infra: package.json, bump script, pre-commit config
- Docs: PHILOSOPHY, GETTING-STARTED, TELEMETRY, per-harness INSTALL

### Changed
- Core workflow skills rewritten as original content
- Company-internal/niche skills moved to `examples/experimental/` (11 skills)

### Numbers
- 70 skills in default path, 73 agents, 97 commands, 11 experimental
