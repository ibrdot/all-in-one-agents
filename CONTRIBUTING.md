# Contributing

Help make agent workflows useful, specific, and verifiable.

## Before adding a skill

Search [INDEX.md](INDEX.md) for overlapping triggers. Improve an existing skill
when the new behavior belongs there. A new folder needs a clear trigger and a
non-obvious procedure, executable helper, or useful reference - not generic advice.

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
`docs/import-manifest.json`. Retain required notices with redistributed material
and update `ATTRIBUTION.md`. Do not remove attribution to make an import look original.
If permission is unclear, do not import it until resolved.

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

## Review focus

Review trigger quality, overlap, safe defaults, practical reproducibility,
license compatibility, and whether the documented commands actually run.
