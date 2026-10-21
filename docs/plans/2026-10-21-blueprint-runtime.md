# Blueprint implementation - executable integration

## Acceptance boundary
The existing runtime is disconnected primitives, not the requested complete system.
This increment connects real embedding/chat adapters, skill indexing, memory RAG,
cost reservations, evidence-bound runs, reviewed skill improvement and scheduled
regression evaluation. No marketplace approval, paid service, live LLM quality,
or host compatibility is inferred from local tests.

## Tasks
1. Add failing behavioral tests for HTTP adapter boundaries, semantic indexing,
   persisted memory retrieval, budget reservation, evidence and promotion gates.
2. Implement bounded OpenAI-compatible adapters using environment-only secrets.
3. Connect indexing -> routing -> memory -> model selection -> council/answer ->
   evidence in a callable workflow and CLI. No import-time network calls.
4. Add evaluation-led candidate generation, held-out checks, hash-guarded explicit
   promotion and rollback receipts; candidates remain untrusted until approved.
5. Add 50 distinct, human-readable contract golden tasks, baseline-aware runner,
   weekly CI and report artifacts. These measure runtime contracts, not intelligence.
6. Run full checks and independent diff review, fix defects, commit and push.

## Verification
Local HTTP server exercises actual HTTP and failure paths without billing.
Fake model/embedding callables are labeled fixtures. Full pytest, validate,
smoke_test, sync_catalog --check, diff --check, golden runner and CLI help.

## Results

- Implemented adapters, integration CLI, full 140-skill index compatibility,
  budget reservations, RAG, critique council wiring, reviewed repeated-evaluation
  improvement with held-out option and stale-safe rollback, 50-contract benchmark
  and weekly CI.
- Independent read-only review produced concrete defects; fixed metadata parsing,
  output-cap mismatches, truncation, redirects/proxies, JUnit scoring, private
  output modes and partial index publishing. Added regression checks.
- Observed red integration collection failure before implementation; observed
  failing benchmark and parsing/held-out/flakiness tests before relevant fixes.
- Final local suite: 228 passed. All 140 skills validate; smoke scripts pass;
  generated catalog current; diff whitespace clean; 50/50 contract benchmark,
  no regressions vs fingerprinted baseline.
- Explicit deviation: 50 software contracts are NOT 50 real-world LLM tasks.
  No live paid model benchmark, official marketplace approval or commercial
  service was performed. Native host sessions and deeper coding playbooks remain.
- Rollback: revert this increment's commit (preserves prior primitive APIs).
