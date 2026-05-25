"""Summarize revenue quality across the period for a board audience."""

from __future__ import annotations

from dataclasses import dataclass

from ..growth.revenue.revenue_quality import RevenueQuality


@dataclass(frozen=True)
class RevenueQualitySummary:
    period: str
    grade: str
    quality_score: float
    gross_margin: float
    churn_risk: float
    repeatability: float
    headline: str


def summarize(period: str, quality: RevenueQuality) -> RevenueQualitySummary:
    """Produce a single-screen RevenueQualitySummary for board consumption."""
    headline = (
        f"Revenue quality grade {quality.grade} "
        f"(margin {quality.gross_margin * 100:.0f}%, churn risk {quality.churn_risk * 100:.0f}%, "
        f"repeatability {quality.repeatability * 100:.0f}%)"
    )
    return RevenueQualitySummary(
        period=period,
        grade=quality.grade,
        quality_score=quality.quality_score,
        gross_margin=quality.gross_margin,
        churn_risk=quality.churn_risk,
        repeatability=quality.repeatability,
        headline=headline,
    )
