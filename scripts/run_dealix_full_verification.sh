#!/usr/bin/env bash
# Dealix full launch-verification suite (Wave 7).
#
# Runs every gate, NEVER hides a failure, and continues even when a check
# fails. Writes a single markdown report and prints a private/public launch
# verdict at the end.
#
#   bash scripts/run_dealix_full_verification.sh
#
# Output: reports/verification/dealix_full_verification_latest.md
set -u  # NOTE: deliberately not -e — we must keep running after a failure.

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

REPORT_DIR="reports/verification"
REPORT="$REPORT_DIR/dealix_full_verification_latest.md"
mkdir -p "$REPORT_DIR"

TS="$(date -u +'%Y-%m-%dT%H:%M:%SZ')"
BRANCH="$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo 'unknown')"

PY="python3"; command -v python3 >/dev/null 2>&1 || PY="python"

# Pick the npm workspace (root has no package.json in this repo; frontend does).
NPM_DIR="."
if [ ! -f package.json ] && [ -f frontend/package.json ]; then NPM_DIR="frontend"; fi

# Result accumulators (parallel arrays — portable across bash versions).
NAMES=(); STATUSES=(); NOTES=()

record() { NAMES+=("$1"); STATUSES+=("$2"); NOTES+=("$3"); }

# run_cmd "Label" cmd args...
run_cmd() {
  local label="$1"; shift
  echo ""; echo "### >>> $label"; echo "\$ $*"
  local out rc
  out="$("$@" 2>&1)"; rc=$?
  echo "$out" | tail -n 40
  if [ $rc -eq 0 ]; then
    record "$label" "PASS" ""
  else
    record "$label" "FAIL" "exit $rc"
  fi
  return 0
}

# run_npm "Label" script — only runs if the script is declared.
run_npm() {
  local label="$1" script="$2"
  if [ "$NPM_DIR" = "." ] && [ ! -f package.json ]; then
    record "$label" "N/A" "no package.json"; return 0
  fi
  if ! grep -q "\"$script\"" "$NPM_DIR/package.json" 2>/dev/null; then
    record "$label" "N/A" "npm script '$script' not defined"; return 0
  fi
  echo ""; echo "### >>> $label"; echo "\$ (cd $NPM_DIR && npm run $script)"
  local out rc
  out="$( (cd "$NPM_DIR" && npm run "$script") 2>&1 )"; rc=$?
  echo "$out" | tail -n 40
  if [ $rc -eq 0 ]; then record "$label" "PASS" ""; else record "$label" "FAIL" "exit $rc"; fi
  return 0
}

# run_make "Label" target — N/A if target absent.
run_make() {
  local label="$1" target="$2"
  if ! grep -qE "^$target:" Makefile 2>/dev/null; then
    record "$label" "N/A" "make target '$target' not found"; return 0
  fi
  run_cmd "$label" make "$target"
}

echo "Dealix full verification — $TS (branch: $BRANCH)"

# --- Asset / safety gates (repo-only, dependency-free) ---
run_cmd "Positioning + claim safety" "$PY" scripts/verify_dealix_positioning.py
run_cmd "CTA map"                    "$PY" scripts/verify_dealix_cta_map.py
run_cmd "Module status"              "$PY" scripts/verify_dealix_module_status.py
run_cmd "Growth assets"             "$PY" scripts/verify_dealix_growth_assets.py
run_cmd "Launch readiness score"    "$PY" scripts/verify_dealix_launch_readiness.py

# --- Build / quality gates ---
run_npm "Frontend build" "build"
run_npm "Frontend lint"  "lint"
# This repo has no JS unit-test runner; fall back to python tests via make.
if grep -q '"test"' "$NPM_DIR/package.json" 2>/dev/null; then
  run_npm "Frontend test" "test"
else
  record "Frontend test" "N/A" "no npm 'test' script in this repo"
fi

# --- Backend / ops gates ---
run_make "env-check"       "env-check"
run_cmd  "Security smoke"  "$PY" scripts/security_smoke.py
run_make "prod-verify"     "prod-verify"

# --- Capture readiness score from the scorer output ---
READINESS_SCORE="$("$PY" scripts/verify_dealix_launch_readiness.py 2>/dev/null | grep '^READINESS_SCORE=' | tail -1 | cut -d= -f2)"
READINESS_SCORE="${READINESS_SCORE:-0}"
READINESS_VERDICT="$("$PY" scripts/verify_dealix_launch_readiness.py 2>/dev/null | grep '^READINESS_VERDICT=' | tail -1 | cut -d= -f2-)"

