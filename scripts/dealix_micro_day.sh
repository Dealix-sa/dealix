#!/usr/bin/env bash
set -u

cd "$(git rev-parse --show-toplevel)" || exit 1

echo "=== Dealix Micro Day ==="
date -u +"%Y-%m-%dT%H:%M:%SZ"

safe_run() {
  title="$1"
  shift
  echo ""
  echo "--- $title ---"
  if command -v timeout >/dev/null 2>&1; then
    timeout 60 "$@" || echo "WARN: $title skipped/failed"
  else
    "$@" || echo "WARN: $title skipped/failed"
  fi
}

[ -x ./scripts/dealix_prod_check.sh ] && safe_run "prod check" ./scripts/dealix_prod_check.sh
[ -x ./scripts/dealix_secret_aware_company_day.sh ] && safe_run "lead research" ./scripts/dealix_secret_aware_company_day.sh
[ -x ./scripts/dealix_company_day.sh ] && safe_run "company day" ./scripts/dealix_company_day.sh

echo ""
echo "--- micro master ---"
python company/micro/micro_master.py

TODAY="$(date +%F)"
echo ""
echo "FILES:"
echo "company/reports/${TODAY}_MICRO_MASTER_CEO_REPORT.md"
echo "company/outbox/${TODAY}_micro_master_approval_queue.csv"
echo "company/crm/pipeline.csv"
