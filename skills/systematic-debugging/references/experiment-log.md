# Debugging experiments and recovery

## Evidence ledger

Use one row per hypothesis, not one row per random edit:

| Observation | Hypothesis | Distinguishing experiment | Prediction | Actual result | Conclusion |
|---|---|---|---|---|---|
| First HTTP call succeeds, second fails | Connection reuse corrupts state | Repeat using fresh server, identical payload | Failure disappears | Failure persists | Reuse rejected; inspect payload-dependent path |

Capture revision, interpreter/runtime, dependency versions, working directory,
exact input and exit code. Redact credentials, not the error category. A snapshot
of a terminal is weaker than a rerunnable command plus recorded output.

## Boundary tracing

Mark the last good and first bad representation. For an API pipeline this can
be input -> serialized request -> transport -> parsed response -> domain value.
Inspect values at the boundary without logging secrets. A 200 status with an
invalid result is not success. A generic catch returning an empty answer hides
the failing boundary and turns diagnostics into misinformation.

## Controlled examples

### Folded skill metadata

Symptom: many skills cannot be indexed although frontmatter contains description.
Hypothesis: the parser reads only inline metadata. Distinguishing experiment:
index one inline and one folded description with the same embedding fixture.
Prediction: only folded input fails. Regression must also reject a body-level
`description:` pretending to be metadata. Fix the parser boundary, not 140 files.

### Cross-check grader contamination

Symptom: check one passes, check two fails only when run together. Hypothesis:
state persists between checks. Experiment: candidate writes a local runner file
on first call. Prediction: shared workdir changes later behavior. Use a fresh
working directory per check. This removes accidental contamination; it does NOT
provide filesystem or network isolation from malicious same-user code.

### Installer symlink overwrite

Symptom: installation changes a file outside destination. Hypothesis: a nested
symlink is followed by recursive copy. Experiment: link one target skill file to
a temporary sentinel, install, inspect sentinel bytes. Correct recovery rejects
the entire destination before any copy. A top-level-only check misses nested
links. Add a no-write assertion as well as nonzero exit status.

## Stop conditions

After three disproved hypotheses, reread original evidence, reduce the case and
ask for a second read-only investigator. If environment access is missing, report
that exact missing boundary. Do not claim a fix from compilation or a mock of
the broken interface. Preserve unrelated changes; never use destructive resets
as a universal debugging tool.

## Closing record

State root cause, observed-red regression, minimal fix, targeted green, full
regression, independent review, remaining risks and rollback. A changed error
message without the original acceptance passing is not a resolved bug.
