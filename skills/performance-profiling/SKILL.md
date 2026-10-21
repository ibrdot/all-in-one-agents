---
name: performance-profiling
description: Use when something is slow, memory use is high, a budget is exceeded, or before merging a change that could regress performance. Requires the ability to run the code.
---

# Optimize from measurements, not guesses

## Workflow

1. Reproduce the problem and record the baseline: environment, dataset, hardware, version, and the exact command. An environment nobody can reproduce is not a baseline.
2. Define a measurable target ("p95 under 300 ms on the sample dataset") instead of "make it faster". Record the measurement method.
3. Profile before changing anything: CPU, allocation, I/O, or network, whichever matches the symptom. Never hand out generic advice such as "add caching" without a profile.
4. Attribute cost to specific functions, queries, or endpoints. Identify the dominant cost before optimizing; rule out the harness measuring the wrong thing.
5. Change one hotspot at a time. For each change, re-run the identical benchmark and keep only changes with a measured, reproducible win. A regression or a wash gets reverted immediately.
6. Check correctness: run the full relevant test suite. Optimizations that change observable behavior are behavior changes and need their own review.
7. Add a regression guard where practical: a benchmark, a budget assertion in CI, or a documented command. Record before/after numbers with variance.

## Report

Deliver baseline, target, profile evidence, each change with its measured effect, final numbers, reverted attempts, and the guard added. State variance and environment limits honestly. Do not extrapolate beyond the measured dataset.
