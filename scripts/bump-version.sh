#!/usr/bin/env bash
# Bump version, commit, tag, push.
# Usage: ./scripts/bump-version.sh 1.1.0
set -euo pipefail

NEW="${1:?usage: bump-version.sh <version>}"

for f in package.json .claude-plugin/plugin.json; do
  python3 - "$f" "$NEW" << 'EOF'
import json, sys
p, v = sys.argv[1], sys.argv[2]
d = json.load(open(p))
d["version"] = v
json.dump(d, open(p, "w"), indent=2)
print(f"{p} -> {v}")
EOF
done

git add -A
git commit -m "chore: release v$NEW"
git tag "v$NEW"
git push origin main --tags
echo "released v$NEW"
