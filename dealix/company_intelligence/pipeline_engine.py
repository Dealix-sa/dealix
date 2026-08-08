"""Pipeline Intelligence Engine — revenue forecasting and deal scoring.

Pure-logic engine that analyzes opportunities, scores pipeline health,
forecasts revenue, tracks deal velocity, and recommends pipeline actions.

No database, network, or LLM calls. All external effects require
human approval. Revenue claims require payment evidence.

Design principles:
- Deterministic content-addressable IDs (SHA-256).
- Frozen Pydantic v2 models — no silent mutation.
- Safety: ``execution_allowed=False``, ``approval_required=True``.
- Revenue recognized only with payment evidence.
"""
from __future__ import annotations

import json
from datetime import UTC, datetime
from enum import StrEnum
from hashlib import sha256
from typing import Annotated, Any

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    StringConstraints,
    model_validator,
)

from dealix.company_intelligence.execution_contracts import OpportunityStage

NonEmptyString = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _stable_id(prefix: str, payload: dict[str, Any]) -> str:
    canonical = json.dumps(
        payload,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
        default=str,
    )
    return f"{prefix}_{sha256(canonical.encode('utf-8')).hexdigest()[:16]}"


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------


class DealHealth(StrEnum):
    """Health classification for an individual deal."""

    THRIVING = "thriving"
    ON_TRACK = "on_track"
    AT_RISK = "at_risk"
    STALLED = "stalled"
    LOST = "lost"


class PipelineHealth(StrEnum):
    """Overall pipeline health classification."""

    EXCELLENT = "excellent"
    HEALTHY = "healthy"
    NEEDS_ATTENTION = "needs_attention"
    AT_RISK = "at_risk"
    CRITICAL = "critical"


class ForecastConfidence(StrEnum):
    """Confidence level in revenue forecast."""

    HIGH = "high"
    MODERATE = "moderate"
    LOW = "low"
    SPECULATIVE = "speculative"


class PipelineActionType(StrEnum):
    """Recommended pipeline action categories."""

    ACCELERATE = "accelerate"
    NURTURE = "nurture"
    RE_ENGAGE = "re_engage"
    ESCALATE = "escalate"
    QUALIFY_DEEPER = "qualify_deeper"
    PREPARE_PROPOSAL = "prepare_proposal"
    CLOSE_NOW = "close_now"
    PARK = "park"


# ---------------------------------------------------------------------------
# Stage conversion probabilities — based on typical B2B SaaS pipeline
# ---------------------------------------------------------------------------

_STAGE_PROBABILITIES: dict[OpportunityStage, float] = {
    OpportunityStage.RESEARCH: 0.05,
    OpportunityStage.QUALIFY: 0.10,
    OpportunityStage.APPROVAL: 0.20,
    OpportunityStage.CONVERSATION: 0.35,
    OpportunityStage.PILOT: 0.55,
    OpportunityStage.PROOF: 0.75,
    OpportunityStage.COMMERCIAL: 0.90,
    OpportunityStage.WON: 1.00,
    OpportunityStage.LOST: 0.00,
    OpportunityStage.PARKED: 0.02,
}


# ---------------------------------------------------------------------------
# Contracts
# ---------------------------------------------------------------------------


class OpportunityScore(BaseModel):
    """Scored opportunity with breakdown factors."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    tenant_id: NonEmptyString
    score_id: NonEmptyString
    opportunity_id: NonEmptyString
    overall_score: float = Field(..., ge=0.0, le=1.0)
    fit_score: float = Field(default=0.5, ge=0.0, le=1.0)
    engagement_score: float = Field(default=0.5, ge=0.0, le=1.0)
    timing_score: float = Field(default=0.5, ge=0.0, le=1.0)
    authority_score: float = Field(default=0.5, ge=0.0, le=1.0)
    stage: OpportunityStage = OpportunityStage.RESEARCH
    deal_health: DealHealth = DealHealth.ON_TRACK
    conversion_probability: float = Field(default=0.05, ge=0.0, le=1.0)
    days_in_stage: int = Field(default=0, ge=0)
    score_reasons: tuple[str, ...] = ()
    source_id: NonEmptyString = ""
    scored_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class DealVelocity(BaseModel):
    """Stage velocity metrics for a deal or pipeline."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    tenant_id: NonEmptyString
    velocity_id: NonEmptyString
    opportunity_id: str = ""
    avg_days_per_stage: float = Field(default=0.0, ge=0.0)
    stages_completed: int = Field(default=0, ge=0)
    stages_remaining: int = Field(default=0, ge=0)
    estimated_days_to_close: float = Field(default=0.0, ge=0.0)
    is_accelerating: bool = False
    velocity_trend: float = Field(default=0.0, ge=-1.0, le=1.0)
    source_id: NonEmptyString = ""


