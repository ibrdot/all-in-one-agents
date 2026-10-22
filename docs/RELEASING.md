# Release procedure

## ⏱️ 30-second TL;DR

Eight steps: fetch tags → bump version → update docs + sync catalog → full validation → commit + tag → build archives → publish release → report evidence separately. Each step below expands on demand.

> **Hard rules**: never rewrite a published tag to conceal a defect — ship a new
> version or mark the release withdrawn. Checksums are not signatures or
> third-party proof. An empty workflow list is not a green CI result.

---

## Steps

<details>
<summary><b>1 — Fetch and inspect</b></summary>

Fetch origin/tags, inspect the clean worktree and current published releases.

</details>

<details>
<summary><b>2 — Bump version</b></summary>

Select a semantic version. Run:

```bash
bash scripts/bump-version.sh X.Y.Z
```

This updates all discovered first-party plugin/extension and marketplace versions
locally, without any implicit staging, commit, tag or network operation.

</details>

<details>
<summary><b>3 — Update docs and catalog</b></summary>

Update `CHANGELOG.md`, `RELEASE-NOTES.md`, `README` and measured inventory. Run
`python3 scripts/sync_catalog.py` and review changes. Version check is
`python3 scripts/release_metadata.py --check`.

</details>

<details>
<summary><b>4 — Full validation</b></summary>

Run full pytest, skill validation, smoke checks, catalog check, diff check,
offline runtime contracts and objective-reference calibration. Repeat from
a detached clean checkout of the intended release commit.

</details>

<details>
<summary><b>5 — Commit and tag</b></summary>

Explicitly commit reviewed paths with the repository's chosen author. Create
a single annotated version tag; push main and that tag, not all local tags.

</details>

<details>
<summary><b>6 — Build archives and receipt</b></summary>

Build source zip/tar.gz with `git archive` from the exact tag. Add a verification
receipt with commit SHA, command results and evidence boundaries; compute
`SHA256SUMS` for each asset. Checksums are not signatures or third-party proof.

</details>

<details>
<summary><b>7 — Publish release</b></summary>

Publish the GitHub release at that existing tag, upload assets, then download
them again and verify digests, tag/head correspondence and latest status.

</details>

<details>
<summary><b>8 — Report evidence separately</b></summary>

Report local and remote-CI evidence separately. An empty workflow list is not
a green CI result; modifying repository Actions policy needs appropriate
repository administration access and is not assumed by release tooling.

</details>

---

## Rollback

Rollback means restoring a backed-up installation; older installer copying does
not automatically remove newer files. Preserve operator-owned runtime databases
and local customizations. Never rewrite a published tag to conceal a defect;
ship a new version or clearly mark a release withdrawn.

---

## Next

- [Measured inventory](MEASURED-INVENTORY.md) — what to verify before tagging
- [Blueprint status](BLUEPRINT-STATUS.md) — delivered vs remaining layers
- [Contributing](../CONTRIBUTING.md) — PR-ready checklist and scope guardrails
- [CHANGELOG](../CHANGELOG.md) — release history
