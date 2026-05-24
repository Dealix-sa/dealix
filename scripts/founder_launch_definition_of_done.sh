#!/usr/bin/env bash
# Definition of Done — Founder OS full launch checklist (automated gates only).
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
export APP_ENV=test

PYTHON_BIN="$(command -v python3 2>/dev/null || echo python3)"
FAIL=0

check() {
  local name="$1"
  shift
  echo "== $name =="
  if "$@"; then
    echo "  $name: PASS"
  else
    echo "  $name: FAIL"
    FAIL=1
  fi
  echo ""
}

echo "== Founder Launch Definition of Done =="
echo ""

check "revenue_ops_autopilot" \
  "$PYTHON_BIN" -m pytest tests/test_revenue_ops_autopilot.py -q --no-cov -x

check "ai_runtime_unit" \
  "$PYTHON_BIN" -m pytest tests/unit/test_ai_runtime_router.py -q --no-cov -x

check "autonomous_ops_stack" \
  "$PYTHON_BIN" scripts/verify_full_autonomous_ops_stack.py

check "founder_go_live" \
  bash scripts/founder_go_live_verify.sh

check "commercial_go_live" \
  bash scripts/verify_dealix_commercial_go_live.sh

check "strongest_plan_status" \
  "$PYTHON_BIN" scripts/founder_strongest_plan_status.py

check "integration_truth" \
  "$PYTHON_BIN" scripts/verify_founder_integration_truth.py

if [[ -n "${DEALIX_API_BASE:-}" ]] && [[ -n "${DEALIX_ADMIN_API_KEY:-}" ]]; then
  check "production_smoke" bash scripts/founder_production_smoke.sh
else
  echo "== production_smoke: SKIP (set DEALIX_API_BASE + DEALIX_ADMIN_API_KEY) =="
  echo ""
fi

if [[ "$FAIL" -eq 0 ]]; then
  echo "FOUNDER_LAUNCH_DOD_VERDICT=PASS"
  exit 0
fi
echo "FOUNDER_LAUNCH_DOD_VERDICT=FAIL"
exit 1
