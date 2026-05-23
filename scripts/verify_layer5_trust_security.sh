#!/usr/bin/env bash
# L5 — Trust & Security: 8 doctrine tests + governance verifiers + secret sweep.
# Wraps tests/test_no_*.py + scripts/verify_governance*.py.
# Exit 0=PASS, 1=FAIL.
set -uo pipefail

REPO="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO"

JSON=0
for arg in "$@"; do
  case "$arg" in
    --json) JSON=1 ;;
    --private-ops) shift; shift ;;
    --private-ops=*) ;;
  esac
done

FAIL=0
FAIL_NAMES=()
log_dir="$(mktemp -d)"
trap 'rm -rf "$log_dir"' EXIT

run_step() {
  local name="$1"; shift
  local log="$log_dir/$name.log"
  if "$@" >"$log" 2>&1; then
    [ "$JSON" -eq 0 ] && echo "  [OK]   $name"
  else
    FAIL=$((FAIL+1))
    FAIL_NAMES+=("$name")
    [ "$JSON" -eq 0 ] && { echo "  [FAIL] $name"; tail -5 "$log" | sed 's/^/        /'; }
  fi
}

# 1. Eight doctrine tests + supporting
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
run_step "doctrine-tests" python3 -m pytest -q --no-cov "${DOCTRINE_TESTS[@]}"

# 2. Governance verifiers
[ -f scripts/verify_governance.py ] && run_step "verify-governance" python3 scripts/verify_governance.py
[ -f scripts/verify_governance_rules.py ] && run_step "verify-governance-rules" python3 scripts/verify_governance_rules.py

# 3. enforce_doctrine_non_negotiables import smoke
run_step "non-negotiables-import" python3 -c "from platform_core.governance import enforce_doctrine_non_negotiables; assert callable(enforce_doctrine_non_negotiables)"

# 4. Secret scan (same regex pattern as v10_master_verify.sh line ~104)
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

if [ "$JSON" -eq 1 ]; then
  if [ "$FAIL" -eq 0 ]; then
    printf '{"layer":5,"verdict":"PASS","failures":[],"summary":"doctrine + governance + secrets clean"}\n'
  else
    printf '{"layer":5,"verdict":"FAIL","failures":['
    for i in "${!FAIL_NAMES[@]}"; do
      [ "$i" -gt 0 ] && printf ','
      printf '"%s"' "${FAIL_NAMES[$i]}"
    done
    printf '],"summary":"%d step(s) failed"}\n' "$FAIL"
  fi
fi

[ "$FAIL" -eq 0 ] && exit 0 || exit 1
