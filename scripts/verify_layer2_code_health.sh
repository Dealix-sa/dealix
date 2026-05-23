#!/usr/bin/env bash
# L2 — Code Health: lint + type-check + security + alembic single-head.
# Wraps existing Makefile targets. Exit 0=PASS, 1=FAIL.
set -uo pipefail

REPO="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO"

JSON=0
SKIP_MYPY="${DEALIX_SKIP_MYPY:-0}"
for arg in "$@"; do
  case "$arg" in
    --json) JSON=1 ;;
    --skip-mypy) SKIP_MYPY=1 ;;
    --private-ops) shift; shift ;;  # ignored at L2
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

# 1. ruff + black (via make lint)
if [ "${DEALIX_SKIP_RUFF:-0}" = "1" ]; then
  [ "$JSON" -eq 0 ] && echo "  [SKIP] lint (DEALIX_SKIP_RUFF=1)"
else
  run_step "lint" make lint
fi

# 2. mypy
if [ "$SKIP_MYPY" = "1" ]; then
  [ "$JSON" -eq 0 ] && echo "  [SKIP] type-check"
else
  run_step "type-check" make type-check
fi

# 3. security scans (bandit + detect-secrets)
run_step "security" make security

# 4. alembic single head
run_step "alembic-single-head" python3 scripts/check_alembic_single_head.py

if [ "$JSON" -eq 1 ]; then
  if [ "$FAIL" -eq 0 ]; then
    printf '{"layer":2,"verdict":"PASS","failures":[],"summary":"lint+type+security+alembic clean"}\n'
  else
    printf '{"layer":2,"verdict":"FAIL","failures":['
    for i in "${!FAIL_NAMES[@]}"; do
      [ "$i" -gt 0 ] && printf ','
      printf '"%s"' "${FAIL_NAMES[$i]}"
    done
    printf '],"summary":"%d step(s) failed"}\n' "$FAIL"
  fi
fi

[ "$FAIL" -eq 0 ] && exit 0 || exit 1