# --- Classify blockers ---
# P0 (all launch):   safety failures (positioning, claim safety, module status)
# P0 (public only):  frontend build failure
# P1:                everything else that failed
P0_ALL=(); P0_PUBLIC=(); P1=()
status_of() { # echo status for a given label
  local want="$1" i
  for i in "${!NAMES[@]}"; do
    if [ "${NAMES[$i]}" = "$want" ]; then echo "${STATUSES[$i]}"; return; fi
  done
  echo "MISSING"
}
for i in "${!NAMES[@]}"; do
  name="${NAMES[$i]}"; st="${STATUSES[$i]}"; note="${NOTES[$i]}"
  [ "$st" = "FAIL" ] || continue
  case "$name" in
    "Positioning + claim safety"|"Module status")
      P0_ALL+=("$name — unsafe-claim / live-module integrity ($note)") ;;
    "Frontend build")
      P0_PUBLIC+=("$name — site build broken ($note)") ;;
    "CTA map"|"Launch readiness score"|"Growth assets")
      P0_ALL+=("$name — missing core launch asset ($note)") ;;
    *)
      P1+=("$name ($note)") ;;
  esac
done

# --- Verdicts ---
PRIVATE_VERDICT="GO"
[ "${#P0_ALL[@]}" -gt 0 ] && PRIVATE_VERDICT="NO-GO"
[ "$READINESS_SCORE" -lt 70 ] && PRIVATE_VERDICT="NO-GO"

# Public launch is the higher bar: no P0 (all or public-only), readiness >= 85,
# AND a clean P1 list (hygiene must be green before the public surface ships).
PUBLIC_VERDICT="GO"
[ "${#P0_ALL[@]}" -gt 0 ] && PUBLIC_VERDICT="NO-GO"
[ "${#P0_PUBLIC[@]}" -gt 0 ] && PUBLIC_VERDICT="NO-GO"
[ "${#P1[@]}" -gt 0 ] && PUBLIC_VERDICT="NO-GO"
[ "$READINESS_SCORE" -lt 85 ] && PUBLIC_VERDICT="NO-GO"

# --- Write the markdown report ---
{
  echo "# Dealix Full Verification Report"
  echo ""
  echo "- **Timestamp (UTC):** $TS"
  echo "- **Branch:** \`$BRANCH\`"
  echo "- **Readiness score:** $READINESS_SCORE/100 ($READINESS_VERDICT)"
  echo ""
  echo "## 1. Git status"
  echo '```'
  git status --short 2>/dev/null | head -50
  echo '```'
  echo ""
  echo "## 2. Command results"
  echo ""
  echo "| Check | Result | Note |"
  echo "|-------|--------|------|"
  for i in "${!NAMES[@]}"; do
    icon="❓"
    case "${STATUSES[$i]}" in
      PASS) icon="✅ PASS" ;;
      FAIL) icon="❌ FAIL" ;;
      N/A)  icon="➖ N/A" ;;
    esac
    echo "| ${NAMES[$i]} | $icon | ${NOTES[$i]} |"
  done
  echo ""
  echo "## 3. P0 blockers (block ALL launch)"
  if [ "${#P0_ALL[@]}" -eq 0 ]; then echo "_None._"; else
    for x in "${P0_ALL[@]}"; do echo "- $x"; done
  fi
  echo ""
  echo "## 4. P0 blockers (block PUBLIC launch only)"
  if [ "${#P0_PUBLIC[@]}" -eq 0 ]; then echo "_None._"; else
    for x in "${P0_PUBLIC[@]}"; do echo "- $x"; done
  fi
  echo ""
  echo "## 5. P1 blockers"
  if [ "${#P1[@]}" -eq 0 ]; then echo "_None._"; else
    for x in "${P1[@]}"; do echo "- $x"; done
  fi
  echo ""
  echo "## 6. Private launch verdict"
  echo ""
  echo "**$PRIVATE_VERDICT** — private launch requires readiness >= 70 and zero all-launch P0 blockers."
  echo ""
  echo "## 7. Public launch verdict"
  echo ""
  echo "**$PUBLIC_VERDICT** — public launch requires readiness >= 85, a passing frontend build, zero P0 blockers, and a clean P1 list."
  echo ""
  echo "## 8. Next fixes (priority order)"
  if [ "${#P0_ALL[@]}" -gt 0 ]; then echo "1. Clear all-launch P0 blockers (safety / core assets) above."; fi
  if [ "$READINESS_SCORE" -lt 70 ]; then echo "1. Raise readiness score to >= 70 (run \`python3 scripts/verify_dealix_launch_readiness.py\` for the MISSING list)."; fi
  if [ "${#P0_PUBLIC[@]}" -gt 0 ]; then echo "1. Fix the frontend build before any public launch."; fi
  if [ "${#P1[@]}" -gt 0 ]; then echo "1. Work the P1 list once private launch is green."; fi
  if [ "${#P0_ALL[@]}" -eq 0 ] && [ "${#P1[@]}" -eq 0 ] && [ "$READINESS_SCORE" -ge 70 ]; then echo "- Private launch is clear. Proceed to the first 5 manual outreach messages (founder-approved)."; fi
  echo ""
  echo "---"
  echo "_Generated by scripts/run_dealix_full_verification.sh — failures are never hidden._"
} > "$REPORT"

echo ""
echo "============================================================"
echo "Report written: $REPORT"
echo "Readiness: $READINESS_SCORE/100  Private: $PRIVATE_VERDICT  Public: $PUBLIC_VERDICT"
echo "============================================================"
