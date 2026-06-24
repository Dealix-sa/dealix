"""
Draft quality gate — Arabic and English validation.
Returns score 0-100 and list of failure flags.
"""

from __future__ import annotations

ARABIC_FAIL_PATTERNS = [
    ("generic_ai", ["الذكاء الاصطناعي يغير", "نقدم حلول ذكاء اصطناعي متطورة", "AI حل شامل"]),
    ("machine_translated", ["نحن نقدم لكم", "تجربة فريدة من نوعها", "الحل الأمثل"]),
    ("overblown_claims", ["نضمن", "مضمون 100%", "نتائج استثنائية"]),
    ("no_pain_angle", []),
    ("no_cta", []),
    ("no_opt_out", ["أقدر أوقف", "إلغاء الاشتراك"]),
]

ENGLISH_FAIL_PATTERNS = [
    ("generic_ai_agency", [
        "cutting-edge AI solutions",
        "transform your business with AI",
        "leverage the power of AI",
        "AI-powered platform",
    ]),
    ("fake_certainty", ["guaranteed ROI", "we guarantee", "definitely will", "100% success"]),
    ("too_long", []),
    ("no_human_approval_signal", []),
    ("no_opt_out", ["happy to stop", "unsubscribe"]),
]

WORD_LIMITS = {
    "email": 200,
    "linkedin": 100,
    "website_form": 150,
    "whatsapp_business": 80,
}


def run_quality_gate(draft: dict) -> dict:
    """Evaluate a draft dict and return score, flags, pass/fail, and reason."""
    score = 100
    flags: list[str] = []
    language = draft.get("language", "en")
    channel = draft.get("channel", "email")
    body = draft.get("body", "")
    subject = draft.get("subject", "")

    word_count = len(body.split())
    limit = WORD_LIMITS.get(channel, 200)
    if word_count > limit:
        score -= 15
        flags.append(f"too_long:{word_count}_words_limit_{limit}")

    if language == "ar":
        for flag_name, patterns in ARABIC_FAIL_PATTERNS:
            if flag_name == "no_opt_out":
                has_optout = any(p in body for p in patterns)
                if not has_optout:
                    score -= 10
                    flags.append("missing_arabic_opt_out")
                continue
            for pattern in patterns:
                if pattern in body or pattern in subject:
                    score -= 15
                    flags.append(f"arabic_fail:{flag_name}")
                    break
    else:
        for flag_name, patterns in ENGLISH_FAIL_PATTERNS:
            if flag_name == "too_long":
                continue
            if flag_name == "no_opt_out":
                has_optout = any(p in body.lower() for p in patterns)
                if not has_optout:
                    score -= 10
                    flags.append("missing_english_opt_out")
                continue
            for pattern in patterns:
                if pattern.lower() in body.lower() or pattern.lower() in subject.lower():
                    score -= 15
                    flags.append(f"english_fail:{flag_name}")
                    break

    has_cta = any(kw in body for kw in [
        "هل يناسبكم", "أرسل", "Would it be useful", "send a", "schedule", "call",
    ])
    if not has_cta:
        score -= 15
        flags.append("missing_cta")

    company_name = draft.get("company", "")
    if company_name and company_name not in body and company_name not in subject:
        score -= 10
        flags.append("company_not_mentioned")

    score = max(0, min(100, score))

    return {
        "score": score,
        "flags": flags,
        "pass": score >= 70,
        "reason": "; ".join(flags) if flags else None,
    }
