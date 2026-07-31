#!/usr/bin/env bash
# Frontend Tier-1 verification — current product-truth contract.
#
# Verifies the public acquisition path, approval-first safety surfaces,
# evidence ladder, canonical sitemap and customer-facing language.

set -u

QUIET=0
if [[ "${1:-}" == "--quiet" ]]; then
  QUIET=1
fi

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
LANDING="$ROOT/landing"
FAILS=0
declare -a OUTPUT

emit() {
  local key="$1" status="$2" detail="${3:-}"
  if [[ "$status" == "FAIL" ]]; then
    FAILS=$((FAILS + 1))
  fi
  OUTPUT+=("$(printf '%s: %s' "$key" "$status")")
  if [[ -n "$detail" ]]; then
    OUTPUT+=("  └─ $detail")
  fi
}

check_present() {
  local key="$1" file="$2" pattern="$3"
  if grep -qE "$pattern" "$LANDING/$file" 2>/dev/null; then
    emit "$key" PASS
  else
    emit "$key" FAIL "missing in $file: $pattern"
  fi
}

check_absent() {
  local key="$1" file="$2" pattern="$3"
  if grep -qE "$pattern" "$LANDING/$file" 2>/dev/null; then
    emit "$key" FAIL "unexpected in $file: $pattern"
  else
    emit "$key" PASS
  fi
}

# 1. Hero H1 remains short and focused. Parse HTML independently of line layout.
H1=$(python3 - "$LANDING/index.html" <<'PY'
from __future__ import annotations

import html
import re
import sys
from pathlib import Path

text = Path(sys.argv[1]).read_text(encoding="utf-8")
match = re.search(
    r'<h1[^>]*class="[^"]*\bhero__title\b[^"]*"[^>]*>(.*?)</h1>',
    text,
    flags=re.IGNORECASE | re.DOTALL,
)
if match:
    value = re.sub(r"<[^>]+>", " ", match.group(1))
    print(" ".join(html.unescape(value).split()))
PY
)
if [[ -n "$H1" ]]; then
  WORDS=$(echo "$H1" | wc -w | tr -d ' ')
  if (( WORDS <= 8 )); then
    emit "HERO_H1_LE_8_WORDS" PASS "h1=\"$H1\" ($WORDS words)"
  else
    emit "HERO_H1_LE_8_WORDS" FAIL "h1 has $WORDS words (>8)"
  fi
else
  emit "HERO_H1_LE_8_WORDS" FAIL "<h1 class=hero__title> not found"
fi

# 2. Hero has exactly one primary CTA and it goes to the diagnostic.
HERO_CTAS=$(awk '/<div class="hero__ctas"/,/<\/div>/' "$LANDING/index.html")
PRIMARY_COUNT=$(echo "$HERO_CTAS" | grep -cE 'btn--primary')
if (( PRIMARY_COUNT == 1 )) && echo "$HERO_CTAS" | grep -E 'btn--primary' | grep -qE 'href="/diagnostic\.html"'; then
  emit "SINGLE_PRIMARY_CTA" PASS "/diagnostic.html"
else
  emit "SINGLE_PRIMARY_CTA" FAIL "expected one primary /diagnostic.html CTA"
fi

# 3. Navigation and WhatsApp Decision Layer contract.
NAV_BLOCK=$(awk '/<nav class="nav__links"/,/<\/nav>/' "$LANDING/index.html")
NAV_LINKS=$(echo "$NAV_BLOCK" | grep -cE '<a\s+[^>]*href=')
if (( NAV_LINKS <= 20 )); then
  emit "NAV_LINKS_BOUNDED" PASS "$NAV_LINKS links including resources"
else
  emit "NAV_LINKS_BOUNDED" FAIL "$NAV_LINKS links"
fi
check_present "WADL_SECTION_PRESENT" "index.html" 'id="wadl"'
WADL_BLOCK=$(awk '/id="wadl"/,/<\/section>/' "$LANDING/index.html")
if echo "$WADL_BLOCK" | grep -q "DEMO"; then
  emit "WADL_DEMO_LABEL" PASS
