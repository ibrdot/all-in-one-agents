---
name: database-optimization
description: "Use when queries are slow, the DB is the bottleneck, or load is growing - measurement-first diagnosis, indexing that actually gets used, and the schema-level fixes ORM habits hide."
---

# Database Optimization

Nine times out of ten the database is not slow - a query is, and it has an execution plan that says exactly why. Look at it before optimizing anything.

## Measure first

- `EXPLAIN (ANALYZE, BUFFERS)` (Postgres) or equivalent on the slow query. Read the plan: sequential scan on a big table, sort spilling to disk, or rows-estimated vs rows-actual off by 10x - each names its own fix.
- Find the top offenders by total time (frequency x duration), not the slowest single query. A 20ms query at 1k QPS costs more than a 2s report.
- Log slow queries in prod with thresholds; optimize from real traffic, not the staging wishlist.

## Indexing that works

- Index the columns in WHERE, JOIN, and ORDER BY together - a composite index `(tenant_id, created_at)` serves both filtering and sorting; column order matters (equality first, range last).
- Index selectivity: an index on `is_active` (2 values) is decoration. Covering indexes (`INCLUDE`) let hot queries skip the table entirely.
- Every index slows every write. Review unused indexes quarterly and drop them.

## Schema-level fixes

- N+1 from the ORM is the default disease: batch-load relations or join explicitly ([api-design-patterns](../api-design-patterns/SKILL.md)).
- Add FK constraints and CHECK constraints - they are the cheapest data-quality team you will ever hire.
- Paginate with keyset (cursor), not OFFSET past 10k rows. Count(*) on every list page is a self-inflicted DoS.
- Batch writes; single-row INSERT loops are a tax on everyone.

## When it is not the query

Lock contention, connection-pool exhaustion, and vacuum/autovacuum neglect all masquerade as "slow queries." Check pg_stat_activity and pool metrics before rewriting working code.
