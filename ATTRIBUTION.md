# Attribution

This pack aggregates work from several sources. MIT requires that the original
copyright notice be retained for derived work; this file and `NOTICE` satisfy that
obligation for the material listed below.

## obra/superpowers

- Upstream: https://github.com/obra/superpowers
- License: MIT, Copyright (c) 2025 Jesse Vincent
- What is derived here:
  - `skills/brainstorming`, `writing-plans`, `executing-plans`,
    `subagent-driven-development`, `test-driven-development`,
    `systematic-debugging`, `writing-skills`, `dispatching-parallel-agents`,
    `using-git-worktrees`, `verification-before-completion`,
    `finishing-a-development-branch`, `requesting-code-review`,
    `receiving-code-review` — condensed from the upstream skills.
  - `skills/diagnosing-the-pack` (upstream: `diagnosing-superpowers`) and
    `skills/using-all-in-one-agents` (upstream: `using-superpowers`).
  - Scripts, prompts, templates and reference files that are reproduced
    verbatim (57 files at the time of the 2026-10-21 audit).
- The upstream MIT notice is reproduced in `NOTICE`.

## Anthropic published skills

- `skills/pptx`, `skills/docx`, `skills/xlsx`, `skills/pdf`
- These contain Anthropic's published document-tooling code and OOXML
  validation schemas. They are vendored, not authored here.
- Verify the current upstream license before redistributing commercially.

## "ECC" pack

Several skills cite or adapt material from an external pack referred to as
"ECC" (`brand-voice`, `docs-governance`, `context-and-decisions`,
`story-lifecycle`, `github-ops`, `delivery-gate`, `module-regression`,
`frontend-design-direction`, `continuous-learning*`, `council-multi-model`,
`manim-video`, `skill-stocktake`, `frontend-slides`, `brand-discovery`).

**Provenance for this material has not been established.** Before publishing a
release, identify the upstream project, confirm its license, and add it here.
Until then treat those skills as unreviewed third-party content.

## Original to this pack

Everything not listed above — including `taste`, `taste-application`,
`taste-distillation`, `skill-comply`, `verify-openhands`, `pack-kernel`,
`agent-self-evaluation`, `rules-distill`, and the agent/command definitions.

## Additional reviewed import

`skills/receiving-code-review` is imported unchanged from obra/superpowers
commit `b739a8af570e10a95898f2bdf6cec97467fa6c12` (MIT). Its upstream license is retained alongside the skill.
File-level SHA-256 hashes are recorded in [docs/import-manifest.json](docs/import-manifest.json).
The seven coding workflow skills added with this change are original to this pack.

## Matt Pocock skills (2026-10-21 import)

- Upstream: https://github.com/mattpocock/skills
- License: MIT, Copyright (c) 2026 Matt Pocock (upstream notice reproduced in `NOTICE`)
- What is derived here: the following skills were imported and lightly adapted
  (descriptions trimmed, personal-name references removed):
  `code-review`, `codebase-design`, `diagnosing-bugs`, `domain-modeling`,
  `grill-with-docs`, `implement`, `implement-spec`,
  `improve-codebase-architecture`, `pr`, `prototype`, `research`, `retro`,
  `to-spec`, `to-tickets`, `triage`, `wayfinder`, `wizard`, `tdd`,
  `git-guardrails` (upstream `git-guardrails-claude-code`), `setup-pre-commit`.
- Skills deliberately not imported: `ask-matt`, `setup-matt-pocock-skills`,
  and everything under upstream `skills/in-progress/`.

## TJ Boudreaux thinking skills (2026-10-21 import)

- Upstream: https://github.com/tjboudreaux/cc-thinking-skills
- License: MIT, Copyright (c) 2025 TJ Boudreaux (upstream notice reproduced in `NOTICE`)
- What is derived here: the 28 `thinking-*` skills were imported unchanged.

## Additional Anthropic imports (2026-10-21)

- `skills/doc-coauthoring` and `skills/discernment-nudge` imported from
  https://github.com/anthropics/skills (see the "Anthropic published skills"
  section above for license caveats).
