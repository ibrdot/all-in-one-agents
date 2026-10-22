# Executable agent runtime foundation

This is standard-library Python code, not another prompt-only skill. It is a
foundation, not a finished autonomous platform or a superiority benchmark.

## ⏱️ 30-second TL;DR

- **Run now** (offline): `python3 examples/runtime/demo.py` then the runtime tests + workflow gate. Fixture vectors and mock responses exercise wiring without pretending real models ran.
- **Implemented contracts**: Memory, route_skills, verify_evidence, select_model, council, evaluate, propose_improvement — each with explicit limits (see [Implemented contracts](#implemented-contracts)).
- **Connected execution** (new): `python3 -m runtime --help` exposes a real network adapter. Credentials come from a named env var, never a CLI token. HTTPS, bounded timeouts, no redirects, disabled env proxies.
- **Provider boundary**: pass a real provider callable only after reviewing its adapter, credentials, timeouts, logging, billing. No live provider, automatic retry, or automatic spend is bundled.

> **Security**: storage is local plaintext, not an encrypted vault. Transcripts
> can contain confidential data — store and redact under your own retention
> policy. Prompt instructions are not a security boundary.

---

## Run now

```sh
python3 examples/runtime/demo.py
python3 -m pytest tests/test_runtime_core.py tests/test_runtime_council_eval.py -q
python3 scripts/workflow_gate.py evals/executable/core-gates.json
```

The demo is explicitly offline: fixture vectors and mock responses exercise the
wiring without pretending that real models ran.

## Implemented contracts

| Contract | What it does | Explicit limits |
|---|---|---|
| `runtime.core.Memory` | SQLite saves, deletion, persistent cosine retrieval | Embedding space ids + vector dims must match. Caller owns obtaining real embeddings. Local plaintext storage, not an encrypted vault. |
| `route_skills` | Rank supplied embeddings, enforce token costs, limit selection, abstain when nothing fits | Vector routing, not an LLM planner or learned context classifier. Use a separate skill-only index. |
| `verify_evidence` | Check local file digests, reject outside-root paths | Hashes establish byte identity, not factual accuracy or trustworthy authorship. |
| `select_model` | Choose cheapest explicitly priced capability-compatible model under estimated budget | Does not infer difficulty, quality, or prices. |
| `runtime.council.council` | Parallel proposals, peer critique, synthesis with retained stage outputs | A failed critique cannot be called a completed debate. Provider signature: `(model_id, messages) -> nonempty string`. |
| `runtime.evaluation.evaluate` | Exact/required/forbidden-text checks with baseline regression detection | Narrow checks, not general intelligence judgment. |
| `propose_improvement` | Attribute failures to a skill, return a candidate carrying original SHA256 | Never silently overwrite after a single failed run; review, repeat, rollback remain required. |

## Provider boundary

Pass a real provider callable only after reviewing its API adapter, credentials,
timeouts, logging, and billing. Council currently has no global hard deadline;
Python worker threads cannot terminate a blocked provider. Each adapter must use
bounded network timeouts. No live provider, automatic retry, or automatic spend
is bundled. Transcripts can contain confidential data: store and redact them
under your own retention policy. Prompt instructions are not a security boundary.

## Remaining roadmap

See [the explicit blueprint status](BLUEPRINT-STATUS.md). The connected runtime
below supersedes the earlier missing-adapter/scheduler notes; live model quality,
real-world golden tasks, official distribution and service commitments remain.

## Connected execution (new)

`python3 -m runtime --help` exposes a real network adapter and connected pipeline.
No network call happens on import. Credentials are read from the named environment
variable, never from a command-line token. HTTPS, bounded timeout/response size,
no redirects, and disabled environment proxies protect the transport boundary.
Truncated/refused completions fail rather than silently becoming complete answers.

The endpoint and embedding model must be chosen explicitly. Configure your key in
your local environment or secret manager; do not paste it into a chat or commit.
`PROVIDER_BASE_URL` must be your reviewed HTTPS endpoint including its API prefix.

<details>
<summary><b>Index the skills</b></summary>

```sh
python3 -m runtime --base-url "$PROVIDER_BASE_URL" --embedding-model "$EMBEDDING_MODEL" \
  --allow-network index --skills skills --database skills-v1.db
```

</details>

<details>
<summary><b>Run a task</b></summary>

```sh
python3 -m runtime --base-url "$PROVIDER_BASE_URL" --embedding-model "$EMBEDDING_MODEL" \
  --allow-network run --database skills-v1.db --models models.json \
  --task 'Review validation boundaries' --budget 0.10 --output .aio/run-001
```

</details>

`models.json` is a list with `id`, `capabilities` (e.g. `text`),
`input_per_million` and `output_per_million`. Supply current explicit provider
prices; no fictional model IDs or prices ship as defaults. Indexing makes one
embedding request per skill. Task execution adds another embedding request.
**Embedding spend is not included in the chat estimate budget.** Review this
separately before enabling network access. Indexing publishes a new database only
on full success; partial indexes are discarded.

`--memory existing.db` retrieves explicitly stored memory. The callable API exposes
`Memory.put/delete`; task execution never automatically stores private task text.
`--debate-models model-a model-b --judge judge-model` enables critique council.
All named models must have supplied capabilities/prices. Failed/blocked calls
retain their conservative reservations because billing status is uncertain.

Input byte counts are conservative loading estimates, not tokenizer usage. The
provider output cap and run estimate must match. Estimates are not a hard billing
limit or measured quality/difficulty routing. Provider callables must enforce
their own network timeout and output limits. The adapter currently discards usage;
actual billing reconciliation remains work to do.

Each new output directory contains `answer.txt`, `report.json`, and `manifest.json`.
The returned report additionally includes the evidence verification result; the
manifest verifies captured bytes, not truth, provenance or model reasoning quality.
No externally trusted signature protects the manifest. Treat transcripts as private.

## Reviewed improvement and repeatable contracts

`runtime.improvement.improve` asks a caller-selected generator for a changed skill,
repeats before/after evaluation (minimum two), rejects unstable scores, requires
strict improvement and no reported regression, and optionally runs a held-out
non-regression evaluator. `promote(..., approved=True)` checks content hashes and
requires explicit review. `rollback` refuses to overwrite subsequent edits. Stop
concurrent writers: these hash guards are not cross-process locking. Receipts and
proposals contain original skill text; store them privately. Scores do not prove
independent review or safe content. Review frontmatter and rebuild the semantic
index after every promoted change.

```sh
python3 -m runtime.benchmark --baseline evals/golden/baseline.json --output .aio/benchmark.json
```

The 50 golden contracts execute actual assertion-bearing tests, not 50 invented
responses. The weekly workflow runs offline, needs no model secrets, and uploads
its report. It is a software-regression benchmark, **not** a general agent-quality
benchmark. See [blueprint status](BLUEPRINT-STATUS.md) for exact remaining work.

## Explicit local memory management

`python3 -m runtime.memory --help` provides put/search/delete without network or
provider credentials. Input records contain `id`, `text`, `embedding`,
`embedding_model`, and optional object `metadata`. Embeddings must be computed
by your chosen embedding model; do not make up vectors for real semantic use.

<details>
<summary><b>Put / search / delete memory records</b></summary>

```sh
python3 -m runtime.memory put --database private-memory.db --input reviewed-entry.json
python3 -m runtime.memory search --database private-memory.db \
  --embedding query-embedding.json --embedding-model your-embedding-space
python3 -m runtime.memory delete --database private-memory.db --id reviewed-lesson
```

</details>

Search opens an existing database read-only and never creates a missing one.
New databases have private file permissions; SQLite is not encrypted. Symlinked
paths are refused. Do not run concurrent untrusted writers. Search outputs include
stored text, so keep terminals/logs private. Deletion removes a logical row, not
forensic remnants from disk/backups. Connect it using runtime `--memory`.

---

## Next

- [Blueprint status](BLUEPRINT-STATUS.md) — what is delivered vs remaining
- [Objective evaluation](OBJECTIVE-EVALUATION.md) — 50 microtasks and native document pipeline
- [Measured inventory](MEASURED-INVENTORY.md) — test counts and inventory numbers
- [Coding workflows](CODING-WORKFLOWS.md) — multi-edit, refactoring, migration patterns
