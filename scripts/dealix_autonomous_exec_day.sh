#!/usr/bin/env bash
set -Eeuo pipefail

cd "$(git rev-parse --show-toplevel)"

echo "=== Dealix Autonomous Executive Day ==="
date -u +"%Y-%m-%dT%H:%M:%SZ"

echo ""
echo "1) Production + company operating day"
./scripts/dealix_company_day.sh

echo ""
echo "2) Founder business day"
if [ -x ./scripts/dealix_founder_business_day.sh ]; then
  ./scripts/dealix_founder_business_day.sh || true
else
  echo "Founder business day script unavailable."
fi

echo ""
echo "3) Autonomous executive orchestration"
python company/scripts/autonomous_exec_orchestrator.py

echo ""
echo "4) Outputs"
TODAY="$(date +%F)"
echo "CEO report: company/reports/${TODAY}_AUTONOMOUS_CEO_REPORT.md"
echo "Approval queue: company/outbox/${TODAY}_approval_queue.csv"
echo "CRM: company/crm/pipeline.csv"

echo ""
echo "DONE"
