---
name: prompt-engineering
description: "Design, measure, and iterate prompts and LLM calls for applications: system prompts, few-shot examples, structured output, and regression-proof prompt changes. Use when building or improving an AI feature, fixing unreliable model output, or tuning instructions, agents, or tools."
---

# Prompt Engineering

Treat prompts as code: versioned, tested, and changed one variable at a time.

## Method

1. **Write the failing cases down.** Collect 10-30 real inputs where output is wrong, inconsistent, or badly formatted. Without a failing set, every edit is vibes.
2. **Change one variable.** Instructions, examples, output format, model version - never two at once. Rerun the failing set after each change.
3. **Prefer examples over adjectives.** "Be concise" loses to two examples of the desired length and shape. One good example is worth ten adverbs.
4. **Constrain the output format.** For structured results, specify the exact schema and add a validation step in code. Retry on parse failure with the validation error appended.
5. **Put stable content first, user content last,** and delimit untrusted input explicitly. Prompts are injection surfaces; see [security-review](../security-review/SKILL.md).

## Checklists

**System prompt:** role and scope, hard rules up front, output contract, failure behavior ("if unsure, say so / ask"), and no contradictions (search the whole prompt for rules that conflict under load).

**Few-shot:** examples cover the hard cases, not the easy ones; include at least one counter-example or boundary case; keep them consistent with the output contract.

**Agents/tools:** each tool has a one-line purpose, explicit when-to-use and when-NOT-to-use, and an idempotent failure mode. Ambiguous tool descriptions cause more agent failures than model quality does.

## Evaluate like a scientist

- Grade outputs with a rubric (correct / partial / wrong), not a vague score.
- Automate the failing-set run; a prompt change that is not re-tested is not merged.
- Track regressions in the repo next to the prompt file, like fixtures. See [agent-evaluation](../agent-evaluation/SKILL.md) for the full harness.

## Anti-patterns

- Editing the live prompt after every single bad output
- A 4,000-word prompt where 200 words and 3 examples would do
- Asking the model to "be careful" instead of showing what careful looks like
