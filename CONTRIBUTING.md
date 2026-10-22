# Contributing

Help make agent workflows useful, specific, and verifiable.

> **30-second orientation** — search [INDEX.md](INDEX.md) for overlapping triggers
> before adding a skill; branch fresh off `main`; make the smallest coherent
> change; run the validation block in [Development checklist](#development-checklist);
> open a PR describing what changed, the verification commands you ran, and any AI
> assistance accurately. Do not invent a human review or a passing test.

---

## Before adding a skill

Search [INDEX.md](INDEX.md) for overlapping triggers. Improve an existing skill
when the new behavior belongs there. A new folder needs a clear trigger and a
non-obvious procedure, executable helper, or useful reference — not generic advice.

## Skill contract

```text
skills/<kebab-case-name>/
  SKILL.md       # name + trigger-rich description frontmatter
  scripts/       # optional, inspected and tested helpers
  references/    # optional, loaded on demand
```

State preconditions, exact commands, failure modes, approval boundaries, and
completion evidence. Link each helper from its skill. Include negative tests
for code that modifies files.

## Original work and imports

Original work is preferred. For an import, record the upstream URL, immutable
revision, source/destination paths, reviewed license, and SHA-256 hashes in
[`docs/import-manifest.json`](docs/import-manifest.json). Retain required notices
with redistributed material (consolidated in `LICENSE`). Do not strip license
notices from an import. If permission is unclear, do not import it until resolved.

---

## Development checklist

1. Branch from the current default branch and preserve unrelated work.
2. Add or update tests; demonstrate failure for a new regression case where practical.
3. Make the smallest coherent change.
4. Regenerate the catalog and routing:

```bash
python3 scripts/sync_catalog.py
python3 scripts/gen_routing.py
python3 scripts/validate.py
python3 scripts/smoke_test.py
python3 -m pytest tests/ -q
python3 scripts/sync_catalog.py --check
git diff --check
```

5. Inspect changed files and imported notices. Use a conventional commit.
6. Open a pull request describing what changed, verification, remaining limits,
   and AI assistance accurately. Do not invent a human review or passing test.

---

## ✅ PR-ready checklist

Tick every box before opening a PR. Each one is command-verifiable or
file-inspectable — if a box cannot be ticked, the PR is not ready.

- [ ] Branched fresh off `main` (no stale base, no unrelated commits bundled)
- [ ] `INDEX.md` searched for overlapping triggers; existing skill improved if behavior belongs there
- [ ] New skill folder has a clear trigger and a non-obvious procedure (not generic advice)
- [ ] `SKILL.md` states preconditions, exact commands, failure modes, approval boundaries, completion evidence
- [ ] Helpers linked from their skill; negative tests included for file-modifying code
- [ ] For imports: upstream URL, immutable revision, source/destination paths, license, SHA-256 hashes recorded in `docs/import-manifest.json`
- [ ] License notices retained (not stripped) — consolidated in `LICENSE`
- [ ] Conventional commit used (e.g. `feat:`, `fix:`, `docs:`, `chore:`)
- [ ] `python3 scripts/sync_catalog.py` ran (catalog regenerated)
- [ ] `python3 scripts/gen_routing.py` ran (routing regenerated)
- [ ] `python3 scripts/validate.py` exits 0
- [ ] `python3 scripts/smoke_test.py` exits 0
- [ ] `python3 -m pytest tests/ -q` shows 0 failures
- [ ] `python3 scripts/sync_catalog.py --check` exits 0 (catalog is in sync)
- [ ] `python3 scripts/check_docs.py` reports 0 errors (local links, heading anchors, SVGs)
- [ ] `git diff --check` is clean (no whitespace damage, no conflict markers)
- [ ] PR body describes: what changed, verification commands run, remaining limits, AI assistance (accurately)
- [ ] No invented human review or passing test claimed

---

## Review focus

Review trigger quality, overlap, safe defaults, practical reproducibility,
license compatibility, and whether the documented commands actually run.

## Scope guardrails

- **In scope**: skills, agents, commands, docs, site, runtime helpers, tests.
- **Out of scope without discussion first**: CI workflow changes, dependency
  bumps that change behavior, license/legal structure changes, removal of
  attribution. Discuss these in a [Discussion](https://github.com/ibrorg/all-in-one-agents/discussions)
  or issue before opening the PR.
- **Hard constraints on the Pages site**: pure black `#000` background, single
  accent `#00FF9C`, page weight under 100KB excluding fonts, no build step.

## Documentation and assets

Use clear headings, working relative links, accessible image text and scoped
commands. Run `python3 scripts/check_docs.py` for maintained project Markdown,
heading anchors and local SVG structure; external URLs are listed but not
certified by the offline checker. Imported skill corpora and archived plans need
separate source-specific review. Do not fabricate SVG assets or native-host
support to satisfy a checklist. Follow [release procedure](docs/RELEASING.md) for
version consistency, artifacts and verification receipts.

---

## Next

- [Code of Conduct](CODE_OF_CONDUCT.md) — community expectations
- [Security policy](SECURITY.md) — report security concerns privately
- [Release procedure](docs/RELEASING.md) — version consistency and artifacts
- [AGENTS.md](AGENTS.md) — onboarding for coding agents working in this repo
- [Discussions](https://github.com/ibrorg/all-in-one-agents/discussions) — coordination hub for ongoing work