else
  emit "WADL_DEMO_LABEL" FAIL "DEMO label missing"
fi

# 4. Customer portal ordering and demo state.
TODAY_LINE=$(grep -nE 'id="today-decision"' "$LANDING/customer-portal.html" | head -1 | cut -d: -f1)
OPS_LINE=$(grep -nE 'id="ops-grid"' "$LANDING/customer-portal.html" | head -1 | cut -d: -f1)
if [[ -n "$TODAY_LINE" && -n "$OPS_LINE" && "$TODAY_LINE" -lt "$OPS_LINE" ]]; then
  emit "PORTAL_TODAY_DECISION_ABOVE_OPS" PASS
else
  emit "PORTAL_TODAY_DECISION_ABOVE_OPS" FAIL
fi
if grep -q "src-pill" "$LANDING/customer-portal.html" && grep -q "DEMO" "$LANDING/customer-portal.html"; then
  emit "DEMO_LABELS" PASS
else
  emit "DEMO_LABELS" FAIL
fi

# 5. Proof ladder.
MISSING_LEVELS=""
for level in L1 L2 L3 L4 L5; do
  if ! grep -q "$level" "$LANDING/proof.html"; then
    MISSING_LEVELS="$MISSING_LEVELS $level"
  fi
done
if [[ -z "$MISSING_LEVELS" ]]; then
  emit "PROOF_L1_TO_L5" PASS
else
  emit "PROOF_L1_TO_L5" FAIL "missing:$MISSING_LEVELS"
fi

# 6. Current commercial path: two entries, quote-only Pilot, no Checkout.
check_present "PRICING_FREE_ENTRY" "pricing.html" 'Free Mini Diagnostic'
check_present "PRICING_QUOTE_ONLY_PILOT" "pricing.html" 'Revenue Command Pilot — 30 days'
check_present "PRICING_QUOTE_ONLY_STATUS" "pricing.html" 'quote_only'
check_present "PRICING_DISCOVERY_CTA" "pricing.html" 'href="/diagnostic\.html"'
check_absent "PRICING_NO_CHECKOUT" "pricing.html" '/checkout\.html'
check_absent "PRICING_NO_RETIRED_FIXED_PRICES" "pricing.html" '499|1,500|2,999|7,999|12,000'

# 7. Trust Center hard gates.
GATES=(NO_LIVE_SEND NO_LIVE_CHARGE NO_COLD_WHATSAPP NO_LINKEDIN_AUTOMATION NO_SCRAPING NO_FAKE_PROOF NO_FAKE_REVENUE NO_UNAPPROVED_TESTIMONIAL)
MISSING_GATES=""
for gate in "${GATES[@]}"; do
  if ! grep -q "$gate" "$LANDING/trust-center.html"; then
    MISSING_GATES="$MISSING_GATES $gate"
  fi
done
if [[ -z "$MISSING_GATES" ]]; then
  emit "TRUST_CENTER_8_GATES" PASS
else
  emit "TRUST_CENTER_8_GATES" FAIL "missing:$MISSING_GATES"
fi

# 8. Partner redirect remains available, but is not required in the canonical sitemap.
if [[ -f "$LANDING/agency-partner.html" ]]; then
  emit "AGENCY_PARTNER_EXISTS" PASS
else
  emit "AGENCY_PARTNER_EXISTS" FAIL
fi
if grep -q 'http-equiv="refresh"' "$LANDING/partners.html" && grep -q '/agency-partner.html' "$LANDING/partners.html"; then
  emit "PARTNERS_REDIRECT" PASS
else
  emit "PARTNERS_REDIRECT" FAIL
fi

# 9. Sitemap uses canonical domain and excludes retired claim pages.
if grep -q 'https://dealix.me/' "$LANDING/sitemap.xml"; then
  emit "SITEMAP_CANONICAL_DOMAIN" PASS
else
  emit "SITEMAP_CANONICAL_DOMAIN" FAIL
