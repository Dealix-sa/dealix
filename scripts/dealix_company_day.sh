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
  echo "Missing production check."
fi

echo ""
echo "2) Secret-aware company day"
if [ -x ./scripts/dealix_secret_aware_company_day.sh ]; then
  ./scripts/dealix_secret_aware_company_day.sh
else
  echo "Legacy secret-aware runner is not present on the canonical branch."
  echo "Continuing the internal draft-only company day; external execution remains disabled."
fi

echo ""
echo "3) CRM"
test -f company/crm/pipeline.csv || cat > company/crm/pipeline.csv <<'CSV'
date,company,sector,contact,phone,email,source,offer,status,next_action,next_followup_date,deal_value_sar,probability,notes
CSV
echo "CRM ready: company/crm/pipeline.csv"

echo ""
echo "DONE"
