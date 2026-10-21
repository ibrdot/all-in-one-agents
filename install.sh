#!/usr/bin/env bash
# all-in-one-agents installer
# Usage:
#   ./install.sh              -> install into Claude Code (~/.claude)
#   ./install.sh opencode     -> install into OpenCode (~/.config/opencode)
#   ./install.sh /custom/dir  -> install into a custom root with skills/ agents/ commands/
set -euo pipefail

SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET="${1:-claude}"

case "$TARGET" in
  claude)   DEST="$HOME/.claude" ;;
  opencode) DEST="$HOME/.config/opencode" ;;
  *)        DEST="$TARGET" ;;
esac

echo "Installing all-in-one-agents into $DEST"
mkdir -p "$DEST/skills" "$DEST/agents" "$DEST/commands"

cp -r "$SRC/skills/"*  "$DEST/skills/"
cp -r "$SRC/agents/"*  "$DEST/agents/" 2>/dev/null || true
cp -r "$SRC/commands/"* "$DEST/commands/" 2>/dev/null || true

# Wire the SessionStart hook for Claude Code so pack-kernel survives compaction
if [ "$TARGET" = "claude" ]; then
  HOOK_SRC="$SRC/hooks/session-start.sh"
  HOOK_DEST="$HOME/.claude/hooks"
  mkdir -p "$HOOK_DEST"
  cp "$HOOK_SRC" "$HOOK_DEST/session-start.sh"
  chmod +x "$HOOK_DEST/session-start.sh"
  cat << 'EOF'

Claude Code hook installed. Add this to ~/.claude/settings.json if not present:

  "hooks": {
    "SessionStart": [{
      "hooks": [{ "type": "command", "command": "$HOME/.claude/hooks/session-start.sh" }]
    }]
  }

EOF
fi

echo "Done. Skills: $(ls "$DEST/skills" | wc -l), kernel: $DEST/skills/pack-kernel/SKILL.md"
