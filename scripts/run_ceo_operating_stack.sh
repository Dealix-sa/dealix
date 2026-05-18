#!/usr/bin/env bash
# CEO operating stack — agent fleet + daily cadence + Railway verify.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

API="${DEALIX_API_BASE:-https://api.dealix.me}"
QUICK=0
SKIP_RAILWAY=0
for arg in "$@"; do
  case "$arg" in
    --quick) QUICK=1 ;;
    --skip-railway) SKIP_RAILWAY=1 ;;
  esac
done

PY="$(command -v python3 2>/dev/null || true)"
[[ -z "$PY" ]] && command -v py >/dev/null 2>&1 && PY="py -3"

echo "== CEO operating stack =="
echo "  policy: drafts + approvals only"
echo ""

echo "== 1/4 Agent queue seed =="
$PY scripts/founder_agent_queue_status.py --seed-today

echo ""
echo "== 2/4 Agent fleet rhythm =="
bash scripts/run_founder_agent_fleet_rhythm.sh

echo ""
echo "== 3/4 Founder daily cadence =="
if [[ "$QUICK" -eq 1 ]] && [[ -f scripts/founder_daily_cadence.sh ]]; then
  bash scripts/founder_daily_cadence.sh --quick
elif [[ -f scripts/founder_daily_cadence.sh ]]; then
  bash scripts/founder_daily_cadence.sh
elif [[ -f scripts/founder_one_command.sh ]]; then
  bash scripts/founder_one_command.sh
fi

if [[ "$SKIP_RAILWAY" -eq 0 ]]; then
  echo ""
  echo "== 4/4 Railway production config =="
  $PY scripts/verify_railway_production_config.py --api-base "$API" || true
fi

echo ""
echo "CEO_OPERATING_STACK=OK"
echo "  UI: /ar/ops/founder (agent queue)"
echo "  Approvals: /ar/ops/approvals"
