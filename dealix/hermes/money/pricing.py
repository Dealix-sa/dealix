"""Pricing intelligence — recommend a price band for a proposal.

This is a deliberately small heuristic model. The goal is to keep the
founder out of the trap of either pricing too low (no margin, no signal
of value) or pricing too high (no close).
"""

from __future__ import annotations

from dataclasses import dataclass

from dealix.hermes.core.schemas import Opportunity
from dealix.hermes.trust.guardrails import (
    PRICING_CEILING_AUTONOMOUS_SAR,
    PRICING_FLOOR_SAR,
)


@dataclass
class PriceBand:
    low_sar: float
    target_sar: float
    high_sar: float
    rationale: str
    requires_approval: bool


def recommend_band(opp: Opportunity, base_price_sar: float) -> PriceBand:
    """Return a (low, target, high) band derived from opportunity scores.

    Target is `base_price_sar` adjusted by close probability and risk.
    """
    confidence = max(0.5, min(1.5, 0.75 + opp.close_probability))
    risk_penalty = 1.0 - (opp.risk_score / 200.0)
    target = base_price_sar * confidence * risk_penalty
    low = max(PRICING_FLOOR_SAR, target * 0.8)
    high = target * 1.25
    requires_approval = high > PRICING_CEILING_AUTONOMOUS_SAR

    rationale = (
        f"base={base_price_sar:.0f}, confidence={confidence:.2f}, "
        f"risk_penalty={risk_penalty:.2f} → target={target:.0f} SAR"
    )
    return PriceBand(
        low_sar=round(low, 2),
        target_sar=round(target, 2),
        high_sar=round(high, 2),
        rationale=rationale,
        requires_approval=requires_approval,
    )
