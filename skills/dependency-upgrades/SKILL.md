---
name: dependency-upgrades
description: Use when updating packages, resolving dependency vulnerabilities, migrating a library major version, or keeping lockfiles and runtime compatibility in sync.
---

# Upgrade dependencies with controlled risk

## Workflow

1. Read manifests, lockfiles, runtime versions, package-manager configuration, and CI jobs. Use the manager already chosen by the project.
2. Reproduce the baseline install and tests in an isolated checkout. Review install scripts before running unfamiliar packages; do not execute downloaded commands blindly.
3. Read release notes and migration guides for the exact old/new versions. Separate security fixes from unrelated upgrades, and distinguish production from development exposure.
4. Upgrade one dependency family at a time. Preserve the lockfile and use deterministic/frozen installation when checking the result.
5. Adapt breaking APIs with `api-migration` or `ast-aware-refactoring`. Never regenerate a lockfile with an unrelated package manager.
6. Run package-manager integrity checks, type checks, targeted tests, the relevant full suite, and production build. Compare bundle size or runtime performance when the change affects them.
7. Review transitive changes, licenses, removed packages, lifecycle scripts, and runtime engine requirements. Record unresolved advisories with their actual impact.

## Evidence table

For each upgraded family record from/to version, reason, migration reference, lockfile diff, verification commands/results, and rollback commit. Do not claim that a scanner finding alone proves exploitability or that a green scanner proves safety.

## Completion gate

Manifest and lockfile agree, the supported runtime matrix remains valid, and no unrelated dependency churn is included.
