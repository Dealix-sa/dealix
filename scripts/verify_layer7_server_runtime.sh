#!/usr/bin/env bash
# L7 — Server Runtime: compileall is hard; Railway + autonomous-ops + API boot advisory.
# Exit 0=PASS, 1=FAIL on hard, 2=PARTIAL on advisory warns.
set -uo pipefail

REPO="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO"

JSON=0
WITH_API_BOOT=1
STRICT="${DEALIX_STRICT_SERVER:-0}"
for arg in "$@"; do
  case "$arg" in
    --json) JSON=1 ;;
    --no-api-boot) WITH_API_BOOT=0 ;;
    --with-api-boot) WITH_API_BOOT=1 ;;
    --strict) STRICT=1 ;;
    --private-ops) shift; shift ;;
    --private-ops=*) ;;
  esac
done

FAIL=0; WARN=0
FAIL_NAMES=(); WARN_NAMES=()
log_dir="$(mktemp -d)"
trap 'rm -rf "$log_dir"' EXIT

run_hard() {
  local name="$1"; shift
  local log="$log_dir/$name.log"
  if "$@" >"$log" 2>&1; then
    [ "$JSON" -eq 0 ] && echo "  [OK]   $name"
  else
    FAIL=$((FAIL+1)); FAIL_NAMES+=("$name")
    [ "$JSON" -eq 0 ] && { echo "  [FAIL] $name"; tail -5 "$log" | sed 's/^/        /'; }
  fi
}

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

# Hard: compileall on main code trees that exist (same as ci.yml line 28 + extras)
COMPILE_TARGETS=()
for d in api auto_client_acquisition platform_core dealix core; do
  [ -d "$d" ] && COMPILE_TARGETS+=("$d")
done
if [ ${#COMPILE_TARGETS[@]} -gt 0 ]; then
  run_hard "compileall" python3 -m compileall -q "${COMPILE_TARGETS[@]}"
fi

# Advisory: Railway production config verifier (needs prod env vars)
[ -f scripts/verify_railway_production_config.py ] && \
  run_advisory "railway-config" python3 scripts/verify_railway_production_config.py

# Advisory: full autonomous ops stack verifier
[ -f scripts/verify_full_autonomous_ops_stack.py ] && \
  run_advisory "autonomous-ops-stack" python3 scripts/verify_full_autonomous_ops_stack.py

# Advisory: FastAPI app boot smoke (may fail without runtime env)
if [ "$WITH_API_BOOT" = "1" ]; then
  export APP_ENV="${APP_ENV:-test}"
  run_advisory "api-import-smoke" python3 -c "from api.main import app; assert len(app.routes) > 0"
fi

EXIT=0; VERDICT="PASS"; SUMMARY="compileall clean"
if [ "$FAIL" -gt 0 ]; then
  EXIT=1; VERDICT="FAIL"; SUMMARY="$FAIL hard step(s) failed"
elif [ "$WARN" -gt 0 ]; then
  EXIT=2; VERDICT="PARTIAL"; SUMMARY="$WARN advisory step(s) warned"
fi

if [ "$JSON" -eq 1 ]; then
  printf '{"layer":7,"verdict":"%s","failures":[' "$VERDICT"
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
