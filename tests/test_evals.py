"""Behavioral eval scenarios are well-formed and enforce the core gates."""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCENARIOS = os.path.join(ROOT, "evals", "scenarios")

def scenario_files():
    return sorted(f for f in os.listdir(SCENARIOS) if f.endswith(".yaml"))

def test_scenarios_exist():
    assert len(scenario_files()) >= 3, f"only {len(scenario_files())} scenarios"

def test_scenario_shape():
    for f in scenario_files():
        text = open(os.path.join(SCENARIOS, f), encoding="utf-8").read()
        assert re.search(r"^name:\s*\S", text, re.M), f"{f}: no name"
        assert re.search(r"^prompt:\s*", text, re.M), f"{f}: no prompt"
        assert re.search(r"^assertions:\s*", text, re.M), f"{f}: no assertions"
        assert "must:" in text, f"{f}: no MUST assertion"

def test_core_gates_covered():
    corpus = "\n".join(open(os.path.join(SCENARIOS, f), encoding="utf-8").read() for f in scenario_files())
    for gate in ("brainstorm", "test", "verif"):
        assert gate in corpus.lower(), f"no scenario covers {gate}"
