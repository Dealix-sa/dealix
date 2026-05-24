"""خادم Hermes — scale / kill recommender.

Implements the §46 scale-or-kill rule table. Given a window of outcomes
the recommender reports SCALE, KILL or HOLD with a confidence and a
list of suggested actions.

The rules are all deterministic, score-based and unit-testable.
"""

from __future__ import annotations

from decimal import Decimal
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field

from dealix.hermes.core.outcomes import Outcome, OutcomeKind


class ScaleKillKind(StrEnum):
    SCALE = "scale"
    KILL = "kill"
    HOLD = "hold"


class ScaleKillRecommendation(BaseModel):
    """Output of the recommender."""

    model_config = ConfigDict(extra="forbid")

    kind: ScaleKillKind
    reasons: list[str] = Field(default_factory=list, max_length=20)
    confidence: float = Field(..., ge=0.0, le=1.0)
    suggested_actions: list[str] = Field(default_factory=list, max_length=20)


# ─────────────────────────────────────────────────────────────
# Rules
# ─────────────────────────────────────────────────────────────


_MIN_REPEAT = 2
_MARGIN_THRESHOLD = Decimal("1000")
_HIGH_RISK_FRACTION = 0.4
_NO_CHANNEL_FRACTION = 0.5
_EXPLAIN_THRESHOLD = 0.6


def _money_total(outcomes: list[Outcome]) -> Decimal:
    total = Decimal("0")
    for o in outcomes:
        if o.value is not None:
            total += o.value.amount
    return total


def _count(outcomes: list[Outcome], kind: OutcomeKind) -> int:
    return sum(1 for o in outcomes if o.kind == kind)


def _fraction(outcomes: list[Outcome], predicate) -> float:
    if not outcomes:
        return 0.0
    return sum(1 for o in outcomes if predicate(o)) / len(outcomes)


class ScaleKillRecommender:
    """Recommend SCALE / KILL / HOLD from an outcome history."""

    def recommend(self, outcome_history: list[Outcome]) -> ScaleKillRecommendation:
        scale_reasons: list[str] = []
        kill_reasons: list[str] = []
        history = list(outcome_history)

        money_count = _count(history, OutcomeKind.MONEY)
        learning_count = _count(history, OutcomeKind.LEARNING)
        asset_count = _count(history, OutcomeKind.ASSET)
        trust_count = _count(history, OutcomeKind.TRUST)
        partner_count = _count(history, OutcomeKind.PARTNER)
        risk_fraction = _fraction(history, lambda o: o.risk_flag)
        total_money = _money_total(history)
        no_channel_fraction = _fraction(
            history,
            lambda o: bool(o.metrics.get("channel_unknown")),
        )
        explain_score = max(
            (float(o.metrics.get("explain_effort", 0.0)) for o in history),
            default=0.0,
        )

        # ── SCALE rules (need 4+ to recommend SCALE) ──────────────
        if money_count >= 1:
            scale_reasons.append("at least one paid outcome")
        if money_count >= _MIN_REPEAT:
            scale_reasons.append("repeated paid outcomes")
        if total_money >= _MARGIN_THRESHOLD:
            scale_reasons.append(f"good margin (>= {_MARGIN_THRESHOLD} SAR)")
        if any(o.metrics.get("repeatable") for o in history):
            scale_reasons.append("repeatable process flagged")
        if asset_count >= 1:
            scale_reasons.append("builds reusable asset")
        if trust_count >= 1:
            scale_reasons.append("builds trust")
        if partner_count >= 1:
            scale_reasons.append("partner uplift")

        # ── KILL rules (need 4+ to recommend KILL) ───────────────
        if money_count == 0:
            kill_reasons.append("no paid outcome recorded")
        if explain_score > _EXPLAIN_THRESHOLD:
            kill_reasons.append("requires excessive explanation")
        if risk_fraction >= _HIGH_RISK_FRACTION:
            kill_reasons.append("high-risk fraction crossed")
        if asset_count == 0 and learning_count == 0:
            kill_reasons.append("no asset or learning produced")
        if any(o.metrics.get("time_drain") for o in history):
            kill_reasons.append("consumes time disproportionately")
        if no_channel_fraction >= _NO_CHANNEL_FRACTION:
            kill_reasons.append("no scalable channel identified")
        if all(o.kind == OutcomeKind.LEARNING for o in history) and history:
            kill_reasons.append("only produces explainer learnings")

        if len(scale_reasons) >= 4 and len(scale_reasons) > len(kill_reasons):
            return ScaleKillRecommendation(
                kind=ScaleKillKind.SCALE,
                reasons=scale_reasons,
                confidence=min(1.0, 0.5 + 0.1 * len(scale_reasons)),
                suggested_actions=[
                    "Add to monthly retainer playbook",
                    "Allocate dedicated agent capacity",
                    "Track NPS + revenue uplift weekly",
                ],
            )
        if len(kill_reasons) >= 4 and len(kill_reasons) > len(scale_reasons):
            return ScaleKillRecommendation(
                kind=ScaleKillKind.KILL,
                reasons=kill_reasons,
                confidence=min(1.0, 0.5 + 0.1 * len(kill_reasons)),
                suggested_actions=[
                    "Sunset the workflow",
                    "Archive learnings to playbook",
                    "Notify owners + reclaim agent capacity",
                ],
            )
        return ScaleKillRecommendation(
            kind=ScaleKillKind.HOLD,
            reasons=scale_reasons + kill_reasons or ["insufficient evidence to scale or kill"],
            confidence=0.4,
            suggested_actions=[
                "Continue limited pilot",
                "Collect at least 3 more outcomes",
                "Re-evaluate next review cycle",
            ],
        )


__all__ = [
    "ScaleKillKind",
    "ScaleKillRecommendation",
    "ScaleKillRecommender",
]
