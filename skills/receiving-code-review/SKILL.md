---
name: receiving-code-review
description: Use when receiving code review feedback, before implementing suggestions, especially if feedback seems unclear or technically questionable - requires technical rigor and verification, not performative agreement or blind implementation
---

# Receiving Code Review

Feedback on a PR is data about the code, not a verdict about you. Treat every comment as a claim to verify, not an order to obey.

## The loop

1. **Read the whole review first.** React to nothing until you have seen every comment; early replies lock you into a defensive frame.
2. **Restate each nontrivial comment** in your own words. If you cannot, you do not understand it yet - ask before touching code.
3. **Verify each claim against the actual codebase.** Reviewers work from partial context; suggestions can be stale, wrong for this architecture, or based on an older revision.
4. **Sort into three buckets:** clearly right (do it), clearly wrong (push back with evidence), genuinely unclear (ask a specific question).
5. **Implement one item at a time**, running the tests after each, so a regression is attributable to one change.

## Replies that work

- Wrong-but-plausible feedback gets a technical rebuttal with a link to the line, test, or doc that proves it - not an apology.
- Right feedback gets a short "done" plus the commit; no essay.
- Unclear feedback gets one precise question, never "could you clarify?" with nothing attached.

Never reply with performative agreement ("great point!", "you're absolutely right!"). It reads as noise, inflates notification volume, and hides the one comment where you actually disagreed.

## When you disagree and it matters

Present the trade-off with costs on both sides and a recommendation. If the reviewer still decides against you, comply and move on - unless the change breaks correctness, security, or data integrity, in which case escalate rather than ship something you know is broken.

## Handling vague feedback

"Make this cleaner" is not actionable. Offer two concrete options with examples and ask which direction. Vague praise needs no action; vague criticism needs one.

## Related

- Giving review? See [pr](../pr/SKILL.md).
