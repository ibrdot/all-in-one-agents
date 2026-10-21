---
name: writing-skills
description: Author new skills for this pack — structure, naming, trigger design, and quality bar. Use when creating a skill, when a repeated pattern deserves codifying, or when `diagnosing-the-pack` reveals a capability gap.
---

# Writing Skills

A skill is a reusable behavior, not a document dump.

## Anatomy

```
skills/<name>/
├── SKILL.md        # required — frontmatter + instructions
├── scripts/        # optional — executable helpers
├── references/     # optional — deep docs loaded on demand
└── templates/      # optional — reusable scaffolds
```

## Frontmatter

```yaml
---
name: kebab-case-name
description: >
  What it does AND when to fire — written as triggers:
  "Use when <situation>, <situation>, or <phrase the user would say>."
---
```

The description is the routing table entry. If it doesn't name real user phrasings, the skill is invisible.

## Quality bar

- **Imperative instructions**, not essays — the reader is an agent mid-task
- **Commands over prose** — exact commands to run, exact outputs to expect
- **Gates stated explicitly** — "done when: X"
- **Substance required** — a skill earns its folder with scripts, references, or a non-obvious procedure. A paragraph of advice is a blog comment, not a skill.

## Before committing a new skill

1. `python3 scripts/validate.py` and `python3 scripts/smoke_test.py` — both green
2. Check for overlap with an existing skill — merge beats duplicate
3. Regenerate INDEX.md
