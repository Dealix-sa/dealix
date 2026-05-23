#!/usr/bin/env bash
# L5 — Trust & Security: doctrine tests + secret sweep (hard).
# Governance verifiers are advisory (not enforced in main CI).
# Exit 0=PASS, 1=FAIL, 2=PARTIAL (only advisory warns).
set -uo pipefail

REPO="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO"

JSON=0
STRICT="${DEALIX_STRICT_TRUST:-0}"
for arg in "$@"; do
  case "$arg" in
    --json) JSON=1 ;;
    --strict) STRICT=1 ;;
    --private-ops) shift; shift ;;
    --private-ops=*) ;;
  esac
done

FAIL=0
WARN=0
FAIL_NAMES=()
WARN_NAMES=()
log_dir="$(mktemp -d)"
trap 'rm -rf "$log_dir"' EXIT

run_hard() {
  local name="$1"; shift
  local log="$log_dir/$name.log"
  if "$@" >"$log" 2>&1; then
    [ "$JSON" -eq 0 ] && echo "  [OK]   $name"
  else
    FAIL=$((FAIL+1))
    FAIL_NAMES+=("$name")
    {
      echo "[FAIL] $name"
      tail -40 "$log" | sed 's/^/  /'
    } >&2
    [ "$JSON" -eq 0 ] && { echo "  [FAIL] $name"; tail -5 "$log" | sed 's/^/        /'; }
  fi
}

run_advisory() {
  local name="$1"; shift
  local log="$log_dir/$name.log"
  if "$@" >"$log" 2>&1; then
    [ "$JSON" -eq 0 ] && echo "  [OK]   $name"
  elif [ "$STRICT" = "1" ]; then
    FAIL=$((FAIL+1))
    FAIL_NAMES+=("$name")
    [ "$JSON" -eq 0 ] && { echo "  [FAIL] $name (strict)"; tail -3 "$log" | sed 's/^/        /'; }
  else
    WARN=$((WARN+1))
    WARN_NAMES+=("$name")
    [ "$JSON" -eq 0 ] && echo "  [WARN] $name (advisory)"
  fi
}

# Hard: doctrine tests + supporting tests (these must always pass)
DOCTRINE_TESTS=(
  tests/test_no_scraping_engine.py
  tests/test_no_cold_whatsapp.py
  tests/test_no_linkedin_automation.py
  tests/test_no_linkedin_scraper_string_anywhere.py
  tests/test_no_pii_in_logs.py
  tests/test_no_guaranteed_claims.py
  tests/test_no_source_passport_no_ai.py
  tests/test_no_source_no_answer.py
  tests/test_doctrine_guardrails.py
  tests/test_landing_forbidden_claims.py
)
export APP_ENV="${APP_ENV:-test}"
run_hard "doctrine-tests" python3 -m pytest -q --no-cov "${DOCTRINE_TESTS[@]}"

# Hard: 11 non-negotiables function present
run_hard "non-negotiables-import" python3 -c "from platform_core.governance import enforce_doctrine_non_negotiables; assert callable(enforce_doctrine_non_negotiables)"

# Hard: secret sweep (mirrors v10_master_verify.sh:104)
SECRET_HITS=$(grep -rE 'sk_live_[A-Za-z0-9]{20,}|ghp_[A-Za-z0-9]{36}|AIza[A-Za-z0-9]{35}' \
  --include='*.py' --include='*.md' . 2>/dev/null \
  | grep -vE 'test_|sk_live_test|EXAMPLE|sk_live_REALDANGEROUSKEYSECRET|sk_live_xxxxx|sk_live_should_|placeholder|sk_live_unsigned|sk_live_REPLACE_ME' \
  | head -1)
if [ -z "$SECRET_HITS" ]; then
  [ "$JSON" -eq 0 ] && echo "  [OK]   secret-scan"
else
  FAIL=$((FAIL+1))
  FAIL_NAMES+=("secret-scan")
  [ "$JSON" -eq 0 ] && echo "  [FAIL] secret-scan: $SECRET_HITS"
fi

# Advisory: existing governance verifiers (not part of main CI)
[ -f scripts/verify_governance.py ] && run_advisory "verify-governance" python3 scripts/verify_governance.py
[ -f scripts/verify_governance_rules.py ] && run_advisory "verify-governance-rules" python3 scripts/verify_governance_rules.py

EXIT=0; VERDICT="PASS"; SUMMARY="doctrine + secret-scan clean"
if [ "$FAIL" -gt 0 ]; then
  EXIT=1; VERDICT="FAIL"; SUMMARY="$FAIL hard step(s) failed"
elif [ "$WARN" -gt 0 ]; then
  EXIT=2; VERDICT="PARTIAL"; SUMMARY="$WARN advisory step(s) warned"
fi

if [ "$JSON" -eq 1 ]; then
  printf '{"layer":5,"verdict":"%s","failures":[' "$VERDICT"
  for i in "${!FAIL_NAMES[@]}"; do
    [ "$i" -gt 0 ] && printf ','
    printf '"%s"' "${FAIL_NAMES[$i]}"
  done
  printf '],"warnings":['
  for i in "${!WARN_NAMES[@]}"; do
    [ "$i" -gt 0 ] && printf ','
    printf '"%s"' "${WARN_NAMES[$i]}"
  done
  printf '],"summary":"%s"}\n' "$SUMMARY"
fi

exit "$EXIT"
