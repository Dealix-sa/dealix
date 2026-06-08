#!/usr/bin/env bash
set -Eeuo pipefail

cd "$(git rev-parse --show-toplevel)"

echo "=== Dealix Company Day ==="
date -u +"%Y-%m-%dT%H:%M:%SZ"

echo ""
echo "1) Production health"
if [ -x ./scripts/dealix_prod_check.sh ]; then
  ./scripts/dealix_prod_check.sh || true
else
  echo "Missing dealix_prod_check.sh"
fi

echo ""
echo "2) Daily offer"
python company/scripts/daily_offer_generator.py

echo ""
echo "3) Founder business autopilot"
if [ -x ./scripts/dealix_founder_business_day.sh ]; then
  ./scripts/dealix_founder_business_day.sh || true
else
  echo "Founder Business OS is not merged yet or script is missing."
fi

echo ""
echo "4) Morning ops"
if [ -x ./scripts/dealix_morning_ops.sh ]; then
  ./scripts/dealix_morning_ops.sh || true
fi

echo ""
echo "5) CRM file"
test -f company/crm/pipeline.csv && echo "CRM pipeline exists"

echo ""
echo "DONE"
