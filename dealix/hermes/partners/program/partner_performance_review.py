"""PartnerPerformance — quarterly review producing keep / coach / drop."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class PartnerPerformance:
    partner_id: str
    period: str
    verified_revenue_sar: float
    incidents: int
    customer_csat: float
    decision: str
    reasons: tuple[str, ...]


def review_partner(
    *,
    partner_id: str,
    period: str,
    verified_revenue_sar: float,
    incidents: int,
    customer_csat: float,
    minimum_verified_revenue_sar: float,
) -> PartnerPerformance:
    reasons: list[str] = []
    if incidents > 3:
        reasons.append("too many incidents this period")
    if customer_csat < 0.6:
        reasons.append("customer satisfaction below threshold")
    if verified_revenue_sar < minimum_verified_revenue_sar:
        reasons.append("below minimum verified revenue for tier")

    if not reasons and verified_revenue_sar >= minimum_verified_revenue_sar * 1.5:
        decision = "scale"
    elif not reasons:
        decision = "keep"
    elif len(reasons) == 1:
        decision = "coach"
    else:
        decision = "drop"

    return PartnerPerformance(
        partner_id=partner_id,
        period=period,
        verified_revenue_sar=verified_revenue_sar,
        incidents=incidents,
        customer_csat=customer_csat,
        decision=decision,
        reasons=tuple(reasons) or ("on track",),
    )
