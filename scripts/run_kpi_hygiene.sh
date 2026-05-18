#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
PYTHON_BIN="$(command -v python3 2>/dev/null || echo py -3)"
$PYTHON_BIN "$ROOT/scripts/bootstrap_founder_kpi_import.py"
$PYTHON_BIN "$ROOT/scripts/apply_kpi_founder_commercial.py" --status
echo "KPI_HYGIENE=OK"
