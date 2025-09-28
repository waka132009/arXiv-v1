#!/usr/bin/env bash
set -euo pipefail
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
for f in scripts/fig*.py; do python "$f"; done
latexmk -pdf main.tex
echo "Done."
