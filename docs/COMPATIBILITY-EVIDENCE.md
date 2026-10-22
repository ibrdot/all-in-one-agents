# Compatibility and evidence levels

## ⏱️ 30-second TL;DR

A manifest file is **not** proof that a host recognizes its schema. Two Gemini
manifests are one integration, not two harnesses. Custom destination copies are
not additional native integrations. **No universal compatibility claim is made.**

> **Honesty rule**: what is tested in this repository is local install/copy
> behavior and JSON format checks. What is **not** established is live host
> sessions, official marketplace listings, or commercial support — those require
> the platform's own review process and a real service operator.

---

## Evidence by surface

| Surface | Evidence in this repository | Not established |
|---|---|---|
| Claude installer | Real isolated installs, repeated installs, configuration preservation, installed SessionStart JSON execution | Live Claude CLI session |
| OpenCode, Grok, Qwen, Factory installer targets | Actual directory copies and repeated installs in isolated homes | Native discovery, commands, hooks, and upstream-approved paths |
| Custom destination | Actual copy with spaces in path | Recognition by any particular host |
| Other plugin/extension manifests | JSON and local referenced-path checks | Host schema approval or real runtime integration |
| Claude marketplace file | Local listing format/path/version checks | Official marketplace listing or endorsement |
| Codex marketplace | No live validation performed | Official distribution |

## Run the local evidence checks

```bash
python3 -m pytest tests/test_install_behavior.py tests/test_harness_coverage.py -q
python3 scripts/workflow_gate.py evals/executable/core-gates.json
```

These tests are not measurements of model reasoning quality and do not establish
superiority over another project.

## Remaining external work

Real harness sessions require installed host clients and appropriate accounts.
Official listings require the platform's publication/review process. Commercial
support requires an actual operator and service agreement; a policy file cannot
create either. Community growth requires real users and maintained responses.

Preserve upstream license and copyright obligations for redistributed material.
Changing names or phrasing does not by itself establish independent authorship.

---

## Next

- [Installation by harness](INSTALL.md) — per-harness setup and adapter manifests
- [Blueprint status](BLUEPRINT-STATUS.md) — delivered vs remaining layers
- [Measured inventory](MEASURED-INVENTORY.md) — test counts and inventory numbers
- [Runtime](RUNTIME.md) — executable contracts and connected execution
