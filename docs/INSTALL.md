# Installation by harness

Pick your harness. The installer wires the SessionStart kernel hook for Claude Code.
Other targets require harness-specific configuration; included manifests are not
a claim that every target has been runtime-tested.

Prerequisites: Git and Bash; Python 3 for the installer and checks, Python 3.10+
for the multi-edit helper. Back up existing same-name skills before installing.

## Claude Code

```bash
git clone https://github.com/ibrdot/all-in-one-agents.git
cd all-in-one-agents
./install.sh            # installs to ~/.claude
```

The installer merges the SessionStart hook into `~/.claude/settings.json` automatically (idempotent; unrelated keys preserved). Preview it with `./install.sh claude --dry-run`. Marketplace manifest: `.claude-plugin/plugin.json`.

## OpenCode

```bash
./install.sh opencode   # installs to ~/.config/opencode
```

See `.opencode/INSTALL.md`.

## Cursor

Copy `skills/`, `agents/`, `commands/` into your Cursor rules/skills location, or use the marketplace manifest `.cursor-plugin/plugin.json` where supported.

## Gemini CLI

This repo ships `gemini-extension.json` + `.gemini/extension.json` at the root — Gemini CLI picks it up as an extension with `GEMINI.md` as context.

## Codex / Copilot CLI / Devin / Hermes / Muse / Kimi Code / Pi / Antigravity

Each harness has its manifest in the repo root:

| Harness | Manifest |
|---|---|
| Codex | `.codex-plugin/plugin.json` |
| GitHub Copilot CLI | `.github-plugin/plugin.json` |
| Devin | `.devin-plugin/plugin.json` |
| Hermes | `.hermes-plugin/plugin.json` |
| Muse | `.muse-plugin/plugin.json` |
| Kimi Code | `.kimi-plugin/plugin.json` |
| Pi | `.pi/plugin.json` |
| Antigravity | `.antigravity-plugin/manifest.json` |

## Custom location

```bash
./install.sh /path/to/anywhere   # creates skills/ agents/ commands/ inside
```

## Option C — system prompt only (no install)

For harnesses without hooks (Codex app, some Gemini configs, sandboxed/cloud
agents, CI), paste **[MASTER-PROMPT.md](../MASTER-PROMPT.md)** into the system
prompt slot. It carries the same methodology — loop, gates, routing table,
anti-patterns, oath — as one portable document. It does not replace hooks;
it is the portable fallback.

## Verify your install

```bash
python3 scripts/validate.py
python3 -m pytest tests/ -q
```

For Claude Code, inspect the SessionStart output and confirm bootstrap context
is present. For other harnesses, verify their own loading mechanism independently.
See [coding workflows](CODING-WORKFLOWS.md) for safe multi-file changes.
