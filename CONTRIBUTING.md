# Contributing

New skills, agents, and commands are welcome.

## Requirements

1. **Tests pass** — `python3 -m pytest tests/ -q` and `python3 scripts/validate.py` both green
2. **Original content** — no copied material from other projects
3. **Skill quality bar** — see `skills/writing-skills/SKILL.md`:
   - `name` + trigger-rich `description` frontmatter
   - real substance: scripts, references, or a non-obvious procedure
4. **Conventional commits** — one idea per commit

## Process

1. Fork, branch from `main`
2. Add your skill under `skills/<name>/`
3. Regenerate `INDEX.md` (see `skills/skill-pack-manager`)
4. Open a PR — fill in the human-written summary section honestly

## What we don't accept

- Duplicates of existing skills (merge into the existing one instead)
- Single-paragraph advice files with no substance
- Company-internal tools that are useless outside one org (those belong in `examples/experimental/`)
