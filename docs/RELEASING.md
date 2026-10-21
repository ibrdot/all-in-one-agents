# Release procedure

1. Fetch origin/tags, inspect the clean worktree and current published releases.
2. Select a semantic version. Run `bash scripts/bump-version.sh X.Y.Z`; this
   updates all discovered first-party plugin/extension and marketplace versions
   locally, without any implicit staging, commit, tag or network operation.
3. Update CHANGELOG.md, RELEASE-NOTES.md, README and measured inventory. Run
   `python3 scripts/sync_catalog.py` and review changes. Version check is
   `python3 scripts/release_metadata.py --check`.
4. Run full pytest, skill validation, smoke checks, catalog check, diff check,
   offline runtime contracts and objective-reference calibration. Repeat from
   a detached clean checkout of the intended release commit.
5. Explicitly commit reviewed paths with the repository's chosen author. Create
   a single annotated version tag; push main and that tag, not all local tags.
6. Build source zip/tar.gz with git archive from the exact tag. Add a verification
   receipt with commit SHA, command results and evidence boundaries; compute
   SHA256SUMS for each asset. Checksums are not signatures or third-party proof.
7. Publish the GitHub release at that existing tag, upload assets, then download
   them again and verify digests, tag/head correspondence and latest status.
8. Report local and remote-CI evidence separately. An empty workflow list is not
   a green CI result; modifying repository Actions policy needs appropriate
   repository administration access and is not assumed by release tooling.

Rollback means restoring a backed-up installation; older installer copying does
not automatically remove newer files. Preserve operator-owned runtime databases
and local customizations. Never rewrite a published tag to conceal a defect;
ship a new version or clearly mark a release withdrawn.
