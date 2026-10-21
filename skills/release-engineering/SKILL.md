---
name: release-engineering
description: Use when cutting a release, publishing a package or image, managing versions and changelogs, or designing the build, tag, and rollback path for a deploy.
---

# Ship releases that can be rolled back

## Workflow

1. Freeze scope: what is in the release, what is explicitly deferred, and what the acceptance checks are. Record the exact commit.
2. Verify from a clean checkout: build, full test suite, smoke tests, and any generated artifacts checked in or published. Never release from a dirty or unknown worktree.
3. Determine the version from the project's scheme (semver or documented policy) and whether the change is breaking. Write changelog entries describing user-visible changes, not commit messages.
4. Build reproducibly where possible and record the artifact digests. Sign or checksum artifacts when the distribution channel supports it.
5. Roll out incrementally when the channel allows: canary, percentage, or staged environments, with a health check defined before the first step, not after.
6. Define the rollback command and its limits before deploying. A rollback that requires manual data repair is an incident plan, not a rollback.
7. After release, verify real telemetry, close or file follow-ups, and record what the release notes promised versus what shipped.

## Release record

Version, commit, artifacts and digests, checks with results, rollout steps, rollback command, and follow-ups. Publishing to public registries is a separate explicit authorization every time.
