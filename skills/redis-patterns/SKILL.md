---
name: redis-patterns
description: "Use when using Redis for caching, queues, or counters - key design, TTL and invalidation strategy, atomic patterns, and avoiding the memory and eviction surprises."
---

# Redis Patterns

Redis is fast, in-memory, and single-threaded per instance. Every pattern below follows from those three facts.

## Key design

- Namespaces with colons: `user:{id}:cart`. Grep-able, cluster-safe, self-documenting.
- **TTL on everything** - every key, no exceptions. Unttl'ed keys are a slow leak until `maxmemory` hits and eviction starts eating your hot data randomly. Explicit `noeviction` + TTLs beats default silent chaos.

## Caching done right

- Cache-aside as default: read cache, miss -> read DB -> write cache with TTL. Stampede protection (lock or in-flight dedupe) for hot keys; a thundering herd on one celebrity key is a self-inflicted outage.
- Invalidation: prefer short TTLs over clever invalidation. Cache coherence is a tax; short TTLs are a subscription.
- Serialize with explicit versions in the value (`{"v":2,...}`) so a deploy can't mix shapes.

## Atomic patterns (single-threaded is a feature)

- Counters/rate limits: `INCR` + `EXPIRE NX` - atomic, no read-modify-write races.
- Locks: `SET key value NX EX ttl` with a unique value (fencing token on release via Lua/check-and-del). Naive `GET`-then-`SET` locks race.
- Queues: `LIST` (LPUSH/BRPOP) for simple FIFO; sorted sets for priority/scheduled jobs. Atp-least-once semantics - consumers must be idempotent, like any queue.

## Operational reality

- Monitor memory vs maxmemory and evicted-keys rate; evictions rising = your cache is lying to you about hit rates.
- Use scan (`SCAN`) never `KEYS *` in prod - KEYS blocks the single thread and freezes everything.
- Persistence choice is a real decision: RDB snapshots lose the last interval; AOF costs fsyncs. For queues, AOF everysec minimum.
