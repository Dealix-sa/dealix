#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
python3 "$ROOT/scripts/founder_strongest_plan_status.py" || true
python3 "$ROOT/scripts/founder_motion_a_pipeline.py" --top-n 15 || true
python3 "$ROOT/scripts/founder_weekly_decision_init.py" 2>/dev/null || true
python3 "$ROOT/scripts/founder_weekly_scorecard.py" 2>/dev/null || true
python3 "$ROOT/scripts/verify_first_paid_diagnostic_tracker.py" || true
echo "FOUNDER_MOTION_A_WEEKLY=OK"
