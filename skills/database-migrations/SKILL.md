---
name: database-migrations
description: "Change database schema safely: expand-and-contract migrations, zero-downtime deploys, backfills, and rollback plans for PostgreSQL, MySQL, and ORMs. Use when adding or altering tables, columns, indexes, or constraints on a live system."
---

# Database Migrations

The rule: **old code must run against the new schema, and new code against the old schema**, for one full deploy cycle.

## Expand and contract

1. **Expand:** additive change only. Add column as nullable (or with a default), create index with `CONCURRENTLY`, add table. Never `NOT NULL` in the first pass.
2. **Migrate:** dual-write or backfill in batches. Backfill jobs must be resumable, rate-limited, and observable.
3. **Switch:** deploy code that reads the new source of truth.
4. **Contract:** in a later release, add the `NOT NULL` constraint, then drop the old column. Never in the same release as the expand.

## Before you run anything

- Measured the table: row count and size. A migration that is instant on 10k rows locks a 500M-row table.
- Tested on a production-scale copy, with production-like data distribution.
- Wrote the down-migration, even if the plan is never to use it. Rollback that has never been rehearsed does not exist.
- Checked lock requirements: `ALTER TABLE` grabs locks that queue behind long queries and block everything behind them. Set `lock_timeout` and retry.

## Verify

- Row counts, checksums, or sampled value comparisons after backfill.
- Application error rate flat through the deploy.
- Index actually used by the planner for the target queries.
- Apply [release-engineering](../release-engineering/SKILL.md) for the deploy itself and [verification-before-completion](../verification-before-completion/SKILL.md) for sign-off.

## Anti-patterns

- Renaming a column directly instead of add-new, dual-write, switch, drop-old
- One giant migration mixing schema, backfill, and code changes
- Running migrations by hand from a chat session with no lease and no log
