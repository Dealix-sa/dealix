#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
# dealix_integration_wave.sh
#
# Runs the canonical gate bundle for a resource integration wave. Use it on an
# integration branch BEFORE opening / merging a promotion PR.
#
# It runs read-only checks and the canonical make gates. It does not push, deploy,
# or send anything.
# ─────────────────────────────────────────────────────────────────────────────
set -euo pipefail
ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"

echo "== Dealix Integration Wave =="
echo "1) Current branch: $(git branch --show-current)"
echo ""

echo "2) Uploaded resource review"
if [ -x scripts/compare_uploaded_resources.sh ]; then
  ./scripts/compare_uploaded_resources.sh || true
else
  echo "   (scripts/compare_uploaded_resources.sh missing or not executable)"
fi
echo ""

echo "3) Core gates"
make doctor
make env-check
make security-smoke
make api-contract-check
make test
make prod-verify
echo ""

echo "4) Web gates"
if [ -d apps/web ]; then
  ( cd apps/web
    if [ -f package-lock.json ]; then npm ci; else npm install; fi
    if npm run 2>/dev/null | grep -q '  verify'; then npm run verify; else npm run build; fi
  )
else
  echo "   (apps/web not present — skipping)"
fi
echo ""

echo "== Integration wave complete =="
