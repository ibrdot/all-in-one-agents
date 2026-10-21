# Philosophy

Four commitments. Everything in this pack follows from them.

## 1. TDD-first

A test that has never been seen failing proves nothing. Write the failing
test, watch it fail, then make it pass. Code without this loop is a rumor.

## 2. Systematic over ad-hoc

Debugging is a process (reproduce → isolate → hypothesize → test), not a
vibe. Planning is a document, not a memory. When a shortcut tempts you,
the checklist is the answer — not the obstacle.

## 3. Evidence over claims

"Done" is a claim about reality, and reality is checked with commands.
Every completion carries its proof: exit codes, test output, build logs.
An agent that says "should work" has said nothing.

## 4. Complexity reduction

The best change often removes rather than adds. Smaller diffs, fewer
moving parts, plain structures. Cleverness is a debt the next reader pays.

---

These are not aspirations. The hooks in `hooks/` enforce them; the gates
in `pack-kernel` block work that violates them.
