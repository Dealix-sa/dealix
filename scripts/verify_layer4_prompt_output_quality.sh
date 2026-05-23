#!/usr/bin/env bash
# L4 — Prompt / Output Quality: runs evals + landing forbidden-claims test.
# Wraps scripts/run_evals.py + tests/test_landing_forbidden_claims.py.
# Exit 0=PASS, 1=FAIL.
set -uo pipefail

REPO="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO"

JSON=0
SUITE=""
for arg in "$@"; do
  case "$arg" in
    --json) JSON=1 ;;
    --suite) shift; SUITE="$1"; shift ;;
    --suite=*) SUITE="${arg#*=}" ;;
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

# 1. Evals (5 YAML suites). Pass --suite if requested.
if [ -n "$SUITE" ]; then
  run_step "evals-$SUITE" python3 scripts/run_evals.py --suite "$SUITE"
else
  run_step "evals-all" python3 scripts/run_evals.py
fi

# 2. Forbidden claims regression
run_step "landing-forbidden-claims" python3 -m pytest -q --no-cov tests/test_landing_forbidden_claims.py

# 3. Decision output contract test (auto-skip if absent)
if [ -f tests/test_decision_output_contract.py ]; then
  run_step "decision-output-contract" python3 -m pytest -q --no-cov tests/test_decision_output_contract.py
fi

if [ "$JSON" -eq 1 ]; then
  if [ "$FAIL" -eq 0 ]; then
    printf '{"layer":4,"verdict":"PASS","failures":[],"summary":"evals + forbidden-claims clean"}\n'
  else
    printf '{"layer":4,"verdict":"FAIL","failures":['
    for i in "${!FAIL_NAMES[@]}"; do
      [ "$i" -gt 0 ] && printf ','
      printf '"%s"' "${FAIL_NAMES[$i]}"
    done
    printf '],"summary":"%d step(s) failed"}\n' "$FAIL"
  fi
fi

[ "$FAIL" -eq 0 ] && exit 0 || exit 1
