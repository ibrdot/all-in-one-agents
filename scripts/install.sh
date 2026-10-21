#!/usr/bin/env bash
# Install all-in-one-agents into a harness.
#
# Usage:
#   ./scripts/install.sh claude              -> ~/.claude
#   ./scripts/install.sh opencode            -> ~/.config/opencode
#   ./scripts/install.sh /custom/dest        -> custom root (skills/ agents/ commands/ inside)
#   ./scripts/install.sh claude --dry-run    -> print the settings that would be written
#
# For Claude Code the installer also merges the SessionStart hook into
# ~/.claude/settings.json. The merge is idempotent and preserves every
# unrelated key already in that file.
set -euo pipefail

SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

TARGET=""
DRY_RUN=0
for arg in "$@"; do
  case "$arg" in
    --dry-run) DRY_RUN=1 ;;
    -h|--help) sed -n '2,12p' "${BASH_SOURCE[0]}"; exit 0 ;;
    --*) echo "Unknown option: $arg" >&2; exit 2 ;;
    *) [ -z "$TARGET" ] || { echo "Only one target is allowed" >&2; exit 2; }; TARGET="$arg" ;;
  esac
done
TARGET="${TARGET:-claude}"

case "$TARGET" in
  claude)   DEST="$HOME/.claude" ;;
  opencode) DEST="$HOME/.config/opencode" ;;
  grok)     DEST="$HOME/.grok" ;;
  qwen)     DEST="$HOME/.qwen" ;;
  factory)  DEST="$HOME/.factory" ;;
  *)        DEST="$TARGET" ;;
esac

# Validate configuration before copying any files. Never partially install on
# malformed settings, and reject symlinked settings to avoid writing elsewhere.
if [ "$TARGET" = "claude" ]; then
  python3 - "$DEST/settings.json" <<'CHECK'
import json, os, sys
p = sys.argv[1]
try:
    if os.path.islink(p):
        raise ValueError("refusing symlinked settings")
    data = json.load(open(p, encoding="utf-8")) if os.path.exists(p) else {}
    if not isinstance(data, dict):
        raise ValueError("settings must be an object")
    hooks = data.get("hooks", {})
    if not isinstance(hooks, dict):
        raise ValueError("hooks must be an object")
    entries = hooks.get("SessionStart", [])
    if not isinstance(entries, list):
        raise ValueError("SessionStart must be a list")
    for entry in entries:
        if not isinstance(entry, dict) or not isinstance(entry.get("hooks", []), list):
            raise ValueError("invalid SessionStart entry")
except (ValueError, OSError) as exc:
    sys.exit(f"refusing invalid settings {p}: {exc}")
CHECK
fi

if [ "$DRY_RUN" -eq 1 ]; then
  echo "dry-run: would install into $DEST" >&2
else
  echo "Installing all-in-one-agents into $DEST"
  for component in skills agents commands; do
    mkdir -p "$DEST/$component"
    cp -R "$SRC/$component/." "$DEST/$component/"
  done
fi

# --- Claude Code: install the SessionStart hook and merge its config ---
if [ "$TARGET" = "claude" ]; then
  HOOK_DIR="$DEST/hooks"
  HOOK_DEST="$HOOK_DIR/session-start.sh"

  if [ "$DRY_RUN" -eq 0 ]; then
    mkdir -p "$HOOK_DIR"
    cp "$SRC/hooks/session-start.sh" "$HOOK_DEST"
    chmod +x "$HOOK_DEST"
  fi

  python3 - "$DEST/settings.json" "$HOOK_DEST" "$DRY_RUN" <<'PY'
import json
import os
import sys
import tempfile
import shlex

settings_path, hook_path, dry_run = sys.argv[1], sys.argv[2], sys.argv[3] == "1"

data = {}
if os.path.exists(settings_path):
    try:
        with open(settings_path, encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as exc:
        sys.exit(f"refusing to overwrite invalid JSON in {settings_path}: {exc}")
    if not isinstance(data, dict):
        sys.exit(f"refusing to overwrite non-object JSON in {settings_path}")

hooks = data.setdefault("hooks", {})
session_start = hooks.setdefault("SessionStart", [])

command = 'bash ' + shlex.quote(hook_path)
already = any(
    isinstance(entry, dict)
    and any(h.get("command") == command for h in entry.get("hooks", []) if isinstance(h, dict))
    for entry in session_start
)

if not already:
    session_start.append({
        "matcher": "startup|clear|compact",
        "hooks": [{"type": "command", "command": command, "timeout": 15}],
    })

rendered = json.dumps(data, indent=2) + "\n"
if dry_run:
    print(rendered)
else:
    os.makedirs(os.path.dirname(settings_path) or ".", exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=".aio-settings-", dir=os.path.dirname(settings_path))
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(rendered)
            f.flush()
            os.fsync(f.fileno())
        os.replace(temporary, settings_path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)
    print(f"SessionStart hook {'updated' if not already else 'already present'} in {settings_path}")
PY
fi

if [ "$DRY_RUN" -eq 0 ]; then
  echo ""
  echo "Done. Entrypoint: $DEST/skills/using-all-in-one-agents/SKILL.md"
  [ "$TARGET" != "claude" ] || echo "Verify with:  bash \"$DEST/hooks/session-start.sh\" | head -c 200"
fi
