#!/usr/bin/env bash
# L2 — Code Health: matches what .github/workflows/ci.yml actually enforces.
#
# Hard checks (exit 1 on failure):
#   - compileall on api auto_client_acquisition (same as CI line 28)
#   - alembic single head (CI line 31)
#
# Advisory checks (exit 2 / WARN — surface lint debt without blocking):
#   - make lint (ruff + black)
#   - make type-check (mypy)
#   - make security (bandit + detect-secrets)
#
# Set DEALIX_STRICT_LINT=1 to promote advisory checks to hard failures.
# Set DEALIX_SKIP_RUFF=1 / DEALIX_SKIP_MYPY=1 to skip advisory blocks.

set -uo pipefail

REPO="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO"

JSON=0
SKIP_MYPY="${DEALIX_SKIP_MYPY:-0}"
STRICT="${DEALIX_STRICT_LINT:-0}"
for arg in "$@"; do
  case "$arg" in
    --json) JSON=1 ;;
    --skip-mypy) SKIP_MYPY=1 ;;
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
    [ "$JSON" -eq 0 ] && { echo "  [FAIL] $name (strict mode)"; tail -3 "$log" | sed 's/^/        /'; }
  else
    WARN=$((WARN+1))
    WARN_NAMES+=("$name")
    [ "$JSON" -eq 0 ] && echo "  [WARN] $name (advisory; use --strict to enforce)"
  fi
}

# Hard: compile-check (subset; full compileall is in L7)
COMPILE_TARGETS=()
for d in api auto_client_acquisition; do
  [ -d "$d" ] && COMPILE_TARGETS+=("$d")
done
if [ ${#COMPILE_TARGETS[@]} -gt 0 ]; then
  run_hard "compileall-quick" python3 -m compileall -q "${COMPILE_TARGETS[@]}"
fi

# Hard: alembic single head
[ -f scripts/check_alembic_single_head.py ] && \
  run_hard "alembic-single-head" python3 scripts/check_alembic_single_head.py

# Advisory: lint
if [ "${DEALIX_SKIP_RUFF:-0}" = "1" ]; then
  [ "$JSON" -eq 0 ] && echo "  [SKIP] lint (DEALIX_SKIP_RUFF=1)"
else
  run_advisory "lint" make lint
fi

# Advisory: type-check
if [ "$SKIP_MYPY" = "1" ]; then
  [ "$JSON" -eq 0 ] && echo "  [SKIP] type-check (DEALIX_SKIP_MYPY=1)"
else
  run_advisory "type-check" make type-check
fi

# Advisory: security (bandit + detect-secrets)
run_advisory "security" make security

# Decide exit + verdict
EXIT=0; VERDICT="PASS"; SUMMARY="compileall + alembic clean"
if [ "$FAIL" -gt 0 ]; then
  EXIT=1; VERDICT="FAIL"; SUMMARY="$FAIL hard step(s) failed"
elif [ "$WARN" -gt 0 ]; then
  EXIT=2; VERDICT="PARTIAL"; SUMMARY="$WARN advisory step(s) warned"
fi

if [ "$JSON" -eq 1 ]; then
  printf '{"layer":2,"verdict":"%s","failures":[' "$VERDICT"
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
