# Release notes - v1.6.0

## Organization move and the new landing site

This release moves the project to the ibrorg organization and ships the new
GitHub Pages site. It includes 140 skills, 73 agents, 97 commands and the same
Python runtime as v1.5.0.

### Highlights

- New landing site at https://ibrorg.github.io/all-in-one-agents/ — pure-black
  console design, typed terminal hero artifact, pipeline engineering-loop
  diagram, bento feature grid, section rail with scrollspy, custom cursor, and
  accessible reduced-motion and no-JS fallbacks. Zero build step, served from /docs.
- Project identity is now ibrorg: LICENSE copyright, plugin and extension
  manifests, README badges, install instructions and all site URLs.
- The portable master prompt lives at
  skills/using-all-in-one-agents/MASTER_PROMPT.md. The root MASTER-PROMPT.md and
  MASTER-PROMPT.min.md were removed; gen_routing.py and the integrity tests now
  target the skill path, and docs/INSTALL.md no longer offers a prompt-only
  install path.
- Explicit local memory CLI with validated put, read-only semantic search and
  delete; new databases use private permissions.

### Upgrade

```sh
git fetch origin --tags
git checkout v1.6.0
./install.sh claude --dry-run
./install.sh claude
```

If installation reports modified files, back them up and review differences
before using `./install.sh claude --force`. Do not overwrite local customizations
blindly. Other adapters retain host-specific evidence limits documented below.

Optional native document dependencies:

```sh
pip install -r requirements-documents.txt
```

### Verification

- Full local suite passing (pytest), skill validation, smoke checks and the
  generated catalog check; release metadata synchronized across all
  plugin/extension manifests.
- Markdown local-link, heading-anchor and SVG checks pass after the prompt move.
- Release source archives are built from the tagged commit; SHA256SUMS accompanies
  the tar.gz and zip assets. Verification receipt records the exact commit.

### Boundaries

No real-provider quality score, native CLI/desktop rendering proof, official
marketplace listing or commercial service is established by this release. Task
Python execution is opt-in and must run in a separate restricted environment:
resource limits are not a sandbox. Estimated chat budgets exclude embeddings.
Remote CI status is independent of these local verification results.

See [runtime guide](docs/RUNTIME.md), [objective evaluation](docs/OBJECTIVE-EVALUATION.md),
[compatibility evidence](docs/COMPATIBILITY-EVIDENCE.md) and
[blueprint status](docs/BLUEPRINT-STATUS.md) for commands and exact limits.

### Rollback

Keep the previous installation and local customizations backed up. To inspect the
previous published source use `git checkout v1.5.0`; restore your installation
backup rather than assuming an older copy will remove newer installed files.
Runtime databases and operator-owned output are not migrated by the installer.
