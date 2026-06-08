#!/usr/bin/env bash
set -Eeuo pipefail

cd "$(git rev-parse --show-toplevel)"

echo "========================================"
echo " Dealix Master Lite Day"
echo " $(date -u +"%Y-%m-%dT%H:%M:%SZ")"
echo "========================================"

run_optional() {
  local name="$1"
  shift
  echo ""
  echo "=== $name ==="
  if command -v timeout >/dev/null 2>&1; then
    timeout 180 "$@" || echo "WARN: $name failed or timed out; continuing."
  else
    "$@" || echo "WARN: $name failed; continuing."
  fi
}

if [ -x ./scripts/dealix_prod_check.sh ]; then
  run_optional "Production health" ./scripts/dealix_prod_check.sh
fi

if [ -x ./scripts/dealix_secret_aware_company_day.sh ]; then
  run_optional "Secret-aware company day" ./scripts/dealix_secret_aware_company_day.sh
fi

if [ -x ./scripts/dealix_company_day.sh ]; then
  run_optional "Company day" ./scripts/dealix_company_day.sh
fi

if [ -x ./scripts/dealix_founder_business_day.sh ]; then
  run_optional "Founder business day" ./scripts/dealix_founder_business_day.sh
fi

echo ""
echo "=== Master Lite Orchestrator ==="
python company/master_lite/master_lite_orchestrator.py

TODAY="$(date +%F)"

echo ""
echo "=== Outputs ==="
echo "CEO report: company/reports/${TODAY}_MASTER_LITE_CEO_REPORT.md"
echo "Approval queue: company/outbox/${TODAY}_master_lite_approval_queue.csv"
echo "CRM: company/crm/pipeline.csv"

echo ""
echo "DONE"
