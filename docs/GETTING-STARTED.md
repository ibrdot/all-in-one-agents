# Getting started

[Home](../README.md) | [Installation details](INSTALL.md) | [Coding workflows](CODING-WORKFLOWS.md)

## ⏱️ 30-second TL;DR

```bash
git clone https://github.com/ibrorg/all-in-one-agents.git
cd all-in-one-agents
./install.sh claude --dry-run   # preview
./install.sh claude             # install
python3 scripts/validate.py && python3 -m pytest tests/ -q
```

Then give the agent a bounded task with acceptance checks. The intended loop is
**understand → plan → execute → verify → deliver**. Ask questions only when a
material unknown cannot be resolved from the project.

> Requires Git, Bash, and Python 3.10+. Review scripts before running them. The
> installer copies files into the selected destination; it is **not** an isolated
> package manager. Back up same-name skills first.

---

## Step-by-step

Each step expands on demand. The summary line stays visible; click to reveal the
commands and the reasoning.

<details>
<summary><b>1. Clone and preview</b></summary>

```bash
git clone https://github.com/ibrorg/all-in-one-agents.git
cd all-in-one-agents
./install.sh claude --dry-run
```

Read the installer and back up existing same-name skills. The installer copies
files into the selected destination; it is not an isolated package manager.

</details>

<details>
<summary><b>2. Install and validate</b></summary>

```bash
./install.sh claude
python3 -m pip install pytest
python3 scripts/validate.py
python3 scripts/smoke_test.py
python3 -m pytest tests/ -q
```

Use `./install.sh opencode` for a plain OpenCode copy. Other harnesses have
[separate setup instructions](INSTALL.md); do not assume Claude hooks work there.

</details>

<details>
<summary><b>3. Give the agent a bounded task</b></summary>

> Add a `--verbose` flag to the build script. First locate the entrypoint and
> tests, preserve existing changes, then implement and show the verification
> commands.

The intended loop is understand → plan → execute → verify → deliver.
Ask questions only when a material unknown cannot be resolved from the project.
For multiple files, load the [multi-edit workflow](CODING-WORKFLOWS.md).

</details>

<details>
<summary><b>4. Check what actually happened</b></summary>

Inspect the diff and actual test output. Loaded instructions do not prove
compliance; Markdown gates do not mechanically block a tool call. The Claude
SessionStart hook emits bootstrap context, but continuity still depends on the
harness and a current task record.

</details>

<details>
<summary><b>5. Resume carefully</b></summary>

Before interrupting, record the revision, changed files, verified steps, and next
command. On resume, use [checkpoint-recovery](../skills/checkpoint-recovery/SKILL.md)
to compare that record with the current worktree. Do not assume automatic recovery
or replay an edit plan whose hashes no longer match.

</details>

---

## ✅ What to check after install

A concrete gate, not a vibe. Each box is something you can verify with a command
or a file inspection — if any box cannot be ticked, treat the install as
incomplete.

- [ ] `./install.sh claude --dry-run` output reviewed before the real install
- [ ] `python3 scripts/validate.py` exits 0 (skill/agent/command frontmatter valid)
- [ ] `python3 scripts/smoke_test.py` exits 0 (catalog and routing consistent)
- [ ] `python3 -m pytest tests/ -q` shows the expected pass count with 0 failures
- [ ] `git diff --check` is clean (no whitespace damage, no conflict markers)
- [ ] The installed destination actually contains `skills/`, `agents/`, `commands/`
- [ ] For Claude installs: the `SessionStart` hook entry is present, not just the skills
- [ ] For non-Claude harnesses: you have read [INSTALL.md](INSTALL.md) — hooks are per-harness, not guaranteed
- [ ] The first bounded task has acceptance checks, not just a description

If a hook did not install for your harness, that is expected for non-Claude hosts —
loaded Markdown does not mechanically enforce tool boundaries. Inspect the diff and
test output after every run.

---

## Next

- [Installation and compatibility](INSTALL.md) — harness-specific paths and hook support
- [Coding workflows](CODING-WORKFLOWS.md) — multi-edit, refactoring, migration scenarios
- [Troubleshooting](TROUBLESHOOTING.md) — common setup failures and fixes
- [Philosophy](PHILOSOPHY.md) — the four commitments every skill follows from
