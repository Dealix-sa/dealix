#!/usr/bin/env bash
# Founder Daily OS — commercial morning + evidence + executive snapshot (no auto-send).
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

EVENING=0
DRY_RUN=0
WITH_BIZ_NOW=0
SKIP_LIVE=0
for arg in "$@"; do
  case "$arg" in
    --evening) EVENING=1 ;;
    --dry-run) DRY_RUN=1 ;;
    --with-business-now) WITH_BIZ_NOW=1 ;;
    --skip-live) SKIP_LIVE=1 ;;
    -h|--help)
      echo "Usage: bash scripts/founder_daily_os_loop.sh [--evening] [--dry-run] [--with-business-now] [--skip-live]"
      exit 0
      ;;
  esac
done

PY="$(command -v python3 2>/dev/null || true)"
[[ -z "$PY" ]] && command -v py >/dev/null 2>&1 && PY="py -3"

echo "== Founder Daily OS =="
echo "  anchor: docs/commercial/MASTER_COMMERCIAL_OPERATING_PLAN_AR.md"
echo ""

COMM_ARGS=()
[[ "$DRY_RUN" -eq 1 ]] && COMM_ARGS+=(--dry-run)
[[ "$WITH_BIZ_NOW" -eq 1 ]] && COMM_ARGS+=(--with-business-now)

echo "== 1/5 commercial morning =="
bash "$ROOT/scripts/run_founder_commercial_day.sh" "${COMM_ARGS[@]}"
echo ""

echo "== 2/5 executive snapshot =="
SNAP_ARGS=(scripts/founder_executive_snapshot.py)
[[ "$SKIP_LIVE" -eq 1 ]] && SNAP_ARGS+=(--skip-live)
$PY "${SNAP_ARGS[@]}"
echo ""

echo "== 3/5 first paid tracker =="
$PY scripts/verify_first_paid_diagnostic_tracker.py
echo ""

echo "== 4/5 railway config =="
RAIL_ARGS=(scripts/verify_railway_production_config.py)
[[ "$SKIP_LIVE" -eq 1 ]] && RAIL_ARGS+=(--skip-live)
$PY "${RAIL_ARGS[@]}"
echo ""

if [[ "$EVENING" -eq 1 ]]; then
  echo "== 5/5 evening evidence =="
  EVE=(scripts/founder_evening_evidence.py --append)
  [[ "$DRY_RUN" -eq 1 ]] && EVE=(scripts/founder_evening_evidence.py --dry-run --append)
  $PY "${EVE[@]}"
else
  echo "== 5/5 evening: skipped (use --evening) =="
fi

echo ""
echo "FOUNDER_DAILY_OS=OK"
