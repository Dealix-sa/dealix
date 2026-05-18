#!/usr/bin/env bash
# Canonical founder day — KPI + commercial morning OR evening evidence.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
for arg in "$@"; do
  if [[ "$arg" == "--evening" ]]; then
    exec python3 "$ROOT/scripts/founder_evening_evidence.py" "${@:2}"
  fi
  if [[ "$arg" == "--executive-rise" ]]; then
    exec python3 "$ROOT/scripts/founder_executive_rise_day.py" "${@:2}"
  fi
done
bash "$ROOT/scripts/run_kpi_hygiene.sh"
bash "$ROOT/scripts/run_founder_commercial_day.sh" "$@"
echo "FOUNDER_DAILY_LOOP=MORNING_OK"
