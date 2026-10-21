---
name: speed-run-refactor
description: "Use when a large refactor must land in hours or days, not weeks - scoping to the 20% with 80% of the payoff, parallel-safe execution via worktrees, and a hard landing checklist."
---

# Speed-Run Refactor

Sometimes the debt is blocking shipping and there is no month for the beautiful plan. This skill is how you do a big refactor fast *without* creating a broken-window crisis for the next person.

## Scope: the ruthless cut

- Define the exit condition as a sentence: "all API handlers return typed errors" - not "make the code good."
- List candidate changes; score each by (pain relieved x frequency touched) / risk. Take the top 3. Everything else is explicitly deferred with a ticket, or scope creep will eat the deadline.
- If a change needs a data migration to be complete, it does not belong in a speed run. Split it out.

## Execute: parallel and safe

- One branch per independent change, each in its own worktree ([using-git-worktrees](../using-git-worktrees/SKILL.md)); land each as soon as green instead of a big-bang merge.
- Mechanical changes (rename, extract, move) are scripted or tool-assisted, never hand-edited - hand-edits are where the "small" refactor becomes a week.
- Behavior-locking characterization tests go in first and are never modified during the run. They are the contract.

## Land: the checklist

- [ ] All tests green, including the ones you did not write.
- [ ] Feature-flag or deprecation path for any consumer of the old interface; nothing removed by surprise.
- [ ] Follow-up tickets exist for the deferred 80%, with one line on why each was deferred.
- [ ] A 10-minute written handoff: what changed, what got faster/better, where the bodies are buried.
- [ ] If anything is half-migrated at deadline, revert it fully rather than leaving both worlds live ([delivery-gate](../delivery-gate/SKILL.md)).

## The trap

Speed runs are addictive. If the team starts planning the *next* speed run before shipping this one, that is the signal the debt needs a real plan, not another sprint of heroics ([improve-codebase-architecture](../improve-codebase-architecture/SKILL.md)).
