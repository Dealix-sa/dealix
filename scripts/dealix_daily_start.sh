#!/usr/bin/env bash
set -euo pipefail

echo "=== Dealix Daily Start ==="
date

echo ""
echo "Git status"
git status --short

echo ""
echo "Latest commits"
git log --oneline -5

echo ""
echo "PR status"
gh pr status || true

echo ""
echo "Latest workflow runs"
gh run list --limit 10 || true

echo ""
echo "Production smoke via Railway variables"
railway run python scripts/check_openapi_contract.py || true

echo ""
echo "CEO Command Center"
test -f ops/daily/CEO_DAILY_COMMAND_CENTER.md && echo "OK"
