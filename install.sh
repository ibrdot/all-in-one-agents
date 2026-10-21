#!/usr/bin/env bash
# Thin wrapper — real installer lives in scripts/install.sh
exec "$(dirname "${BASH_SOURCE[0]}")/scripts/install.sh" "$@"
