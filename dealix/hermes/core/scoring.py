"""
Hermes scoring — pure functions for opportunity & money scores.

Formulas mirror the canonical spec:

    Opportunity Score =
        0.25 cash_speed
      + 0.20 strategic
      + 0.20 repeatability
      + 0.15 data_moat
      - 0.10 difficulty
      - 0.10 risk

    Money Score =
        0.30 cash_speed
      + 0.25 close_probability
      + 0.20 deal_value (normalized)
      + 0.15 strategic
      - 0.10 risk
"""

from __future__ import annotations

from dealix.hermes.core.schemas import Opportunity, SovereigntyLevel


def score_opportunity(opp: Opportunity) -> float:
    """Compute the canonical opportunity score (range roughly -1.0 .. 5.0)."""
    return round(
        0.25 * opp.cash_speed_score
        + 0.20 * opp.strategic_score
        + 0.20 * opp.repeatability_score
        + 0.15 * opp.data_moat_score
        - 0.10 * opp.difficulty_score
        - 0.10 * opp.risk_score,
        4,
    )


def score_money(
    cash_speed: int,
    close_probability: float,
    deal_value_sar: float,
    strategic: int,
    risk: int,
    value_cap_sar: float = 100_000.0,
) -> float:
    """Money Score per the canonical formula. Deal value is normalized to [0,5]."""
    normalized_value = min(deal_value_sar / value_cap_sar, 1.0) * 5
    return round(
        0.30 * cash_speed
        + 0.25 * (close_probability * 5)
        + 0.20 * normalized_value
        + 0.15 * strategic
        - 0.10 * risk,
        4,
    )


def classify_sovereignty(opp: Opportunity) -> SovereigntyLevel:
    """Recommend a sovereignty level based on the opportunity shape.

    S0/S1 are auto-runnable; S2 routes through Sami before execution; S4 is
    sovereign-only (marketplace, public API, venture); S5 is never autonomous.
    S3 is reserved for explicitly-set "approve-by-policy, review-after" flows.
    """
    if opp.opportunity_type in {"marketplace", "api", "venture"}:
        return SovereigntyLevel.S4_SOVEREIGN_ONLY
    if opp.risk_score >= 4 or opp.estimated_value_sar >= 25_000:
        return SovereigntyLevel.S2_SAMI_APPROVAL
    return SovereigntyLevel.S1_INTERNAL
