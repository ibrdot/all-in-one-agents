---
name: skill-pack-manager
description: Manage a local skill pack — validate all skills, regenerate the index, find duplicates and stale skills. Use when maintaining a collection of SKILL.md-based skills, before pushing skill updates, or when the user asks to audit, lint, or catalog their skills folder.
---

# Skill Pack Manager

Maintains a folder of skills (`skills/*/SKILL.md`) as a healthy, indexed collection.

## Workflows

### 1. Full audit
```bash
python3 scripts/validate.py
```
Fix every reported error before committing.

### 2. Regenerate the index
After adding/removing/renaming any skill, rebuild `INDEX.md` so the catalog stays truthful. Group by category, link each entry to its `SKILL.md`, and keep counts exact — never round numbers.

### 3. Duplicate detection
Two skills are duplicates when their `description` triggers overlap heavily. Prefer merging into the stronger skill (more scripts/references) and deleting the weaker one.

### 4. Health rules
- Every skill: `SKILL.md` with `name` + `description` frontmatter
- Scripts must be referenced from `SKILL.md`, otherwise they are dead weight
- No empty folders, no orphaned assets

## Definition of done
- `validate.py` passes
- `INDEX.md` counts match the real folder counts
- Commit with a conventional message (`feat:`, `fix:`, `docs:`)
