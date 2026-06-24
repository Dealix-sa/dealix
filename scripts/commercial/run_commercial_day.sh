#!/usr/bin/env bash
set -euo pipefail

PYTHON_BIN="${PYTHON:-python3}"

"$PYTHON_BIN" scripts/commercial/commercial_readiness_check.py
"$PYTHON_BIN" scripts/commercial/generate_commercial_go_live_pack.py

echo "Commercial day completed. Review reports/commercial/latest.md."
