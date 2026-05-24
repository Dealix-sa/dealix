#!/usr/bin/env bash
# Founder launch day-0 — env check, ops wiring smoke, commercial morning, launch gates.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

PYTHON_BIN="$(command -v python3 2>/dev/null || echo python3)"
FAIL=0

echo "== Founder Launch Day-0 =="
echo ""

echo "== 1/6 AI runtime config =="
if "$PYTHON_BIN" scripts/verify_ai_runtime_providers.py; then
  echo "  ai_runtime: PASS"
else
  echo "  ai_runtime: FAIL (keys in .env.local?)"
  FAIL=1
fi
echo ""

echo "== 2/6 ops-autopilot pytest =="
if APP_ENV=test "$PYTHON_BIN" -m pytest tests/test_revenue_ops_autopilot.py -q --no-cov -x; then
  echo "  revenue_ops_autopilot: PASS"
else
  echo "  revenue_ops_autopilot: FAIL"
  FAIL=1
fi
echo ""

echo "== 3/6 autonomous ops stack =="
if "$PYTHON_BIN" scripts/verify_full_autonomous_ops_stack.py; then
  echo "  autonomous_stack: PASS"
else
  echo "  autonomous_stack: FAIL"
  FAIL=1
fi
echo ""

echo "== 4/6 founder go-live =="
if bash scripts/founder_go_live_verify.sh; then
  echo "  go_live: PASS"
else
  echo "  go_live: FAIL"
  FAIL=1
fi
echo ""

echo "== 5/6 commercial morning (quick) =="
if bash scripts/run_founder_commercial_day.sh 2>/dev/null; then
  echo "  commercial_day: PASS"
else
  echo "  commercial_day: PARTIAL (deps or API optional)"
fi
echo ""

echo "== 6/6 integration truth report =="
"$PYTHON_BIN" scripts/verify_founder_integration_truth.py || FAIL=1
echo ""

if [[ "$FAIL" -eq 0 ]]; then
  echo "FOUNDER_LAUNCH_DAY0_VERDICT=PASS"
  exit 0
fi
echo "FOUNDER_LAUNCH_DAY0_VERDICT=FAIL"
exit 1
