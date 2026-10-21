---
name: brainstorming
description: Structured understanding before building — clarify intent, explore approaches, agree on a design. Use for any non-trivial request, vague briefs, new features, or when the urge to start coding arrives before the problem is fully understood.
---

# Brainstorming

Code written against a vague brief is rework. Understand first.

## Why this phase exists

The most expensive sentence in software is "oh, you meant THAT." Every minute
here buys ten in implementation. Skipping understanding doesn't save time —
it converts a design conversation into a rewrite, with interest.

## The protocol

### 1. Restate

One paragraph: what we are building, for whom, and why it matters. If your
restatement surprises the asker, you just saved the project.

### 2. Question

Ask the 3–6 questions whose answers would actually change the design:

- What does success look like concretely? (Get an example, not an adjective)
- What must this NOT do? (Anti-requirements kill scope creep at birth)
- What exists today that constrains us? (Systems, habits, data, politics)
- Who or what consumes the result — and what breaks if we're wrong?
- What's the deadline's real shape: hard date, quality bar, or budget?

Ask them in one batch, numbered, easy to answer selectively.

### 3. Explore

Offer 2–3 approaches with honest trade-offs:

- **The minimal thing** — smallest change that delivers the value
- **The right thing** — what you'd build with no legacy constraints
- **The pragmatic thing** — your recommendation, and WHY

Exploring one option is advocacy; exploring three is engineering.

### 4. Converge

Get explicit approval on ONE design. "Sounds good" is approval;
"yeah whatever just build it" is a deferred argument — push once more.

## Output — the design note

Short, on disk, feeding directly into `writing-plans`:

- Goal + one-sentence definition of done
- Chosen approach and why
- Rejected alternatives and why (so nobody re-litigates them at hour 6)
- Constraints and open risks
- Out of scope (named, to protect the boundary)

## Refusal rule

On non-trivial work, if told to skip this and "just code it" — push back
once, briefly: name the top 2 design risks of skipping. If the human still
insists, record the decision in the design note and proceed. Never silently.

## Companion tools

- `builder-check-prompt.md` — five questions to answer before the first line of code
- `visual-companion.md` — when the design needs a sketch before words suffice

## Done when

Both sides can state the same one-sentence definition of done — and a design
note exists on disk to prove it.
