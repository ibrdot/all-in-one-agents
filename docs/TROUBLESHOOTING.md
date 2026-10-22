# Troubleshooting

[Home](../README.md) | [Install](INSTALL.md) | [Runtime](RUNTIME.md)

## ⏱️ 30-second TL;DR

Most failures fall into one of six buckets below. Match your symptom to the
section, expand it for the fix. If none fit, [report a bug](#report-a-bug) with
revision, OS, Python version, the exact redacted command, and exit status.

> **Before you file**: re-run with `./install.sh claude --dry-run` to preview
> conflicts, and `python3 scripts/check_docs.py` to confirm the docs themselves
> are not the cause. Both are offline checks; neither requires network access.

---

## Common failures

Each section expands on demand — the symptom stays visible, the fix is one
click away.

<details>
<summary><b>Installer refuses an existing destination</b></summary>

Read the reported path. A symlinked directory/file is refused to prevent writes
outside the intended tree; use a normal directory after reviewing its contents.
Modified installed files require a backup and comparison before `--force`.
`./install.sh claude --dry-run` previews copies; it does not bypass unsafe paths.
Do not install concurrently with another writer.

</details>

<details>
<summary><b>Missing Python or optional document dependencies</b></summary>

Use Python 3.10+ and a virtual environment. Install pytest for the main suite;
install `requirements-documents.txt` for all four document round trips. A skipped
optional test is not successful document verification. Bash is required by the
installer; native Windows shells need an appropriate Bash environment.

</details>

<details>
<summary><b>No API credential or HTTP failure</b></summary>

Set the credential in the environment variable selected by `--key-env` using your
local secret manager. Never post it in an issue. Check the explicit HTTPS base
URL, model IDs, supplied pricing and provider account access. The adapter refuses
redirects and incomplete answers, and does not retry paid requests silently.
A call cap is not a billing guarantee; chat estimates exclude embedding spend.

</details>

<details>
<summary><b>No skill result or stale retrieval</b></summary>

Use the same embedding model/space for indexing and querying. Index into a new
database path; deleted or changed skills need a rebuild, including after reviewed
skill promotion. Check descriptions and token limits before assuming the router
is broken. Fixture embeddings prove wiring, not semantic ranking quality.

</details>

<details>
<summary><b>Task grading asks for code-execution consent</b></summary>

Generation and evaluation are separate. JSON grading executes no candidate code;
Python grading requires explicit consent and a disposable restricted execution
environment without secrets or network. Built-in resource limits are not a
security sandbox. Never run unknown model code on a personal checkout.

</details>

<details>
<summary><b>Badges, SVGs and documentation links</b></summary>

The validation badge points to `.github/workflows/validate.yml`; an unavailable
remote badge does not override local test results. `python3 scripts/check_docs.py`
checks maintained Markdown local paths, heading anchors and local SVG XML/viewBox.
External badges depend on their providers and GitHub workflow availability.
This repository currently has no maintained local SVG assets to repair; do not
invent missing icons. Include the exact broken URL in a reproducible issue.

</details>

---

## Report a bug

Provide revision/version, OS and Python version, exact redacted command, exit
status, expected/actual behavior and a minimal input. State whether the failure
is local, native-host or remote-provider behavior. Follow [security policy](../SECURITY.md)
for sensitive reports rather than posting credentials or private data publicly.

---

## Next

- [Installation by harness](INSTALL.md) — per-harness setup and adapter manifests
- [Runtime](RUNTIME.md) — semantic routing, council, evaluation pipeline
- [Getting started](GETTING-STARTED.md) — first-time path and post-install checklist
- [Security policy](../SECURITY.md) — report sensitive issues privately
