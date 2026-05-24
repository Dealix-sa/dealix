"""Pricing — converts an offer + opportunity into a recommended price.

Pricing logic is deliberately simple. The point of the module is not a
clever model; it is to enforce that *no proposal goes out without a
recorded pricing rationale*.
"""

from __future__ import annotations

from dataclasses import dataclass

from dealix.hermes.core.schemas import Opportunity


@dataclass(slots=True)
class PriceQuote:
    floor_sar: float
    target_sar: float
    ceiling_sar: float
    rationale: str
    confidence: float  # 0..1


def quote(
    *,
    base_floor: float,
    base_ceiling: float,
    opportunity: Opportunity,
    delivery_complexity: float = 0.5,
    risk_loading: float = 0.0,
) -> PriceQuote:
    """Return floor/target/ceiling for an offer in SAR.

    The target sits between the floor and the ceiling, biased upward by
    `delivery_complexity` (effort) and `risk_loading` (insurance) and
    downward by `close_probability` (concession).
    """
    if base_floor <= 0 or base_ceiling < base_floor:
        raise ValueError("invalid base price range")

    width = base_ceiling - base_floor
    bias = 0.5 + (delivery_complexity - 0.5) * 0.4 + risk_loading * 0.3
    bias = max(0.0, min(1.0, bias))

    target = base_floor + width * bias
    target = round(target * (0.9 + 0.2 * opportunity.fit_score), 2)
    target = max(base_floor, min(base_ceiling, target))

    confidence = round(
        0.4
        + 0.3 * opportunity.fit_score
        + 0.2 * opportunity.close_probability
        - 0.2 * opportunity.risk_score,
        3,
    )
    confidence = max(0.0, min(1.0, confidence))

    rationale = (
        f"floor={base_floor:.0f} ceiling={base_ceiling:.0f} "
        f"fit={opportunity.fit_score:.2f} risk={opportunity.risk_score:.2f} "
        f"complexity={delivery_complexity:.2f} loading={risk_loading:.2f}"
    )
    return PriceQuote(
        floor_sar=base_floor,
        target_sar=target,
        ceiling_sar=base_ceiling,
        rationale=rationale,
        confidence=confidence,
    )


__all__ = ["PriceQuote", "quote"]
