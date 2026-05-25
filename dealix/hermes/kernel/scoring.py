"""Opportunity scoring and Asset quality scoring."""

from __future__ import annotations

from dealix.hermes.kernel.schemas import Opportunity, RecommendedAction


# Weights are tunable from config — these are the doctrine defaults.
OPPORTUNITY_WEIGHTS = {
    "cash_speed": 0.25,
    "strategic": 0.20,
    "repeatability": 0.20,
    "data_moat": 0.15,
    "difficulty_penalty": -0.10,
    "risk_penalty": -0.10,
}


def score_opportunity(opp: Opportunity) -> float:
    """Composite score on a 0..5 scale (signed)."""
    s = (
        opp.cash_speed_score * OPPORTUNITY_WEIGHTS["cash_speed"]
        + opp.strategic_score * OPPORTUNITY_WEIGHTS["strategic"]
        + opp.repeatability_score * OPPORTUNITY_WEIGHTS["repeatability"]
        + opp.data_moat_score * OPPORTUNITY_WEIGHTS["data_moat"]
        + opp.difficulty_score * OPPORTUNITY_WEIGHTS["difficulty_penalty"]
        + opp.risk_score * OPPORTUNITY_WEIGHTS["risk_penalty"]
    )
    return round(s, 4)


def recommend(opp: Opportunity) -> RecommendedAction:
    score = opp.composite_score or score_opportunity(opp)
    if opp.risk_score >= 5:
        return RecommendedAction.kill
    if score >= 2.5:
        return RecommendedAction.execute
    if score >= 1.0:
        return RecommendedAction.defer
    return RecommendedAction.kill


def asset_quality_score(
    *,
    reuse_count: int,
    revenue_attributed_sar: float,
    moat_score: float,
) -> float:
    """0..1 score combining reuse, revenue, and moat."""
    reuse_term = min(reuse_count / 10.0, 1.0) * 0.4
    revenue_term = min(revenue_attributed_sar / 100_000.0, 1.0) * 0.4
    moat_term = max(0.0, min(moat_score, 1.0)) * 0.2
    return round(reuse_term + revenue_term + moat_term, 4)
