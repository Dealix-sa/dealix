"""Turn a market trend into a proposed offer hypothesis."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class OfferHypothesis:
    trend: str
    buyer: str
    pain: str
    proposed_offer_name: str
    plausibility_score: int


def trend_to_offer(*, trend: str, buyer: str, pain: str) -> OfferHypothesis:
    name = f"{trend} Quick-Win Kit"
    plausibility = 3
    if "regulation" in trend.lower() or "compliance" in trend.lower():
        plausibility = 4
    if "ai governance" in trend.lower():
        plausibility = 5
    return OfferHypothesis(
        trend=trend,
        buyer=buyer,
        pain=pain,
        proposed_offer_name=name,
        plausibility_score=plausibility,
    )
