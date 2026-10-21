---
name: graphql-design
description: "Use when designing or hardening a GraphQL API - schema shape, resolver performance (N+1), security boundaries, and pagination that survive real clients."
---

# GraphQL Design

GraphQL's superpower (clients ask for anything) is also its attack surface. Design the schema for the queries you have not thought of yet.

## Schema shape

- Design types around the domain, not the database tables; expose `Node`-ish interfaces only when clients truly need polymorphic fetch.
- Nullability is an API contract: fields that can fail are non-null wrappers around nullable values, so errors propagate cleanly instead of nuking whole objects.
- One canonical pagination type (Relay-style connections) from day one - retrofitting pagination is a breaking change.

## Resolver performance

- The N+1 problem is default-on in GraphQL: one query per field per object. Use DataLoader-style batching for every relationship, always, before any client exists.
- Depth and complexity limits are not optional: cap query depth (e.g. 10) and total complexity, and reject introspection-heavy junk in production.
- Persisted queries for first-party clients: they turn "arbitrary query endpoint" into "known queries only," which kills most attack surface at once.

## Security

- Authentication is per-resolver, not per-endpoint: a missing check on one field leaks. Enforce with schema directives or middleware, not memory.
- Field-level authorization: object-level checks stop IDOR, field-level stops role leakage (e.g. `email` on a `User` only for admins).
- Never trust query whitelisting alone - autocomplete IS an attack surface in prod; disable introspection there.

## Operations

- Errors: partial success is normal. Put machine-readable `extensions.code` on every error; clients branch on codes.
- Deprecate fields with `@deprecated(reason:)` and actually watch query telemetry before removing anything.
- Trace per-field latency in dev; a slow resolver hides behind "the API is slow" forever otherwise.
