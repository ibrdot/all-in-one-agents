# Security Policy

## Reporting a vulnerability

Do NOT open a public issue for security problems.
Use GitHub's private vulnerability reporting (Security tab → Report a vulnerability).

You will get an acknowledgement within 72 hours.

## Scope

- The installer and hook scripts (`install.sh`, `hooks/`) — they execute on your machine
- Skills containing executable scripts (`skills/*/scripts/`)
- CI workflows

## What we do

- CodeQL scanning on every push
- Smoke tests syntax-check every shipped script
- No telemetry, no network calls in the bootstrap (see `docs/TELEMETRY.md`)
