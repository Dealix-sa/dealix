"""Pydantic models for the Saudi Opportunity Command Room (local JSON persistence).

All models are draft-first: an OutreachDraft can only reach ``sent`` state
through explicit, human-attributed admin action (see ``pipeline`` and the
``opportunity_command_room`` router). Nothing here performs a live send.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

CompanyType = Literal[
    "foreign",
    "saudi",
    "government_related",
    "partner",
    "vendor",
    "unknown",
]

Segment = Literal[
    "foreign_saas_ai_entering_saudi",
    "foreign_supplier_needing_distributor",
    "saudi_clinic_revenue_leak",
    "saudi_training_or_b2b_service_growth",
    "b2g_readiness_candidate",
    "rhq_vendor_or_partner_candidate",
    "event_expo_tourism_supplier",
    "not_fit",
]

CompanyStatus = Literal[
    "new",
    "scored",
    "drafted",
    "approved",
    "contacted_manual",
    "replied",
    "hold",
    "not_fit",
]

Channel = Literal["linkedin", "email", "whatsapp_manual", "phone_script"]

Language = Literal["ar", "en"]

ApprovalStatus = Literal["pending", "approved", "rejected", "revise"]

# Score classification bands (see scoring.classify).
ScoreClass = Literal["hot", "warm", "research", "not_fit"]


def _utcnow() -> datetime:
    return datetime.now(UTC)


class OpportunitySignal(BaseModel):
    """A discrete market signal attached to a company (public, human-sourced)."""

    model_config = ConfigDict(extra="forbid")

    id: str
    company_id: str
    signal_type: str = ""
    signal_text: str = ""
    source_url: str = ""
    confidence: float = 0.5
    discovered_at: datetime = Field(default_factory=_utcnow)


class OpportunityCompany(BaseModel):
    """A scored company node in the Saudi Opportunity Graph."""

    model_config = ConfigDict(extra="forbid")

    id: str
    name: str = ""
    website: str = ""
    country: str = ""
    city: str = ""
    sector: str = ""
    company_type: CompanyType = "unknown"
    source: str = "manual_seed"
    source_url: str = ""
    saudi_signal: str = ""
    signal_type: str = ""
    signal_date: str = ""
    buyer_persona: str = ""
    pain_hypothesis: str = ""
    offer_match: str = ""
    estimated_deal_size: str = ""

    # Deterministic sub-scores (see scoring.score_company).
    fit_score: int = 0
    signal_score: int = 0
    urgency_score: int = 0
    value_score: int = 0
    accessibility_score: int = 0
    trust_risk_score: int = 0
    total_score: int = 0
    score_class: ScoreClass = "not_fit"
    score_breakdown: dict[str, int] = Field(default_factory=dict)

    segment: Segment = "not_fit"
    recommended_next_action: str = ""
    status: CompanyStatus = "new"
    consent_to_contact: bool = False

    created_at: datetime = Field(default_factory=_utcnow)
    updated_at: datetime = Field(default_factory=_utcnow)


class OutreachDraft(BaseModel):
    """A human-reviewable outreach draft. Never auto-sent."""

    model_config = ConfigDict(extra="forbid")

    id: str
    company_id: str
    persona: str = ""
    channel: Channel = "linkedin"
    language: Language = "ar"
    draft_text: str = ""
    personalization_notes: str = ""
    risk_notes: str = ""
    approval_status: ApprovalStatus = "pending"
    approved_by: str = ""
    approved_at: datetime | None = None
    sent_at: datetime | None = None
    human_sender: str = ""

    created_at: datetime = Field(default_factory=_utcnow)
    updated_at: datetime = Field(default_factory=_utcnow)


class DailyCommandReport(BaseModel):
    """Structured payload behind the daily markdown report."""

    model_config = ConfigDict(extra="forbid")

    date: str
    total_companies_scored: int = 0
    top_opportunities: list[dict] = Field(default_factory=list)
    top_foreign_entry: list[dict] = Field(default_factory=list)
    top_saudi_recovery: list[dict] = Field(default_factory=list)
    top_partner_candidates: list[dict] = Field(default_factory=list)
    b2g_watchlist: list[dict] = Field(default_factory=list)
    top_followups: list[dict] = Field(default_factory=list)
    risky_items: list[dict] = Field(default_factory=list)
    approved_drafts: int = 0
    pending_approvals: int = 0
    recommended_decisions: list[str] = Field(default_factory=list)
    tomorrow_actions: list[str] = Field(default_factory=list)
    proof_summary: str = ""
    generated_at: datetime = Field(default_factory=_utcnow)


class ProofPack(BaseModel):
    """Weekly evidence pack — no fabricated metrics, estimates flagged."""

    model_config = ConfigDict(extra="forbid")

    id: str
    client_id: str = ""
    period: str = ""
    before_state: str = ""
    actions_taken: list[str] = Field(default_factory=list)
    evidence_links: list[str] = Field(default_factory=list)
    metrics: dict[str, int] = Field(default_factory=dict)
    decisions: list[str] = Field(default_factory=list)
    next_steps: list[str] = Field(default_factory=list)
    acceptance_status: Literal["draft", "accepted", "revise"] = "draft"
    generated_at: datetime = Field(default_factory=_utcnow)
