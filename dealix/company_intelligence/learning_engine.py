"""Learning Intelligence Engine — pattern recognition and continuous improvement.

Pure-logic engine that analyzes win/loss outcomes, extracts patterns,
generates actionable insights, and recommends strategy adjustments.

No database, network, or LLM calls. Learning events are proposals —
they cannot mutate policy directly. All recommendations require
human approval.

Design principles:
- Deterministic content-addressable IDs (SHA-256).
- Frozen Pydantic v2 models — no silent mutation.
- Safety: ``approval_required=True``, ``applied=False`` always.
- Learning events are hypotheses, never direct policy mutations.
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


class PatternStrength(StrEnum):
    """Strength of a discovered pattern."""

    STRONG = "strong"
    MODERATE = "moderate"
    WEAK = "weak"
    ANECDOTAL = "anecdotal"


class InsightCategory(StrEnum):
    """Category of a generated insight."""

    TARGETING = "targeting"
    MESSAGING = "messaging"
    PRICING = "pricing"
    TIMING = "timing"
    CHANNEL = "channel"
    OBJECTION = "objection"
    DELIVERY = "delivery"
    PROCESS = "process"


class StrategyAdjustmentType(StrEnum):
    """Type of strategy adjustment recommended."""

    REFINE_ICP = "refine_icp"
    ADJUST_MESSAGING = "adjust_messaging"
    CHANGE_CHANNEL = "change_channel"
    MODIFY_PRICING = "modify_pricing"
    IMPROVE_TIMING = "improve_timing"
    ADD_PROOF_POINT = "add_proof_point"
    TRAIN_OBJECTION = "train_objection"
    STREAMLINE_PROCESS = "streamline_process"
    EXPAND_CAPABILITY = "expand_capability"


# ---------------------------------------------------------------------------
# Contracts
# ---------------------------------------------------------------------------


class WinLossAnalysis(BaseModel):
    """Structured win/loss analysis from outcome data."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    tenant_id: NonEmptyString
    analysis_id: NonEmptyString
    period: NonEmptyString
    total_outcomes: int = Field(default=0, ge=0)
    wins: int = Field(default=0, ge=0)
    losses: int = Field(default=0, ge=0)
    no_decisions: int = Field(default=0, ge=0)
    win_rate: float = Field(default=0.0, ge=0.0, le=1.0)
    common_win_factors: tuple[str, ...] = ()
    common_loss_factors: tuple[str, ...] = ()
    top_objections: tuple[str, ...] = ()
    avg_cycle_days: float = Field(default=0.0, ge=0.0)
    evidence_refs: tuple[str, ...] = ()
    source_id: NonEmptyString = ""
    analyzed_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    is_hypothesis: bool = True


class PatternInsight(BaseModel):
    """A discovered pattern from outcome data with evidence."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    tenant_id: NonEmptyString
    pattern_id: NonEmptyString
    category: InsightCategory
    pattern_description: NonEmptyString
    strength: PatternStrength
    occurrences: int = Field(default=1, ge=1)
    evidence_refs: tuple[str, ...] = Field(default=(), min_length=0)
    confidence: float = Field(default=0.5, ge=0.0, le=1.0)
    actionable: bool = True
    is_hypothesis: bool = True
    source_id: NonEmptyString = ""

    @model_validator(mode="after")
    def _enforce_hypothesis(self) -> PatternInsight:
        if not self.is_hypothesis:
            raise ValueError(
                "patterns are hypotheses until validated by human review"
            )
        return self


class StrategyRecommendation(BaseModel):
    """A strategy adjustment recommendation based on learnings."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    tenant_id: NonEmptyString
    recommendation_id: NonEmptyString
    adjustment_type: StrategyAdjustmentType
    description: NonEmptyString
    rationale: NonEmptyString
    expected_impact: NonEmptyString
    confidence: float = Field(default=0.5, ge=0.0, le=1.0)
    evidence_refs: tuple[str, ...] = ()
    affected_departments: tuple[str, ...] = ()
    priority: float = Field(default=0.5, ge=0.0, le=1.0)
    approval_required: bool = True
    applied: bool = False
    source_id: NonEmptyString = ""

    @model_validator(mode="after")
    def _enforce_safety(self) -> StrategyRecommendation:
        if not self.approval_required:
            raise ValueError(
                "strategy recommendations must require approval"
            )
        if self.applied:
            raise ValueError(
                "strategy recommendations are proposals — "
                "they cannot be pre-applied"
            )
        return self


