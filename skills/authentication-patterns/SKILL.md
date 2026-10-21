---
name: authentication-patterns
description: "Use when adding or fixing login, sessions, tokens, or authorization - battle-tested patterns for password auth, session vs JWT, OAuth/OIDC, MFA, and the ten mistakes that cause breaches."
---

# Authentication Patterns

Auth is the highest-consequence, least-invented code you will write. Use the established pattern; invent nothing here.

## Choose the session model first

| Model | Use when | Watch for |
|---|---|---|
| Server sessions (cookie) | Traditional web apps | Cookie `Secure`, `HttpOnly`, `SameSite=Lax`; session store that survives restarts |
| Short-lived JWT + refresh | SPAs calling APIs, microservices | Token revocation - you need a denylist or very short TTLs |
| OIDC via provider | Almost always, if allowed | Never hand-roll the crypto; use a certified library |

The mistake is not picking wrong; it is mixing them (JWT in a cookie with server sessions also active) and then not knowing where logout happens.

## Password handling

- Argon2id, bcrypt (cost 12+), or scrypt - never SHA-anything, ever.
- Length is the real policy: allow 64+ chars, block only the top-10k breached passwords, never block symbols.
- Constant-time comparison everywhere a secret is checked.
- Login, reset, and signup return the SAME response and timing for "user exists" vs "wrong password" - enumeration is a bug class, not a trick.

## The ten breach-causing mistakes

1. JWTs accepted without `alg` pinned (the `none` algorithm bug, still alive).
2. Refresh tokens stored in localStorage (any XSS = account takeover).
3. Password reset tokens that never expire or are not single-use.
4. No rate limiting on login/OTP endpoints.
5. Authorization checked in the UI but not re-checked server-side on every request (IDOR - test it: every object access checks ownership/role server-side).
6. Secrets in JWT payloads (it is base64, not encryption).
7. Sessions not rotated on login and privilege change.
8. OAuth redirect_uri not allowlisted exactly.
9. "Remember me" that survives password change.
10. MFA that is SMS-only, or worse, TOTP that can be reset via email + no support identity check.

## Rule of thumb

Every auth change ships with a test that proves the *failure* path (expired token, wrong tenant, reused reset code) is rejected - not just that the happy path works.
