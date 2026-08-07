#!/usr/bin/env bash
set -Eeuo pipefail

cd "$(git rev-parse --show-toplevel)"

export DEALIX_API_URL="${DEALIX_API_URL:-https://api.dealix.me}"

echo "=== Dealix Morning Ops ==="
date -u +"%Y-%m-%dT%H:%M:%SZ"

echo ""
echo "1) Production API"
./scripts/dealix_prod_check.sh

echo ""
echo "2) GitHub Actions"
gh run list --branch main --limit 10 || true

echo ""
echo "3) Railway"
railway status || true

echo ""
echo "4) Daily CEO Command Center"
if [ -f ops/daily/CEO_DAILY_COMMAND_CENTER.md ]; then
  sed -n '1,120p' ops/daily/CEO_DAILY_COMMAND_CENTER.md
else
  echo "Missing ops/daily/CEO_DAILY_COMMAND_CENTER.md"
fi

echo ""
echo "DONE"
