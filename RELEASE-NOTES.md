# Release Notes — v1.1.0

**all-in-one-agents v1.1.0** — the pack goes from 83 to 133 skills.

## Highlights

- 🧠 **50 new skills** — 133 total: full engineering workflow (spec to PR), 28 on-demand reasoning models, and document co-authoring
- 🔀 **Stronger coding core** — code-review with parallel standards/spec axes, refactoring plans, bug reproduction, git guardrails
- 🧩 **Reasoning on tap** — first-principles, OODA, pre-mortem, red-team, systems, TRIZ, and 22 more thinking skills
- 📚 **Docs & catalog refreshed** — INDEX, routing map, and counts regenerated; all tests green (66/66)
- 🪝 Same install, same 12 harnesses, same orchestration kernel

## Upgrade

```bash
git pull && ./install.sh claude
```

Nothing breaks: all v1.0.0 skills, agents, and commands keep their names.

---

# Release Notes — v1.0.0

## Highlights

- 🧠 **Orchestration kernel** — every task runs UNDERSTAND → PLAN → EXECUTE → VERIFY → DELIVER with hard gates; unverified work cannot be delivered
- 🪝 **Hooks that survive compaction** — SessionStart hook reloads the kernel and resumes from the on-disk plan
- 🔌 **12 harness manifests** — install as a plugin in Claude Code, Cursor, Codex, Gemini, OpenCode, Copilot CLI, and more
- ✅ **Tested** — pytest suite + script smoke tests + CodeQL, all enforced in CI
- 📦 **One command install** — `git clone … && ./install.sh`

## Install

```bash
git clone https://github.com/ibrdot/all-in-one-agents.git
cd all-in-one-agents
./install.sh            # Claude Code
./install.sh opencode   # OpenCode
```

## Contents

70 skills (default path) · 73 agents · 97 commands · 11 experimental skills
