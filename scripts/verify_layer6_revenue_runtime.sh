#!/usr/bin/env bash
# L6 — Revenue Runtime: all checks are advisory (not in main CI).
# This layer surfaces revenue-OS signal without blocking merge.
# Exit 0=PASS, 1=FAIL (only in --strict), 2=PARTIAL on advisory warns.
set -uo pipefail

REPO="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO"

JSON=0
STRICT="${DEALIX_STRICT_REVENUE:-0}"
for arg in "$@"; do
  case "$arg" in
    --json) JSON=1 ;;
    --strict) STRICT=1 ;;
    --private-ops) shift; shift ;;
    --private-ops=*) ;;
  esac
done

FAIL=0; WARN=0
FAIL_NAMES=(); WARN_NAMES=()
log_dir="$(mktemp -d)"
trap 'rm -rf "$log_dir"' EXIT

run_advisory() {
  local name="$1"; shift
  local log="$log_dir/$name.log"
  if "$@" >"$log" 2>&1; then
    [ "$JSON" -eq 0 ] && echo "  [OK]   $name"
  elif [ "$STRICT" = "1" ]; then
    FAIL=$((FAIL+1)); FAIL_NAMES+=("$name")
    [ "$JSON" -eq 0 ] && { echo "  [FAIL] $name (strict)"; tail -3 "$log" | sed 's/^/        /'; }
  else
    WARN=$((WARN+1)); WARN_NAMES+=("$name")
    [ "$JSON" -eq 0 ] && echo "  [WARN] $name (advisory)"
  fi
}

# All revenue-os checks are advisory — none enforced in .github/workflows/ci.yml
[ -f scripts/revenue_os_master_verify.sh ] && \
  run_advisory "revenue-os-master" bash scripts/revenue_os_master_verify.sh
[ -f scripts/verify_proof_pack.py ] && \
  run_advisory "verify-proof-pack" python3 scripts/verify_proof_pack.py
[ -f scripts/verify_quality_score.py ] && \
  run_advisory "verify-quality-score" python3 scripts/verify_quality_score.py

EXIT=0; VERDICT="PASS"; SUMMARY="revenue OS clean"
if [ "$FAIL" -gt 0 ]; then
  EXIT=1; VERDICT="FAIL"; SUMMARY="$FAIL hard step(s) failed (strict mode)"
elif [ "$WARN" -gt 0 ]; then
  EXIT=2; VERDICT="PARTIAL"; SUMMARY="$WARN advisory step(s) warned"
fi

if [ "$JSON" -eq 1 ]; then
  printf '{"layer":6,"verdict":"%s","failures":[' "$VERDICT"
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
