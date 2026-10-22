# Objective task evaluation and native documents

## ⏱️ 30-second TL;DR

- **50 microtasks** in `evals/tasks/tasks.json`: 35 coding (boundary cases included) + 15 infrastructure (Kubernetes, IAM, Redis, Postgres, CI perms). A starting suite, not a comprehensive quality claim.
- **Generate → grade → calibrate** is a three-step split: generation sends only public task prompts (never check payloads), grading runs in your isolated sandbox, calibration verifies the graders themselves.
- **Native documents**: `runtime.documents` generates DOCX/XLSX/PDF/PPTX and CI reopens all four formats to verify content. Proves generation/readback, not desktop rendering.
- **Honesty**: private-to-prompt checks are not secret from same-user candidate code. File hashes bind bytes only. A public task suite is not a secure hidden benchmark.

> **Safety**: never run unknown candidate code on a personal workstation. Use an
> isolated sandbox with no secrets, no network, restricted filesystem, separate
> UID. Built-in subprocess limits are time/memory/file + env scrubbing — **not
> security isolation**.

---

## What now exists

`evals/tasks/tasks.json` contains 50 distinct microtasks: 35 coding tasks with
multiple input/output checks and 15 infrastructure tasks with exact JSON
contracts. Inputs include boundary cases (empty lists, cycles, absent values,
quoted CSV, repeated query keys, prime squares). Infrastructure tasks cover
Kubernetes deployment/service/resources/security/probes/PDB, IAM, container
health checks, Redis, PostgreSQL pools, CI permissions, alerts and recovery.
These are a starting task suite, not a claim of comprehensive real-world quality.

Private-to-the-prompt checks are NOT secret from same-user candidate code.
`generate` sends only public task prompts to providers, never check payloads.
All tasks, references and graders are public repository files. Use an isolated
sandbox with no secrets, no network, a restricted filesystem and a separate UID
before grading untrusted Python. The built-in subprocess has time/memory/file
limits and environment scrubbing, **not security isolation**. Every report
records this boundary. Do not run unknown candidates on a personal workstation.
Each check gets fresh local source files to avoid accidental state contamination.

## Generate answers explicitly

<details>
<summary><b>Generate responses from a provider</b></summary>

```sh
python3 -m runtime.taskgenerate --base-url "$PROVIDER_BASE_URL" \
  --model "$MODEL_ID" --max-calls 50 --max-output-tokens 2048 \
  --allow-network --output responses.json
```

Credentials come from `OPENAI_API_KEY` or a named `--key-env` variable. Never put
keys in prompts or source control. Provider/model selection and spend approval
are operator decisions: call count and output caps are not dollar guarantees.
The existing HTTPS adapter supplies timeout, response validation and redirect
protection. Generation never executes returned source code. A partial run saves
successful responses and error classes, then exits 1; no failure becomes a
fabricated model answer. Output is created exclusively with 0600 mode.

</details>

## Grade separately

<details>
<summary><b>Grade saved responses (replay, no network)</b></summary>

Inside your disposable isolated grading environment:

```sh
python3 -m runtime.taskbench --responses responses.json \
  --output .aio/model-run --allow-code-execution
```

The default report source is `replay`, because grading saved responses is replay
regardless of what the input file claims. Generation's supplied model/source are
recorded as unauthenticated metadata. `--source reference-calibration` is an
explicit operator label, not a signed attestation. File hashes bind bytes only;
reports are not tamper-proof or third-party certified. Baseline comparison checks
suite fingerprints, identical task IDs and source category; never compare author
references to model responses as if they were the same population.

</details>

## Calibrate the graders, not model intelligence

<details>
<summary><b>Verify the graders themselves</b></summary>

`reference-responses.json` contains author-written solutions/configurations.
Correct references establish that checks are executable and internally
consistent, not that an LLM solved the tasks. CI labels these results calibration:

```sh
python3 -m runtime.taskbench --responses evals/tasks/reference-responses.json \
  --source reference-calibration --output .aio/calibration --allow-code-execution
```

The existing `runtime.benchmark` remains a separate 50-contract software suite.
Do not add these counts and call them 100 live model tasks. Held-out evaluations
for skill promotion still require caller-selected evaluators and review.

</details>

## Native document execution

```sh
pip install -r requirements-documents.txt
python3 -m runtime.documents --input report-data.json --output .aio/report
```

Input schema: `{"title":"Sales review","rows":[{"name":"North","value":120}]}`.
The pipeline creates report.docx, report.xlsx, report.pdf and report.pptx. Limits:
1..100 rows, bounded labels/title, finite numeric values; no user formulas in
labels. The workbook includes a total formula (not recalculated by openpyxl).
PDF text is escaped and long tables can paginate; slides split at six rows.
Tests reopen all four native formats and verify content, spreadsheet formula
storage and formula-like names kept as text. This proves generation/readback,
not rendering in desktop Office/LibreOffice or perfect layout with every font.
The mandatory CI job installs pinned optional dependencies and runs round trips.

## Remaining quality gates

- Actual paid/local-provider runs and quality/cost comparisons need an available,
  explicitly chosen provider and funded configuration. None are invented here.
- Broader real-world repository tasks, document visual graders and host-native
  CLI sessions remain additional evaluation work.
- A public task suite is not a secure hidden benchmark or proof of "strongest".

---

## Next

- [Blueprint status](BLUEPRINT-STATUS.md) — delivered vs remaining layers
- [Runtime](RUNTIME.md) — executable contracts and connected execution
- [Measured inventory](MEASURED-INVENTORY.md) — test counts and inventory numbers
- [Coding workflows](CODING-WORKFLOWS.md) — multi-edit, refactoring, migration patterns
