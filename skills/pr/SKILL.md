---
name: pr
description: "Open, polish, or review a pull request: title, body, diff hygiene, and merge readiness checks."
---

# Pull Request

A PR body is a briefing for two readers: the reviewer now, and the archaeologist in six months. Write for both.

## Body structure

### 1. What and why (three sentences max)

- What changed, in the user's own domain vocabulary.
- Why now: the bug, the requirement, or the follow-up this unblocks.
- One-line scope statement: what this PR deliberately does NOT touch.

### 2. The shape of the change

Pick the smallest view that carries the point. One visual, not five:

| Change type | Show it as |
|---|---|
| Algorithm or caching logic | Short pseudocode |
| Runtime control flow | Call tree |
| New module or file layout | Shallow file tree with one-line responsibilities |
| Component or data flow | Mermaid sequence/flow diagram |
| Local change inside existing shape | Targeted diff (only the lines that moved) |
| Everything new | One complete code block, copyable |

A diff whose surrounding context the reviewer does not already know is not a diff; it is a puzzle. When in doubt, show the whole block.

### 3. Evidence

The change works, shown not claimed:

- **Visual change:** before/after screenshots.
- **Behavior change:** the test that failed and now passes, or the exact command output before and after.
- **No user-visible change:** what you verified instead (typecheck, unit tests, dry run).

"Should work" is not evidence. Run the thing; see [verification-before-completion](../verification-before-completion/SKILL.md).

### 4. Risk

Two questions, answered plainly:

- **Reversibility:** if this turns out wrong tomorrow, is reverting a five-minute chore or a data migration? Flag anything that is hard to undo: destructive operations, schema changes, contract breaks.
- **Blast radius:** who else depends on this? Downstream consumers, other surfaces, load-bearing callers. Name them.

## Diff hygiene

Before opening:

- Commits are atomic and tell a story; rebase away "fix typo 2".
- No unrelated formatting churn. It buries real changes and angers reviewers.
- No commented-out code, no debug prints, no TODOs without tickets.

## Reviewing someone else's PR

- Read the "what and why" first and restate the intent to yourself before looking at any diff line.
- Comment on the code, not the coder; propose, do not command.
- Distinguish blocking (correctness, security) from nits (style) explicitly, and block only for blocking.
- For receiving review feedback instead of giving it, see [receiving-code-review](../receiving-code-review/SKILL.md).
