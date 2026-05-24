#!/usr/bin/env bash
# Ensure gitignored KPI import file exists from example (no invented numbers).
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
EXAMPLE="${ROOT}/dealix/transformation/kpi_founder_commercial_import.example.yaml"
TARGET="${ROOT}/dealix/transformation/kpi_founder_commercial_import.yaml"

if [[ -f "$TARGET" ]]; then
  echo "KPI_IMPORT=exists path=$TARGET"
  python3 "${ROOT}/scripts/apply_kpi_founder_commercial.py" --status 2>/dev/null || true
  exit 0
fi

if [[ ! -f "$EXAMPLE" ]]; then
  echo "MISSING example: $EXAMPLE" >&2
  exit 1
fi

cp "$EXAMPLE" "$TARGET"
echo "KPI_IMPORT=created from example"
echo "  action: fill from real CRM only, then: python3 scripts/apply_kpi_founder_commercial.py"
exit 0
