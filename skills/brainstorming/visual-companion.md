# Visual Companion — Sketching Before Building

Some designs only become clear when drawn. Use this when the feature involves
UI, data flow, state machines, or architecture with moving parts.

## When to sketch

- UI work → draw the states (empty, loading, error, populated)
- Data flow → boxes and arrows: who produces, who transforms, who consumes
- Concurrency → timelines: what can overlap, what must serialize
- APIs → the request/response shapes, before any endpoint exists

## Rules

1. **Ugly is fine** — the sketch is thinking aid, not deliverable
2. **Label the arrows** — an unlabeled arrow hides an undecided question
3. **Mark the unknowns** — put a `?` on every edge you can't explain; those
   `?`s become your brainstorming questions
4. **Throw it away after** — the sketch's job ends when the plan begins;
   the plan is the durable artifact

## Feeding the plan

Convert each drawn box into a task; each labeled arrow into an integration
point to verify; each `?` into a question that must be answered before the
corresponding task starts.
