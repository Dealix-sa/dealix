#!/usr/bin/env bash
# Founder launch-close — fast, honest, read-only diagnostic for the private launch.
#
# What it does:  runs the deterministic launch gates, reports each result, prints
#                the founder-only checklist, and returns non-zero if a HARD gate fails.
# What it never does:  no deploy, no external messages, no charges, no secret writes.
#
# For the deeper company/go-live/GTM battery use:  bash scripts/official_launch_verify.sh
#
# Usage:
#   bash scripts/founder_launch_close_now.sh            # gates + checklist
#   bash scripts/founder_launch_close_now.sh --web      # also run apps/web verify
#   bash scripts/founder_launch_close_now.sh --health http://localhost:8000   # also curl health
set -uo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

RUN_WEB=0
HEALTH_BASE=""
for arg in "$@"; do
  case "$arg" in
    --web) RUN_WEB=1 ;;
    --health) shift; HEALTH_BASE="${1:-}" ;;
    --health=*) HEALTH_BASE="${arg#*=}" ;;
  esac
done

HARD_FAIL=0
SOFT_NOTE=0
declare -a SUMMARY=()

# run_gate <label> <hard|soft> <command...>
run_gate() {
  local label="$1"; local kind="$2"; shift 2
  echo "── ${label}"
  if "$@"; then
    SUMMARY+=("PASS  ${label}")
  else
    if [[ "$kind" == "hard" ]]; then
      SUMMARY+=("FAIL  ${label}  (hard)")
      HARD_FAIL=1
    else
      SUMMARY+=("WARN  ${label}  (soft/env — runs in CI)")
      SOFT_NOTE=1
    fi
  fi
  echo
}

echo "== Dealix Founder Launch Close =="
echo "Repo: $ROOT"
echo "Branch: $(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo '?')   Commit: $(git rev-parse --short HEAD 2>/dev/null || echo '?')"
echo "Working tree: $(test -z "$(git status --porcelain 2>/dev/null)" && echo clean || echo dirty)"
echo

# 1) Deterministic gates (hard = real signal; soft = needs full deps/DB, validated in CI)
run_gate "make env-check"          hard make env-check
run_gate "make security-smoke"     hard make security-smoke
run_gate "make alembic-heads"      soft make alembic-heads
run_gate "make api-contract-check" soft make api-contract-check

# 2) Optional web verify
if [[ "$RUN_WEB" == "1" ]]; then
  if [[ -f apps/web/package.json ]]; then
    echo "── apps/web verify"
    ( cd apps/web && { [ -f package-lock.json ] && npm ci || npm install; } && npm run verify ) \
      && SUMMARY+=("PASS  apps/web verify") || { SUMMARY+=("FAIL  apps/web verify  (hard)"); HARD_FAIL=1; }
    echo
  else
    SUMMARY+=("SKIP  apps/web verify  (no apps/web/package.json)")
  fi
fi

# 3) Optional local health smoke (only if a base URL is given; never hits production by default)
if [[ -n "$HEALTH_BASE" ]]; then
  echo "── health smoke @ ${HEALTH_BASE}"
  if curl -fsS "${HEALTH_BASE}/health" >/dev/null 2>&1; then
    curl -fsS "${HEALTH_BASE}/health"; echo
    curl -fsS "${HEALTH_BASE}/health/deep" >/dev/null 2>&1 && echo "(/health/deep reachable)" || echo "(/health/deep not reachable)"
    SUMMARY+=("PASS  health smoke ${HEALTH_BASE}/health")
  else
    SUMMARY+=("WARN  health smoke  (no API at ${HEALTH_BASE}; start it or pass a live base)")
    SOFT_NOTE=1
  fi
  echo
fi

# 4) Summary
echo "== Gate summary =="
for line in "${SUMMARY[@]}"; do echo "  $line"; done
echo

# 5) Founder-only checklist (documented, NOT executed by this script)
cat <<'CHECKLIST'
== Founder-only steps (manual — secrets / money / GitHub UI) ==
  [ ] Merge #638 -> add ANTHROPIC_API_KEY secret -> merge #650  (review #638 full diff; resolve #650 free-tier P0)
  [ ] Close the make security-smoke blocker (see docs/ops/OFFICIAL_PRIVATE_LAUNCH_DECISION.md §3.1)
  [ ] Set production secrets (docs/ops/PRODUCTION_ENV_TEMPLATE.md)
  [ ] Apply branch protection + environments (docs/ops/CI_PERMISSIONS_AND_BRANCH_PROTECTION.md)
  [ ] Verify DNS/TLS for api.dealix.me
  [ ] Moyasar KYC + live cutover (python scripts/moyasar_live_cutover.py) ; verify payment + webhook
  [ ] Deploy + smoke: curl /health, /health/deep, /api/v1/pricing/plans ; make production-smoke PRODUCTION_BASE_URL=...
  Never automatic: customer messages, live payments, external commitments.
CHECKLIST
echo

if [[ "$HARD_FAIL" == "1" ]]; then
  echo "VERDICT: NO-GO — a hard gate failed above. Fix the root cause (do not disable guards)."
  exit 1
fi
if [[ "$SOFT_NOTE" == "1" ]]; then
  echo "VERDICT: hard gates green locally; soft/env items validate in CI. Complete the founder-only steps for Private Launch GO."
else
  echo "VERDICT: hard gates green. Complete the founder-only steps for Private Launch GO."
fi
