#!/usr/bin/env bash
# Install all-in-one-agents into a harness.
# Usage:
#   ./scripts/install.sh claude              -> ~/.claude
#   ./scripts/install.sh opencode            -> ~/.config/opencode
#   ./scripts/install.sh /custom/dest        -> custom root (skills/ agents/ commands/ inside)
set -euo pipefail

SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
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

# Wire the SessionStart hook for Claude Code so the kernel survives compaction
if [ "$TARGET" = "claude" ]; then
  HOOK_DEST="$HOME/.claude/hooks"
  mkdir -p "$HOOK_DEST"
  cp "$SRC/hooks/session-start.sh" "$HOOK_DEST/session-start.sh"
  chmod +x "$HOOK_DEST/session-start.sh"
  cat << 'EOF'

Claude Code hook installed. Add to ~/.claude/settings.json if not present:

  "hooks": {
    "SessionStart": [{
      "hooks": [{ "type": "command", "command": "$HOME/.claude/hooks/session-start.sh" }]
    }]
  }

EOF
fi

echo "Done. Kernel: $DEST/skills/using-all-in-one-agents/SKILL.md"
