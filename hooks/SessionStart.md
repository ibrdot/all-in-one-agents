# SessionStart Hook

Fires at conversation start and after every compaction.

## Action

Load the `using-all-in-one-agents` skill immediately — before responding to anything else.

Then announce (one line):

> all-in-one-agents kernel loaded. Current phase: UNDERSTAND. Say "status" for the checklist.

## After compaction

1. Re-load `using-all-in-one-agents`.
2. Find the active plan file (the plan on disk is the memory).
3. Resume from the first unchecked task — never restart, never improvise from memory.
