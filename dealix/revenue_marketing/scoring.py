"""Scoring helpers for the Revenue Marketing Engine.

All scoring functions are pure and deterministic. Inputs are clamped to [0, 1].
"""

from __future__ import annotations

from typing import Literal

from dealix.revenue_marketing.schemas import compute_lead_score as _compute_lead_score

OutcomeClassification = Literal[
    "noise",
    "engagement_only",
    "leads_only",
    "sales_motion",
    "revenue_validated",
]


def _clamp01(value: float) -> float:
    return max(0.0, min(1.0, float(value)))


def compute_lead_score(
    icp_fit: float,
    pain: float,
    ability_to_pay: float,
    urgency: float,
    partner_potential: float,
    trust_fit: float,
) -> float:
    """Weighted lead score in [0, 1]. Re-exported for convenience."""
    return _compute_lead_score(
        icp_fit=icp_fit,
        pain=pain,
        ability_to_pay=ability_to_pay,
        urgency=urgency,
        partner_potential=partner_potential,
        trust_fit=trust_fit,
    )


# Money-quality weights — positives sum to 1.0 before risk subtraction.
MQS_WEIGHTS = {
    "margin_pct": 0.25,
    "repeatability": 0.20,
    "low_delivery_effort": 0.15,
    "upsell_potential": 0.15,
    "data_moat": 0.10,
    "partner_potential": 0.15,
}


def compute_money_quality_score(
    margin_pct: float,
    repeatability: float,
    low_delivery_effort: float,
    upsell_potential: float,
    data_moat: float,
    partner_potential: float,
    risk: float,
) -> float:
    """Weighted positives minus risk, normalized to [0, 1].

    Each input is in [0, 1]. Risk subtracts up to 0.5 from the positive base
    so a maximally risky offer can still register some quality if positives
    are perfect.
    """
    positives = (
        _clamp01(margin_pct) * MQS_WEIGHTS["margin_pct"]
        + _clamp01(repeatability) * MQS_WEIGHTS["repeatability"]
        + _clamp01(low_delivery_effort) * MQS_WEIGHTS["low_delivery_effort"]
        + _clamp01(upsell_potential) * MQS_WEIGHTS["upsell_potential"]
        + _clamp01(data_moat) * MQS_WEIGHTS["data_moat"]
        + _clamp01(partner_potential) * MQS_WEIGHTS["partner_potential"]
    )
    penalty = _clamp01(risk) * 0.5
    return round(_clamp01(positives - penalty), 4)


def classify_outcome(
    touches: int,
    leads: int,
    calls: int,
    proposals: int,
    wins: int,
) -> OutcomeClassification:
    """Anti-vanity ladder classification.

    Ascending: noise -> engagement_only -> leads_only -> sales_motion -> revenue_validated.
    Each rung requires the previous funnel-step to be present.
    """
    touches = max(0, int(touches))
    leads = max(0, int(leads))
    calls = max(0, int(calls))
    proposals = max(0, int(proposals))
    wins = max(0, int(wins))

    if wins > 0 and proposals > 0:
        return "revenue_validated"
    if proposals > 0 and calls > 0:
        return "sales_motion"
    if calls > 0 and leads > 0:
        return "sales_motion"
    if leads > 0:
        return "leads_only"
    if touches > 0:
        return "engagement_only"
    return "noise"
