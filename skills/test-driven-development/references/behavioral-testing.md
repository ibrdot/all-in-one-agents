# Behavioral tests beyond green counts

## Acceptance matrix

Before the implementation, enumerate the input domain and externally observable
outcome. Tests protect contracts, not line count or similarity to another repo.

| Boundary | Success case | Negative case | Required observable |
|---|---|---|---|
| HTTP adapter | Local server receives real request | Redirect, malformed JSON, truncation | No credential forwarding; incomplete answer fails |
| Skill retrieval | Relevant vector and correct space | Different space, bad dimensions | Abstention or explicit rejection, never mixed spaces |
| Installer | Repeated install preserves settings | Nested symlink and invalid JSON | No write outside target; invalid preflight writes nothing |
| Document pipeline | Generate and read native file | Formula-like label, invalid numeric data | Text preserved as text; invalid input leaves no report |
| Improvement | Stable better score | Flaky score, regression, stale file | No automatic overwrite; review and content guards |

## RED quality

A missing import is useful initial red evidence for a new API, but it is not a
behavioral demonstration of every promised feature. Add boundary tests that fail
for the actual wrong behavior before fixing it. Record command and failure, not
just a checked box in a plan.

## Test doubles and real boundaries

A mock embedding proves plumbing, not semantic relevance. A local HTTP server
proves serialization and transport handling, not a real provider's compatibility.
A reference solution proves a grader can accept a correct candidate, not that a
model solved the task. Native-file readback proves content and structure, not
visual layout in Office. Name tests and reports to preserve these distinctions.

Use mocks above the boundary under test, not in place of it. Include at least one
negative test that would catch a constant-return or always-success implementation.
Check side effects: unchanged external files, no partial outputs, no provider
call before validation, and no persistence without explicit save.

## Refactoring and fixtures

Keep fixture helpers boring and small. A fixture containing the production
algorithm can reproduce the same bug on both sides of an assertion. Expected
values should be independently specified. Parameterization is fine for a real
input partition; duplicating a test into 40 files to win a metric is not.

Do not weaken exact numeric/type assertions to absorb an unexplained failure.
Booleans compare equal to integers in Python; JSON contracts often require them
to remain distinct. Duplicate JSON keys and nonfinite numbers need explicit
handling rather than parser defaults.

## Test-suite health

Run focused tests while iterating, full suite before delivery. Report skips and
why they occurred. Optional document dependencies can skip locally but the
mandatory document CI job must install them and execute round trips. A test
that fails on the wrong exception can be as misleading as one that never fails.

Before shipping, ask: if the implementation returned a constant, ignored auth,
followed symlinks, dropped errors, or skipped a whole stage, which exact test
would fail? If the answer is none, that behavior lacks protection.
