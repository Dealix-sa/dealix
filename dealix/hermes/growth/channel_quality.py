"""
ChannelQuality — does this channel produce *verified* revenue, or just
pipeline noise?
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ChannelMetrics:
    name: str
    touches: int
    leads: int
    qualified: int
    proposals: int
    payments: int
    verified_revenue_sar: float
    cost_sar: float


@dataclass
class ChannelQualityScore:
    channel: str
    score: float
    verified_revenue_sar: float
    margin_ratio: float
    grade: str
    recommendation: str


def score_channel(metrics: ChannelMetrics) -> ChannelQualityScore:
    if metrics.touches == 0:
        return ChannelQualityScore(
            channel=metrics.name,
            score=0.0,
            verified_revenue_sar=0.0,
            margin_ratio=0.0,
            grade="F",
            recommendation="Channel inactive.",
        )
    convert = metrics.payments / max(metrics.touches, 1)
    qualify = metrics.qualified / max(metrics.leads, 1)
    proposal_rate = metrics.proposals / max(metrics.qualified, 1)
    margin_ratio = (metrics.verified_revenue_sar - metrics.cost_sar) / max(metrics.verified_revenue_sar, 1.0)
    score = round(
        0.5 * convert + 0.2 * qualify + 0.1 * proposal_rate + 0.2 * max(0.0, margin_ratio),
        4,
    )
    if score >= 0.4 and margin_ratio > 0.5:
        grade, rec = "A", "Scale spend; document the play."
    elif score >= 0.25:
        grade, rec = "B", "Optimize messaging; double down selectively."
    elif score >= 0.1:
        grade, rec = "C", "Investigate before increasing spend."
    else:
        grade, rec = "D", "Pause channel until margin or conversion improves."
    return ChannelQualityScore(
        channel=metrics.name,
        score=score,
        verified_revenue_sar=metrics.verified_revenue_sar,
        margin_ratio=round(margin_ratio, 4),
        grade=grade,
        recommendation=rec,
    )
