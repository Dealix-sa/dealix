"""Forbidden-marketing-claims sweep across the Next.js frontend (canonical site).

Mirror of ``tests/test_landing_forbidden_claims.py`` but for ``frontend/`` —
the surface the company is consolidating onto. Customer-visible TSX + i18n JSON
must not contain unapproved instances of:
  Arabic — نضمن، مضمون
  English — guaranteed, blast, scrape, scraping, cold {whatsapp|outreach|email|messaging}

Negation / disclaimer / sample-data occurrences are explicitly allowlisted per
file with a reason. Any *new* file picking up one of these phrases — or any new
phrase in an existing file beyond its allowlist — fails the test, so the
canonical site can never over-claim more than the doctrine allows.
"""
from __future__ import annotations

import re
from pathlib import Path

FRONTEND = Path(__file__).resolve().parents[1] / "frontend"
SCAN_ROOTS = [
    FRONTEND / "src" / "app",
    FRONTEND / "src" / "components",
    FRONTEND / "messages",
]

FORBIDDEN_PATTERNS = [
    ("نضمن", re.compile(r"نضمن")),
    ("مضمون", re.compile(r"مضمون")),
    ("guaranteed", re.compile(r"\bguaranteed?\b", re.IGNORECASE)),
    ("blast", re.compile(r"\bblast\b", re.IGNORECASE)),
    ("scrape", re.compile(r"\bscrape\b", re.IGNORECASE)),
    ("scraping", re.compile(r"\bscraping\b", re.IGNORECASE)),
    ("cold", re.compile(r"\bcold\s+(whatsapp|outreach|email|messaging)\b", re.IGNORECASE)),
]

# Per-file allowlist, keyed by path relative to ``frontend/`` (posix).
# Reason codes:
#   NEGATION       — "لا/no/never/بدون/صفر <term>" describing what we DON'T do.
#   SAMPLE_DATA    — appears inside demo/sample CRM data (a lead's source label).
#   REVIEW_PENDING — positive context (money-back wording) tracked for founder
#                    review; allowed for now to avoid a unilateral copy change.
ALLOWLIST: dict[str, dict[str, str]] = {
    "messages/ar.json": {"scraping": "NEGATION"},
    "messages/en.json": {"cold": "NEGATION", "scraping": "NEGATION"},
    "src/app/[locale]/offer/lead-intelligence-sprint/page.tsx": {"scraping": "NEGATION"},
    "src/app/[locale]/privacy/page.tsx": {"cold": "NEGATION", "scraping": "NEGATION"},
    "src/app/[locale]/trust/page.tsx": {"cold": "NEGATION"},
    "src/components/company/AboutPage.tsx": {"cold": "NEGATION", "scraping": "NEGATION"},
    # CRM demo data: a sample lead with source="Cold Email" (not a Dealix claim).
    "src/components/crm/CRMDashboard.tsx": {"cold": "SAMPLE_DATA"},
    "src/components/forms/CustomSolutionForm.tsx": {"cold": "NEGATION"},
    "src/components/gtm/CommercialLaunchHome.tsx": {"cold": "NEGATION"},
    "src/components/gtm/PartnerApplyForm.tsx": {"cold": "NEGATION", "scraping": "NEGATION"},
    "src/components/gtm/PricingPage.tsx": {
        "cold": "NEGATION",
        "scraping": "NEGATION",
        "مضمون": "NEGATION",          # "يدوي وغير مضمون" — not guaranteed (negation)
        "guaranteed": "REVIEW_PENDING",  # "money-back guarantee" wording
    },
    "src/components/gtm/TrustPage.tsx": {"cold": "NEGATION", "scraping": "NEGATION"},
    "src/components/layout/FooterSection.tsx": {"cold": "NEGATION"},
    "src/components/services/ServicesPage.tsx": {"cold": "NEGATION", "scraping": "NEGATION"},
    # "Money-Back Guarantee" refund wording — mirrors landing roi.html treatment.
    "src/components/subscriptions/PricingPlans.tsx": {"guaranteed": "REVIEW_PENDING"},
    "src/components/trust/TrustCenter.tsx": {"cold": "NEGATION"},
}


def _scan(text: str) -> set[str]:
    return {tok for tok, pat in FORBIDDEN_PATTERNS if pat.search(text)}


def _iter_files():
    for root in SCAN_ROOTS:
        if not root.exists():
            continue
        for ext in ("*.tsx", "*.json"):
            yield from root.rglob(ext)


def _rel(path: Path) -> str:
    return path.relative_to(FRONTEND).as_posix()


def test_no_unallowlisted_forbidden_claims():
    violations: list[str] = []
    for path in sorted(_iter_files()):
        hits = _scan(path.read_text(encoding="utf-8"))
        if not hits:
            continue
        allowed = set(ALLOWLIST.get(_rel(path), {}).keys())
        for token in sorted(hits - allowed):
            violations.append(f"{_rel(path)}: forbidden token {token!r} not allowlisted")
    assert not violations, (
        "Forbidden marketing claims found on the canonical frontend. Either "
        "rephrase the copy or — if the term is a negation/disclaimer — add it to "
        "ALLOWLIST in tests/test_frontend_forbidden_claims.py.\n" + "\n".join(violations)
    )


def test_allowlist_entries_actually_present():
    """Drop stale allowlist entries so the perimeter stays tight."""
    stale: list[str] = []
    for rel, tokens in ALLOWLIST.items():
        path = FRONTEND / rel
        if not path.exists():
            stale.append(f"{rel}: file not found")
            continue
        hits = _scan(path.read_text(encoding="utf-8"))
        for token in tokens:
            if token not in hits:
                stale.append(f"{rel}: {token!r} allowlisted but no longer present")
    assert not stale, "stale allowlist entries:\n" + "\n".join(stale)


def test_review_pending_count_is_stable():
    """REVIEW_PENDING items surface here so they cannot be silently forgotten.
    Update this count after the founder approves or rephrases a phrase."""
    review_pending = [
        f"{rel}: {tok!r}"
        for rel, tokens in ALLOWLIST.items()
        for tok, reason in tokens.items()
        if reason == "REVIEW_PENDING"
    ]
    assert len(review_pending) == 2, (
        "REVIEW_PENDING list changed; expected 2 (money-back 'guarantee' on "
        "PricingPage.tsx + PricingPlans.tsx). Update after founder decision. "
        f"Current: {review_pending}"
    )
