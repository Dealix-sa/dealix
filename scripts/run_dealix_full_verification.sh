#!/usr/bin/env bash
# Dealix Full Verification — run every Wave gate and write a single report.
#
# Runs each verification script, records PASS/FAIL, and assembles
# reports/verification/dealix_full_verification_<ts>.md (+ _latest.md).
# Exits non-zero if any gate fails. Safe to run locally or in CI.

set -uo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

PY="${PYTHON:-python3}"
OUT_DIR="reports/verification"
mkdir -p "$OUT_DIR"

TS="$(date +%Y%m%d_%H%M%S)"
HUMAN_TS="$(date '+%Y-%m-%d %H:%M:%S')"
REPORT="$OUT_DIR/dealix_full_verification_${TS}.md"
LATEST="$OUT_DIR/dealix_full_verification_latest.md"

# Gate label | command
GATES=(
  "Positioning|$PY scripts/verify_dealix_positioning.py"
  "Module status|$PY scripts/verify_dealix_module_status.py"
  "Growth assets|$PY scripts/verify_dealix_growth_assets.py"
  "Launch readiness|$PY scripts/verify_dealix_launch_readiness.py"
  "E2E dry run|$PY scripts/run_dealix_e2e_dry_run.py"
)

declare -a RESULTS
OVERALL=0

{
  echo "# Dealix Full Verification"
  echo
  echo "_Run: ${HUMAN_TS}_"
  echo
  echo "| Gate | Result |"
  echo "|---|---|"
} > "$REPORT"

echo "== Dealix Full Verification =="
for entry in "${GATES[@]}"; do
  label="${entry%%|*}"
  cmd="${entry#*|}"
  echo
  echo "--- ${label} ---"
  output="$($cmd 2>&1)"
  code=$?
  echo "$output"
  if [ $code -eq 0 ]; then
    result="PASS"
  else
    result="FAIL"
    OVERALL=1
  fi
  RESULTS+=("${label}: ${result}")
  echo "| ${label} | ${result} |" >> "$REPORT"
done

{
  echo
  if [ $OVERALL -eq 0 ]; then
    echo "## RESULT: PASS — all gates green."
    echo
    echo "System is reviewable and operable. Proceed to the launch-readiness decision."
  else
    echo "## RESULT: FAIL — one or more gates failed."
    echo
    echo "Fix the failing gate(s) above before launch. See per-gate output in the"
    echo "console log and the relevant docs/ entries."
  fi
  echo
  echo "> Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة"
} >> "$REPORT"

cp "$REPORT" "$LATEST"

echo
echo "== Summary =="
for r in "${RESULTS[@]}"; do
  echo "  $r"
done
echo
echo "Report: $REPORT"
[ $OVERALL -eq 0 ] && echo "OVERALL: PASS" || echo "OVERALL: FAIL"
exit $OVERALL
