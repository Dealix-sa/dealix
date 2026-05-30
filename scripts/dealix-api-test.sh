#!/usr/bin/env bash
set -euo pipefail

curl -s http://localhost:8787/builder/health | jq . || true

curl -s -X POST http://localhost:8787/builder/plan \
  -H "Content-Type: application/json" \
  -d '{"goal":"Build Dealix Growth OS v6 inside dealix-v2 only","constraints":["do not touch legacy repo","write tests","update CLI"]}' | jq . || true
