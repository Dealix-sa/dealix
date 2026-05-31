"""Pydantic v2 models for the Dealix Revenue Marketing Engine.

Internal schemas are English. Customer-facing fields carry both AR + EN where the
artifact will be shown externally (offer name, message variant, case study).
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, computed_field

OfferRung = Literal["free", "entry", "core", "expansion", "enterprise"]
MessageStatus = Literal["draft", "approved", "retired"]
CampaignStatus = Literal[
    "draft",
    "approval_pending",
    "active",
    "paused",
    "killed",
    "completed",
]
ExperimentStatus = Literal["draft", "running", "decided"]
CaseStudyStatus = Literal["draft", "approved", "published"]
AttributionType = Literal[
    "first_touch",
    "last_touch",
    "multi_touch",
    "pipeline_only",
    "direct",
]

# Lead scoring weights (sum to 1.0).
LEAD_SCORE_WEIGHTS = {
    "icp_fit": 0.25,
    "pain": 0.20,
    "ability_to_pay": 0.20,
    "urgency": 0.15,
    "partner_potential": 0.10,
    "trust_fit": 0.10,
}


def _clamp01(value: float) -> float:
    return max(0.0, min(1.0, float(value)))


def compute_lead_score(
    icp_fit: float,
    pain: float,
    ability_to_pay: float,
    urgency: float,
    partner_potential: float,
    trust_fit: float,
) -> float:
    """Weighted lead score in [0, 1]. Weights sum to 1.0."""
    parts = {
        "icp_fit": _clamp01(icp_fit),
        "pain": _clamp01(pain),
        "ability_to_pay": _clamp01(ability_to_pay),
        "urgency": _clamp01(urgency),
        "partner_potential": _clamp01(partner_potential),
        "trust_fit": _clamp01(trust_fit),
    }
    score = sum(parts[k] * w for k, w in LEAD_SCORE_WEIGHTS.items())
    return round(_clamp01(score), 4)


class MarketSignal(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    source: str
    segment: str
    pain_hypothesis: str
    observed_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    confidence: float = Field(0.5, ge=0.0, le=1.0)
    payload: dict[str, object] = Field(default_factory=dict)


class Audience(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    name: str
    segment_tag: str
    fit_criteria: list[str] = Field(default_factory=list)
    size_estimate: int | None = None
    pain_points: list[str] = Field(default_factory=list)


class Offer(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    name_ar: str
    name_en: str
    rung: OfferRung
    price_min_sar: float = Field(0.0, ge=0.0)
    price_max_sar: float = Field(0.0, ge=0.0)
    target_segment: str
    pain_addressed: str
    deliverables_ar: list[str] = Field(default_factory=list)
    deliverables_en: list[str] = Field(default_factory=list)
    success_metric: str
    scale_kill_rule: str


class MessageVariant(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    offer_id: str
    angle: str
    headline_ar: str
    headline_en: str
    body_ar: str
    body_en: str
    cta_ar: str
    cta_en: str
    status: MessageStatus = "draft"
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class MarketingCampaign(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    campaign_name: str
    target_segment: str
    offer_id: str
    channel: str
    message_angle: str
    budget_sar: float = Field(0.0, ge=0.0)
    success_metric: str
    scale_kill_rule: str
    tracking_url_pattern: str = ""
    status: CampaignStatus = "draft"
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class MarketingTouch(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    campaign_id: str | None = None
    lead_id: str = ""
    touch_type: str = ""
    channel: str = ""
    content_id: str = ""
    message_variant: str = ""
    occurred_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class RevenueAttribution(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    revenue_sar: float = Field(..., ge=0.0)
    deal_id: str
    campaign_id: str | None = None
    offer_id: str | None = None
    channel: str | None = None
    asset_id: str | None = None
    agent_id: str | None = None
    attribution_type: AttributionType
    payment_received: bool = False
    signed_agreement: bool = False
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    @computed_field  # type: ignore[prop-decorator]
    @property
    def is_real_revenue(self) -> bool:
        return bool(self.payment_received or self.signed_agreement)


class MarketingExperiment(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    experiment_name: str
    target_segment: str
    offer_id: str
    variable_tested: str
    variant_a: str
    variant_b: str
    success_metric: str
    result: dict[str, float] = Field(default_factory=dict)
    decision: str = ""
    status: ExperimentStatus = "draft"
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class CaseStudyDraft(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    deal_id: str
    before_ar: str = ""
    before_en: str = ""
    action_ar: str = ""
    action_en: str = ""
    output_ar: str = ""
    output_en: str = ""
    outcome_ar: str = ""
    outcome_en: str = ""
    learning_ar: str = ""
    learning_en: str = ""
    next_steps_ar: str = ""
    next_steps_en: str = ""
    status: CaseStudyStatus = "draft"
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class Lead(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    source: str
    campaign_id: str | None = None
    segment: str
    pain: str = ""
    fit_score: float = Field(0.0, ge=0.0, le=1.0)
    ability_to_pay_score: float = Field(0.0, ge=0.0, le=1.0)
    urgency_score: float = Field(0.0, ge=0.0, le=1.0)
    partner_potential_score: float = Field(0.0, ge=0.0, le=1.0)
    trust_fit_score: float = Field(0.0, ge=0.0, le=1.0)
    pain_score: float = Field(0.0, ge=0.0, le=1.0)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    @computed_field  # type: ignore[prop-decorator]
    @property
    def overall_score(self) -> float:
        return compute_lead_score(
            self.fit_score,
            self.pain_score,
            self.ability_to_pay_score,
            self.urgency_score,
            self.partner_potential_score,
            self.trust_fit_score,
        )
