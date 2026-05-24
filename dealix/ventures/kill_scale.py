"""خادم المغامرات — VentureKillScale (spec §35).

Specialised SCALE/KILL/HOLD recommender that respects venture-specific
weights: revenue is the primary signal, but pilot count + churn
matter more than they do at the product level.
"""

from __future__ import annotations

from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from dealix.hermes.core.outcomes import Outcome, OutcomeKind
from dealix.hermes.core.scale import (
    ScaleKillKind,
    ScaleKillRecommendation,
    ScaleKillRecommender,
)


class VentureSignal(BaseModel):
    """Venture-level counters fed alongside the outcome stream."""

    model_config = ConfigDict(extra="forbid")

    pilots_run: int = Field(default=0, ge=0)
    pilots_churned: int = Field(default=0, ge=0)
    revenue_floor_sar: Decimal = Field(default=Decimal("10000"))


class VentureKillScale:
    """Recommend whether a vertical should scale, kill, or hold."""

    def __init__(self, recommender: ScaleKillRecommender | None = None) -> None:
        self._recommender = recommender or ScaleKillRecommender()

    def recommend(
        self,
        outcomes: list[Outcome],
        signal: VentureSignal | None = None,
    ) -> ScaleKillRecommendation:
        signal = signal or VentureSignal()
        base = self._recommender.recommend(outcomes)
        revenue = sum(
            (o.value.amount for o in outcomes
             if o.kind == OutcomeKind.MONEY and o.value is not None),
            start=Decimal("0"),
        )

        scale_extra: list[str] = []
        kill_extra: list[str] = []

        if signal.pilots_run >= 3 and revenue >= signal.revenue_floor_sar:
            scale_extra.append(
                f"{signal.pilots_run} pilots run with revenue >= "
                f"{signal.revenue_floor_sar} SAR"
            )
        if signal.pilots_churned >= 2 and signal.pilots_run > 0:
            churn_rate = signal.pilots_churned / signal.pilots_run
            if churn_rate >= 0.5:
                kill_extra.append(
                    f"venture churn rate {churn_rate:.0%} >= 50 %"
                )

        kind = base.kind
        reasons = list(base.reasons)
        if scale_extra and len(scale_extra) >= len(kill_extra):
            kind = ScaleKillKind.SCALE
            reasons.extend(scale_extra)
        elif kill_extra and len(kill_extra) > len(scale_extra):
            kind = ScaleKillKind.KILL
            reasons.extend(kill_extra)
        confidence = min(
            1.0,
            base.confidence + 0.05 * len(scale_extra + kill_extra),
        )
        return ScaleKillRecommendation(
            kind=kind,
            reasons=reasons[:20],
            confidence=round(confidence, 3),
            suggested_actions=list(base.suggested_actions),
        )


__all__ = ["VentureKillScale", "VentureSignal"]
