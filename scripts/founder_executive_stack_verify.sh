#!/usr/bin/env bash
# Founder executive stack — Railway + GTM surfaces + commercial soft launch + first-paid.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
export APP_ENV=test

API_BASE="${DEALIX_API_BASE:-https://api.dealix.me}"
FAIL=0

PY="$(command -v python3 2>/dev/null || true)"
[[ -z "$PY" ]] && command -v py >/dev/null 2>&1 && PY="py -3"

echo "== Founder executive stack verify =="
echo "  api: $API_BASE"
echo ""

echo "== 1/6 railway_production_config =="
if $PY scripts/verify_railway_production_config.py --api-base "$API_BASE"; then
  :
else
  FAIL=1
fi
echo ""

echo "== 2/6 gtm_public_surfaces =="
if $PY scripts/verify_gtm_public_surfaces.py; then
  :
else
  FAIL=1
fi
echo ""

echo "== 3/6 founder_executive_snapshot =="
$PY scripts/founder_executive_snapshot.py --api-base "$API_BASE" || true
echo ""

echo "== 4/6 commercial_launch_ready =="
if $PY scripts/verify_commercial_launch_ready.py; then
  :
else
  FAIL=1
fi
echo ""

echo "== 5/6 first_paid_proof_pack_path =="
$PY scripts/run_first_paid_proof_pack_path.py || true
echo ""

echo "== 6/6 paid_launch_readiness (soft) =="
$PY scripts/verify_paid_launch_readiness.py || true
echo ""

if [[ "$FAIL" -eq 0 ]]; then
  echo "FOUNDER_EXECUTIVE_STACK=PASS"
  exit 0
fi
echo "FOUNDER_EXECUTIVE_STACK=FAIL"
exit 1
