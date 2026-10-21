# Worked case: pagination must not skip tied timestamps

## Define observable behavior
Two rows share a timestamp. Fetch page one, insert another row, then fetch page
two. Existing rows must appear exactly once. The cursor contract must specify a
stable unique tie-breaker, such as (created_at, id), plus sort direction.

## RED
Write the test against the public list function and a real temporary database.
Run that exact test and confirm an assertion fails because rows repeat or
vanish. Import errors, unavailable databases, and invalid fixtures are setup
failures, not the RED phase. Record the command and diagnostic.

## GREEN
Make the smallest query change: compare the ordered timestamp/id tuple to the
cursor tuple and order by the same columns. Keep page size bounded. Do not
rewrite the test to fit the broken implementation.

## REFACTOR and negative controls
Run the targeted test and neighbors before extracting helpers. Test no rows,
one row, exactly a page, ties spanning pages, invalid cursors, and both sort
directions if supported. Temporarily restore the old predicate: the regression
must fail again. This mutation check proves the test distinguishes the repair.

A green test written after the patch proves current behavior; it does not prove
that a test-first workflow occurred. Report that distinction honestly.
