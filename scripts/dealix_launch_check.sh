#!/usr/bin/env bash
# dealix_launch_check.sh — pre-launch readiness verification
# Run: bash scripts/dealix_launch_check.sh
# Safe: read-only checks only, no external calls, no side effects

set -euo pipefail

PASS=0
FAIL=0
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

ok()   { echo "  ✅  $1"; PASS=$((PASS+1)); }
fail() { echo "  ❌  $1"; FAIL=$((FAIL+1)); }
hdr()  { echo; echo "── $1 ──"; }

echo "╔══════════════════════════════════════════╗"
echo "║   Dealix Launch Readiness Check          ║"
echo "╚══════════════════════════════════════════╝"

# ── Frontend Pages ──────────────────────────────
hdr "Frontend Pages (apps/web)"
for page in about contact privacy terms; do
  if [ -f "$ROOT/apps/web/app/$page/page.tsx" ]; then
    ok "$page/page.tsx"
  else
    fail "$page/page.tsx MISSING"
  fi
done
for page in pricing services; do
  if [ -f "$ROOT/apps/web/app/$page/page.tsx" ]; then
    ok "$page/page.tsx"
  else
    fail "$page/page.tsx MISSING"
  fi
done

# ── Nav & Footer ────────────────────────────────
hdr "Navigation"
if grep -q '"/about"' "$ROOT/apps/web/components/Nav.tsx" 2>/dev/null; then
  ok "Nav includes /about"
else
  fail "Nav missing /about link"
fi
if grep -q '"/contact"' "$ROOT/apps/web/components/Nav.tsx" 2>/dev/null; then
  ok "Nav includes /contact"
else
  fail "Nav missing /contact link"
fi
if grep -q '"/privacy"' "$ROOT/apps/web/components/Footer.tsx" 2>/dev/null; then
  ok "Footer includes /privacy"
else
  fail "Footer missing /privacy link"
fi
if grep -q '"/terms"' "$ROOT/apps/web/components/Footer.tsx" 2>/dev/null; then
  ok "Footer includes /terms"
else
  fail "Footer missing /terms link"
fi

# ── API ─────────────────────────────────────────
hdr "API Endpoints"
if grep -q '"/contact"' "$ROOT/api/routers/public_intake.py" 2>/dev/null; then
  ok "POST /contact endpoint defined"
else
  fail "POST /contact endpoint MISSING"
fi
if grep -q '"queued_for_founder_review"' "$ROOT/api/routers/public_intake.py" 2>/dev/null; then
  ok "Governance gate present in public_intake"
else
  fail "Governance gate MISSING in public_intake"
fi

# ── Python syntax ────────────────────────────────
hdr "Python Syntax"
if python3 -c "import ast; ast.parse(open('$ROOT/api/routers/public_intake.py').read())" 2>/dev/null; then
  ok "public_intake.py syntax OK"
else
  fail "public_intake.py syntax ERROR"
fi

# ── Company OS ───────────────────────────────────
hdr "Company OS Scripts"
for script in dealix_micro_day dealix_revenue_day dealix_intake_day dealix_followup_day dealix_trust_day; do
  if [ -f "$ROOT/scripts/$script.sh" ]; then
    if bash -n "$ROOT/scripts/$script.sh" 2>/dev/null; then
      ok "$script.sh syntax OK"
    else
      fail "$script.sh syntax ERROR"
    fi
  else
    fail "$script.sh MISSING"
  fi
done

# ── Data ─────────────────────────────────────────
hdr "Data Files"
if [ -f "$ROOT/data/warm_list.csv" ]; then
  LINES=$(grep -v '^#' "$ROOT/data/warm_list.csv" | grep -v '^name,' | grep -c '[a-zA-Z]' || true)
  if [ "$LINES" -gt 1 ]; then
    ok "warm_list.csv has $LINES data rows"
  else
    fail "warm_list.csv is empty — add 30-50 warm contacts before campaign"
  fi
else
  fail "warm_list.csv MISSING"
fi

# ── Security checks ──────────────────────────────
hdr "Security"
if ! grep -r 'auto.send\|auto_send\|send_whatsapp\|send_email' \
    "$ROOT/api/routers/public_intake.py" 2>/dev/null | grep -v '#' | grep -q .; then
  ok "No auto-send in public_intake"
else
  fail "Auto-send detected in public_intake — BLOCKED"
fi
if [ -f "$ROOT/.env" ]; then
  fail ".env file committed — REMOVE IMMEDIATELY"
else
  ok ".env not committed"
fi

# ── Summary ──────────────────────────────────────
echo
echo "════════════════════════════════════════════"
echo "  ✅ Passed: $PASS   ❌ Failed: $FAIL"
echo "════════════════════════════════════════════"

if [ "$FAIL" -gt 0 ]; then
  echo "  Fix the ❌ items above before launch."
  exit 1
else
  echo "  All checks passed — ready for founder review."
fi
