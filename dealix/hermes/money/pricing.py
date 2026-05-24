"""Pricing Intelligence — recommends prices within approved bands."""

from __future__ import annotations

from dataclasses import dataclass

from dealix.hermes.core.schemas import Opportunity


@dataclass
class PriceRecommendation:
    floor_sar: float
    target_sar: float
    ceiling_sar: float
    rationale: str


class PricingIntelligence:
    def recommend(self, opp: Opportunity) -> PriceRecommendation:
        # Anchor the band on estimated value and strategic score.
        base = max(opp.estimated_value_sar, 1_000.0)
        strategic_mult = 1.0 + (opp.strategic_score - 3) * 0.1
        target = base * strategic_mult
        return PriceRecommendation(
            floor_sar=round(target * 0.7, 2),
            target_sar=round(target, 2),
            ceiling_sar=round(target * 1.4, 2),
            rationale=(
                f"Anchor SAR {base:.0f} × strategic mult {strategic_mult:.2f}; "
                "ceiling is +40% to leave negotiation room."
            ),
        )
