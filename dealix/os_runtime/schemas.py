"""
schemas.py — Pydantic models for Dealix OS Runtime entities.

Covers:
  - OfferTier, Market, ScoringConfig, ApprovalGate (core OS)
  - Channel, AntibanRule, PersuasionDossier, DraftQueueItem (growth OS)
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field, model_validator


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------


class OfferCategory(str, Enum):
    entry = "entry"
    pilot = "pilot"
    vertical_system = "vertical_system"
    governance = "governance"
    retainer = "retainer"
    expansion = "expansion"


class ScoringTier(str, Enum):
    priority_high = "priority_high"
    priority_medium = "priority_medium"
    nurture = "nurture"
    disqualified = "disqualified"


class ChannelName(str, Enum):
    Email = "Email"
    WhatsApp_opt_in = "WhatsApp_opt_in"
    LinkedIn_manual = "LinkedIn_manual"
    Meta_inbound = "Meta_inbound"
    TikTok_lead_forms = "TikTok_lead_forms"
    Google_lead_ads = "Google_lead_ads"
    Website_form = "Website_form"
    Phone_calls = "Phone_calls"
    Partners = "Partners"
    Referrals = "Referrals"
    Webinars = "Webinars"
    Procurement_portals = "Procurement_portals"


class CountryCode(str, Enum):
    SA = "SA"
    AE = "AE"
    KW = "KW"
    QA = "QA"
    BH = "BH"
    OM = "OM"
    EG = "EG"
    JO = "JO"


class Language(str, Enum):
    ar = "ar"
    en = "en"
    bilingual = "bilingual"


class DraftStatus(str, Enum):
    draft = "draft"
    pending_approval = "pending_approval"
    approved = "approved"
    rejected = "rejected"
    sent = "sent"
    failed = "failed"
    archived = "archived"


class RiskLevel(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


# ---------------------------------------------------------------------------
# Governance Decision (doctrine requirement on all output objects)
# ---------------------------------------------------------------------------


class GovernanceDecision(BaseModel):
    approved: bool | None = None
    reviewed_by: str | None = None
    reviewed_at: datetime | None = None
    notes: str | None = None
    no_live_action: bool = True
    requires_founder_approval_before_send: bool = True


# ---------------------------------------------------------------------------
# Core OS models
# ---------------------------------------------------------------------------


class PriceSAR(BaseModel):
    min: float | None = None
    max: float | None = None
    typical: float | None = None
    note: str | None = None


class Deliverable(BaseModel):
    id: str | None = None
    name: str
    description: str | None = None


class OfferTier(BaseModel):
    """A single Dealix offer from os/03_OFFERS.yml"""

    id: str
    name: str
    name_ar: str | None = None
    tagline: str | None = None
    category: OfferCategory
    price_sar: PriceSAR | None = None
    price_sar_monthly: PriceSAR | None = None
    duration_days: dict[str, int] | None = None
    best_for: list[str] = Field(default_factory=list)
    not_for: list[str] = Field(default_factory=list)
    deliverables: list[Deliverable | str] = Field(default_factory=list)
    natural_next_offer: str | None = None
    sales_angle: str | None = None


class Market(BaseModel):
    """A target market from os/04_MARKETS.yml"""

    id: str
    name: str
    name_ar: str | None = None
    priority: int
    why_dealix_fits: str | None = None
    typical_companies: list[str] = Field(default_factory=list)
    typical_pain_points: list[str] = Field(default_factory=list)
    best_buyer_titles: list[str] = Field(default_factory=list)
    recommended_entry_offer: str | None = None
    natural_upsell: str | None = None


class ScoringDimensionLevel(BaseModel):
    score: int
    indicators: list[str] = Field(default_factory=list)


class ScoringDimension(BaseModel):
    weight: int
    name: str
    description: str | None = None
    levels: dict[str, ScoringDimensionLevel] = Field(default_factory=dict)


class DecisionThreshold(BaseModel):
    min_score: int | None = None
    max_score: int | None = None
    action: str
    color: str | None = None


class ScoringConfig(BaseModel):
    """Scoring system from os/05_SCORING.yml"""

    version: str
    max_score: int
    scoring_dimensions: dict[str, ScoringDimension] = Field(default_factory=dict)
    decision_thresholds: dict[str, DecisionThreshold] = Field(default_factory=dict)

    @model_validator(mode="after")
    def weights_sum_to_100(self) -> "ScoringConfig":
        total = sum(d.weight for d in self.scoring_dimensions.values())
        if total != 100:
            raise ValueError(
                f"Scoring dimension weights must sum to 100, got {total}"
            )
        return self


class ApprovalGate(BaseModel):
    """A single approval gate from os/06_APPROVAL_GATES.yml"""

    id: str
    name: str
    requires_human_approval: bool
    reason: str | None = None
    what_agent_can_do: list[str] = Field(default_factory=list)
    what_requires_approval: list[str] = Field(default_factory=list)
    approval_checklist: list[str] = Field(default_factory=list)
    allowed: bool | None = None
    note: str | None = None
    escalation: str | None = None


# ---------------------------------------------------------------------------
# Growth OS models
# ---------------------------------------------------------------------------


class Channel(BaseModel):
    """A channel definition from os/growth/CHANNEL_ROUTER.yml"""

    priority: int
    type: str
    approval_required: bool
    conditions: list[str] = Field(default_factory=list)
    template_type: str | None = None
    expected_response_rate: float | None = None
    anti_ban_rules: list[str] = Field(default_factory=list)
    notes: str | None = None


class AntibanRule(BaseModel):
    """Anti-ban rules from os/growth/ANTI_BAN_GUARDIAN.yml"""

    daily_limit: int
    hourly_limit: int
    min_interval_seconds: int
    required_opt_in: bool
    forbidden_patterns: list[str] = Field(default_factory=list)
    warning_thresholds: dict[str, int] = Field(default_factory=dict)
    circuit_breaker_conditions: list[str] = Field(default_factory=list)
    compliance_notes: list[str] = Field(default_factory=list)


class MessagePack(BaseModel):
    subject_line: str
    opening_ar: str | None = None
    opening_en: str | None = None
    value_prop_ar: str | None = None
    value_prop_en: str | None = None
    cta_ar: str | None = None
    cta_en: str | None = None


class PersuasionDossier(BaseModel):
    """
    A persuasion dossier for a single B2B target company.
    Conforms to os/growth/PERSUASION_DOSSIER_SCHEMA.json.

    Doctrine: governance_decision is MANDATORY on all output objects.
    """

    company: str
    country: CountryCode
    sector: str
    buyer_persona: str
    likely_pain: list[str] = Field(min_length=1)
    trust_angle: str
    best_offer: str
    best_channel: ChannelName
    message_pack: MessagePack
    language: Language = Language.bilingual
    company_size: str | None = None
    annual_revenue_sar: float | None = None
    decision_maker_title: str | None = None
    risk_angle: str | None = None
    proof_asset: str | None = None
    objections_expected: list[str] = Field(default_factory=list)
    objection_responses: dict[str, str] = Field(default_factory=dict)
    persuasion_score: float | None = Field(default=None, ge=0, le=100)
    created_at: datetime | None = None
    scored_at: datetime | None = None
    governance_decision: GovernanceDecision = Field(
        default_factory=GovernanceDecision,
        description="Mandatory governance field — doctrine requirement",
    )


class DraftQueueItem(BaseModel):
    """
    A single outreach draft in the approval queue.
    Conforms to os/growth/DRAFT_QUEUE_SCHEMA.json.

    Doctrine: requires_approval is always True for outbound channels.
    """

    draft_id: str
    company_id: str
    channel: ChannelName
    offer_tier: str
    language: Language
    status: DraftStatus = DraftStatus.pending_approval
    requires_approval: bool = True
    company_name: str | None = None
    subject_line: str | None = None
    body_ar: str | None = None
    body_en: str | None = None
    persuasion_score: float | None = Field(default=None, ge=0, le=100)
    risk_level: RiskLevel = RiskLevel.medium
    created_at: datetime | None = None
    submitted_for_approval_at: datetime | None = None
    approved_at: datetime | None = None
    approved_by: str | None = None
    rejected_at: datetime | None = None
    rejection_reason: str | None = None
    sent_at: datetime | None = None
    source_dossier_id: str | None = None
    anti_ban_checked: bool = False
    governance_decision: GovernanceDecision = Field(
        default_factory=GovernanceDecision,
        description="Mandatory governance field — doctrine requirement",
    )

    @model_validator(mode="after")
    def outbound_always_requires_approval(self) -> "DraftQueueItem":
        outbound_channels = {
            ChannelName.Email,
            ChannelName.WhatsApp_opt_in,
            ChannelName.LinkedIn_manual,
            ChannelName.Phone_calls,
        }
        if self.channel in outbound_channels and not self.requires_approval:
            raise ValueError(
                f"Channel '{self.channel}' requires approval — "
                f"requires_approval cannot be False for outbound channels"
            )
        return self


# ---------------------------------------------------------------------------
# Scoring output
# ---------------------------------------------------------------------------


class DimensionScore(BaseModel):
    dimension_id: str
    score: int
    level: str
    max: int


class CompanyScoringResult(BaseModel):
    """Result of scoring a company with os/05_SCORING.yml dimensions."""

    company_name: str
    total_score: int
    tier: ScoringTier
    dimension_scores: list[DimensionScore] = Field(default_factory=list)
    top_strengths: list[str] = Field(default_factory=list)
    top_weaknesses: list[str] = Field(default_factory=list)
    recommended_offer: str | None = None
    next_action: str | None = None
    scored_at: datetime | None = None
    scored_by: str = "dealix.os_runtime"
    governance_decision: GovernanceDecision = Field(
        default_factory=GovernanceDecision,
        description="Mandatory governance field — doctrine requirement",
    )
