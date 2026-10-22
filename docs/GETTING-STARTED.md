# Getting started

[Home](../README.md) | [Installation details](INSTALL.md) | [Coding workflows](CODING-WORKFLOWS.md)

## 1. Clone and preview

```bash
git clone https://github.com/ibrorg/all-in-one-agents.git
cd all-in-one-agents
./install.sh claude --dry-run
```

Read the installer and back up existing same-name skills. The installer copies
files into the selected destination; it is not an isolated package manager.

## 2. Install and validate

```bash
./install.sh claude
python3 -m pip install pytest
python3 scripts/validate.py
python3 scripts/smoke_test.py
python3 -m pytest tests/ -q
```

Use `./install.sh opencode` for a plain OpenCode copy. Other harnesses have
[separate setup instructions](INSTALL.md); do not assume Claude hooks work there.

## 3. Give the agent a bounded task

> Add a --verbose flag to the build script. First locate the entrypoint and tests,
> preserve existing changes, then implement and show the verification commands.

The intended loop is understand -> plan -> execute -> verify -> deliver.
Ask questions only when a material unknown cannot be resolved from the project.
For multiple files, load the [multi-edit workflow](CODING-WORKFLOWS.md).

## 4. Check what actually happened

Inspect the diff and actual test output. Loaded instructions do not prove
compliance; Markdown gates do not mechanically block a tool call. The Claude
SessionStart hook emits bootstrap context, but continuity still depends on the
harness and a current task record.

## 5. Resume carefully

Before interrupting, record the revision, changed files, verified steps, and next
command. On resume, use [checkpoint-recovery](../skills/checkpoint-recovery/SKILL.md)
to compare that record with the current worktree. Do not assume automatic recovery
or replay an edit plan whose hashes no longer match.
