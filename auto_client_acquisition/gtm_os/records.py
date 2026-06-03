"""GTM data records — prospects, founder-input signals, replies, suppression.

All records are PII-free: companies are labels + public domains, people are
*roles* not names, recipients are opaque refs. Signals are **founder-input or
public** observations — there is no scraping anywhere in this module (doctrine
non-negotiable #1). Helpers encode the plan's scoring + reply-routing rules so
they are testable rather than prose.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

# ---------------------------------------------------------------------------
# Signals (founder-input / public only — never scraped)
# ---------------------------------------------------------------------------
SIGNAL_TYPES: tuple[str, ...] = (
    "hiring_sales_ops",
    "hiring_crm_manager",
    "hiring_marketing",
    "hiring_support",
    "new_branch",
    "website_update",
    "booking_link",
    "new_ad_spend",
    "funding",
    "event_attendance",
    "partnership",
    "product_launch",
    "tender",
    "review_change",
    "headcount_growth",
    "slow_reply",
)
SIGNAL_SOURCES: tuple[str, ...] = (
    "founder_input",
    "public_post",
    "public_job_board",
    "customer_referral",
    "event",
    "inbound",
)


class CompanySignal(BaseModel):
    """A buying-timing signal observed by the founder or from public data."""

    model_config = ConfigDict(extra="forbid")

    signal_id: str
    observed_at: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())
    company_label: str = ""
    sector: str = ""
    signal_type: str = ""  # one of SIGNAL_TYPES (validated by the gate/report)
    source: str = "founder_input"  # one of SIGNAL_SOURCES — never "scraping"
    evidence_note: str = ""
    strength: Literal["low", "medium", "high"] = "medium"
    suggested_offer: str = ""
    suggested_angle_ar: str = ""
    suggested_angle_en: str = ""
    governance_decision: str = "approval_required"


# ---------------------------------------------------------------------------
# Prospects + scoring (plan §7 weights)
# ---------------------------------------------------------------------------
PROSPECT_SCORE_WEIGHTS: dict[str, int] = {
    "sector_fit": 20,
    "buying_signal": 20,
    "lead_flow_likelihood": 15,
    "decision_maker_clarity": 15,
    "payment_ability": 15,
    "personalization_signal": 10,
    "risk_low": 5,
}


class Prospect(BaseModel):
    """A qualified company record. No personal data — roles + public domains."""

    model_config = ConfigDict(extra="forbid")

    prospect_ref: str
    company_label: str = ""
    website_domain: str = ""  # company domain (not personal data)
    sector: str = ""
    region: str = "Saudi Arabia"
    source: str = "founder_input"
    signal_ref: str = ""
    decision_maker_role: str = ""  # a role, never a name
    pain_hypothesis: str = ""
    offer_match: str = ""
    personalization_note: str = ""
    risk_level: Literal["low", "medium", "high"] = "low"
    evidence_level: str = "L1"
    status: Literal[
        "new", "researching", "drafted", "queued", "contacted", "replied", "nurture", "do_not_contact"
    ] = "new"
    next_action: str = ""
    score: float = 0.0
    score_tier: str = "C"
    governance_decision: str = "approval_required"


def score_prospect(
    *,
    sector_fit: float,
    buying_signal: float,
    lead_flow_likelihood: float,
    decision_maker_clarity: float,
    payment_ability: float,
    personalization_signal: float,
    risk_low: float,
) -> dict[str, object]:
    """Weighted 0–100 prospect score. Each component is a 0..1 confidence."""
    components = {
        "sector_fit": sector_fit,
        "buying_signal": buying_signal,
        "lead_flow_likelihood": lead_flow_likelihood,
        "decision_maker_clarity": decision_maker_clarity,
        "payment_ability": payment_ability,
        "personalization_signal": personalization_signal,
        "risk_low": risk_low,
    }
    breakdown = {
        name: round(max(0.0, min(1.0, value)) * PROSPECT_SCORE_WEIGHTS[name], 2)
        for name, value in components.items()
    }
    total = round(sum(breakdown.values()), 2)
    tier = "A" if total >= 70 else "B" if total >= 50 else "C"
    return {"total": total, "tier": tier, "breakdown": breakdown}


# ---------------------------------------------------------------------------
# Replies + routing (plan §13)
# ---------------------------------------------------------------------------
REPLY_CLASSES: tuple[str, ...] = (
    "positive",
    "interested_later",
    "price_question",
    "send_more_info",
    "wrong_person",
    "not_interested",
    "unsubscribe",
    "angry",
    "auto_reply",
    "bounce",
)

# classification -> (action_id, suppress?, bilingual action)
_REPLY_ROUTING: dict[str, tuple[str, bool, str, str]] = {
    "positive": ("route_to_discovery", False, "حوّل إلى مكالمة/واتساب بعد الموافقة", "Route to discovery / WhatsApp after consent"),
    "interested_later": ("nurture", False, "ضعه في التنشئة (nurture)", "Move to nurture"),
    "price_question": ("send_offer_card", False, "أرسل بطاقة العرض", "Send the offer card"),
    "send_more_info": ("send_proof_pack", False, "أرسل حزمة الإثبات", "Send the proof pack"),
    "wrong_person": ("ask_referral", False, "اطلب تحويلًا للشخص الصحيح", "Ask for a referral"),
    "not_interested": ("close_polite", False, "أغلق بأدب", "Close politely"),
    "unsubscribe": ("suppress_now", True, "كبح فوري", "Suppress immediately"),
    "angry": ("apologize_and_suppress", True, "اعتذار + كبح", "Apologize + suppress"),
    "auto_reply": ("hold", False, "انتظر/تجاهل", "Hold / ignore"),
    "bounce": ("suppress_now", True, "كبح (ارتداد)", "Suppress (bounce)"),
}


class Reply(BaseModel):
    """A classified inbound reply to an approved outreach send."""

    model_config = ConfigDict(extra="forbid")

    reply_id: str
    received_at: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())
    draft_ref: str = ""
    prospect_ref: str = ""
    classification: str = ""  # one of REPLY_CLASSES
    suggested_action: str = ""
    requires_suppression: bool = False
    next_step_ar: str = ""
    next_step_en: str = ""
    governance_decision: str = "approval_required"


def route_reply(classification: str) -> dict[str, object]:
    """Map a reply classification to its next action (plan §13)."""
    action, suppress, ar, en = _REPLY_ROUTING.get(
        classification, ("manual_review", False, "مراجعة يدوية", "Manual review")
    )
    return {
        "classification": classification,
        "suggested_action": action,
        "requires_suppression": suppress,
        "next_step_ar": ar,
        "next_step_en": en,
    }


# ---------------------------------------------------------------------------
# Suppression
# ---------------------------------------------------------------------------
SUPPRESSION_REASONS: tuple[str, ...] = ("unsubscribe", "complaint", "bounce", "angry", "manual")


class SuppressionEntry(BaseModel):
    """A recipient that must never be contacted again (opaque ref only)."""

    model_config = ConfigDict(extra="forbid")

    recipient_ref: str
    reason: str = "manual"  # one of SUPPRESSION_REASONS
    added_at: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())
    source: str = "founder"
    permanent: bool = True


__all__ = [
    "PROSPECT_SCORE_WEIGHTS",
    "REPLY_CLASSES",
    "SIGNAL_SOURCES",
    "SIGNAL_TYPES",
    "SUPPRESSION_REASONS",
    "CompanySignal",
    "Prospect",
    "Reply",
    "SuppressionEntry",
    "route_reply",
    "score_prospect",
]
