#!/usr/bin/env bash
# Founder commercial morning — canonical daily command (governed: drafts + approval, no auto-send)
# Usage:
#   bash scripts/run_founder_commercial_day.sh
#   bash scripts/run_founder_commercial_day.sh --dry-run
#   bash scripts/run_founder_commercial_day.sh --with-business-now
#   bash scripts/run_founder_commercial_day.sh --full   # business_now + sync evidence
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

DRY_RUN=0
WITH_BIZ_NOW=0
SYNC_EVIDENCE=0
for arg in "$@"; do
  case "$arg" in
    --dry-run) DRY_RUN=1 ;;
    --with-business-now) WITH_BIZ_NOW=1 ;;
    --full)
      WITH_BIZ_NOW=1
      SYNC_EVIDENCE=1
      ;;
  esac
done

PYTHON_BIN="$(command -v python3 2>/dev/null || true)"
if [[ -z "${PYTHON_BIN}" ]] && command -v py >/dev/null 2>&1; then
  PYTHON_BIN="py -3"
fi
if [[ -z "${PYTHON_BIN}" ]]; then
  echo "FOUNDER_COMMERCIAL_DAY: FAIL — python3 not found"
  exit 1
fi

API_URL="${DEALIX_API_URL:-${NEXT_PUBLIC_API_URL:-http://localhost:8000}}"
API_URL="${API_URL%/}"
ADMIN_KEY="${DEALIX_ADMIN_API_KEY:-}"
DATE="$(date -u +%Y-%m-%d 2>/dev/null || date +%Y-%m-%d)"

echo "== Dealix Founder Commercial Day (canonical) =="
echo "  repo: $ROOT"
echo "  date: $DATE"
echo "  dry_run: $DRY_RUN"
echo ""

if [[ "$DRY_RUN" -eq 1 ]]; then
  exec "$PYTHON_BIN" "$ROOT/scripts/founder_revenue_day_runner.py" --dry-run
fi

DAILY_ARGS=(--api-only)
if [[ -z "$ADMIN_KEY" ]]; then
  DAILY_ARGS=(--skip-api)
fi
echo "== 0/7 Dealix daily ops (bridge + health) =="
$PYTHON_BIN "$ROOT/scripts/run_dealix_daily_ops.py" "${DAILY_ARGS[@]}"
echo ""

echo "== 1/7 Founder daily brief =="
$PYTHON_BIN "$ROOT/scripts/dealix_founder_daily_brief.py" --out "data/founder_briefs/brief_${DATE}.md"
echo ""

echo "== 2/7 KPI commercial status =="
$PYTHON_BIN "$ROOT/scripts/apply_kpi_founder_commercial.py" --status || true
echo ""

if [[ "$WITH_BIZ_NOW" -eq 1 ]]; then
  echo "== optional: Business NOW =="
  if [[ -f "$ROOT/scripts/run_business_now.sh" ]]; then
    bash "$ROOT/scripts/run_business_now.sh" || echo "  (business_now warning — continuing)"
  fi
  echo ""
fi

echo "== 3/8 War Room sync (P0 rotation) =="
$PYTHON_BIN "$ROOT/scripts/commercial_war_room_sync.py"
echo ""

echo "== 4/8 War Room CSV import (skips duplicates) =="
if [[ -n "$ADMIN_KEY" ]]; then
  export DEALIX_API_BASE="${DEALIX_API_BASE:-$API_URL}"
  $PYTHON_BIN "$ROOT/scripts/import_war_room_targets.py" --apply --via-api \
    || $PYTHON_BIN "$ROOT/scripts/import_war_room_targets.py" --apply \
    || echo "  (import warning — continuing)"
else
  $PYTHON_BIN "$ROOT/scripts/import_war_room_targets.py" --apply || echo "  (import warning — continuing)"
fi
echo ""

echo "== 5/8 Commercial digest =="
SYNC_ARGS=()
if [[ "$SYNC_EVIDENCE" -eq 1 || "${DEALIX_SYNC_EVIDENCE:-}" == "1" ]]; then
  SYNC_ARGS+=(--sync-evidence --pull-evidence)
fi
$PYTHON_BIN "$ROOT/scripts/founder_commercial_digest.py" --out "data/founder_briefs/commercial_${DATE}.md" "${SYNC_ARGS[@]}"
echo ""

echo "== 5b/8 War Room touch drafts (governed, no send) =="
$PYTHON_BIN "$ROOT/scripts/generate_war_room_touch_drafts.py" --top-n 10 || echo "  (touch drafts warning — continuing)"
echo ""

echo "== 6/9 Social queue today =="
$PYTHON_BIN "$ROOT/scripts/social_queue_today.py" || true
echo ""

echo "== 7/9 AEO + War Room summary + verdict =="
$PYTHON_BIN "$ROOT/scripts/founder_revenue_day_runner.py" --skip-substeps
echo ""

echo "== 8/9 Expand social queue (idempotent weeks 9–12) =="
$PYTHON_BIN "$ROOT/scripts/expand_social_queue_12w.py" || true
echo ""

echo "== 9/9 Daily pack index =="
echo "  See data/founder_briefs/ and data/war_room_today.json"
echo ""

echo "== Automated drafts (production) =="
echo "  GitHub: .github/workflows/daily-revenue-machine.yml (04:00 UTC, draft_only)"
echo "  GitHub: .github/workflows/founder_commercial_daily.yml (05:00 UTC Sun-Thu)"
echo "  Weekly content: python scripts/generate_weekly_content_drafts.py"
echo "  Queue approvals: python scripts/queue_content_drafts_for_approval.py --dry-run"
if [[ -n "$ADMIN_KEY" ]]; then
  echo "  War Room API: ${API_URL}/api/v1/ops-autopilot/war-room?needs_follow_up=true"
else
  echo "  Set DEALIX_ADMIN_API_KEY for live War Room API fetch."
fi
echo ""

echo "FOUNDER_COMMERCIAL_DAY: OK"
echo "Soft launch verify: python3 scripts/verify_commercial_launch_ready.py"
echo "Extended morning (+ Business NOW): bash scripts/run_founder_revenue_day.sh"
echo "Company ready: docs/company/DEALIX_COMPANY_READY_MASTER_AR.md"
echo "5 min ops: docs/commercial/MASTER_COMMERCIAL_OPERATING_PLAN_AR.md"
echo "Launch checklist: docs/commercial/COMMERCIAL_LAUNCH_CHECKLIST_AR.md"
