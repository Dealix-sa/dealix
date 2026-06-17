#!/usr/bin/env bash
set -euo pipefail
mkdir -p reports/server
python3 scripts/server/server_preflight.py 2>&1 | tee reports/server/preflight.log || true
bash scripts/server/server_healthcheck.sh 2>&1 | tee reports/server/healthcheck.log || true
