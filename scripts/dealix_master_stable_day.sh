#!/usr/bin/env bash
set -Eeuo pipefail

cd "$(git rev-parse --show-toplevel)"

echo "========================================"
echo " Dealix Master Stable Day"
echo " $(date -u +"%Y-%m-%dT%H:%M:%SZ")"
echo "========================================"

run_optional() {
  local title="$1"
  shift

  echo ""
  echo "=== $title ==="

  if command -v timeout >/dev/null 2>&1; then
    timeout 120 "$@" || echo "WARN: $title failed or timed out; continuing."
  else
    "$@" || echo "WARN: $title failed; continuing."
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
echo "=== Master Stable Orchestrator ==="
python company/master_stable/master_stable_orchestrator.py

TODAY="$(date +%F)"

echo ""
echo "=== Outputs ==="
echo "CEO report: company/reports/${TODAY}_MASTER_STABLE_CEO_REPORT.md"
echo "Approval queue: company/outbox/${TODAY}_master_stable_approval_queue.csv"
echo "CRM: company/crm/pipeline.csv"

echo ""
echo "DONE"
