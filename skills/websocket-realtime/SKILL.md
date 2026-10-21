---
name: websocket-realtime
description: "Use when building realtime features over WebSockets or SSE - connection lifecycle, scaling with pub/sub backends, backpressure, and the reconnect logic clients actually need."
---

# WebSocket Realtime

Realtime systems fail at the seams: reconnects, partial messages, and the second server you added last month. Design those seams first.

## Transport choice

- WebSockets for bidirectional, low-latency; **SSE for server-to-client streams** - it is HTTP, autoreconnects for free, and half the use cases (feeds, progress, notifications) never needed upstream anyway.
- Polling is an honest fallback for low-frequency updates; do not pay WebSocket complexity for a 30s refresh.

## Connection lifecycle

- Auth at connect (token in query/subprotocol or first message) AND re-verify on privileged actions - a socket is a long-lived session, and sessions get revoked.
- Heartbeat/ping-pong both directions (e.g. 30s) to detect half-open connections behind NATs and load balancers.
- Client reconnect with exponential backoff + jitter, resubscribe to topics on reconnect, and a sequence/cursor so missed messages can be caught up instead of silently lost.

## Scaling past one server

- A socket lives on one box; broadcast needs a pub/sub backend (Redis pub/sub, NATS) relaying between nodes. Direct in-memory broadcast only works until your second instance - design for it from day one.
- Sticky sessions at the LB if handshakes need state; better, make handshake stateless.
- Room/channel semantics server-side; never let clients broadcast to arbitrary topics - authz per subscribe.

## Backpressure and hygiene

- Bound server-side send queues per connection; slow consumers get dropped or downsampled, or they OOM the relay.
- Rate-limit inbound messages; a client flooding frames is an attack, not a user.
- JSON schema-validate inbound messages like any API input - "it's our own client" ages badly.
