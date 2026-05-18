#!/usr/bin/env bash
# Founder production probe — verify_railway_production_config + curl healthz/version/meta
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

API_BASE="${DEALIX_API_BASE:-https://api.dealix.me}"
PY="$(command -v python3 2>/dev/null || true)"
[[ -z "$PY" ]] && command -v py >/dev/null 2>&1 && PY="py -3"

ARGS=(scripts/verify_railway_production_config.py --api-base "$API_BASE")
[[ "${SKIP_LIVE:-}" == "1" ]] && ARGS+=(--skip-live)

echo "== verify_railway_production_config =="
$PY "${ARGS[@]}"
RC=$?

if [[ "${SKIP_LIVE:-}" != "1" ]]; then
  echo ""
  echo "== curl probes =="
  for path in /healthz /version /api/v1/meta; do
    echo "  GET ${API_BASE}${path}"
    curl -fsS "${API_BASE}${path}" && echo "" || echo "    FAIL"
  done
fi

echo "FOUNDER_PRODUCTION_PROBE_RC=$RC"
exit "$RC"
