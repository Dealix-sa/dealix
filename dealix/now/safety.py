"""Email Safety Agent for the Dealix Now engine (os/02 #5).

Rule-based, deterministic checks over an outreach draft. No network, no LLM.
Returns ``{safety_score, personalization_score, issues, approved_for_review,
checks}`` where ``checks`` covers: mentions_company, single_pain, single_cta,
no_pricing, within_length, no_overclaim.

``approved_for_review`` is False if any hard check fails. "Approved for review"
means the draft may be shown to the founder — it never means "send". Dealix
never sends.
"""

from __future__ import annotations

import re

_MAX_WORDS = 150

# Pricing signals. Outreach drafts must never quote money. We flag
# *money-shaped* content, not every digit, so legitimate regulatory
# identifiers (e.g. "ZATCA Wave 24") do not trip the gate:
#   - a price/currency word in either language, or
#   - a currency word/symbol adjacent to a number, or
#   - a large or grouped number (>= 4 digits, or comma/period-grouped like
#     "20,000" / "20.000") that reads as an amount.
_PRICE_WORDS = (
    "sar",
    "ريال",
    "سعر",
    "أسعار",
    "تكلفة",
    "السعر",
    "بسعر",
    "price",
    "priced",
    "cost",
    "costs",
    "pricing",
    "usd",
    "ر.س",
    "دولار",
)
_CURRENCY_NEAR_NUMBER_RE = re.compile(
    r"(\d[\d,\.]*\s*(?:sar|usd|ريال|ر\.س|\$|دولار))|((?:sar|usd|ريال|ر\.س|\$|دولار|سعر|تكلفة)\s*\d)",
    re.IGNORECASE,
)
# 4+ digit run, or grouped thousands (1,000 / 1.000 / 1 000).
_AMOUNT_SHAPE_RE = re.compile(r"\d{4,}|\d{1,3}(?:[,\.\s]\d{3})+")


def _has_pricing(text: str) -> bool:
    lowered = text.lower()
    if "$" in text:
        return True
    if any(w in lowered for w in _PRICE_WORDS):
        return True
    if _CURRENCY_NEAR_NUMBER_RE.search(text):
        return True
    return bool(_AMOUNT_SHAPE_RE.search(text))


# Overclaim / superlative phrasing the doctrine forbids.
_OVERCLAIM_PHRASES = (
    "شركة رائدة",
    "نحن رائدون",
    "الأفضل في",
    "الأول في السوق",
    "رقم 1",
    "رقم واحد",
    "نضمن",
    "ضمان كامل",
    "guaranteed",
    "guarantee",
    "best in",
    "market leader",
    "#1",
    "world-class",
    "أفضل شركة",
)

# Spam-trigger words (subset relevant to AR/EN B2B outreach). Presence lowers
# the safety score but is not by itself a hard fail unless combined with a
# pricing/overclaim hard fail.
_SPAM_WORDS = (
    "act now",
    "limited time",
    "free",
    "100%",
    "click here",
    "اشترك الآن",
    "عرض حصري",
    "مجاناً",
    "مجانا",
    "خصم",
    "اضغط هنا",
)


def _count_questions(body: str) -> int:
    return body.count("؟") + body.count("?")


def check_draft_safety(draft: dict) -> dict:
    """Run rule-based safety checks over a draft dict.

    Expects keys ``body``, ``subject``, ``company_name``, ``word_count``.
    """
    body = str(draft.get("body") or "")
    subject = str(draft.get("subject") or "")
    company = str(draft.get("company_name") or "").strip()
    combined = f"{subject}\n{body}"
    combined_l = combined.lower()
    word_count = int(draft.get("word_count") or len(body.split()))

    issues: list[str] = []

    # ── Hard checks ──
    mentions_company = bool(company) and company in combined
    if not mentions_company:
        issues.append("company_name not mentioned in subject or body")

    question_count = _count_questions(body)
    single_cta = question_count == 1
    if question_count == 0:
        issues.append("no CTA question found")
    elif question_count > 1:
        issues.append(f"multiple CTA questions found ({question_count}) — must be exactly one")

    has_pricing = _has_pricing(combined)
    no_pricing = not has_pricing
    if has_pricing:
        issues.append("pricing/numeric content detected — drafts must not quote money")

    within_length = word_count <= _MAX_WORDS
    if not within_length:
        issues.append(f"body exceeds {_MAX_WORDS} words ({word_count})")

    overclaim_hit = next((p for p in _OVERCLAIM_PHRASES if p in combined_l), None)
    no_overclaim = overclaim_hit is None
    if overclaim_hit is not None:
        issues.append(f"overclaim phrase detected: {overclaim_hit!r}")

    # ── Soft check: spam-trigger words (affects score, not hard gate) ──
    spam_hits = [w for w in _SPAM_WORDS if w in combined_l]
    if spam_hits:
        issues.append(f"spam-trigger words: {', '.join(spam_hits)}")

    # Pain heuristic: a single, specific pain. We approximate "single pain" by
    # requiring the body to be focused (one CTA, within length) and not a
    # service list (no bullet markers / multiple ' / ' service separators).
    looks_like_service_list = combined.count("•") >= 2 or combined.count(" - ") >= 3
    single_pain = within_length and single_cta and not looks_like_service_list
    if looks_like_service_list:
        issues.append("draft looks like a service list, not a single pain")

    checks = {
        "mentions_company": mentions_company,
        "single_pain": single_pain,
        "single_cta": single_cta,
        "no_pricing": no_pricing,
        "within_length": within_length,
        "no_overclaim": no_overclaim,
    }

    hard_pass = all(checks.values())

    # Scores: start at 100, deduct per issue class. Deterministic.
    safety = 100
    if not no_pricing:
        safety -= 40
    if not no_overclaim:
        safety -= 30
    if not within_length:
        safety -= 20
    if not single_cta:
        safety -= 15
    safety -= 5 * len(spam_hits)
    safety = max(0, min(100, safety))

    personalization = 100
    if not mentions_company:
        personalization -= 50
    if not single_pain:
        personalization -= 20
    # A short, focused body personalizes better; long bodies dilute.
    if word_count > 120:
        personalization -= 10
    personalization = max(0, min(100, personalization))

    return {
        "safety_score": safety,
        "personalization_score": personalization,
        "issues": issues,
        "approved_for_review": hard_pass,
        "checks": checks,
    }


__all__ = ["check_draft_safety"]
