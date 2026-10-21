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

Assertions use MUST / MUST NOT language — a scenario fails on the first
violated assertion.