class PipelineAnalysis(BaseModel):
    """Pipeline-wide health assessment."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    tenant_id: NonEmptyString
    analysis_id: NonEmptyString
    pipeline_health: PipelineHealth = PipelineHealth.HEALTHY
    total_opportunities: int = Field(default=0, ge=0)
    active_opportunities: int = Field(default=0, ge=0)
    won_count: int = Field(default=0, ge=0)
    lost_count: int = Field(default=0, ge=0)
    stalled_count: int = Field(default=0, ge=0)
    stage_distribution: tuple[tuple[str, int], ...] = ()
    avg_deal_score: float = Field(default=0.0, ge=0.0, le=1.0)
    pipeline_velocity: float = Field(default=0.0, ge=0.0)
    coverage_ratio: float = Field(default=0.0, ge=0.0)
    top_risks: tuple[str, ...] = ()
    source_id: NonEmptyString = ""
    analyzed_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    approval_required: bool = True
    execution_allowed: bool = False

    @model_validator(mode="after")
    def _enforce_safety(self) -> PipelineAnalysis:
        if self.execution_allowed:
            raise ValueError(
                "pipeline analysis must never authorize execution"
            )
        return self


class RevenueForecast(BaseModel):
    """Revenue forecast with confidence bands."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    tenant_id: NonEmptyString
    forecast_id: NonEmptyString
    forecast_period: NonEmptyString
    weighted_pipeline_value: float = Field(default=0.0, ge=0.0)
    best_case_value: float = Field(default=0.0, ge=0.0)
    worst_case_value: float = Field(default=0.0, ge=0.0)
    committed_value: float = Field(default=0.0, ge=0.0)
    confidence: ForecastConfidence = ForecastConfidence.SPECULATIVE
    opportunity_count: int = Field(default=0, ge=0)
    assumptions: tuple[str, ...] = ()
    source_id: NonEmptyString = ""
    forecasted_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    is_hypothesis: bool = True
    recognized_revenue: bool = False

    @model_validator(mode="after")
    def _enforce_evidence(self) -> RevenueForecast:
        if self.recognized_revenue:
            raise ValueError(
                "forecasts cannot recognize revenue — "
                "revenue requires payment evidence"
            )
        if not self.is_hypothesis:
            raise ValueError("forecasts are hypotheses until evidenced")
        return self


