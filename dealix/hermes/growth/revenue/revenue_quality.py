"""Compute revenue quality: gross margin, churn risk, repeatability."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RevenueQuality:
    gross_margin: float
    churn_risk: float
    repeatability: float
    quality_score: float
    grade: str


def _grade(score: float) -> str:
    if score >= 0.85:
        return "A"
    if score >= 0.70:
        return "B"
    if score >= 0.55:
        return "C"
    return "D"


def assess(*, gross_margin: float, churn_risk: float, repeatability: float) -> RevenueQuality:
    """Combine margin, churn risk, and repeatability into a quality score and letter grade."""
    gm = max(0.0, min(1.0, gross_margin))
    cr = max(0.0, min(1.0, churn_risk))
    rep = max(0.0, min(1.0, repeatability))
    score = round(0.4 * gm + 0.3 * (1.0 - cr) + 0.3 * rep, 4)
    return RevenueQuality(
        gross_margin=gm,
        churn_risk=cr,
        repeatability=rep,
        quality_score=score,
        grade=_grade(score),
    )
