"""Opportunity scoring helpers.

Scores are deterministic and explainable so the founder can inspect why Dealix
selected a target before approving any external action.
"""

from __future__ import annotations


def clamp_score(value: int) -> int:
    return max(0, min(100, value))


def score_opportunity(
    *,
    fit: int,
    signal: int,
    urgency: int,
    value: int,
    access: int,
    risk: int,
) -> int:
    """Return a 0-100 score where risk is a penalty.

    The weights intentionally favor fit and signal quality over raw deal value.
    """

    weighted = (
        fit * 0.28
        + signal * 0.22
        + urgency * 0.16
        + value * 0.18
        + access * 0.16
        - risk * 0.20
    )
    return clamp_score(round(weighted))


def score_label(score: int) -> str:
    if score >= 80:
        return "hot"
    if score >= 60:
        return "warm"
    if score >= 40:
        return "research"
    return "hold"
