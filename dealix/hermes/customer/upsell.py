"""Upsell candidate surfacing."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class UpsellCandidate:
    customer_id: str
    target_offer_id: str
    estimated_value_sar: float
    rationale: str


def surface_upsell(
    *,
    customer_id: str,
    health_score: float,
    usage_growth_pct: float,
    target_offer_id: str,
    estimated_value_sar: float,
) -> UpsellCandidate | None:
    if health_score < 0.6 or usage_growth_pct < 0.1:
        return None
    return UpsellCandidate(
        customer_id=customer_id,
        target_offer_id=target_offer_id,
        estimated_value_sar=estimated_value_sar,
        rationale=f"healthy ({health_score:.2f}) and growing ({usage_growth_pct:.1%})",
    )
