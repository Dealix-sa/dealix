"""Growth engine — generates draft-only content for the content queue.

Every output is a draft. Nothing is auto-posted. Content is "viral by value":
insight-led lead magnets and posts with a soft CTA to request a custom Snapshot.
"""

from __future__ import annotations

from datetime import date

# Forbidden phrasing that must never appear in generated content.
FORBIDDEN_PHRASES = (
    "guaranteed revenue",
    "guaranteed clients",
    "guaranteed government",
    "government access",
    "مضمون",
)


def _clean(text: str) -> str:
    low = text.lower()
    for bad in FORBIDDEN_PHRASES:
        if bad in low:
            # Defensive: neutralise rather than emit a forbidden claim.
            text = text.replace(bad, "[claim removed]")
    return text


def build_content_queue(run_date: date) -> str:
    """Return a markdown content queue of drafts (never posted automatically)."""

    d = run_date.isoformat()
    lines = [
        f"# Dealix Content Queue — {d} (DRAFT ONLY, do not auto-post)",
        "",
        "> All items are drafts for founder review. Publish manually after approval.",
        "",
        "## 1. LinkedIn post (AR/EN)",
        "- Hook: أكثر تسريب للإيراد في شركات B2B السعودية هو ضعف المتابعة، لا نقص العملاء.",
        "- Value: 3 نقاط قابلة للتطبيق اليوم لإغلاق فجوة المتابعة.",
        "- Soft CTA: اطلب Saudi Opportunity Snapshot مخصص لقطاعك.",
        "",
        "## 2. X thread (EN)",
        "- 5 tweets: the Saudi B2B revenue-leak checklist (follow-up, pipeline, proof).",
        "- We expect / the goal is / we will measure — hypothesis language only.",
        "- CTA: reply 'Snapshot' to request a custom market snapshot.",
        "",
        "## 3. Short video script (30–45s)",
        "- Problem → one concrete fix → invite to request a Snapshot.",
        "",
        "## 4. Newsletter draft",
        "- One market insight + one operator tip + one CTA (Revenue Proof Sprint 499 SAR).",
        "",
        "## 5. One-page market insight (lead magnet)",
        "- Title: Saudi B2B Revenue Leak Scanner — self-check in 10 questions.",
        "- Gate: request the full custom Snapshot.",
        "",
        "## Compliance",
        "- No cold blasts. No mass automation. No fabricated proof. No unfounded claims.",
        "- Manual, high-signal distribution only, after founder approval.",
    ]
    return _clean("\n".join(lines)) + "\n"


def content_has_forbidden_claims(text: str) -> list[str]:
    low = text.lower()
    return [bad for bad in FORBIDDEN_PHRASES if bad in low and "[claim removed]" not in low]
