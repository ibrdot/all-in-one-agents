# Executable agent runtime foundation

This is standard-library Python code, not another prompt-only skill. It is a
foundation, not a finished autonomous platform or a superiority benchmark.

## Run now

```sh
python3 examples/runtime/demo.py
python3 -m pytest tests/test_runtime_core.py tests/test_runtime_council_eval.py -q
python3 scripts/workflow_gate.py evals/executable/core-gates.json
```

The demo is explicitly offline: fixture vectors and mock responses exercise the
wiring without pretending that real models ran.

## Implemented contracts

- `runtime.core.Memory`: explicit SQLite saves, deletion, persistent cosine
  retrieval. Embedding space ids and vector dimensions must match. Caller owns
  obtaining real embeddings. Storage is local plaintext, not an encrypted vault.
- `route_skills`: rank supplied embeddings, enforce caller-provided token costs,
  limit selection, abstain when nothing fits. This is vector routing, not an LLM
  planner or a learned context classifier. Use a separate skill-only index.
- `verify_evidence`: check local file digests and reject outside-root paths.
  Hashes establish byte identity, not factual accuracy or trustworthy authorship.
- `select_model`: choose the cheapest explicitly priced capability-compatible
  model under an estimated budget. Does not infer difficulty, quality, or prices.
- `runtime.council.council`: parallel proposals, peer critique, synthesis with
  retained stage outputs. A failed critique cannot be called a completed debate.
  Provider callable signature is `(model_id, messages) -> nonempty string`.
- `runtime.evaluation.evaluate`: exact/required/forbidden-text checks with baseline
  regression detection. These narrow checks do not judge general intelligence.
- `propose_improvement`: attribute failures to a skill and return a candidate
  carrying the original SHA256. Never silently overwrite a skill after a single
  failed run; review, repeat evaluation, and rollback remain required.

## Provider boundary

Pass a real provider callable only after reviewing its API adapter, credentials,
timeouts, logging, and billing. Council currently has no global hard deadline;
Python worker threads cannot terminate a blocked provider. Each adapter must use
bounded network timeouts. No live provider, automatic retry, or automatic spend
is bundled. Transcripts can contain confidential data: store and redact them
under your own retention policy. Prompt instructions are not a security boundary.

## Remaining roadmap

Real embedding/provider adapters and live model validation; a curated 50-task
benchmark (not 50 duplicated fixtures); measured model-quality routing; weekly
benchmark scheduling; human-reviewed improvement promotion; document-stack
end-to-end examples; native host sessions; official marketplace submission;
commercial service commitments. None is claimed complete by this foundation.
