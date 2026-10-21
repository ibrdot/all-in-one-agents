# All-in-One Agents

![validate](https://github.com/ibrdot/all-in-one-agents/actions/workflows/validate.yml/badge.svg)
![version](https://img.shields.io/badge/version-1.0.0-blue)
![license](https://img.shields.io/badge/license-MIT-green)

An installable agent skill framework — **70 skills, 73 agents, 97 commands** — with an orchestration kernel that turns any harness from an eager intern into a disciplined engineer: UNDERSTAND → PLAN → EXECUTE → VERIFY → DELIVER, with hard gates that block unverified work.

## One-command install

```bash
git clone https://github.com/ibrdot/all-in-one-agents.git
cd all-in-one-agents
./install.sh            # Claude Code  (~/.claude)
./install.sh opencode   # OpenCode     (~/.config/opencode)
```

The installer wires skills + agents + commands **and** a SessionStart hook so the kernel survives context compaction. Plugin manifests included for 12 harnesses (Claude Code, Cursor, Codex, Gemini, OpenCode, Copilot CLI, Devin, Hermes, Muse, Kimi Code, Pi, Antigravity) — see `docs/INSTALL.md`.

## What's inside — the core workflow

Seven skills form the backbone; the rest of the pack plugs into it:

1. **brainstorming** — design before code; refuses to build on vague briefs
2. **using-git-worktrees** — isolated branch, green baseline first
3. **writing-plans** — atomic tasks with files, code, verification, rollback
4. **subagent-driven-development** / **executing-plans** — task-by-task execution with review between steps
5. **test-driven-development** — failing test first
6. **requesting-code-review** — independent eyes before merge
7. **finishing-a-development-branch** — suite green, then merge/PR/discard + cleanup

Enforcement: `hooks/SessionStart.md` (kernel survives compaction) · `hooks/Stop.md` (delivery gate) · `hooks/PostToolUse.md` (verification gate).

## Structure

```
all-in-one-agents/
├── skills/        70 skills (each: SKILL.md + scripts + references)
├── agents/        73 agent definitions
├── commands/      97 slash commands
├── hooks/         enforcement hooks
├── tests/         pytest suite (runs in CI)
├── evals/         behavioral scenarios
├── examples/experimental/   11 niche skills (opt-in)
└── .*-plugin/     per-harness plugin manifests
```

📖 **[INDEX.md](INDEX.md)** — full catalog · 🛠 **[docs/INSTALL.md](docs/INSTALL.md)** — per-harness install · 🧭 **[docs/PHILOSOPHY.md](docs/PHILOSOPHY.md)** — the methodology

## Stats

| Collection | Count |
|------------|-------|
| Skills (default path) | 70 |
| Agents | 73 |
| Commands | 97 |
| Experimental skills | 11 |
| Harness manifests | 12 |
