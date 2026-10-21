# Release notes - v1.5.0

## Runtime, objective evaluation and safer installs

This release packages the changes since published v1.2.0. It includes 140 skills,
73 agents, 97 commands, a connected Python runtime and 272 passing local checks.

### Highlights

- Semantic skill indexing and persistent memory retrieval; explicit configurable
  HTTP chat/embedding adapters, cost estimates and budgeted critique council.
- Evidence manifests and reviewed evaluation-led skill improvement with rollback.
- 50 offline runtime contracts, plus 50 objective coding/infra microtasks with
  provider generation and separate replay grading. No invented live-model scores.
- Executable DOCX/XLSX/PDF/PPTX reporting, tested by reopening each native format.
- Installer preflight blocks symlink writes and preserves modified installed
  content unless replacement is explicitly requested with --force.
- Stronger coding playbooks, synchronized plugin versions and safer release tools.

### Upgrade

```sh
git fetch origin --tags
git checkout v1.5.0
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

- Full local suite: 272 passed.
- Skill validation: 140 valid; script smoke checks and generated catalog pass.
- Runtime contract benchmark: 50/50, no baseline regressions.
- Author-reference objective-task calibration: 50/50 (NOT model performance).
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
previous published source use `git checkout v1.2.0`; restore your installation
backup rather than assuming an older copy will remove newer installed files.
Runtime databases and operator-owned output are not migrated by the installer.
