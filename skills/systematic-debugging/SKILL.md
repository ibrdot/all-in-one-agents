---
name: systematic-debugging
description: A disciplined process for bugs whose cause is unknown — reproduce, isolate, hypothesize, test, fix once. Use for any non-obvious bug, flaky failure, regression, or when catch yourself guessing at fixes or changing code "to see if it helps".
---

# Systematic Debugging

Guessing is the slowest debugging method ever invented. Process beats intuition on every bug that survives five minutes of staring.

## The law

**One hypothesis, one experiment, one conclusion.** If you changed two things and the bug moved, you learned nothing.

## The process

### 1. Reproduce — reliably

- Find the smallest input/steps that trigger the bug
- "It happens sometimes" is not reproduction. Keep shrinking until it fails *on demand*
- Can't reproduce? The task is now "make it reproducible" — add logging, tighten the loop, capture state

### 2. Isolate — bisect the space

- Binary search the system: comment out half, mock half, check the middle layer
- For regressions: `git bisect` beats reading a week of diffs
- Draw the boundary: input good here, output bad there → the bug lives between

### 3. Hypothesize — explicitly

- Write the hypothesis down: "I believe X because Y"
- Rank hypotheses by *evidence*, not by which fix you'd enjoy writing
- The hypothesis you like least but matches the data is usually right

### 4. Test the hypothesis — not the fix

- Design an experiment whose outcome distinguishes your hypothesis from alternatives
- Predict the result BEFORE running: "if X is the cause, I'll see Z"
- Wrong prediction → hypothesis dead, write down what you learned, go to 3

### 5. Fix once

- Fix the root cause, not the symptom at the call site
- Then load `test-driven-development`: capture the bug as a failing test before fixing, so it can never return silently

## What this skill forbids

- Shotgun changes: editing 4 files then rerunning
- "Fixes" that add `try/except` around a mystery
- Reboot-and-pray as a strategy
- Declaring victory because the error message changed

## Stuck? Escalate correctly

After 3 dead hypotheses, step back: re-read the actual error (not your summary of it), check the environment (versions, env vars, caches), and explain the bug out loud — to a teammate, to a rubber duck, in a comment. Articulation finds what staring misses.

## Done when

- Root cause identified and stated in one sentence
- Fix verified with command output
- A regression test exists proving the bug is dead

## Applied case

See [worked case and failure analysis](references/worked-case.md) for concrete experiments, acceptance checks, and recovery rules.
