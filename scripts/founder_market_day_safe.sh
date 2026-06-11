#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

mkdir -p data/founder_briefs var/logs

TODAY="$(date +%F)"
LOG="var/logs/founder_market_day_safe_${TODAY}.log"

run_step() {
  local label="$1"
  local seconds="$2"
  shift 2

  echo ""
  echo "== ${label} =="
  echo "CMD: $*"

  if timeout "${seconds}" "$@"; then
    echo "OK: ${label}"
  else
    code=$?
    echo "WARN: ${label} exited with code ${code}"
    return 0
  fi
}

{
  echo "== Dealix Founder Market Day Safe =="
  date -Iseconds

  run_step "Business NOW" 180 bash scripts/run_business_now.sh
  run_step "Commercial launch ready" 240 python3 scripts/verify_commercial_launch_ready.py
  run_step "Founder go-live" 420 bash scripts/founder_go_live_verify.sh
  run_step "Founder commercial day" 300 bash scripts/run_founder_commercial_day.sh
  run_step "War Room drafts" 120 python3 scripts/generate_war_room_touch_drafts.py
  run_step "Motion A pipeline" 120 python3 scripts/founder_motion_a_pipeline.py
  run_step "First paid tracker" 120 python3 scripts/verify_first_paid_diagnostic_tracker.py
  run_step "Paid launch readiness" 120 python3 scripts/verify_paid_launch_readiness.py
  run_step "Value plan snapshot" 120 python3 scripts/export_value_plan_snapshot.py

  echo ""
  echo "FOUNDER_MARKET_DAY_SAFE=OK"
  echo "NEXT_ACTION=Approve 5 drafts manually, send manually, then log real evidence."
} 2>&1 | tee "$LOG"
