# Evals — Behavioral Scenarios

Drill-style behavior tests: each scenario is a scripted user prompt plus
assertions about what the agent MUST and MUST NOT do.

## Running

Point your harness at this repo with the pack installed, feed the scenario's
`prompt`, then check the transcript against the assertions. A minimal runner:

```bash
# pseudocode — adapt to your harness's headless mode
agent run --skills ./skills --prompt "$(yq .prompt evals/scenarios/brainstorming.yaml)"
# then assert on the transcript
```

## Scenarios

| File | Behavior under test |
|---|---|
| `scenarios/brainstorming.yaml` | no code before design approval on non-trivial asks |
| `scenarios/tdd.yaml` | failing test written before implementation |
| `scenarios/verification.yaml` | no "done" without real command output |
| `scenarios/multi-edit.yaml` | stale or over-broad multi-file plans refused, preview first |
| `scenarios/test-design.yaml` | regression test written before the bug fix |
| `scenarios/dispatch.yaml` | parallel subagents get non-overlapping file ownership |
| `scenarios/plan-execution.yaml` | plan steps verified in order, not batch-skipped |

Assertions use MUST / MUST NOT language — a scenario fails on the first
violated assertion.
