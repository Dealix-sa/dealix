#!/usr/bin/env bash
# =============================================================================
# Dealix Close-Now — Founder Private-Launch Verification
# Owner: Founder | Audience: Founder-operator | Arabic-first project
# =============================================================================
# Usage:
#   bash scripts/dealix_close_now.sh                         # core gates + health smoke (fast)
#   DEALIX_CLOSE_FULL=1 bash scripts/dealix_close_now.sh     # + web build + docker build
#   PRODUCTION_BASE_URL=https://api.example bash scripts/dealix_close_now.sh   # + prod smoke
#
# Purpose:
#   One read-only command that runs the canonical verification gates and reports
#   a single PRIVATE-LAUNCH verdict. It does NOT deploy, NOT send any message,
#   NOT charge any customer, and NOT print secrets. Heavy build steps (web,
#   docker) are opt-in via DEALIX_CLOSE_FULL=1 to keep the default run fast.
#
# Relationship to other verifiers (avoid duplication):
#   - `make prod-verify` is the canonical production-readiness bundle (called here).
#   - `scripts/official_launch_verify.sh` is the deeper soft -> production gate.
#   This script is the founder convenience wrapper around the make gates + health.
#
# Doctrine: honors the 11 non-negotiables — no live send, no live charge,
#   no scraping, no cold WhatsApp, no fake proof. Verification only.
# v1: initial close-now runner.
# =============================================================================
set -uo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

# ---- output helpers ---------------------------------------------------------
if [[ -t 1 ]]; then
  GREEN=$'\033[0;32m'; RED=$'\033[0;31m'; YELLOW=$'\033[0;33m'
  BLUE=$'\033[0;34m'; BOLD=$'\033[1m'; NC=$'\033[0m'
else
  GREEN=""; RED=""; YELLOW=""; BLUE=""; BOLD=""; NC=""
fi

PASS=0; FAIL=0; SKIP=0
declare -a FAILED_GATES=()

section() { printf '\n%s== %s ==%s\n' "$BLUE" "$1" "$NC"; }
pass()    { printf '%s  PASS%s  %s\n' "$GREEN" "$NC" "$1"; PASS=$((PASS+1)); }
fail()    { printf '%s  FAIL%s  %s\n' "$RED" "$NC" "$1"; FAIL=$((FAIL+1)); FAILED_GATES+=("$1"); }
skip()    { printf '%s  SKIP%s  %s\n' "$YELLOW" "$NC" "$1"; SKIP=$((SKIP+1)); }
info()    { printf '        %s\n' "$1"; }

# run_gate "label" command...
run_gate() {
  local label="$1"; shift
  local log="/tmp/dealix_close_${label// /_}.log"
  if "$@" >"$log" 2>&1; then
    pass "$label"
  else
    fail "$label  (log: $log)"
  fi
}

printf '%s================================================%s\n' "$BOLD" "$NC"
printf '%s Dealix Close-Now — Private-Launch Verification %s\n' "$BOLD" "$NC"
printf '%s================================================%s\n' "$BOLD" "$NC"

# ---- 1. repository context (read-only) --------------------------------------
section "1) Repository context"
info "Branch:  $(git branch --show-current 2>/dev/null || echo 'n/a')"
info "Commit:  $(git log -1 --oneline 2>/dev/null || echo 'n/a')"
if [[ -n "$(git status --short 2>/dev/null)" ]]; then
  info "Working tree: has uncommitted changes"
else
  info "Working tree: clean"
fi

# ---- 2. canonical verification gates ----------------------------------------
section "2) Canonical verification gates (make)"
run_gate "make doctor"             make doctor
run_gate "make env-check"          make env-check
run_gate "make security-smoke"     make security-smoke
run_gate "make api-contract-check" make api-contract-check
run_gate "make test"               make test
run_gate "make prod-verify"        make prod-verify

# ---- 3. web build (opt-in) --------------------------------------------------
section "3) Web build (apps/web)"
if [[ "${DEALIX_CLOSE_FULL:-0}" != "1" ]]; then
  skip "web build — set DEALIX_CLOSE_FULL=1 to enable"
elif [[ ! -d apps/web ]]; then
  skip "web build — apps/web not found"
else
  if (
    cd apps/web
    if [[ -f package-lock.json ]]; then npm ci; else npm install; fi
    if npm run 2>/dev/null | grep -qE 'verify'; then npm run verify; else npm run build; fi
  ) >/tmp/dealix_close_web.log 2>&1; then
    pass "web build"
  else
    fail "web build  (log: /tmp/dealix_close_web.log)"
  fi
fi

# ---- 4. docker build (opt-in) -----------------------------------------------
section "4) Docker build"
if [[ "${DEALIX_CLOSE_FULL:-0}" != "1" ]]; then
  skip "docker build — set DEALIX_CLOSE_FULL=1 to enable"
elif [[ -f docker-compose.yml || -f compose.yml ]]; then
  run_gate "docker compose build" docker compose build
else
  skip "docker build — no compose file found"
fi

# ---- 5. local health smoke (read-only GET) ----------------------------------
section "5) Local health smoke (:8000)"
if command -v curl >/dev/null 2>&1 && curl -fsS http://localhost:8000/health >/dev/null 2>&1; then
  if curl -fsS http://localhost:8000/health >/dev/null 2>&1; then pass "/health (local)"; else fail "/health (local)"; fi
  if curl -fsS http://localhost:8000/health/deep >/dev/null 2>&1; then pass "/health/deep (local)"; else skip "/health/deep (local) degraded or unavailable"; fi
else
  skip "local API not running on :8000"
fi

# ---- 6. production smoke (opt-in via env) -----------------------------------
section "6) Production smoke"
if [[ -n "${PRODUCTION_BASE_URL:-}" ]]; then
  if curl -fsS "$PRODUCTION_BASE_URL/health" >/dev/null 2>&1; then pass "/health (prod)"; else fail "/health (prod)"; fi
  if curl -fsS "$PRODUCTION_BASE_URL/health/deep" >/dev/null 2>&1; then pass "/health/deep (prod)"; else fail "/health/deep (prod)"; fi
  run_gate "make production-smoke" make production-smoke PRODUCTION_BASE_URL="$PRODUCTION_BASE_URL"
else
  skip "PRODUCTION_BASE_URL not set"
fi

# ---- verdict ----------------------------------------------------------------
section "Verdict"
printf 'PASS=%s  FAIL=%s  SKIP=%s\n' "$PASS" "$FAIL" "$SKIP"
if [[ $FAIL -eq 0 ]]; then
  printf '%sDEALIX_CLOSE_NOW=GREEN%s — core gates passed.\n' "$GREEN" "$NC"
  printf 'Private Launch: technical GO (founder sign-off + founder-only steps still required).\n'
  printf 'Public Launch: remains NO-GO until first paid proof exists (see docs/LAUNCH_GATES.md G5).\n'
  exit 0
else
  printf '%sDEALIX_CLOSE_NOW=RED%s — %s gate(s) failed:\n' "$RED" "$NC" "$FAIL"
  for g in "${FAILED_GATES[@]}"; do printf '  - %s\n' "$g"; done
  printf 'Fix the root cause; do not weaken any gate.\n'
  exit 1
fi
