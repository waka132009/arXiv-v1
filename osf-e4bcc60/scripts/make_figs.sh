#!/usr/bin/env bash
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$HERE" && cd .. && pwd)"
echo "Running figure scripts ..."
shopt -s nullglob
for F in "$ROOT/scripts"/fig_*.py; do
  echo "  -> $(basename "$F")"
  python "$F"
done
echo "Done. See figures/"
