#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════════════
# Dealix — Close-Now launch verification + founder orientation
# ═══════════════════════════════════════════════════════════════════
# Runs the canonical repository gates and prints the founder-only
# checklist for a private launch.
#
# SAFETY (doctrine): this script is READ-ONLY. It NEVER deploys, NEVER
# charges a customer, NEVER sends outreach, and NEVER touches secrets.
# It only runs local gates and prints guidance.
#
# Authoritative gate run is CI on the merge head — some gates need app
# dependencies (fastapi/alembic) that may be absent in a thin shell.
#
# Usage:
#   scripts/dealix_close_now.sh            # gates + orientation
#   scripts/dealix_close_now.sh --with-tests   # also run `make test` (heavy)
# ═══════════════════════════════════════════════════════════════════
set -uo pipefail   # intentionally NOT -e: run every gate, then summarize

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

WITH_TESTS=0
[ "${1:-}" = "--with-tests" ] && WITH_TESTS=1

FAILS=0
run_gate() {
  local label="$1"; shift
  echo ""
  echo "── ${label} ──────────────────────────────────────────"
  if "$@"; then
    echo "✅ ${label}: passed"
  else
    echo "❌ ${label}: FAILED (or needs full env / CI)"
    FAILS=$((FAILS + 1))
  fi
}

echo "================================================================"
echo " Dealix Close-Now — Founder Launch Verification (READ-ONLY)"
echo "================================================================"
echo "Branch:  $(git branch --show-current 2>/dev/null || echo '?')"
echo "Commit:  $(git log -1 --oneline 2>/dev/null || echo '?')"
echo "Dirty:   $(test -n "$(git status --porcelain)" && echo 'yes (uncommitted changes)' || echo 'no')"

echo ""
echo "### 1) Canonical gates ###"
run_gate "env-check"          make env-check
run_gate "security-smoke"     make security-smoke
run_gate "api-contract-check" make api-contract-check
run_gate "prod-verify"        make prod-verify
if [ "$WITH_TESTS" -eq 1 ]; then
  run_gate "test (full suite)" make test
else
  echo ""
  echo "(skipping full test suite — pass --with-tests to include it)"
fi

echo ""
echo "### 2) Local health smoke (only if API already running on :8000) ###"
if curl -fsS http://localhost:8000/health >/dev/null 2>&1; then
  echo "✅ /health reachable:";       curl -fsS http://localhost:8000/health || true
  echo ""; echo "→ /health/deep:";    curl -fsS http://localhost:8000/health/deep || true
else
  echo "ℹ️  Local API not running on :8000 — skipping HTTP smoke."
fi

echo ""
echo "### 3) Production smoke (only if PRODUCTION_BASE_URL is set) ###"
if [ -n "${PRODUCTION_BASE_URL:-}" ]; then
  make production-smoke PRODUCTION_BASE_URL="$PRODUCTION_BASE_URL" || FAILS=$((FAILS + 1))
else
  echo "ℹ️  PRODUCTION_BASE_URL not set — skipping production smoke."
fi

echo ""
echo "================================================================"
echo " FOUNDER-ONLY checklist (NOT executed by this script)"
echo "================================================================"
cat <<'CHECKLIST'
  [ ] Set GitHub Secrets (ANTHROPIC_API_KEY + production set) — never commit
  [ ] Enable branch protection / ruleset on main
  [ ] Create staging + production environments (required reviewers on prod)
  [ ] Verify DNS/TLS for api.dealix.me
  [ ] Moyasar: KYC, then scripts/moyasar_live_cutover.py (founder-only)
  [ ] Railway deploy: railway up (founder-only)
  [ ] Warm-list outreach: drafts only, nothing sent without approval

  Merge path:  #638 (Claude Code + CLAUDE.md)  →  #650 (release candidate)
               then triage/close overlapping #641–#649.
  Decision:    docs/ops/OFFICIAL_PRIVATE_LAUNCH_DECISION.md
  Doctrine:    Public launch stays NO-GO until paid-customer proof exists.
CHECKLIST

echo ""
echo "================================================================"
if [ "$FAILS" -eq 0 ]; then
  echo " ✅ All run gates passed. Private-launch technical signal: GO-pending."
  echo "    (Authoritative result = CI on the merge head.)"
else
  echo " ⚠️  ${FAILS} gate(s) failed or need a full env/CI. Review output above."
  echo "    Some gates need app deps (fastapi/alembic) — run in CI for truth."
fi
echo " Public launch remains NO-GO until a real paid Proof Pack exists."
echo "================================================================"

# Read-only orientation tool: do not fail the shell on gate state.
exit 0
