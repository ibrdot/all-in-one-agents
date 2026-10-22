# Measured inventory — v1.5.0

## ⏱️ 30-second TL;DR

Measured on 2026-10-21 from tracked/release-intended files, excluding `.git`,
ignored artifacts and bytecode. **Counts describe surface area, not quality.**
No current competitor comparison is asserted without a pinned audit.

> **Honesty rule**: 272 local tests passing, 50/50 offline runtime contracts,
> and 50/50 author-reference task calibrations are **software regressions and
> grader calibration**, not model performance. Native document
> generation/readback covers DOCX/XLSX/PDF/PPTX; desktop visual rendering and
> native host sessions remain unverified.

---

## Inventory by dimension

| Dimension | all-in-one-agents |
|---|---:|
| Skills | 141 |
| Agents | 73 |
| Slash commands | 97 |
| Test files | 29 |
| Eval files | 13 |
| Runtime Python files | 12 |
| Runtime lines | 1038 |
| Repository files | 1133 |

## Verification

- 272 local tests passed
- 50/50 offline runtime contracts
- 50/50 author-reference task calibrations

Calibration is not model performance. Native document generation/readback covers
DOCX/XLSX/PDF/PPTX; desktop visual rendering and native host sessions remain
unverified.

Source size is measured from release archives rather than a working directory
containing caches or `.git` history; asset sizes/checksums are in the release.

---

## Next

- [Blueprint status](BLUEPRINT-STATUS.md) — delivered vs remaining layers
- [Runtime](RUNTIME.md) — executable contracts and connected execution
- [Objective evaluation](OBJECTIVE-EVALUATION.md) — 50 microtasks and native documents
- [Compatibility evidence](COMPATIBILITY-EVIDENCE.md) — tested vs unverified integrations
