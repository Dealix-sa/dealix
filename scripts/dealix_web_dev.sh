#!/usr/bin/env bash
set -Eeuo pipefail

cd "$(git rev-parse --show-toplevel)/apps/web"

rm -rf .next
npm install
npm run verify

echo ""
echo "Starting web on http://localhost:3100"
npm run dev
