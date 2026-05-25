"""Quarterly partner performance reviews keyed on verified revenue + compliance."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PerformanceReview:
    partner_id: str
    period: str
    verified_revenue_sar: float
    deals_closed: int
    compliance_violations: int
    rating: str
    keep_tier: bool


def evaluate(
    partner_id: str,
    period: str,
    *,
    verified_revenue_sar: float,
    deals_closed: int,
    compliance_violations: int,
) -> PerformanceReview:
    """Rate a partner for a period and recommend whether to retain their tier."""
    rating = "A"
    if compliance_violations > 0:
        rating = "C"
    elif deals_closed == 0 and verified_revenue_sar == 0:
        rating = "D"
    elif verified_revenue_sar < 25_000:
        rating = "B"
    keep_tier = rating in {"A", "B"} and compliance_violations == 0
    return PerformanceReview(
        partner_id=partner_id,
        period=period,
        verified_revenue_sar=float(verified_revenue_sar),
        deals_closed=int(deals_closed),
        compliance_violations=int(compliance_violations),
        rating=rating,
        keep_tier=keep_tier,
    )
