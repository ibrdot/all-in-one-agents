# AGENTS.md — Repo Map (for agents)

You are in **all-in-one-agents**, an installable agent skill framework.

## Start here

1. Load `skills/using-all-in-one-agents/SKILL.md` — the bootstrap (workflow + rules)
2. Load `skills/pack-kernel/SKILL.md` — the orchestration loop when planning
3. Consult `INDEX.md` to find a domain skill for the task

## Layout

| Path | What |
|---|---|
| `skills/` | 81 skills, each a folder with `SKILL.md` |
| `agents/` | 73 agent definitions |
| `commands/` | 97 slash commands |
| `hooks/` | SessionStart / Stop / PostToolUse enforcement hooks |
| `.*-plugin/` | per-harness plugin manifests |
| `scripts/` | validate.py, smoke_test.py, install tooling |
| `tests/` | pytest suite — run before every commit |
| `evals/` | behavioral scenarios |
| `docs/` | install, philosophy, telemetry, catalogs |

## Rules of this repo

- Tests green before any commit: `python3 -m pytest tests/ -q`
- No third-party attribution in files — original content only
- Conventional commits, one idea per commit
