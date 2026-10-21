---
name: postgres-optimization
description: "Use when Postgres is slow, bloated, or unstable - plan reading, index and vacuum mechanics, connection management, and the operational settings that prevent 3am incidents."
---

# Postgres Optimization

Postgres is fast until a specific, findable thing makes it slow. The job is diagnosis, not folklore.

## Read the plan, not the vibes

- `EXPLAIN (ANALYZE, BUFFERS)` on the real query with real parameters. Key tells: Seq Scan on large filtered tables, estimated vs actual rows off by orders of magnitude (stale statistics -> `ANALYZE`), sorts spilling to disk (work_mem), nested loops over huge sets.
- Optimize total time x frequency. pg_stat_statements ranked by total_exec_time is your to-do list, in order.

## Index mechanics that matter

- Match composite index order to the query: equality columns first, range/sort last. `WHERE tenant_id = $1 ORDER BY created_at DESC` wants `(tenant_id, created_at)`.
- Partial indexes for hot subsets: `CREATE INDEX ... WHERE status = 'pending'` on a queue table is tiny and blazing.
- Bloat is real: dead tuples from heavy UPDATE/DELETE churn need autovacuum tuned (lower scale factors on hot tables), not ignored.

## Operational settings that prevent incidents

- Connection limits: Postgres connections are expensive; use PgBouncer (transaction pooling) rather than raising max_connections into swap death.
- `work_mem` per operation, not per connection - raising it globally on a busy box is an OOM generator.
- Replication lag is a read-replica correctness issue: route read-your-writes to primary or handle staleness explicitly.
- Backup restore drills quarterly. A backup never restored is a hope, not a backup.

## Data-changing operations

Big table changes: batch them (10k rows, sleep, repeat) or use `CREATE INDEX CONCURRENTLY` / `ALTER ... NOT VALID` + validate. Unbatched, they lock the table and take the app down - see [database-migrations](../database-migrations/SKILL.md).
