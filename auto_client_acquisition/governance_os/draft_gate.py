"""Draft and intake governance helpers (delegates to Revenue OS anti-waste where useful)."""

from __future__ import annotations

import re

from auto_client_acquisition.revenue_os.anti_waste import validate_pipeline_step
from auto_client_acquisition.revenue_os.source_registry import Tier1LeadSource

# Deceptive subject prefixes — faking a reply/forward thread on cold outreach
# is misleading and forbidden. Matched only at the start of the (stripped) text.
_FAKE_THREAD_PREFIX = re.compile(r"^\s*(re|fwd|fw)\s*:", re.IGNORECASE)


def audit_draft_text(text: str) -> list[str]:
    """
    Flag risky phrases in **draft** marketing or outreach copy.

    This is a shallow guardrail — human review remains mandatory.
    """
    issues: list[str] = []
    blob = text.lower()

    # Deceptive "Re:" / "Fwd:" subject lines on cold outreach.
    if _FAKE_THREAD_PREFIX.match(text):
        issues.append("misleading_subject:fake_reply_or_forward")

    forbidden_terms = (
        "scraping",
        "scrape ",
        "purchased list",
        "cold whatsapp",
        "bulk whatsapp",
        "whatsapp blast",
        "mass whatsapp",
        "linkedin automation",
        "auto-send",
        "auto send",
        "send automatically without approval",
    )
    for term in forbidden_terms:
        if term in blob:
            issues.append(f"forbidden_term:{term}")
    guarantee_or_misrep = (
        "guaranteed sales",
        "guaranteed results",
        "guaranteed roi",
        "guarantee roi",
        "نضمن لك",
        "نضمن لكم",
        "نضمن النتائج",
        "نضمن لك مبيعات",
        "مضمون",
        "fake proof",
        "fake testimonial",
    )
    for term in guarantee_or_misrep:
        if term in blob:
            issues.append(f"forbidden_claim:{term}")

    # Broader guarantee / risk-free / inflated-promise detection. Any standalone
    # "guarantee"/"guaranteed", "risk-free", or "promise <N>x" claim is a
    # forbidden marketing claim even when it doesn't match the exact phrases
    # above (e.g. "We guarantee 10x ROI", "Guaranteed to double your sales").
    guarantee_patterns = (
        r"\bguarantee[ds]?\b",
        r"\brisk[\s-]*free\b",
        r"\bpromise[ds]?\s+\d+\s*x\b",
        r"\bpromise[ds]?\b.*\b(revenue|sales|results?|roi|double|triple|increase|growth|leads?)\b",
        r"\b100%\s+(risk[\s-]*free|guaranteed)\b",
    )
    for pattern in guarantee_patterns:
        if re.search(pattern, blob):
            issues.append(f"forbidden_claim:{pattern}")

    # De-duplicate while preserving order.
    return list(dict.fromkeys(issues))



def intake_violations_for_source(lead_source: str) -> list[str]:
    """Anti-waste intake check on a lead source string (e.g. Tier1 value)."""
    vio = validate_pipeline_step(
        has_decision_passport=False,
        lead_source=lead_source,
        action_external=False,
        upsell_attempt=False,
        proof_event_count=0,
        evidence_level_for_public=0,
        public_marketing_attempt=False,
        feature_request_count=0,
    )
    if vio:
        return [f"{v.code}:{v.detail_en}" for v in vio]
    try:
        Tier1LeadSource(lead_source)
    except ValueError:
        return [f"unknown_tier1_source:{lead_source}"]
    return []
