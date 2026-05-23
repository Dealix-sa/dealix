#!/usr/bin/env bash
# L6 — Revenue Runtime: wraps revenue_os_master_verify.sh + proof pack + quality score.
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

# 1. Revenue OS master verifier
if [ -x scripts/revenue_os_master_verify.sh ] || [ -f scripts/revenue_os_master_verify.sh ]; then
  run_step "revenue-os-master" bash scripts/revenue_os_master_verify.sh
else
  FAIL=$((FAIL+1))
  FAIL_NAMES+=("revenue-os-master-missing")
  [ "$JSON" -eq 0 ] && echo "  [FAIL] revenue-os-master-missing"
fi

# 2. Proof pack validator
[ -f scripts/verify_proof_pack.py ] && run_step "verify-proof-pack" python3 scripts/verify_proof_pack.py

# 3. Quality score validator
[ -f scripts/verify_quality_score.py ] && run_step "verify-quality-score" python3 scripts/verify_quality_score.py

if [ "$JSON" -eq 1 ]; then
  if [ "$FAIL" -eq 0 ]; then
    printf '{"layer":6,"verdict":"PASS","failures":[],"summary":"revenue OS + proof + quality clean"}\n'
  else
    printf '{"layer":6,"verdict":"FAIL","failures":['
    for i in "${!FAIL_NAMES[@]}"; do
      [ "$i" -gt 0 ] && printf ','
      printf '"%s"' "${FAIL_NAMES[$i]}"
    done
    printf '],"summary":"%d step(s) failed"}\n' "$FAIL"
  fi
fi

[ "$FAIL" -eq 0 ] && exit 0 || exit 1
