---
name: api-migration
description: Use when changing an API contract, migrating SDK calls, renaming shared interfaces, or coordinating a breaking change across backend, frontend, tests, and documentation.
---

# Migrate contracts without breaking consumers

## Workflow

1. Inventory the contract: request/response schemas, errors, authorization, pagination, event consumers, SDK versions, and externally maintained clients.
2. Choose additive compatibility first. Define a deprecation window and owner; do not claim control over external consumers.
3. Add contract tests for both existing and intended behavior. Pin fixtures to explicit versions and include invalid-input and authorization cases.
4. Introduce an adapter or versioned endpoint. Deploy compatible producers before consumers; do not remove the old contract in the same step if external clients remain.
5. Migrate owned callers in bounded batches using `multi-file-editing` or `ast-aware-refactoring`. Update examples and generated schemas via their documented generators.
6. Compare telemetry for errors, latency, missing fields, and fallback usage. Define a measurable rollback trigger and retain the old implementation until the agreed window closes.
7. Remove compatibility code only when all known consumers and the owner confirm readiness. Verify fixtures, integration tests, generated client checks, and docs together.

## Migration ledger

Record old/new versions, consumer owners, compatibility mechanism, deployment order, test evidence, rollback command, and unresolved external consumers. Never run production migrations or destructive data changes without explicit authorization.

## Completion gate

Tests demonstrate the new behavior and retained compatibility; every unverified consumer is named rather than silently treated as migrated.
