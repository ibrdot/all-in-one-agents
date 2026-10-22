# Blueprint implementation status

Status is based on executable checks, not line counts or imported marketing claims.

## ⏱️ 30-second TL;DR

The runtime ships real contracts — embedding adapter, persisted skill index,
cosine rank, token budget, council debate, memory, improvement pipeline, 50
golden contracts, 50 objective microtasks, native document round-trips. What
remains is **real model quality evaluation, real-world golden tasks, official
distribution approval, and enterprise service** — none of which can be claimed
from wiring alone.

> **Honesty rule**: byte identity is not proof the answer is correct; manifest
> hashes are not externally signed; a public task suite is not a secure hidden
> benchmark; calibration results are not live model scores.

---

## Status by layer

| Requested layer | Delivered in repository | Remaining / evidence boundary |
|---|---|---|
| Disciplined coding core | Bootstrap, TDD/debugging/subagent skills, workflow gates, regression tests | Not a byte-for-byte Superpowers fork; core now has dispatch/two-pass review, experiment ledgers and boundary-testing references. No equivalence to its complete per-harness suite claimed |
| Breadth | 140 skills, reasoning/document/frontend/infra guides, 73 agents, 97 commands | DOCX/XLSX/PDF/PPTX now have generation + native-file readback tests. Visual desktop rendering and native host sessions remain |
| Skill router | Real embedding adapter + persisted skill index + cosine rank + token budget + task CLI | Embedding-model quality and ranking must be evaluated with real tasks; no learned context classifier |
| Evidence | Run artifacts, SHA256 manifest, verified file boundaries | Byte identity is not proof the answer is correct; manifest is not externally signed |
| Council debate | Parallel proposals, peer critique, judge synthesis, stage failures block completion; integrated cost reservations | Real model quality and adversarial debate evaluation remain |
| Memory/RAG | SQLite persistent semantic retrieval included in task context, explicit saves/deletes | No automatic personal data capture, encryption, retention service or learned consolidation |
| Cost routing | Cheapest explicitly priced capability-compatible model, per-call conservative reservations | Not difficulty prediction; no live prices or actual usage reconciliation; embedding spend excluded |
| Self improvement | Caller-supplied generator/evaluator, repeated stable before/after results, optional held-out gate, explicit promotion and stale-safe rollback receipt | Not autonomous production rewriting; evaluator independence, skill validity and real quality remain caller responsibilities; rebuild index after promotion |
| Golden evaluation | 50 distinct executable contract cases, fingerprinted baseline, weekly CI and downloadable artifacts | Also 50 objective coding/infra microtasks with generation/replay CLI and grader calibration. No live-model score or weekly intelligence claim |
| Distribution | Existing install scripts and local installation tests | No official marketplace approval, 12 live host validations, commercial tier or enterprise service established |

## What the previous push actually was

Commit 412c786 provided useful primitives, not this entire blueprint. The follow-up
connects those primitives to an executable runtime and adds transport/integration
proof. Neither commit establishes "world's strongest" or production readiness.

## Next acceptance milestones

1. Run the new 50-task coding/infra suite with explicitly selected models and
   approved spend, then expand from microtasks to real repository/document tasks.
2. Run and publish real-provider retrieval and council experiments. Compare a
   single-model baseline and quality/cost; do not infer improvement from wiring.
3. Extend core coding playbooks with verified examples, failure recovery, reviewer
   loops and real native-harness sessions; preserve required upstream attribution.
4. Add visual document checks and promised native host runs; native-file
   generation/readback fixtures now execute for all four document formats.
5. Submit platform listings via platform review and define a real service operator
   before making commercial or enterprise commitments.

## Follow-up gap closure

See [objective evaluation and documents](OBJECTIVE-EVALUATION.md) for executable
commands and limits. Installer preflight now refuses symlink destinations and
modified installed files unless explicit `--force` is supplied. Test-file counts
are measured in [MEASURED-INVENTORY.md](MEASURED-INVENTORY.md), not used as a quality score.

---

## Next

- [Runtime](RUNTIME.md) — executable contracts and connected execution
- [Objective evaluation](OBJECTIVE-EVALUATION.md) — 50 microtasks and native documents
- [Measured inventory](MEASURED-INVENTORY.md) — test counts and inventory numbers
- [Compatibility evidence](COMPATIBILITY-EVIDENCE.md) — tested vs unverified integrations
