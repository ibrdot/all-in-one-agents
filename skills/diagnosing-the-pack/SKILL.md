---
name: diagnosing-the-pack
description: Debug the agent framework itself — when skills fail to trigger, hooks misfire, sessions go off the rails, or the workflow loop was skipped. Use when behavior, not code, is the bug.
---

# Diagnosing the Pack

When the agent misbehaves, debug the process before the code.

## Symptom → cause map

| Symptom | Likely cause | Check |
|---|---|---|
| Skill never triggered | description doesn't match how the request was phrased | read the skill's trigger line, compare with the user prompt |
| Skills stopped mid-session | compaction dropped them | is the SessionStart hook installed and firing? |
| Code shipped untested | verification gate skipped | find the "done" claim — was there command output? |
| Agent redesigned mid-task | deviation protocol skipped | find where the plan stopped being followed |
| Same failure repeating | no learning capture | is `continuous-learning` recording outcomes? |

## Method

1. **Reproduce the behavior** — smallest prompt that triggers the misbehavior
2. **Trace the transcript** — find the exact message where the loop broke
3. **Name the missing gate** — which skill/hook should have caught this?
4. **Fix at the right layer:**
   - wording issue → tighten the skill's description
   - missing enforcement → wire the hook
   - genuine gap → write a new skill (`writing-skills`)

## Evidence rule

Quote the transcript line, the skill file, or the hook config that proves the diagnosis. "The agent probably..." is not a diagnosis.
