#!/usr/bin/env bash
set -u

cd "$(git rev-parse --show-toplevel)" || exit 1

echo "=== Dealix Revenue Day ==="
date -u +"%Y-%m-%dT%H:%M:%SZ"

safe_run() {
  title="$1"
  shift
  echo ""
  echo "--- $title ---"
  if command -v timeout >/dev/null 2>&1; then
    timeout 90 "$@" || echo "WARN: $title skipped or failed"
  else
    "$@" || echo "WARN: $title skipped or failed"
  fi
}

[ -x ./scripts/dealix_micro_day.sh ] && safe_run "Micro Day" ./scripts/dealix_micro_day.sh
[ -x ./scripts/dealix_company_day.sh ] && safe_run "Company Day" ./scripts/dealix_company_day.sh

echo ""
echo "--- Revenue Engine v2 ---"
python company/revenue_engine/revenue_engine_v2.py

TODAY="$(date +%F)"
echo ""
echo "FILES:"
echo "company/runtime/revenue/${TODAY}/CEO_REVENUE_REPORT.md"
echo "company/runtime/revenue/${TODAY}/TOP_20_OUTBOUND.csv"
echo "company/runtime/revenue/${TODAY}/WHATSAPP_DRAFTS.md"
echo "company/runtime/revenue/${TODAY}/PROPOSAL_STUBS.md"
