# Release Notes — v1.0.0

**all-in-one-agents v1.0.0** — from skill catalog to installable framework.

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
