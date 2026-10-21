# Installation

This pack works with any agent harness that reads `SKILL.md`-style skills.

## Quick install (any harness)

```bash
git clone https://github.com/ibrdot/all-in-one-agents.git
```

Then copy or symlink what you need:

```bash
# a single skill
cp -r all-in-one-agents/skills/pdf ~/.config/your-harness/skills/

# everything
cp -r all-in-one-agents/skills/* ~/.config/your-harness/skills/
```

## Per-harness locations

| Harness | Skills directory |
|---|---|
| Claude Code | `~/.claude/skills/` |
| OpenCode | `~/.config/opencode/skills/` or `.opencode/skills/` in project |
| Cursor | `.cursor/rules/` (paste SKILL.md body) |
| Codex / others | follow the harness's skill/plugin folder convention |

## Agents & commands

- `agents/` — drop into your harness's agents directory (e.g. `~/.claude/agents/`)
- `commands/` — drop into your harness's commands directory (e.g. `~/.claude/commands/`) and invoke as `/name`

## Verify

```bash
python3 scripts/validate.py
```

All skills should report valid frontmatter.
