# Installation — per harness

Pick your harness. Every path ends with the kernel loaded and hooks armed.

## Claude Code

```bash
git clone https://github.com/ibrdot/all-in-one-agents.git
cd all-in-one-agents
./install.sh            # installs to ~/.claude
```

Then add the SessionStart hook to `~/.claude/settings.json` (the installer prints the exact snippet). Marketplace manifest: `.claude-plugin/plugin.json`.

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

## Verify your install

```bash
python3 scripts/validate.py
python3 -m pytest tests/ -q
```

Then start a session — the first thing you should see is the kernel loading
`using-all-in-one-agents`.
