#!/usr/bin/env bash
set -Eeuo pipefail

cd "$(git rev-parse --show-toplevel)/apps/web"

rm -rf .next
npm install
npm run verify

echo "Frontend verified. To run locally:"
echo "cd apps/web && npm run dev"
