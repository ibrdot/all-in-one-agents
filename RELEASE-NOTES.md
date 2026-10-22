# Release notes - v1.7.0

## Browser and desktop operation skills, hardened gates, polished docs

This release adds two operation-domain skills, closes the gaps found by deep
accessibility and code-quality passes, and turns the day's lessons into
mechanical CI gates. It includes 142 skills, 73 agents, 97 commands and the
same Python runtime as v1.6.0.

### Highlights

- **computer-use** — native desktop and OS UI automation: accessibility-first
  action ladder, observe-act-observe verification, and a bundled
  `scripts/desktop.py` helper (screenshot, click, drag, type, key, scroll) for
  hosts without built-in desktop automation.
- **browser-use** — operating a real browser for web tasks: observe-first over
  pixels, durable locators, one action per observation cycle, structured
  recovery. Native apps go to computer-use; test authoring to webapp-testing.
- **Hardened validation** — `check_docs.py` now fails on heading level skips;
  a new consistency test fails if skills/agents/commands counts drift from the
  README badges, INDEX header, site stats or measured inventory.
- **Installer fix** — the SessionStart hook is now covered by `--force`
  protection; reinstalls no longer silently overwrite a modified hook.
- **Site accessibility** — copy status announced via aria-live region (WCAG
  4.1.3), repo tree exposed correctly with `role="img"`, install-step heading
  order corrected; keyboard-only navigation verified end to end.
- **Site performance** — Google Fonts CSS preloaded with an onload swap and a
  noscript fallback; measured 13% faster FCP and LCP.
- **Documentation** — all 14 maintained guides refreshed: 30-second TL;DRs,
  collapsible procedures, harness and command category tables, Next sections;
  CONTRIBUTING gains an orientation and an 18-box PR-ready checklist.

### Upgrade

```sh
git fetch origin --tags
git checkout v1.7.0
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

- Full local suite passing: skill validation (142 valid), smoke checks,
  generated catalog check, release metadata synchronized across all manifests.
- New regression coverage: installer hooks `--force` behavior, heading-order
  gate (both directions), inventory-count consistency across four surfaces.
- Markdown local-link, heading-anchor, heading-order and SVG checks pass.
- Site verified live: keyboard-only navigation, screen-reader announcements,
  preload timing improvements measured with Lighthouse.
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
previous published source use `git checkout v1.6.0`; restore your installation
backup rather than assuming an older copy will remove newer installed files.
Runtime databases and operator-owned output are not migrated by the installer.
