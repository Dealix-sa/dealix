#!/usr/bin/env bash
set -Eeuo pipefail

API_URL="${DEALIX_API_URL:-https://api.dealix.me}"

echo "Checking Dealix production: $API_URL"

curl -fsS "$API_URL/healthz" >/tmp/dealix_healthz.json
echo "healthz OK"

curl -fsS "$API_URL/health" >/tmp/dealix_health.json
echo "health OK"

curl -fsS "$API_URL/version" >/tmp/dealix_version.json
echo "version OK"

curl -fsS "$API_URL/api/v1/meta" >/tmp/dealix_meta.json
echo "meta OK"

curl -fsS "$API_URL/api/v1/pricing/plans" >/tmp/dealix_pricing.json
echo "pricing OK"

echo "PASS"
