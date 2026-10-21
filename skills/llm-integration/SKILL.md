---
name: llm-integration
description: "Use when wiring LLM calls into a product - prompt structure that survives model swaps, structured output you can parse, fallback chains, evaluation, and cost/latency control."
---

# LLM Integration

Shipping LLM features is easy; shipping them reliably is engineering. The failure modes are predictable - design for them up front.

## Prompt architecture

- System prompt = role, rules, and output contract; user content = data, clearly delimited (XML-ish tags or fenced blocks). Never interpolate untrusted user text into instructions - prompt injection is the SQL injection of this era; treat all user content as untrusted data.
- Few-shot examples beat adjectives: two good examples teach a model more than "be concise and accurate."
- Version prompts like code: named, in-repo, diffed in review. "The prompt changed somewhere" is not an engineering practice.

## Structured output or bust

- Ask for JSON with an explicit schema; validate on every response (Pydantic/Zod) and retry once on parse failure with the validation error appended. Unvalidated LLM output in your DB is a future incident report.
- Tools/function-calling beats JSON-in-text when available - the harness enforces the shape for you.

## Reliability patterns

- Fallback chain: primary model -> cheaper model -> canned response. Define what the user sees when ALL fail before writing the first call.
- Timeouts + max_tokens on every call; a wedged generation should cost cents, not minutes of hung requests.
- Idempotency and caching: exact-match cache for deterministic prompts; semantic cache where staleness is acceptable.

## Evaluate before and after

- Golden set of 20-50 real cases, judged on every prompt/model change - even a simple pass/fail rubric catches regressions vibes never will.
- Log input, output, latency, tokens, and cost per call ([cost-optimization](../cost-optimization/SKILL.md)). What you cannot see, you cannot improve - and you are paying per token either way.

## Model-agnostic by design

Wrap the provider SDK behind one interface in your codebase. Model swaps are a when, not an if; keep the switch a config change, not a rewrite.
