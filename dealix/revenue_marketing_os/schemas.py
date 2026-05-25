"""
Pydantic models for Revenue Marketing OS (Hermes growth tables).

Every record in this module is a node in the Money Loop:

    Market Signal → ICP → Offer → Message → Campaign → Channel →
    Lead → Touch → Deal → Revenue → Attribution → Outcome → Learning.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

# ── Type aliases ────────────────────────────────────────────────────

LeadStatus = Literal[
    "new",
    "mql",
    "sql",
    "discovery_booked",
    "discovery_done",
    "proposal_sent",
    "closed_won",
    "closed_lost",
    "nurture",
]

CampaignStatus = Literal[
    "draft",
    "approval_pending",
    "active",
    "paused",
    "killed",
    "scaled",
]

RevenueStatus = Literal[
    "influenced",
    "pipeline",
    "proposal_sent",
    "committed",
    "invoiced",
    "paid",
    "retainer_active",
    "renewed",
    "expanded",
]

AttributionType = Literal[
    "first_touch",
    "last_touch",
    "multi_touch",
    "asset_influenced",
    "agent_influenced",
    "partner_influenced",
    "campaign_influenced",
    "channel_influenced",
]

ChannelKind = Literal[
    "direct_outreach",
    "linkedin",
    "x",
    "warm_intro",
    "referral",
    "inbound_dm",
    "partner",
    "content",
    "landing",
    "webinar",
    "workshop",
    "email_nurture",
    "paid_search",
    "paid_social",
    "geo_ai_search",
]

ScaleDecision = Literal["scale", "pause", "kill", "hold", "reprice", "reposition"]


# ── ICP ─────────────────────────────────────────────────────────────


class ICPRecord(BaseModel):
    """Ideal Customer Profile card. Drives every campaign + message."""

    model_config = ConfigDict(extra="forbid")

    id: str
    name: str = Field(..., min_length=1)
    buyer: str = ""
    pain: str = ""
    ability_to_pay: Literal["low", "medium", "medium_high", "high"] = "medium"
    urgency: Literal["low", "medium", "high"] = "medium"
    best_offer_id: str = ""
    best_channel: ChannelKind = "direct_outreach"
    message_angle: str = ""
    entry_offer_id: str = ""
    expansion_offer_id: str = ""
    notes_ar: str = ""
    notes_en: str = ""
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


# ── Offer ───────────────────────────────────────────────────────────


class OfferRecord(BaseModel):
    """Productized offer card. Every campaign must point to one."""

    model_config = ConfigDict(extra="forbid")

    id: str
    name: str = Field(..., min_length=1)
    tier: Literal["free", "entry", "core", "expansion", "enterprise", "platform"] = "core"
    ladder_step: int = Field(default=2, ge=0, le=10)
    starting_price_sar: float = 0.0
    repeatability: float = Field(default=0.5, ge=0.0, le=1.0)
    margin: float = Field(default=0.5, ge=0.0, le=1.0)
    retainer_potential: float = Field(default=0.5, ge=0.0, le=1.0)
    data_moat: float = Field(default=0.3, ge=0.0, le=1.0)
    partner_potential: float = Field(default=0.3, ge=0.0, le=1.0)
    delivery_burden: float = Field(default=0.3, ge=0.0, le=1.0)
    notes_ar: str = ""
    notes_en: str = ""
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


# ── Message angle ───────────────────────────────────────────────────


class MessageRecord(BaseModel):
    """A registered message angle to be tested against a target ICP/offer."""

    model_config = ConfigDict(extra="forbid")

    id: str
    offer_id: str
    icp_id: str
    angle: str = Field(..., min_length=1)
    body_draft_ar: str = ""
    body_draft_en: str = ""
    requires_trust_check: bool = True
    trust_check_passed: bool = False
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


# ── Campaign ────────────────────────────────────────────────────────


class CampaignRecord(BaseModel):
    """The unit of revenue-marketing execution."""

    model_config = ConfigDict(extra="forbid")

    id: str
    name: str = Field(..., min_length=1)
    target_icp_id: str = ""
    target_segment: str = ""
    pain: str = ""
    offer_id: str = ""
    message_id: str = ""
    message_angle: str = ""
    channel: ChannelKind = "direct_outreach"
    cta: str = ""
    success_metric: str = "paid_diagnostics"
    target_accounts: int = 100
    tracking_enabled: bool = True
    scale_rule: str = ""
    kill_rule: str = ""
    status: CampaignStatus = "draft"
    approval_required: bool = True
    approved_by: str | None = None
    approved_at: datetime | None = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


# ── Lead ────────────────────────────────────────────────────────────


class LeadRecord(BaseModel):
    """Lead inside a campaign funnel. Every lead must have a source."""

    model_config = ConfigDict(extra="forbid")

    id: str
    campaign_id: str = ""
    source: str = Field(..., min_length=1)
    company_name: str = ""
    contact_name: str = ""
    contact_email: str = ""
    contact_role: str = ""
    icp_id: str = ""
    fit_score: int = Field(default=0, ge=0, le=100)
    score_breakdown: dict[str, int] = Field(default_factory=dict)
    pain_hypothesis: str = ""
    status: LeadStatus = "new"
    consent_marketing: bool = False
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


# ── Touch ───────────────────────────────────────────────────────────


class TouchRecord(BaseModel):
    """A single interaction in the funnel. Every touch has an outcome."""

    model_config = ConfigDict(extra="forbid")

    id: str
    lead_id: str
    campaign_id: str = ""
    channel: ChannelKind = "direct_outreach"
    touch_type: Literal[
        "outbound_draft",
        "outbound_sent_manual",
        "inbound_reply",
        "call_booked",
        "call_done",
        "proposal_sent",
        "asset_delivered",
        "follow_up",
    ] = "outbound_draft"
    message_variant: str = ""
    outcome: str = ""
    next_action: str = ""
    occurred_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


# ── Revenue ─────────────────────────────────────────────────────────


class RevenueRecord(BaseModel):
    """
    Verified revenue, not noise.

    Likes/views/replies do NOT count. Only ``paid`` /
    ``retainer_active`` /  ``invoiced`` (with proof) are real.
    """

    model_config = ConfigDict(extra="forbid")

    id: str
    amount_sar: float = Field(..., ge=0.0)
    status: RevenueStatus = "pipeline"
    source_offer_id: str = ""
    customer_id: str = ""
    lead_id: str = ""
    deal_id: str = ""
    campaign_id: str = ""
    channel: ChannelKind = "direct_outreach"
    payment_verified: bool = False
    invoice_verified: bool = False
    agreement_signed: bool = False
    received_at: datetime | None = None
    margin: float = Field(default=0.5, ge=0.0, le=1.0)
    repeatability: float = Field(default=0.5, ge=0.0, le=1.0)
    retainer_potential: float = Field(default=0.5, ge=0.0, le=1.0)
    data_moat: float = Field(default=0.3, ge=0.0, le=1.0)
    partner_potential: float = Field(default=0.3, ge=0.0, le=1.0)
    delivery_burden: float = Field(default=0.3, ge=0.0, le=1.0)
    quality_score: float = 0.0
    notes: str = ""
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


# ── Attribution ─────────────────────────────────────────────────────


class AttributionRecord(BaseModel):
    """
    Link a revenue event to the assets/agents/partners/campaigns that
    influenced it. One revenue event MAY produce multiple attribution
    rows (e.g. first_touch + last_touch + asset_influenced).
    """

    model_config = ConfigDict(extra="forbid")

    id: str
    revenue_id: str
    deal_id: str = ""
    campaign_id: str = ""
    lead_id: str = ""
    offer_id: str = ""
    channel: ChannelKind = "direct_outreach"
    attribution_type: AttributionType = "multi_touch"
    asset_ids: list[str] = Field(default_factory=list)
    agent_ids: list[str] = Field(default_factory=list)
    partner_ids: list[str] = Field(default_factory=list)
    weight: float = Field(default=1.0, ge=0.0, le=1.0)
    amount_sar: float = 0.0
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


# ── Experiment ──────────────────────────────────────────────────────


class ExperimentRecord(BaseModel):
    """A registered A/B / message-angle / channel experiment."""

    model_config = ConfigDict(extra="forbid")

    id: str
    campaign_id: str = ""
    hypothesis: str = Field(..., min_length=1)
    variants: list[str] = Field(default_factory=list)
    success_metric: str = "paid_diagnostics"
    target_sample: int = 100
    current_sample: int = 0
    winner_variant: str | None = None
    status: Literal["running", "paused", "stopped", "concluded"] = "running"
    learning_note: str = ""
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


# ── Scale/Kill decision ─────────────────────────────────────────────


class ScaleKillDecision(BaseModel):
    """Auto-suggested decision; founder still approves before any action."""

    model_config = ConfigDict(extra="forbid")

    campaign_id: str
    decision: ScaleDecision
    reason_ar: str = ""
    reason_en: str = ""
    metrics_snapshot: dict[str, float] = Field(default_factory=dict)
    next_action: str = ""
    requires_founder_approval: bool = True
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
