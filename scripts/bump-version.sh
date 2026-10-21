#!/usr/bin/env bash
# Local metadata update only. Publication is a separate reviewed action.
# Usage: ./scripts/bump-version.sh 1.5.0
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
python3 "$ROOT/scripts/release_metadata.py" "${1:?usage: bump-version.sh <version>}"
