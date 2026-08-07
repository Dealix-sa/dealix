#!/usr/bin/env bash
set -Eeuo pipefail

cd "$(git rev-parse --show-toplevel)"

TODAY="$(date +%F)"

echo "=================================================="
echo " Dealix Master Company Day"
echo " $TODAY"
echo "=================================================="

echo ""
echo "1) Git state"
git branch --show-current
git status --short || true

echo ""
echo "2) Production health"
if [ -x ./scripts/dealix_prod_check.sh ]; then
  ./scripts/dealix_prod_check.sh
else
  echo "Missing scripts/dealix_prod_check.sh"
fi

echo ""
echo "3) Company operating day"
if [ -x ./scripts/dealix_company_day.sh ]; then
  ./scripts/dealix_company_day.sh
else
  echo "Missing scripts/dealix_company_day.sh"
fi

echo ""
echo "4) Founder business day"
if [ -x ./scripts/dealix_founder_business_day.sh ]; then
  ./scripts/dealix_founder_business_day.sh || true
else
  echo "Missing scripts/dealix_founder_business_day.sh"
fi

echo ""
echo "5) Autonomous executive day"
if [ -x ./scripts/dealix_autonomous_exec_day.sh ]; then
  ./scripts/dealix_autonomous_exec_day.sh || true
else
  echo "Autonomous executive script not merged yet."
fi

echo ""
echo "6) Frontend quick verify"
if [ -x ./scripts/dealix_frontend_verify.sh ]; then
  ./scripts/dealix_frontend_verify.sh || true
else
  (
    cd apps/web
    rm -rf .next
    npm install
    npm run verify
  ) || true
fi

echo ""
echo "7) GitHub latest runs"
gh run list --branch main --limit 10 || true

echo ""
echo "8) Output index"
echo "CEO report:"
ls -1 company/reports/*AUTONOMOUS_CEO_REPORT.md 2>/dev/null | tail -3 || true

echo ""
echo "Approval queue:"
ls -1 company/outbox/*approval_queue.csv 2>/dev/null | tail -3 || true

echo ""
echo "Lead research:"
ls -1 company/lead_research/"$TODAY"/* 2>/dev/null || true

echo ""
echo "Founder output:"
ls -la founder_os/output/"$TODAY" 2>/dev/null || true

echo ""
echo "9) Today’s required founder actions"
echo "- Review company/reports/${TODAY}_AUTONOMOUS_CEO_REPORT.md"
echo "- Review company/outbox/${TODAY}_approval_queue.csv"
echo "- Send 20 reviewed messages manually"
echo "- Push Diagnostic Sprint to warm replies"
echo "- Update company/crm/pipeline.csv"

echo ""
echo "DONE"
