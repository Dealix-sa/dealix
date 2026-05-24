"""خادم المنتج — ProductScaleKill (spec §46).

Specialised wrapper around `ScaleKillRecommender` for product-level
signals. Adds product-level reasons (pricing volatility, churn,
conversion) on top of the generic SCALE/KILL/HOLD verdict.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal

from dealix.hermes.core.outcomes import Outcome, OutcomeKind
from dealix.hermes.core.scale import (
    ScaleKillKind,
    ScaleKillRecommendation,
    ScaleKillRecommender,
)


@dataclass(frozen=True)
class ProductMetrics:
    """Cross-cutting product KPIs that overlay the generic recommender."""

    churn_pct: float = 0.0
    conversion_pct: float = 0.0
    avg_price: Decimal = Decimal("0")
    pricing_volatility_pct: float = 0.0


_CHURN_KILL_THRESHOLD = 0.25  # 25 % monthly churn = product is bleeding
_CONVERSION_SCALE_THRESHOLD = 0.10  # 10 % conversion = healthy
_PRICING_VOLATILITY_LIMIT = 0.30  # >30 % swings = unstable pricing


class ProductScaleKill:
    """Product-specialised SCALE/KILL/HOLD recommender."""

    def __init__(self, recommender: ScaleKillRecommender | None = None) -> None:
        self._recommender = recommender or ScaleKillRecommender()

    def recommend(
        self,
        outcomes: list[Outcome],
        metrics: ProductMetrics | None = None,
    ) -> ScaleKillRecommendation:
        base = self._recommender.recommend(outcomes)
        if metrics is None:
            return base

        extra_scale: list[str] = []
        extra_kill: list[str] = []

        if metrics.conversion_pct >= _CONVERSION_SCALE_THRESHOLD:
            extra_scale.append(
                f"conversion {metrics.conversion_pct:.1%} >= scale threshold"
            )
        if metrics.churn_pct >= _CHURN_KILL_THRESHOLD:
            extra_kill.append(
                f"churn {metrics.churn_pct:.1%} >= kill threshold"
            )
        if metrics.pricing_volatility_pct >= _PRICING_VOLATILITY_LIMIT:
            extra_kill.append(
                f"pricing volatility {metrics.pricing_volatility_pct:.1%} >= "
                f"{_PRICING_VOLATILITY_LIMIT:.0%}"
            )
        if metrics.avg_price > 0 and any(
            o.value is not None and o.value.amount >= metrics.avg_price for o in outcomes
            if o.kind == OutcomeKind.MONEY
        ):
            extra_scale.append("paid outcomes at or above avg_price")

        kind = base.kind
        reasons = list(base.reasons)
        actions = list(base.suggested_actions)

        if extra_kill and len(extra_kill) >= len(extra_scale):
            kind = ScaleKillKind.KILL
            reasons.extend(extra_kill)
            actions.append("Review pricing volatility + churn drivers")
        elif extra_scale and len(extra_scale) > len(extra_kill):
            kind = ScaleKillKind.SCALE
            reasons.extend(extra_scale)
            actions.append("Promote to standing offer in catalog")

        # Re-cap confidence at slightly higher when product KPIs reinforce.
        confidence = min(1.0, base.confidence + 0.05 * len(extra_scale + extra_kill))

        return ScaleKillRecommendation(
            kind=kind,
            reasons=reasons[:20],
            confidence=round(confidence, 3),
            suggested_actions=actions[:20],
        )


__all__ = ["ProductMetrics", "ProductScaleKill"]
