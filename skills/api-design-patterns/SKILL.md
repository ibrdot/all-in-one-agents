---
name: api-design-patterns
description: "Use when designing or versioning a REST/RPC API - resource modeling, error contracts, pagination, idempotency, and versioning decisions that will not need a breaking change next quarter."
---

# API Design Patterns

An API is a promise. Every field you ship, someone depends on. Design for the deletion you will not be allowed to do.

## Resource modeling

- Nouns for resources, verbs only for operations that are not CRUD (e.g. `/orders/{id}/cancel`, not `/cancelOrder?id=`).
- Relationships as nesting one level max: `/projects/{id}/tasks`. Deeper nesting means you needed a resource.
- Return the resource, not a view of it; shape for consumers via fields or `?include=`, not separate endpoints per screen.

## Error contract

- Use HTTP status codes honestly: 4xx is the caller's bug, 5xx is yours, 422 for validation, 409 for conflicts.
- Error body is machine-readable: `{error: {code, message, details[]}}` with stable string codes. Callers branch on `code`, never on `message`.
- Never 200-with-error-payload. That pattern spreads like mold through every SDK.

## The boring-but-critical four

1. **Pagination everywhere**, even when data is small today. Cursor-based by default; offsets break under writes.
2. **Idempotency keys** on every POST that moves money or state. Retries are not optional in real networks.
3. **Rate limiting with headers** (`Retry-After`, remaining counts) so well-behaved clients can back off instead of dying.
4. **Consistent timestamps**: UTC, ISO 8601, suffixed with `_at`. One convention, everywhere, forever.

## Versioning

- Version in the URL (`/v2/`) for anything with third-party consumers; prefer additive changes and feature flags inside a version.
- Breaking change checklist: removed field? changed type? new required input? altered status semantics? If yes, new version - no exceptions for "small" ones.
- Deprecate with a clock: sunset header + docs + direct notice to known consumers, then remove.

## Review checklist

- [ ] Can every endpoint be retried safely?
- [ ] Are all error codes documented and stable?
- [ ] Does pagination exist on every list?
- [ ] Is there an example request/response pair in the docs for each endpoint?
