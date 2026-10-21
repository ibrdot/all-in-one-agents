# Builder Check — Pre-Implementation Prompt

Use this prompt on yourself (or a subagent) right before writing the first line
of implementation. Every answer must come from the approved design, not vibes.

---

Before you code, answer out loud:

1. **What is the one-sentence definition of done?** Quote it from the design
   note. If you can't, stop — go back to brainstorming.
2. **Which files will this task touch?** List them. If the list has "and
   maybe…" in it, the task is too big — split it.
3. **What command proves this task works?** Write it down now, before coding.
   If no command can prove it, the task lacks a success criterion.
4. **What is the rollback?** One line: how to undo this task cleanly.
5. **What does this task NOT do?** Name the nearest temptation to scope-creep
   and explicitly rule it out.

Only when all five have concrete answers: begin.

---

## Why this exists

Most rework isn't caused by bad coding — it's caused by starting to code one
minute before understanding crystallized. This check costs sixty seconds and
returns hours.
