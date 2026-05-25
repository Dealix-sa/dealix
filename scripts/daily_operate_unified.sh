#!/usr/bin/env bash
# Unified morning commercial loop — local or production API.
# Usage:
#   bash scripts/daily_operate_unified.sh
#   DEALIX_API=http://localhost:8000 bash scripts/daily_operate_unified.sh

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
API="${DEALIX_API:-${DEALIX_API_BASE:-http://localhost:8000}}"
API="${API%/}"

echo "═══════════════════════════════════════════════════════════════"
echo "  DEALIX — Unified Daily Commercial Loop"
echo "  API=$API  $(date -u +'%Y-%m-%d %H:%M UTC')"
echo "═══════════════════════════════════════════════════════════════"

echo ""
echo "== 0. Gap report (secrets) =="
python3 "$ROOT/scripts/commercial_launch_gap_report.py" || true

echo ""
echo "== 1. Health =="
curl -fsS "$API/health" | head -c 400 || { echo "API unreachable"; exit 1; }
echo ""

echo ""
echo "== 2. Lead prep (draft-only, no sends) =="
if [ -f "$ROOT/scripts/dealix_daily_lead_prep.py" ]; then
  DEALIX_API_BASE="$API" python3 "$ROOT/scripts/dealix_daily_lead_prep.py" --json 2>/dev/null | head -c 2000 || true
  echo ""
fi

echo ""
echo "== 3. Revenue machine (draft_only) =="
curl -fsS -X POST "$API/api/v1/automation/revenue-machine/run" \
  -H 'Content-Type: application/json' \
  -d '{"daily_candidates":200,"gmail_drafts":50,"linkedin_drafts":20,"approval_mode":"draft_only"}' \
  2>/dev/null | python3 -m json.tool 2>/dev/null | head -n 30 || echo "(skipped)"

echo ""
echo "== 4. Founder daily sales pack =="
curl -fsS "$API/api/v1/founder/daily-sales-pack" 2>/dev/null \
  | python3 -c "import sys,json; d=json.load(sys.stdin); print('pending_approvals', d.get('pending_approvals',{}).get('count')); print('outreach_pending', d.get('outreach_queue',{}).get('pending_count')); print('launch_stage', d.get('launch_readiness',{}).get('stage'))" \
  || echo "(skipped)"

echo ""
echo "== 5. Personal operator brief =="
curl -fsS "$API/api/v1/personal-operator/daily-brief" 2>/dev/null | head -c 600 || echo "(skipped)"
echo ""

echo ""
echo "== 6. Follow-ups queue =="
curl -fsS -X POST "$API/api/v1/automation/followups/run" -d '{}' 2>/dev/null | head -c 400 || true
echo ""

echo "═══════════════════════════════════════════════════════════════"
echo "  Done. Review /ar/operator and /ar/approvals in the dashboard."
echo "═══════════════════════════════════════════════════════════════"
