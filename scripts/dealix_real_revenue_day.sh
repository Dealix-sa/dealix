#!/usr/bin/env bash
set -eo pipefail

cd "$(git rev-parse --show-toplevel)"

echo "=== Dealix Real Revenue Day ==="
date -u +"%Y-%m-%dT%H:%M:%SZ"

echo ""
echo "1) Real Places Leads"
python company/leads/real_leads_engine.py || true

echo ""
echo "2) Revenue Day"
./scripts/dealix_revenue_day.sh

TODAY="$(date +%F)"
echo ""
echo "FILES:"
echo "company/runtime/places/${TODAY}/REAL_LEADS_REPORT.md"
echo "company/runtime/places/${TODAY}/real_leads.csv"
echo "company/runtime/revenue/${TODAY}/CEO_REVENUE_REPORT.md"
echo "company/runtime/revenue/${TODAY}/WHATSAPP_DRAFTS.md"
