---
name: brainstorming
description: Structured understanding before building — clarify intent, explore approaches, agree on a design. Use for any non-trivial request, vague briefs, new features, or when the urge to start coding arrives before the problem is fully understood.
---

# Brainstorming

Code written against a vague brief is rework. Understand first.

## The protocol

1. **Restate** — one paragraph: what we are building and why
2. **Question** — ask the 3–6 questions whose answers would change the design:
   - What does success look like concretely?
   - What must this NOT do?
   - What exists today that constrains us?
   - Who/what consumes the result?
3. **Explore** — offer 2–3 approaches with honest trade-offs, recommend one
4. **Converge** — get explicit approval on ONE design before any code

## Output

A short design note: goal, chosen approach, rejected alternatives (and why), constraints, open risks. This feeds directly into `writing-plans`.

## Refusal rule

On non-trivial work, if asked to skip this and "just code it" — push back once, briefly: list the top 2 design risks of skipping. If the human still insists, note the decision and proceed — but never silently.

## Done when

Both sides can state the same one-sentence definition of done.
