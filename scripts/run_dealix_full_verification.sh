#!/usr/bin/env bash
# Dealix full verification — founder-operations completion pack.
#
# Chains compile sanity, the four new Dealix verifiers, the end-to-end dry run,
# and (when present) the existing Wave 7.5 and Wave 8 verifiers as regression.
# Records PASS/FAIL per check and writes a markdown report.
set -uo pipefail

cd "$(dirname "$0")/.."

REPORT_DIR="reports/verification"
REPORT="${REPORT_DIR}/dealix_full_verification_latest.md"
mkdir -p "${REPORT_DIR}"

results=()
overall_pass=true

run_check() {
  local name="$1"
  local cmd="$2"
  if eval "${cmd}" >/dev/null 2>&1; then
    results+=("${name}=PASS")
    echo "  [PASS] ${name}"
  else
    results+=("${name}=FAIL")
    overall_pass=false
    echo "  [FAIL] ${name}"
  fi
}

echo "-- Compile sanity ----------------------------------------"
run_check "COMPILEALL" "python3 -m compileall -q scripts/run_dealix_e2e_dry_run.py scripts/create_customer_workspace.py scripts/founder_daily_command.py scripts/verify_dealix_positioning.py scripts/verify_dealix_module_status.py scripts/verify_dealix_growth_assets.py scripts/verify_dealix_launch_readiness.py"

echo "-- New Dealix verifiers ----------------------------------"
run_check "POSITIONING" "python3 scripts/verify_dealix_positioning.py"
run_check "MODULE_STATUS" "python3 scripts/verify_dealix_module_status.py"
run_check "GROWTH_ASSETS" "python3 scripts/verify_dealix_growth_assets.py"
run_check "LAUNCH_READINESS" "python3 scripts/verify_dealix_launch_readiness.py"

echo "-- End-to-end dry run ------------------------------------"
run_check "E2E_DRY_RUN" "python3 scripts/run_dealix_e2e_dry_run.py"

echo "-- Existing wave regression (if present) -----------------"
if [ -f scripts/wave7_5_service_truth_verify.sh ]; then
  run_check "WAVE7_5_REGRESSION" "bash scripts/wave7_5_service_truth_verify.sh"
else
  results+=("WAVE7_5_REGRESSION=SKIP")
  echo "  [SKIP] WAVE7_5_REGRESSION (script not present)"
fi
if [ -f scripts/wave8_customer_ready_verify.sh ]; then
  run_check "WAVE8_REGRESSION" "bash scripts/wave8_customer_ready_verify.sh"
else
  results+=("WAVE8_REGRESSION=SKIP")
  echo "  [SKIP] WAVE8_REGRESSION (script not present)"
fi

timestamp="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
if [ "${overall_pass}" = true ]; then
  verdict="PASS"
else
  verdict="FAIL"
fi

{
  echo "# Dealix Full Verification"
  echo ""
  echo "Timestamp: ${timestamp}"
  echo ""
  echo "| Check | Result |"
  echo "| --- | --- |"
  for entry in "${results[@]}"; do
    name="${entry%%=*}"
    value="${entry##*=}"
    echo "| ${name} | ${value} |"
  done
  echo ""
  echo "Overall: ${verdict}"
} > "${REPORT}"

echo ""
echo "Report: ${REPORT}"
echo "Overall: ${verdict}"

if [ "${overall_pass}" = true ]; then
  exit 0
fi
exit 1
