> Compatibility status: consult [tested behavior and unverified integrations](COMPATIBILITY-EVIDENCE.md) before treating an adapter as native host support.

# Installation by harness

Pick your harness. The installer wires the SessionStart kernel hook for Claude Code.
Other targets require harness-specific configuration; included manifests are not
a claim that every target has been runtime-tested.

## ⏱️ 30-second TL;DR

```bash
git clone https://github.com/ibrorg/all-in-one-agents.git
cd all-in-one-agents
./install.sh claude --dry-run   # preview
./install.sh claude             # install to ~/.claude
python3 scripts/validate.py && python3 -m pytest tests/ -q
```

For non-Claude harnesses, see the [harness table](#pick-your-harness) below — the
installer supports OpenCode and a custom path directly; other harnesses use their
adapter manifest in the repo root.

> **Prerequisites**: Git and Bash; Python 3 for the installer and checks,
> Python 3.10+ for the multi-edit helper. **Back up existing same-name skills
> before installing.** The installer is not an isolated package manager — it
> copies files into the selected destination.

---

## Pick your harness

| Harness | Install command / manifest | Notes |
|---|---|---|
| [Claude Code](#claude-code) | `./install.sh claude` | SessionStart hook auto-merged into `~/.claude/settings.json` |
| [OpenCode](#opencode) | `./install.sh opencode` | Plain copy to `~/.config/opencode` |
| [Cursor](#cursor) | Copy `skills/`, `agents/`, `commands/` | Or use `.cursor-plugin/plugin.json` where supported |
| [Gemini CLI](#gemini-cli) | Adapter candidates in repo | Verify discovery in a real session |
| [Codex / Copilot CLI / Devin / Hermes / Muse / Kimi / Pi / Antigravity](#other-harnesses) | Per-harness manifest in repo root | See table below |
| [Custom location](#custom-location) | `./install.sh /path/to/anywhere` | Creates `skills/`, `agents/`, `commands/` inside |

---

## Claude Code

```bash
git clone https://github.com/ibrorg/all-in-one-agents.git
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

This repository includes `gemini-extension.json`, `.gemini/extension.json` and
`GEMINI.md` as adapter candidates. Follow your installed Gemini CLI version's
extension-loading procedure and verify discovery in a real session; local JSON
validation does not establish native loading.

## Other harnesses

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

---

## Verify your install

```bash
python3 scripts/validate.py
python3 -m pytest tests/ -q
```

For Claude Code, inspect the SessionStart output and confirm bootstrap context
is present. For other harnesses, verify their own loading mechanism independently.
See [coding workflows](CODING-WORKFLOWS.md) for safe multi-file changes.

## Protect existing local edits

Installer preflight rejects symlinked destination trees before any copy. Identical
reinstallation remains idempotent. If installed files differ from the incoming
pack, installation stops and lists conflicts; back up local changes and use
`--force` only when replacement is intended. `--dry-run` lists conflicts without
writing. Run installation without concurrent untrusted writers; preflight is
not a cross-process lock.

---

## Next

- [Getting started](GETTING-STARTED.md) — the 30-second first-time path
- [Troubleshooting](TROUBLESHOOTING.md) — common install and runtime failures
- [Coding workflows](CODING-WORKFLOWS.md) — safe multi-file changes
- [Compatibility evidence](COMPATIBILITY-EVIDENCE.md) — tested vs unverified integrations
