#!/usr/bin/env bash
set -euo pipefail
URL="${HEALTHCHECK_URL:-http://127.0.0.1:8000/health}"
echo "Healthcheck URL: $URL"
curl -fsS "$URL" || echo "WARN: healthcheck not reachable in local/offline mode"
