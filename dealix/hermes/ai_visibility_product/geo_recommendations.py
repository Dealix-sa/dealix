"""Generate GEO recommendations based on customer mention/citation gaps."""

from __future__ import annotations

from dataclasses import dataclass

from .trust_signal_score import TrustSignalScore


@dataclass(frozen=True)
class GeoRecommendation:
    customer_id: str
    headline: str
    actions: tuple[str, ...]
    priority: str


def recommend(score: TrustSignalScore) -> GeoRecommendation:
    """Return a prioritized GeoRecommendation based on the current trust signal band."""
    if score.band == "strong":
        return GeoRecommendation(
            customer_id=score.customer_id,
            headline="Maintain visibility and protect ranking",
            actions=("publish quarterly citation asset", "monitor competitor mentions"),
            priority="low",
        )
    if score.band == "fair":
        return GeoRecommendation(
            customer_id=score.customer_id,
            headline="Convert visibility into citations",
            actions=("add evidence-backed answer pages", "request third-party citations"),
            priority="medium",
        )
    if score.band == "weak":
        return GeoRecommendation(
            customer_id=score.customer_id,
            headline="Raise brand presence in target queries",
            actions=("publish answer-engine pages", "submit to authoritative directories"),
            priority="high",
        )
    return GeoRecommendation(
        customer_id=score.customer_id,
        headline="Establish baseline visibility",
        actions=("audit entity consistency", "publish foundational case studies"),
        priority="critical",
    )
