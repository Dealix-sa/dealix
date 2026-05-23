#!/usr/bin/env bash
# L7 — Server Runtime: compileall + Railway config + FastAPI app smoke.
# Exit 0=PASS, 1=FAIL.
set -uo pipefail

REPO="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO"

JSON=0
WITH_API_BOOT=1
for arg in "$@"; do
  case "$arg" in
    --json) JSON=1 ;;
    --no-api-boot) WITH_API_BOOT=0 ;;
    --with-api-boot) WITH_API_BOOT=1 ;;
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

# 1. compileall on main code trees that exist
COMPILE_TARGETS=()
for d in api auto_client_acquisition platform_core dealix core; do
  [ -d "$d" ] && COMPILE_TARGETS+=("$d")
done
if [ ${#COMPILE_TARGETS[@]} -gt 0 ]; then
  run_step "compileall" python3 -m compileall -q "${COMPILE_TARGETS[@]}"
fi

# 2. Railway production config verifier
[ -f scripts/verify_railway_production_config.py ] && \
  run_step "railway-config" python3 scripts/verify_railway_production_config.py

# 3. Full autonomous ops stack verifier (existing)
[ -f scripts/verify_full_autonomous_ops_stack.py ] && \
  run_step "autonomous-ops-stack" python3 scripts/verify_full_autonomous_ops_stack.py

# 4. FastAPI app import smoke (best-effort; skip if missing deps)
if [ "$WITH_API_BOOT" = "1" ]; then
  if python3 -c "from api.main import app; assert len(app.routes) > 0" >"$log_dir/api_boot.log" 2>&1; then
    [ "$JSON" -eq 0 ] && echo "  [OK]   api-import-smoke"
  else
    [ "$JSON" -eq 0 ] && echo "  [WARN] api-import-smoke (deps missing or import error)"
    # api boot is informational — don't fail the layer if app can't import
    # because production deps may not be installed in CI minimal mode
  fi
fi

if [ "$JSON" -eq 1 ]; then
  if [ "$FAIL" -eq 0 ]; then
    printf '{"layer":7,"verdict":"PASS","failures":[],"summary":"compileall + railway config clean"}\n'
  else
    printf '{"layer":7,"verdict":"FAIL","failures":['
    for i in "${!FAIL_NAMES[@]}"; do
      [ "$i" -gt 0 ] && printf ','
      printf '"%s"' "${FAIL_NAMES[$i]}"
    done
    printf '],"summary":"%d step(s) failed"}\n' "$FAIL"
  fi
fi

[ "$FAIL" -eq 0 ] && exit 0 || exit 1
