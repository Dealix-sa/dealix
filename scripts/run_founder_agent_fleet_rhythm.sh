#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
WEEKLY=0
SKIP_RAILWAY=0
for arg in "$@"; do
  case "$arg" in
    --weekly) WEEKLY=1 ;;
    --skip-railway) SKIP_RAILWAY=1 ;;
  esac
done
PY="$(command -v python3 2>/dev/null || echo python)"
echo "== Founder agent fleet rhythm =="
$PY scripts/founder_soaen_daily.py --out "data/founder_briefs/soaen_$(date -u +%Y-%m-%d 2>/dev/null || date +%Y-%m-%d).md" || true
$PY scripts/founder_agent_queue_status.py --seed-today --unified || true
$PY scripts/verify_soaen_loop.py || true
$PY scripts/founder_gtm_proof_loop.py || true
if [[ "$SKIP_RAILWAY" -eq 0 ]]; then
  $PY scripts/verify_railway_production_config.py --skip-live \
    --ui-start-command "${RAILWAY_UI_START_COMMAND:-./start.sh}" \
    --ui-predeploy "${RAILWAY_UI_PREDEPLOY:-echo \"no migration needed\"}" || true
fi
if [[ "$WEEKLY" -eq 1 ]]; then
  $PY scripts/founder_weekly_board_init.py --write || true
  $PY scripts/founder_agent_weekly_learning.py --seed-quarterly || true
  $PY scripts/founder_agent_weekly_learning.py --apply-hints || true
fi
echo "FOUNDER_AGENT_FLEET_RHYTHM=OK"