class PipelineRecommendation(BaseModel):
    """Actionable pipeline recommendation."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    tenant_id: NonEmptyString
    recommendation_id: NonEmptyString
    opportunity_id: NonEmptyString
    action_type: PipelineActionType
    description: NonEmptyString
    rationale: NonEmptyString
    priority: float = Field(default=0.5, ge=0.0, le=1.0)
    approval_required: bool = True
    execution_allowed: bool = False
    source_id: NonEmptyString = ""

    @model_validator(mode="after")
    def _enforce_safety(self) -> PipelineRecommendation:
        if not self.approval_required:
            raise ValueError(
                "pipeline recommendations must require approval"
            )
        if self.execution_allowed:
            raise ValueError(
                "pipeline recommendations must never authorize execution"
            )
        return self


# ---------------------------------------------------------------------------
# Engine functions
# ---------------------------------------------------------------------------


def score_opportunity(
    *,
    tenant_id: str,
    opportunity_id: str,
    stage: OpportunityStage = OpportunityStage.RESEARCH,
    fit_score: float = 0.5,
    engagement_score: float = 0.5,
    timing_score: float = 0.5,
    authority_score: float = 0.5,
    days_in_stage: int = 0,
    source_id: str = "pipeline_engine",
) -> OpportunityScore:
    """Score an opportunity based on multiple factors."""

    # Weighted composite score
    overall = (
        fit_score * 0.30
        + engagement_score * 0.25
        + timing_score * 0.20
        + authority_score * 0.25
    )
    overall = round(min(1.0, max(0.0, overall)), 4)

    conversion_probability = _STAGE_PROBABILITIES.get(stage, 0.05)

    # Determine deal health
    reasons: list[str] = []
    deal_health = DealHealth.ON_TRACK

    if stage in (OpportunityStage.LOST,):
        deal_health = DealHealth.LOST
        reasons.append("opportunity is lost")
    elif days_in_stage > 30:
        deal_health = DealHealth.STALLED
        reasons.append(f"stalled: {days_in_stage} days in {stage.value}")
    elif days_in_stage > 14:
        deal_health = DealHealth.AT_RISK
        reasons.append(f"at risk: {days_in_stage} days in {stage.value}")
    elif overall >= 0.7:
        deal_health = DealHealth.THRIVING
        reasons.append("strong scores across all factors")
    else:
        reasons.append("progressing normally")

    if fit_score < 0.3:
        reasons.append("low fit score — may not match ICP")
    if engagement_score < 0.3:
        reasons.append("low engagement — needs re-engagement")
    if authority_score < 0.3:
        reasons.append("decision-maker access unclear")

    score_id = _stable_id(
        "oppscore",
        {
            "tenant_id": tenant_id.strip(),
            "opportunity_id": opportunity_id.strip(),
            "stage": stage.value,
            "fit_score": fit_score,
            "engagement_score": engagement_score,
            "timing_score": timing_score,
            "authority_score": authority_score,
        },
    )

    return OpportunityScore(
        tenant_id=tenant_id,
        score_id=score_id,
        opportunity_id=opportunity_id,
        overall_score=overall,
        fit_score=fit_score,
        engagement_score=engagement_score,
        timing_score=timing_score,
        authority_score=authority_score,
        stage=stage,
        deal_health=deal_health,
        conversion_probability=conversion_probability,
        days_in_stage=days_in_stage,
        score_reasons=tuple(reasons),
        source_id=source_id,
    )


def analyze_pipeline(
    *,
    tenant_id: str,
    scores: tuple[OpportunityScore, ...] | list[OpportunityScore] = (),
    revenue_target: float = 0.0,
    source_id: str = "pipeline_engine",
) -> PipelineAnalysis:
    """Analyze pipeline health across all scored opportunities."""

    scores_list = list(scores)
    total = len(scores_list)
    active = sum(
        1
        for s in scores_list
        if s.stage not in (OpportunityStage.WON, OpportunityStage.LOST, OpportunityStage.PARKED)
    )
    won = sum(1 for s in scores_list if s.stage == OpportunityStage.WON)
    lost = sum(1 for s in scores_list if s.stage == OpportunityStage.LOST)
    stalled = sum(1 for s in scores_list if s.deal_health == DealHealth.STALLED)

    # Stage distribution
    stage_counts: dict[str, int] = {}
    for s in scores_list:
        stage_counts[s.stage.value] = stage_counts.get(s.stage.value, 0) + 1
    stage_distribution = tuple(sorted(stage_counts.items()))

    # Average score
    avg_score = (
        round(sum(s.overall_score for s in scores_list) / total, 4)
        if total > 0
        else 0.0
    )

    # Pipeline velocity — average conversion probability
    pipeline_velocity = (
        round(
            sum(s.conversion_probability for s in scores_list if s.stage not in (
                OpportunityStage.WON, OpportunityStage.LOST,
            )) / max(active, 1),
            4,
        )
        if active > 0
        else 0.0
    )

    # Coverage ratio (active pipeline vs target)
    coverage_ratio = round(active / max(revenue_target, 1.0), 4) if revenue_target > 0 else 0.0

    # Determine health
    risks: list[str] = []
    if total == 0:
        health = PipelineHealth.CRITICAL
        risks.append("empty pipeline — no opportunities")
    elif stalled > active * 0.5 and active > 0:
        health = PipelineHealth.CRITICAL
        risks.append(f"{stalled} of {active} active deals stalled")
    elif stalled > active * 0.3 and active > 0:
        health = PipelineHealth.AT_RISK
        risks.append(f"{stalled} stalled deals need attention")
    elif avg_score < 0.3:
        health = PipelineHealth.NEEDS_ATTENTION
        risks.append("low average deal score")
    elif active < 3:
        health = PipelineHealth.NEEDS_ATTENTION
        risks.append("thin pipeline — fewer than 3 active opportunities")
    elif avg_score >= 0.7 and stalled == 0:
        health = PipelineHealth.EXCELLENT
    else:
        health = PipelineHealth.HEALTHY

    if lost > won and (won + lost) > 0:
        risks.append(f"loss rate concerning: {lost} lost vs {won} won")

    analysis_id = _stable_id(
        "pipeline",
        {
            "tenant_id": tenant_id.strip(),
            "total": total,
            "active": active,
            "won": won,
            "lost": lost,
            "stalled": stalled,
            "avg_score": avg_score,
        },
    )

    return PipelineAnalysis(
        tenant_id=tenant_id,
        analysis_id=analysis_id,
        pipeline_health=health,
        total_opportunities=total,
        active_opportunities=active,
        won_count=won,
        lost_count=lost,
        stalled_count=stalled,
        stage_distribution=stage_distribution,
        avg_deal_score=avg_score,
        pipeline_velocity=pipeline_velocity,
        coverage_ratio=coverage_ratio,
        top_risks=tuple(risks),
        source_id=source_id,
    )


def forecast_revenue(
    *,
    tenant_id: str,
    scores: tuple[OpportunityScore, ...] | list[OpportunityScore] = (),
    deal_values: dict[str, float] | None = None,
    forecast_period: str = "next_quarter",
    source_id: str = "pipeline_engine",
) -> RevenueForecast:
    """Forecast revenue from scored pipeline. Always a hypothesis."""

    values = deal_values or {}
    scores_list = list(scores)

    active_scores = [
        s for s in scores_list
        if s.stage not in (OpportunityStage.LOST, OpportunityStage.PARKED)
    ]

    weighted = 0.0
    best_case = 0.0
    worst_case = 0.0
    committed = 0.0

    for s in active_scores:
        deal_value = values.get(s.opportunity_id, 0.0)
        weighted += deal_value * s.conversion_probability
        best_case += deal_value
        worst_case += deal_value * max(0.0, s.conversion_probability - 0.2)
        if s.stage == OpportunityStage.WON:
            committed += deal_value

    assumptions: list[str] = [
        f"based on {len(active_scores)} active opportunities",
        "stage-based conversion probabilities applied",
        "deal values are estimates until contracted",
    ]

    # Confidence based on pipeline quality
    if len(active_scores) == 0:
        confidence = ForecastConfidence.SPECULATIVE
        assumptions.append("no active pipeline — speculative forecast")
    elif all(s.overall_score >= 0.6 for s in active_scores):
        confidence = ForecastConfidence.HIGH
    elif any(s.deal_health in (DealHealth.STALLED, DealHealth.AT_RISK) for s in active_scores):
        confidence = ForecastConfidence.LOW
    else:
        confidence = ForecastConfidence.MODERATE

    forecast_id = _stable_id(
        "forecast",
        {
            "tenant_id": tenant_id.strip(),
            "forecast_period": forecast_period.strip(),
            "opportunity_count": len(active_scores),
            "weighted": round(weighted, 2),
        },
    )

    return RevenueForecast(
        tenant_id=tenant_id,
        forecast_id=forecast_id,
        forecast_period=forecast_period,
        weighted_pipeline_value=round(weighted, 2),
        best_case_value=round(best_case, 2),
        worst_case_value=round(worst_case, 2),
        committed_value=round(committed, 2),
        confidence=confidence,
        opportunity_count=len(active_scores),
        assumptions=tuple(assumptions),
        source_id=source_id,
        is_hypothesis=True,
        recognized_revenue=False,
    )


def assess_deal_velocity(
    *,
    tenant_id: str,
    opportunity_id: str,
    stage: OpportunityStage,
    days_in_stage: int = 0,
    total_days: int = 0,
    stages_completed: int = 0,
    source_id: str = "pipeline_engine",
) -> DealVelocity:
    """Assess how fast a deal is moving through the pipeline."""

    # Total pipeline stages (excluding terminal)
    total_stages = 7  # RESEARCH through COMMERCIAL
    remaining = max(0, total_stages - stages_completed)

    avg_days = round(total_days / max(stages_completed, 1), 2)
    estimated_close = round(avg_days * remaining, 2)

    # Velocity trend — negative if slowing down
    if stages_completed > 1 and days_in_stage > avg_days * 1.5:
        trend = -0.5
        accelerating = False
    elif stages_completed > 1 and days_in_stage < avg_days * 0.7:
        trend = 0.5
        accelerating = True
    else:
        trend = 0.0
        accelerating = False

    velocity_id = _stable_id(
        "velocity",
        {
            "tenant_id": tenant_id.strip(),
            "opportunity_id": opportunity_id.strip(),
            "stage": stage.value,
            "stages_completed": stages_completed,
            "total_days": total_days,
        },
    )

    return DealVelocity(
        tenant_id=tenant_id,
        velocity_id=velocity_id,
        opportunity_id=opportunity_id,
        avg_days_per_stage=avg_days,
        stages_completed=stages_completed,
        stages_remaining=remaining,
        estimated_days_to_close=estimated_close,
        is_accelerating=accelerating,
        velocity_trend=trend,
        source_id=source_id,
    )


def identify_at_risk_deals(
    scores: tuple[OpportunityScore, ...] | list[OpportunityScore],
) -> list[OpportunityScore]:
    """Return deals that are stalled or at risk, sorted by severity."""

    at_risk = [
        s for s in scores
        if s.deal_health in (DealHealth.STALLED, DealHealth.AT_RISK)
        and s.stage not in (OpportunityStage.WON, OpportunityStage.LOST)
    ]
    # Stalled first, then at_risk; within each, worst score first
    return sorted(
        at_risk,
        key=lambda s: (
            0 if s.deal_health == DealHealth.STALLED else 1,
            s.overall_score,
        ),
    )


def recommend_pipeline_actions(
    *,
    scores: tuple[OpportunityScore, ...] | list[OpportunityScore],
    source_id: str = "pipeline_engine",
) -> list[PipelineRecommendation]:
    """Generate actionable recommendations for each opportunity."""

    recommendations: list[PipelineRecommendation] = []

    for s in scores:
        if s.stage in (OpportunityStage.WON, OpportunityStage.LOST):
            continue

        # Determine recommended action based on health and stage
        if s.deal_health == DealHealth.STALLED:
            action_type = PipelineActionType.RE_ENGAGE
            description = f"Re-engage stalled deal — {s.days_in_stage} days in {s.stage.value}"
            rationale = "deal has not progressed; re-engagement or parking recommended"
            priority = 0.9
        elif s.deal_health == DealHealth.AT_RISK:
            action_type = PipelineActionType.ESCALATE
            description = f"Escalate at-risk deal in {s.stage.value} stage"
            rationale = "deal showing risk signals; needs senior attention"
            priority = 0.8
        elif s.stage == OpportunityStage.COMMERCIAL:
            action_type = PipelineActionType.CLOSE_NOW
            description = "Close deal — commercial stage reached"
            rationale = "opportunity is commercially ready for closing"
            priority = 0.95
        elif s.stage == OpportunityStage.PROOF:
            action_type = PipelineActionType.PREPARE_PROPOSAL
            description = "Prepare proposal — proof stage complete"
            rationale = "proof established; proposal preparation is next"
            priority = 0.85
        elif s.stage in (OpportunityStage.RESEARCH, OpportunityStage.QUALIFY):
            action_type = PipelineActionType.QUALIFY_DEEPER
            description = f"Qualify deeper — currently in {s.stage.value}"
            rationale = "early stage; needs deeper qualification before investing resources"
            priority = 0.4
        elif s.overall_score >= 0.7:
            action_type = PipelineActionType.ACCELERATE
            description = f"Accelerate high-scoring deal (score: {s.overall_score:.2f})"
            rationale = "strong fit and engagement; worth investing resources to accelerate"
            priority = 0.75
        elif s.stage == OpportunityStage.PARKED:
            action_type = PipelineActionType.PARK
            description = "Review parked opportunity for re-activation"
            rationale = "parked deals should be periodically reviewed"
            priority = 0.2
        else:
            action_type = PipelineActionType.NURTURE
            description = f"Nurture relationship — {s.stage.value} stage"
            rationale = "maintain engagement and build relationship"
            priority = 0.5

        rec_id = _stable_id(
            "piperec",
            {
                "tenant_id": s.tenant_id,
                "opportunity_id": s.opportunity_id,
                "action_type": action_type.value,
                "stage": s.stage.value,
            },
        )

        recommendations.append(
            PipelineRecommendation(
                tenant_id=s.tenant_id,
                recommendation_id=rec_id,
                opportunity_id=s.opportunity_id,
                action_type=action_type,
                description=description,
                rationale=rationale,
                priority=priority,
                approval_required=True,
                execution_allowed=False,
                source_id=source_id,
            )
        )

    return sorted(recommendations, key=lambda r: r.priority, reverse=True)
