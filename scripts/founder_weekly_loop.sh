#!/usr/bin/env bash
# Founder weekly loop — offline gates + strongest plan wiring + dogfood war room.
# Used by founder_weekly_verify CI and local Sunday retro prep.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

echo "== Founder operating system =="
bash scripts/verify_founder_operating_system.sh

echo "== Commercial launch readiness =="
python3 scripts/verify_commercial_launch_ready.py

echo "== Strongest plan checklist =="
python3 scripts/founder_strongest_plan_status.py

echo "== Comprehensive plan =="
python3 scripts/founder_comprehensive_plan_status.py

echo "== Dogfooding war room =="
python3 scripts/founder_dogfooding_war_room_sync.py

echo "FOUNDER_WEEKLY_LOOP=PASS"
