# Getting Started — 5 minutes to your first autonomous run

## 1. Install (1 min)

```bash
git clone https://github.com/ibrdot/all-in-one-agents.git
cd all-in-one-agents
./install.sh            # or ./install.sh opencode
```

## 2. Verify (30 sec)

```bash
python3 scripts/validate.py && python3 -m pytest tests/ -q
```

Both green = install healthy.

## 3. Start a session (30 sec)

Open your harness in any project. The SessionStart hook loads
`using-all-in-one-agents` — you'll see the kernel announce itself.

## 4. Give it real work (3 min)

Pick something small but real, e.g.:

> "Add a --verbose flag to the build script with tests."

Watch the loop happen:

1. **UNDERSTAND** — it asks 2–3 questions instead of coding immediately
2. **PLAN** — you get an atomic task list with verify commands
3. **EXECUTE** — tasks land one by one, each with test evidence
4. **VERIFY** — the diff is reviewed before merge
5. **DELIVER** — suite runs green, you're offered merge/PR options

## 5. Interrupt it (optional)

Close the session mid-run, reopen, say "continue". The SessionStart hook
reloads the kernel, finds the plan file, and resumes at the first
unchecked task. That is the compaction-recovery guarantee.

## Next

- Browse `INDEX.md` for domain skills
- Read `docs/PHILOSOPHY.md` for the why
- Run a behavioral scenario from `evals/scenarios/` to see the gates hold