class LearningVelocity(BaseModel):
    """How fast the system is learning and improving."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    tenant_id: NonEmptyString
    velocity_id: NonEmptyString
    period: NonEmptyString
    patterns_discovered: int = Field(default=0, ge=0)
    recommendations_generated: int = Field(default=0, ge=0)
    recommendations_approved: int = Field(default=0, ge=0)
    win_rate_trend: float = Field(default=0.0, ge=-1.0, le=1.0)
    cycle_time_trend: float = Field(default=0.0, ge=-1.0, le=1.0)
    is_improving: bool = False
    source_id: NonEmptyString = ""


# ---------------------------------------------------------------------------
# Engine functions
# ---------------------------------------------------------------------------


def analyze_win_loss(
    *,
    tenant_id: str,
    period: str,
    win_outcomes: tuple[str, ...] | list[str] = (),
    loss_outcomes: tuple[str, ...] | list[str] = (),
    no_decision_outcomes: tuple[str, ...] | list[str] = (),
    win_factors: tuple[str, ...] | list[str] = (),
    loss_factors: tuple[str, ...] | list[str] = (),
    objections: tuple[str, ...] | list[str] = (),
    avg_cycle_days: float = 0.0,
    source_id: str = "learning_engine",
) -> WinLossAnalysis:
    """Analyze win/loss patterns for a given period."""

    wins = len(list(win_outcomes))
    losses = len(list(loss_outcomes))
    no_decisions = len(list(no_decision_outcomes))
    total = wins + losses + no_decisions

    win_rate = round(wins / max(total, 1), 4) if total > 0 else 0.0

    # Collect evidence references
    evidence = sorted(
        set(list(win_outcomes) + list(loss_outcomes) + list(no_decision_outcomes))
    )

    analysis_id = _stable_id(
        "winloss",
        {
            "tenant_id": tenant_id.strip(),
            "period": period.strip(),
            "wins": wins,
            "losses": losses,
            "no_decisions": no_decisions,
        },
    )

    return WinLossAnalysis(
        tenant_id=tenant_id,
        analysis_id=analysis_id,
        period=period,
        total_outcomes=total,
        wins=wins,
        losses=losses,
        no_decisions=no_decisions,
        win_rate=win_rate,
        common_win_factors=tuple(win_factors),
        common_loss_factors=tuple(loss_factors),
        top_objections=tuple(objections),
        avg_cycle_days=avg_cycle_days,
        evidence_refs=tuple(evidence),
        source_id=source_id,
        is_hypothesis=True,
    )


def extract_patterns(
    *,
    tenant_id: str,
    analysis: WinLossAnalysis,
    source_id: str = "learning_engine",
) -> list[PatternInsight]:
    """Extract actionable patterns from win/loss analysis."""

    patterns: list[PatternInsight] = []

    # Pattern from win rate
    if analysis.win_rate >= 0.6:
        patterns.append(
            _build_pattern(
                tenant_id=tenant_id,
                category=InsightCategory.TARGETING,
                description="high win rate indicates strong ICP alignment",
                strength=PatternStrength.STRONG if analysis.total_outcomes >= 10 else PatternStrength.MODERATE,
                occurrences=analysis.wins,
                confidence=min(0.9, analysis.win_rate),
                evidence_refs=analysis.evidence_refs,
                source_id=source_id,
            )
        )
    elif analysis.win_rate < 0.3 and analysis.total_outcomes >= 5:
        patterns.append(
            _build_pattern(
                tenant_id=tenant_id,
                category=InsightCategory.TARGETING,
                description="low win rate suggests ICP or messaging misalignment",
                strength=PatternStrength.STRONG if analysis.total_outcomes >= 10 else PatternStrength.MODERATE,
                occurrences=analysis.losses,
                confidence=0.7,
                evidence_refs=analysis.evidence_refs,
                source_id=source_id,
            )
        )

    # Pattern from common loss factors
    for factor in analysis.common_loss_factors:
        patterns.append(
            _build_pattern(
                tenant_id=tenant_id,
                category=InsightCategory.OBJECTION,
                description=f"recurring loss factor: {factor}",
                strength=PatternStrength.MODERATE,
                occurrences=1,
                confidence=0.6,
                evidence_refs=analysis.evidence_refs,
                source_id=source_id,
            )
        )

    # Pattern from objections
    for objection in analysis.top_objections:
        patterns.append(
            _build_pattern(
                tenant_id=tenant_id,
                category=InsightCategory.OBJECTION,
                description=f"common objection: {objection}",
                strength=PatternStrength.MODERATE,
                occurrences=1,
                confidence=0.6,
                evidence_refs=analysis.evidence_refs,
                source_id=source_id,
            )
        )

    # Cycle time pattern
    if analysis.avg_cycle_days > 45:
        patterns.append(
            _build_pattern(
                tenant_id=tenant_id,
                category=InsightCategory.PROCESS,
                description=f"long sales cycle ({analysis.avg_cycle_days:.0f} days) — "
                "consider process streamlining",
                strength=PatternStrength.MODERATE,
                occurrences=analysis.total_outcomes,
                confidence=0.7,
                evidence_refs=analysis.evidence_refs,
                source_id=source_id,
            )
        )

    return patterns


def _build_pattern(
    *,
    tenant_id: str,
    category: InsightCategory,
    description: str,
    strength: PatternStrength,
    occurrences: int,
    confidence: float,
    evidence_refs: tuple[str, ...] = (),
    source_id: str,
) -> PatternInsight:
    """Build a single pattern insight with deterministic ID."""

    pattern_id = _stable_id(
        "pattern",
        {
            "tenant_id": tenant_id.strip(),
            "category": category.value,
            "description": description.strip(),
        },
    )

    return PatternInsight(
        tenant_id=tenant_id,
        pattern_id=pattern_id,
        category=category,
        pattern_description=description,
        strength=strength,
        occurrences=occurrences,
        confidence=confidence,
        evidence_refs=evidence_refs,
        actionable=True,
        is_hypothesis=True,
        source_id=source_id,
    )


def generate_insights(
    *,
    patterns: tuple[PatternInsight, ...] | list[PatternInsight],
    source_id: str = "learning_engine",
) -> list[StrategyRecommendation]:
    """Generate strategy recommendations from discovered patterns."""

    recommendations: list[StrategyRecommendation] = []

    _CATEGORY_TO_ADJUSTMENT: dict[InsightCategory, StrategyAdjustmentType] = {
        InsightCategory.TARGETING: StrategyAdjustmentType.REFINE_ICP,
        InsightCategory.MESSAGING: StrategyAdjustmentType.ADJUST_MESSAGING,
        InsightCategory.PRICING: StrategyAdjustmentType.MODIFY_PRICING,
        InsightCategory.TIMING: StrategyAdjustmentType.IMPROVE_TIMING,
        InsightCategory.CHANNEL: StrategyAdjustmentType.CHANGE_CHANNEL,
        InsightCategory.OBJECTION: StrategyAdjustmentType.TRAIN_OBJECTION,
        InsightCategory.DELIVERY: StrategyAdjustmentType.EXPAND_CAPABILITY,
        InsightCategory.PROCESS: StrategyAdjustmentType.STREAMLINE_PROCESS,
    }

    for pattern in patterns:
        if not pattern.actionable:
            continue

        adjustment = _CATEGORY_TO_ADJUSTMENT.get(
            pattern.category, StrategyAdjustmentType.STREAMLINE_PROCESS
        )

        priority = _compute_recommendation_priority(pattern)

        rec_id = _stable_id(
            "strategyrec",
            {
                "tenant_id": pattern.tenant_id,
                "pattern_id": pattern.pattern_id,
                "adjustment_type": adjustment.value,
            },
        )

        recommendations.append(
            StrategyRecommendation(
                tenant_id=pattern.tenant_id,
                recommendation_id=rec_id,
                adjustment_type=adjustment,
                description=f"Based on pattern: {pattern.pattern_description}",
                rationale=f"Pattern confidence: {pattern.confidence:.0%}, "
                f"strength: {pattern.strength.value}, "
                f"occurrences: {pattern.occurrences}",
                expected_impact=f"address {pattern.category.value} pattern "
                f"to improve outcomes",
                confidence=pattern.confidence,
                evidence_refs=pattern.evidence_refs,
                affected_departments=_departments_for_category(pattern.category),
                priority=priority,
                approval_required=True,
                applied=False,
                source_id=source_id,
            )
        )

    return sorted(recommendations, key=lambda r: r.priority, reverse=True)


def _compute_recommendation_priority(pattern: PatternInsight) -> float:
    """Compute priority from pattern strength and confidence."""

    strength_weights = {
        PatternStrength.STRONG: 0.9,
        PatternStrength.MODERATE: 0.6,
        PatternStrength.WEAK: 0.3,
        PatternStrength.ANECDOTAL: 0.1,
    }
    base = strength_weights.get(pattern.strength, 0.5)
    return round(min(1.0, base * 0.6 + pattern.confidence * 0.4), 4)


def _departments_for_category(category: InsightCategory) -> tuple[str, ...]:
    """Map insight category to affected departments."""

    mapping: dict[InsightCategory, tuple[str, ...]] = {
        InsightCategory.TARGETING: ("sales", "marketing", "data"),
        InsightCategory.MESSAGING: ("sales", "marketing"),
        InsightCategory.PRICING: ("sales", "finance"),
        InsightCategory.TIMING: ("sales",),
        InsightCategory.CHANNEL: ("sales", "marketing"),
        InsightCategory.OBJECTION: ("sales",),
        InsightCategory.DELIVERY: ("operations", "product"),
        InsightCategory.PROCESS: ("operations", "sales"),
    }
    return mapping.get(category, ("operations",))


def compute_learning_velocity(
    *,
    tenant_id: str,
    period: str,
    patterns_discovered: int = 0,
    recommendations_generated: int = 0,
    recommendations_approved: int = 0,
    previous_win_rate: float = 0.0,
    current_win_rate: float = 0.0,
    previous_cycle_days: float = 0.0,
    current_cycle_days: float = 0.0,
    source_id: str = "learning_engine",
) -> LearningVelocity:
    """Compute how fast the system is learning and improving."""

    win_rate_trend = round(current_win_rate - previous_win_rate, 4)
    # Negative cycle time trend = improvement (faster)
    cycle_trend = round(
        (previous_cycle_days - current_cycle_days) / max(previous_cycle_days, 1.0),
        4,
    ) if previous_cycle_days > 0 else 0.0
    cycle_trend = max(-1.0, min(1.0, cycle_trend))

    is_improving = win_rate_trend > 0 or cycle_trend > 0

    velocity_id = _stable_id(
        "learnvel",
        {
            "tenant_id": tenant_id.strip(),
            "period": period.strip(),
            "patterns": patterns_discovered,
            "recs_generated": recommendations_generated,
        },
    )

    return LearningVelocity(
        tenant_id=tenant_id,
        velocity_id=velocity_id,
        period=period,
        patterns_discovered=patterns_discovered,
        recommendations_generated=recommendations_generated,
        recommendations_approved=recommendations_approved,
        win_rate_trend=win_rate_trend,
        cycle_time_trend=cycle_trend,
        is_improving=is_improving,
        source_id=source_id,
    )
