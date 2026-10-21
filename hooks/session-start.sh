#!/usr/bin/env bash
# SessionStart hook: re-injects the pack kernel after session start or compaction,
# so the orchestration loop never silently stops applying.
set -euo pipefail

PACK_DIR="${PACK_DIR:-$HOME/.claude/skills}"
KERNEL="$PACK_DIR/pack-kernel/SKILL.md"

if [ -f "$KERNEL" ]; then
  echo "all-in-one-agents pack-kernel active: $KERNEL"
  echo "Resume rule: read the current plan file, continue from the first unchecked task, follow UNDERSTAND→PLAN→EXECUTE→VERIFY→DELIVER."
else
  echo "pack-kernel not found at $KERNEL — run install.sh from the all-in-one-agents repo."
fi