fi
SITEMAP_RETIRED=""
for retired in roi.html case-study.html compare.html launchpad.html; do
  if grep -q "$retired" "$LANDING/sitemap.xml"; then
    SITEMAP_RETIRED="$SITEMAP_RETIRED $retired"
  fi
done
if [[ -z "$SITEMAP_RETIRED" ]]; then
  emit "SITEMAP_RETIRED_PAGES_EXCLUDED" PASS
else
  emit "SITEMAP_RETIRED_PAGES_EXCLUDED" FAIL "present:$SITEMAP_RETIRED"
fi

# 10. Required homepage anchors remain stable.
ANCHORS=(pillars for-who sectors how trust proof pricing faq pilot)
MISSING_ANCHORS=""
for anchor in "${ANCHORS[@]}"; do
  if ! grep -q "id=\"$anchor\"" "$LANDING/index.html"; then
    MISSING_ANCHORS="$MISSING_ANCHORS #$anchor"
  fi
done
if [[ -z "$MISSING_ANCHORS" ]]; then
  emit "ANCHOR_IDS_PRESERVED" PASS
else
  emit "ANCHOR_IDS_PRESERVED" FAIL "removed:$MISSING_ANCHORS"
fi

# 11. RTL and customer-safe language.
RTL_FAIL=""
for page in index.html customer-portal.html pricing.html proof.html trust-center.html diagnostic.html agency-partner.html; do
  if ! grep -qE 'lang="ar"[^>]*dir="rtl"|dir="rtl"[^>]*lang="ar"' "$LANDING/$page"; then
    RTL_FAIL="$RTL_FAIL $page"
  fi
done
if [[ -z "$RTL_FAIL" ]]; then
  emit "RTL_LANG_DIR" PASS
else
  emit "RTL_LANG_DIR" FAIL "missing:$RTL_FAIL"
fi

INTERNAL_TERMS='(\bv1[0-2]\b|growth_beast|stacktrace)'
INTERNAL_FAIL=""
for page in index.html customer-portal.html pricing.html proof.html trust-center.html agency-partner.html; do
  STRIPPED=$(sed -E 's/<script[^>]*>.*?<\/script>//g; s/href="[^"]*"//g' "$LANDING/$page")
  if echo "$STRIPPED" | grep -qiE "$INTERNAL_TERMS"; then
    INTERNAL_FAIL="$INTERNAL_FAIL $page"
  fi
done
if [[ -z "$INTERNAL_FAIL" ]]; then
  emit "NO_INTERNAL_TERMS" PASS
else
  emit "NO_INTERNAL_TERMS" FAIL "pages:$INTERNAL_FAIL"
fi

# 12. Mobile target and forbidden visible claims.
if grep -qE 'min-height:\s*44px' "$LANDING/assets/css/design-system.css"; then
  emit "MOBILE_TAP_TARGETS" PASS
else
  emit "MOBILE_TAP_TARGETS" FAIL
fi
FORBIDDEN_FAIL=""
for page in index.html agency-partner.html trust-center.html pricing.html proof.html customer-portal.html diagnostic.html; do
  if grep -qE '\bguarantee[d]?\b|\bblast\b' "$LANDING/$page"; then
    FORBIDDEN_FAIL="$FORBIDDEN_FAIL $page"
  fi
done
if [[ -z "$FORBIDDEN_FAIL" ]]; then
  emit "NO_FORBIDDEN_TOKENS_SHELL" PASS
else
  emit "NO_FORBIDDEN_TOKENS_SHELL" FAIL "pages:$FORBIDDEN_FAIL"
fi

if (( FAILS == 0 )); then
  VERDICT="PASS"
elif (( FAILS <= 3 )); then
  VERDICT="PARTIAL"
else
  VERDICT="FAIL"
fi
emit "DEALIX_FRONTEND_TIER1_VERDICT" "$VERDICT" "$FAILS check(s) failed"

if (( QUIET == 0 )); then
  printf '%s\n' "${OUTPUT[@]}"
fi

if [[ "$VERDICT" == "PASS" ]]; then
  exit 0
fi
exit 1
