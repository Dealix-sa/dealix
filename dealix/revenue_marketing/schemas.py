"""Pydantic models for the Revenue Marketing Engine.

Mirrors the SQL contract (see migrations/versions/20260525_014_revenue_marketing.py):
campaigns, marketing_touches, revenue_attribution, marketing_experiments.

All records are draft-first. Nothing in this layer triggers external sends.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

CampaignStatus = Literal["draft", "approval_pending", "live", "paused", "killed", "scaled"]
ChannelKind = Literal[
    "linkedin",
    "x",
    "email_newsletter",
    "direct_outreach",
    "workshop",
    "paid_search",
    "paid_social",
    "partner",
    "podcast",
    "event",
    "landing_page",
    "referral",
    "content_syndication",
]
TouchKind = Literal[
    "impression",
    "engagement",
    "click",
    "form_submit",
    "reply",
    "meeting_booked",
    "proposal_sent",
    "won",
    "lost",
    "payment",
]
AttributionType = Literal["first_touch", "last_touch", "multi_touch", "asset_influenced", "agent_influenced"]
ExperimentStatus = Literal["draft", "running", "decided_scale", "decided_kill", "inconclusive"]
OfferTier = Literal["free", "entry", "core", "expansion", "enterprise"]
SignalSource = Literal[
    "founder_observation",
    "customer_interview",
    "war_room_lead",
    "support_ticket",
    "partner",
    "market_report",
    "regulatory",
    "social_listening_manual",
]


class MarketSignalRecord(BaseModel):
    """A market signal — founder-provided or sourced through governed channels.

    Never scraped. Maps to /api/v1/revenue-os/signals/normalize input shape.
    """

    model_config = ConfigDict(extra="forbid")

    id: str
    source: SignalSource
    summary_ar: str
    summary_en: str = ""
    segment: str
    pain: str
    suggested_offer_id: str = ""
    why_now: str = ""
    proof_target: str = ""
    confidence: float = Field(default=0.5, ge=0.0, le=1.0)
    captured_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class OfferRecord(BaseModel):
    """A revenue offer on the 5-rung ladder (free → enterprise)."""

    model_config = ConfigDict(extra="forbid")

    id: str
    name_ar: str
    name_en: str
    tier: OfferTier
    price_min_sar: float = 0
    price_max_sar: float = 0
    promise_ar: str
    deliverables_ar: list[str] = Field(default_factory=list)
    target_segments: list[str] = Field(default_factory=list)
    primary_pain: str = ""
    success_metric: str = ""
    money_quality: float = Field(default=0.5, ge=-1.0, le=2.0)
    active: bool = True


class CampaignRecord(BaseModel):
    """A Revenue Marketing campaign — every field that gates the quality check."""

    model_config = ConfigDict(extra="forbid")

    id: str
    campaign_name: str
    target_segment: str
    offer_id: str
    channel: ChannelKind
    message_angle: str = ""
    cta_label_ar: str = ""
    cta_path: str = ""
    success_metric: str = ""
    scale_kill_rule: str = ""
    budget_sar: float = 0
    status: CampaignStatus = "draft"
    signal_id: str | None = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class MarketingTouchRecord(BaseModel):
    """A single touch — used to build attribution chains."""

    model_config = ConfigDict(extra="forbid")

    id: str
    campaign_id: str | None = None
    lead_id: str | None = None
    touch_type: TouchKind
    channel: ChannelKind | None = None
    content_id: str | None = None
    asset_id: str | None = None
    agent_id: str | None = None
    message_variant: str = ""
    occurred_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class RevenueAttributionRecord(BaseModel):
    """Revenue tied to a deal — only created after payment_received or signed_agreement."""

    model_config = ConfigDict(extra="forbid")

    id: str
    revenue_sar: float = Field(..., ge=0)
    deal_id: str
    primary_source: str
    secondary_source: str = ""
    campaign_id: str | None = None
    offer_id: str | None = None
    channel: ChannelKind | None = None
    asset_ids: list[str] = Field(default_factory=list)
    agent_ids: list[str] = Field(default_factory=list)
    influenced_by: list[str] = Field(default_factory=list)
    attribution_type: AttributionType = "multi_touch"
    payment_confirmed: bool = True
    money_quality: float = Field(default=0.5, ge=-1.0, le=2.0)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class MarketingExperimentRecord(BaseModel):
    """A single-variable marketing experiment with explicit decision rule."""

    model_config = ConfigDict(extra="forbid")

    id: str
    experiment_name: str
    target_segment: str
    offer_id: str
    variable_tested: str
    variant_a: str
    variant_b: str
    success_metric: str
    minimum_sample: int = 50
    decision_rule: str
    samples_a: int = 0
    samples_b: int = 0
    wins_a: int = 0
    wins_b: int = 0
    status: ExperimentStatus = "draft"
    result: dict[str, Any] = Field(default_factory=dict)
    decision: str = ""
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class ContentCardRecord(BaseModel):
    """A content idea bound to a target segment, pain, offer, CTA and metric."""

    model_config = ConfigDict(extra="forbid")

    id: str
    topic_ar: str
    target_segment: str
    pain: str
    offer_id: str
    cta_ar: str
    channel: ChannelKind
    success_metric: str = "leads_booked"
    pillar: str = ""
    status: Literal["idea", "drafted", "approved", "published"] = "idea"
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class FunnelSnapshotRecord(BaseModel):
    """A point-in-time snapshot of conversion stages used by the dashboard."""

    model_config = ConfigDict(extra="forbid")

    id: str
    captured_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    visitors: int = 0
    leads: int = 0
    qualified_leads: int = 0
    calls_booked: int = 0
    proposals_sent: int = 0
    won: int = 0
    lost: int = 0
    paid: int = 0
    retainers: int = 0
    period_label: str = ""
