#!/usr/bin/env bash
set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
REPORT_DIR="$ROOT/reports/runtime/full_repo_test_matrix"
LOG_DIR="$REPORT_DIR/logs-$STAMP"
MD_REPORT="$REPORT_DIR/latest.md"
JSON_REPORT="$REPORT_DIR/latest.json"

mkdir -p "$LOG_DIR"
cd "$ROOT" || exit 1

export APP_ENV="${APP_ENV:-test}"
export ENVIRONMENT="${ENVIRONMENT:-test}"
export PYTHONIOENCODING="${PYTHONIOENCODING:-utf-8}"
export DATABASE_URL="${DATABASE_URL:-sqlite+aiosqlite:///./dealix_local_test.db}"
export APP_SECRET_KEY="${APP_SECRET_KEY:-local-test-secret-change-me}"
export JWT_SECRET_KEY="${JWT_SECRET_KEY:-local-jwt-secret-change-me}"
export EXTERNAL_SEND_ENABLED="${EXTERNAL_SEND_ENABLED:-false}"
export EMAIL_SEND_ENABLED="${EMAIL_SEND_ENABLED:-false}"
export WHATSAPP_SEND_ENABLED="${WHATSAPP_SEND_ENABLED:-false}"
export WHATSAPP_ALLOW_LIVE_SEND="${WHATSAPP_ALLOW_LIVE_SEND:-false}"
export SMS_SEND_ENABLED="${SMS_SEND_ENABLED:-false}"
export OUTBOUND_MODE="${OUTBOUND_MODE:-draft_only}"

TOTAL=0
PASSED=0
FAILED=0
SKIPPED=0
RESULTS=()

json_escape() {
  python3 -c 'import json,sys; print(json.dumps(sys.stdin.read())[1:-1])'
}

run_step() {
  local name="$1"
  local required="$2"
  shift 2
  local slug
  slug="$(echo "$name" | tr '[:upper:]' '[:lower:]' | tr -cs 'a-z0-9' '-' | sed 's/^-//;s/-$//')"
  local log="$LOG_DIR/${slug}.log"

  TOTAL=$((TOTAL + 1))
  echo "=== RUN: $name ==="
  echo "Command: $*" > "$log"
  echo >> "$log"

  if "$@" >> "$log" 2>&1; then
    PASSED=$((PASSED + 1))
    RESULTS+=("PASS|$required|$name|$log")
    echo "PASS: $name"
  else
    local status=$?
    if [[ "$required" == "optional" ]]; then
      SKIPPED=$((SKIPPED + 1))
      RESULTS+=("SKIP|$required|$name|$log")
      echo "SKIP: $name (optional failed, see log)"
    else
      FAILED=$((FAILED + 1))
      RESULTS+=("FAIL|$required|$name|$log")
      echo "FAIL: $name (exit=$status, see log)"
    fi
  fi
}

run_step "python-version" required python3 --version
run_step "python-compileall-core-surfaces" required python3 -m compileall -q api app core db dealix scripts
run_step "env-contract" required python3 scripts/check_env_contract.py
run_step "security-smoke" required python3 scripts/ops/security_smoke_ci.py
run_step "no-auto-external-send" required python3 scripts/verify_no_auto_external_send.py
run_step "company-launch-ready" required python3 scripts/verify_company_launch_ready.py
run_step "pytest-full-suite" required python3 -m pytest -q
run_step "launch-os-dry-runs" optional make launch-all-dry-runs
run_step "production-verify-bundle" optional make prod-verify

if [[ -f "apps/web/package.json" ]]; then
  if [[ -f "apps/web/package-lock.json" ]]; then
    run_step "apps-web-npm-ci" required npm --prefix apps/web ci
  else
    run_step "apps-web-npm-install" required npm --prefix apps/web install
  fi
  run_step "apps-web-verify" required npm --prefix apps/web run verify
else
  TOTAL=$((TOTAL + 1))
  SKIPPED=$((SKIPPED + 1))
  RESULTS+=("SKIP|optional|apps-web-verify|missing apps/web/package.json")
  echo "SKIP: apps-web-verify (missing apps/web/package.json)"
fi

run_step "testsprite-env-check" optional python3 scripts/ops/check_testsprite_mcp_env.py

if [[ -n "${TESTSPRITE_API_KEY:-}" ]]; then
  run_step "testsprite-mcp-smoke" optional bash scripts/ops/run_testsprite_mcp_smoke.sh
else
  TOTAL=$((TOTAL + 1))
  SKIPPED=$((SKIPPED + 1))
  RESULTS+=("SKIP|optional|testsprite-mcp-smoke|TESTSPRITE_API_KEY missing")
  echo "SKIP: testsprite-mcp-smoke (TESTSPRITE_API_KEY missing)"
fi

{
  echo "# Dealix Full Repo Test Matrix"
  echo
  echo "- Timestamp UTC: $STAMP"
  echo "- Root: $ROOT"
  echo "- Total steps: $TOTAL"
  echo "- Passed: $PASSED"
  echo "- Failed: $FAILED"
  echo "- Skipped/optional failures: $SKIPPED"
  echo "- Safety mode: EXTERNAL_SEND_ENABLED=$EXTERNAL_SEND_ENABLED, OUTBOUND_MODE=$OUTBOUND_MODE"
  echo
  echo "## Results"
  echo
  echo "| Status | Required | Step | Log |"
  echo "|---|---|---|---|"
  for item in "${RESULTS[@]}"; do
    IFS='|' read -r status required name log <<< "$item"
    if [[ "$log" == /* ]]; then
      rel="${log#$ROOT/}"
    else
      rel="$log"
    fi
    echo "| $status | $required | $name | $rel |"
  done
} > "$MD_REPORT"

{
  echo "{"
  echo "  \"timestamp_utc\": \"$STAMP\","
  echo "  \"total\": $TOTAL,"
  echo "  \"passed\": $PASSED,"
  echo "  \"failed\": $FAILED,"
  echo "  \"skipped\": $SKIPPED,"
  echo "  \"safety\": {"
  echo "    \"external_send_enabled\": \"$EXTERNAL_SEND_ENABLED\","
  echo "    \"outbound_mode\": \"$OUTBOUND_MODE\""
  echo "  },"
  echo "  \"results\": ["
  first=1
  for item in "${RESULTS[@]}"; do
    IFS='|' read -r status required name log <<< "$item"
    esc_name="$(printf '%s' "$name" | json_escape)"
    esc_log="$(printf '%s' "$log" | json_escape)"
    if [[ $first -eq 0 ]]; then echo ","; fi
    first=0
    printf '    {"status":"%s","required":"%s","step":"%s","log":"%s"}' "$status" "$required" "$esc_name" "$esc_log"
  done
  echo
  echo "  ]"
  echo "}"
} > "$JSON_REPORT"

echo
echo "FULL_REPO_TEST_MATRIX_REPORT=$MD_REPORT"
echo "FULL_REPO_TEST_MATRIX_JSON=$JSON_REPORT"

if [[ "$FAILED" -gt 0 ]]; then
  echo "FULL_REPO_TEST_MATRIX=FAIL"
  exit 1
fi

echo "FULL_REPO_TEST_MATRIX=PASS"
exit 0
