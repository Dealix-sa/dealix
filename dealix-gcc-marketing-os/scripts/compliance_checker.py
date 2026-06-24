"""
Compliance gate — GCC multi-country rules validation.
Returns score 0-100 and flags for non-compliant patterns.
"""

from __future__ import annotations

HIGH_RISK_PATTERNS = [
    "we have your data",
    "we found your information",
    "we know that your company",
    "from our database",
    "our records show",
    "we scraped",
    "we collected your",
]

SENSITIVE_SECTOR_REQUIRED = ["confidentiality", "privacy", "secure", "سرية", "خصوصية", "آمن"]

COUNTRY_HIGH_CONSENT_REQUIRED = {"qatar", "oman", "saudi_arabia"}


def run_compliance_check(draft: dict) -> dict:
    """Evaluate a draft dict against GCC compliance rules and return score, flags, and reason."""
    score = 100
    flags: list[str] = []

    body: str = draft.get("body", "")
    subject: str = draft.get("subject", "")
    country: str = draft.get("country", "")
    sector: str = draft.get("sector", "")
    language: str = draft.get("language", "en")
    full_text = (body + " " + subject).lower()

    for pattern in HIGH_RISK_PATTERNS:
        if pattern in full_text:
            score -= 25
            flags.append(f"data_sourcing_claim:{pattern}")

    opt_out_signals = [
        "أقدر أوقف المتابعة",
        "إلغاء الاشتراك",
        "happy to stop",
        "unsubscribe",
        "opt out",
        "stop following up",
    ]
    has_opt_out = any(s in body for s in opt_out_signals)
    if not has_opt_out:
        score -= 20
        flags.append("missing_opt_out")

    if sector in ("legal", "healthcare_admin", "financial_services", "government_related"):
        has_privacy_signal = any(s in full_text for s in SENSITIVE_SECTOR_REQUIRED)
        if not has_privacy_signal:
            score -= 15
            flags.append(f"sensitive_sector_missing_privacy_language:{sector}")

    if country in COUNTRY_HIGH_CONSENT_REQUIRED:
        if "production data" in full_text or "your current data" in full_text:
            score -= 20
            flags.append(f"high_consent_country_data_reference:{country}")

    deceptive_patterns = [
        ("fake_urgency", ["last chance", "expires today", "only 3 spots"]),
        ("fake_familiarity", ["as we discussed", "following our conversation", "per our chat"]),
    ]
    for flag_name, patterns in deceptive_patterns:
        for p in patterns:
            if p in full_text:
                score -= 20
                flags.append(f"deceptive:{flag_name}")
                break

    score = max(0, min(100, score))
    return {
        "score": score,
        "flags": flags,
        "pass": score >= 70,
        "reason": "; ".join(flags) if flags else None,
    }
