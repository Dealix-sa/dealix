"""Can this asset be sold? Should it become a productized offer?"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CommercialReview:
    commercialize: bool
    reason: str
    recommended_offer_id: str | None = None


def evaluate_commercialization(
    *,
    reuse_count: int,
    revenue_attributed_sar: float,
    quality_score: float,
) -> CommercialReview:
    if reuse_count >= 3 and revenue_attributed_sar >= 25_000 and quality_score >= 0.5:
        return CommercialReview(
            commercialize=True,
            reason="meets reuse + revenue + quality thresholds",
        )
    return CommercialReview(commercialize=False, reason="below commercial threshold")
