"""Scoring rules for Hermes opportunities and money actions."""

from __future__ import annotations

from dataclasses import replace

from dealix.hermes.sovereign.models import Opportunity


def _score(value: int | float) -> float:
    """Clamp a 1..5 score to a float."""

    return max(1.0, min(5.0, float(value)))


def compute_opportunity_score(
    *,
    cash_speed_score: int | float,
    strategic_score: int | float,
    repeatability_score: int | float,
    data_moat_score: int | float,
    difficulty_score: int | float,
    risk_score: int | float,
) -> float:
    """Compute the universal Hermes Opportunity Score."""

    raw = (
        0.25 * _score(cash_speed_score)
        + 0.20 * _score(strategic_score)
        + 0.20 * _score(repeatability_score)
        + 0.15 * _score(data_moat_score)
        - 0.10 * _score(difficulty_score)
        - 0.10 * _score(risk_score)
    )
    return round(raw, 3)


def compute_money_score(
    *,
    cash_speed_score: int | float,
    close_probability_score: int | float,
    deal_value_score: int | float,
    strategic_score: int | float,
    risk_score: int | float,
) -> float:
    """Compute Money Engine priority score."""

    raw = (
        0.30 * _score(cash_speed_score)
        + 0.25 * _score(close_probability_score)
        + 0.20 * _score(deal_value_score)
        + 0.15 * _score(strategic_score)
        - 0.10 * _score(risk_score)
    )
    return round(raw, 3)


def score_opportunity(opp: Opportunity) -> Opportunity:
    """Return a copy of an Opportunity with opportunity_score populated."""

    return replace(
        opp,
        opportunity_score=compute_opportunity_score(
            cash_speed_score=opp.cash_speed_score,
            strategic_score=opp.strategic_score,
            repeatability_score=opp.repeatability_score,
            data_moat_score=opp.data_moat_score,
            difficulty_score=opp.difficulty_score,
            risk_score=opp.risk_score,
        ),
    )


def lifecycle_recommendation(opp: Opportunity) -> str:
    """Recommend scale, execute, defer, or retire using score and risk."""

    scored = score_opportunity(opp)
    if scored.risk_score >= 5:
        return "retire_or_red_team"
    if scored.opportunity_score >= 2.75 and scored.repeatability_score >= 4:
        return "scale"
    if scored.opportunity_score >= 2.0:
        return "execute"
    if scored.opportunity_score >= 1.25:
        return "defer_or_request_more_info"
    return "retire"
