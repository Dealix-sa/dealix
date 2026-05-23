#!/usr/bin/env bash
# L4 — Prompt / Output Quality: evals + landing forbidden-claims.
# Both are enforced in main CI; treat both as hard.
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

run_hard() {
  local name="$1"; shift
  local log="$log_dir/$name.log"
  if "$@" >"$log" 2>&1; then
    [ "$JSON" -eq 0 ] && echo "  [OK]   $name"
  else
    FAIL=$((FAIL+1)); FAIL_NAMES+=("$name")
    # Always emit log tail to stderr so the master orchestrator can surface it
    {
      echo "[FAIL] $name"
      tail -40 "$log" | sed 's/^/  /'
    } >&2
    [ "$JSON" -eq 0 ] && { echo "  [FAIL] $name"; tail -5 "$log" | sed 's/^/        /'; }
  fi
}

# CI uses these env-var defaults for tests
export APP_ENV="${APP_ENV:-test}"
export APP_DEBUG="${APP_DEBUG:-false}"
export ANTHROPIC_API_KEY="${ANTHROPIC_API_KEY:-test-anthropic-key}"
export DEEPSEEK_API_KEY="${DEEPSEEK_API_KEY:-test-deepseek-key}"
export GROQ_API_KEY="${GROQ_API_KEY:-test-groq-key}"
export GLM_API_KEY="${GLM_API_KEY:-test-glm-key}"
export GOOGLE_API_KEY="${GOOGLE_API_KEY:-test-google-key}"

# Hard: deterministic eval smoke (same as ci.yml line 106)
if [ -n "$SUITE" ]; then
  run_hard "evals-$SUITE" python3 scripts/run_evals.py --suite "$SUITE"
else
  run_hard "evals-all" python3 scripts/run_evals.py
fi

# Hard: forbidden claims regression
run_hard "landing-forbidden-claims" python3 -m pytest -q --no-cov tests/test_landing_forbidden_claims.py

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
