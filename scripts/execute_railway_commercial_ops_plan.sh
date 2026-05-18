#!/usr/bin/env bash
# Full plan verification — Railway + KPI + launch phase + executive snapshot.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
API="${DEALIX_API_BASE:-https://api.dealix.me}"
echo "== Production probes =="
curl -fsS "${API%/}/healthz" | head -c 120 || echo "(healthz unreachable)"
echo ""
curl -fsS "${API%/}/version" | head -c 200 || echo "(version 404 until deploy)"
echo ""
python3 "$ROOT/scripts/verify_railway_production_config.py" --api-base "$API"
bash "$ROOT/scripts/run_kpi_hygiene.sh"
python3 "$ROOT/scripts/founder_executive_rise_day.py" --json-only --api-base "$API"
bash "$ROOT/scripts/founder_motion_a_weekly_review.sh"
python3 "$ROOT/scripts/verify_launch_phase.py"
echo "RAILWAY_COMMERCIAL_OPS_PLAN=OK"
