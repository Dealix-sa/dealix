#!/usr/bin/env bash
set -Eeuo pipefail

cd "$(git rev-parse --show-toplevel)/apps/web"

rm -rf .next
npm install
npm run typecheck
npm run build

echo ""
echo "Start dev server:"
echo "cd apps/web && npm run dev"
