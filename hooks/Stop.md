# Stop Hook

Fires before the agent is allowed to end its turn.

## Action

Run both checks. If either fails, do not stop — fix first.

1. **`agent-self-evaluation`** — did I follow the phase loop? Any gate skipped?
2. **`delivery-gate`** — is there unverified work being presented as done?

## Blocking conditions

Stop is BLOCKED when:
- Tests were changed to make them pass instead of fixing code
- A task is claimed complete without command-output evidence
- Scaffolding/temp files are left behind
