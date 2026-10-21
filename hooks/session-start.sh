#!/usr/bin/env bash
# SessionStart hook for all-in-one-agents.
#
# Re-injects the framework kernel after session start, /clear, and compaction so
# the methodology survives context loss.
#
# Emits the structured Claude Code hook contract on stdout:
#   {"hookSpecificOutput":{"hookEventName":"SessionStart","additionalContext":"..."}}
#
# Design constraints:
#   - POSIX-ish bash only. No jq, no python, no coreutils beyond awk/tr.
#     SessionStart hooks can run before PATH repair on some hosts.
#   - Never emit partial JSON. If the kernel files are missing we exit 0 silently
#     rather than handing the host a malformed payload.
#   - Idempotent marker so a second injection in the same transcript is visible.
set -uo pipefail

MARKER='[aio-kernel v2]'

SCRIPT_DIR=''
case "${BASH_SOURCE[0]:-$0}" in
  */*|*\\*) SCRIPT_DIR="$(cd "${0%[/\\]*}" 2>/dev/null && pwd)" ;;
esac

# Resolve the skills directory across the three supported layouts:
#   1. plugin install:   <plugin>/skills
#   2. user install:     ~/.claude/skills
#   3. custom PACK_DIR
candidates=()
[ -n "${PACK_DIR:-}" ] && candidates+=("$PACK_DIR")
[ -n "$SCRIPT_DIR" ] && candidates+=("$SCRIPT_DIR/../skills")
candidates+=("${HOME:-}/.claude/skills")

SKILLS_DIR=''
for c in "${candidates[@]}"; do
  if [ -n "$c" ] && [ -f "$c/pack-kernel/SKILL.md" ]; then
    SKILLS_DIR="$(cd "$c" 2>/dev/null && pwd)"
    break
  fi
done

# Not installed / not a configured pack: stay silent, do not break the session.
[ -z "$SKILLS_DIR" ] && exit 0

KERNEL="$SKILLS_DIR/pack-kernel/SKILL.md"
ENTRY="$SKILLS_DIR/using-all-in-one-agents/SKILL.md"

# Strip YAML frontmatter. Handles: no frontmatter, CRLF, frontmatter-only files.
strip_frontmatter() {
  awk '
    BEGIN { state = 0 }                       # 0=before, 1=inside, 2=after
    state == 0 && NR == 1 {
      sub(/\r$/, "")
      if ($0 == "---") { state = 1; next }
      state = 2
    }
    state == 1 {
      sub(/\r$/, "")
      if ($0 == "---") state = 2
      next
    }
    { sub(/\r$/, ""); print }
  ' "$1"
}

# JSON-escape via bash builtins only. Backslash first, then the rest.
json_escape() {
  local s=$1
  s=${s//\\/\\\\}
  s=${s//\"/\\\"}
  s=${s//$'\t'/\\t}
  s=${s//$'\r'/\\r}
  s=${s//$'\n'/\\n}
  printf '%s' "$s"
}

[ -r "$KERNEL" ] || exit 0

kernel_body="$(strip_frontmatter "$KERNEL")"
entry_body=''
[ -r "$ENTRY" ] && entry_body="$(strip_frontmatter "$ENTRY")"

payload="<EXTREMELY_IMPORTANT>
$MARKER
You have the all-in-one-agents framework. The kernel below is already loaded - do not re-read it with a tool. Follow it.

$kernel_body"

if [ -n "$entry_body" ]; then
  payload="$payload

---

$entry_body"
fi

payload="$payload
</EXTREMELY_IMPORTANT>"

printf '{"hookSpecificOutput":{"hookEventName":"SessionStart","additionalContext":"%s"}}\n' \
  "$(json_escape "$payload")"
exit 0
