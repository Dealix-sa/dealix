"""Prospect scoring — 7 weighted factors summing to 100.

Pure functions. Each factor is supplied as a 0.0..1.0 fitness fraction and
scaled by its weight. Total >= ``QUALIFY_THRESHOLD`` marks the prospect
qualified for draft production.
"""

from __future__ import annotations

from dataclasses import dataclass

WEIGHTS: dict[str, int] = {
    "sector_fit": 20,
    "likely_lead_flow": 20,
    "decision_maker_clarity": 15,
    "pain_signal": 15,
    "payment_ability": 15,
    "personalization_signal": 10,
    "risk_low": 5,
}

QUALIFY_THRESHOLD: int = 60

assert sum(WEIGHTS.values()) == 100, "prospect score weights must sum to 100"


@dataclass(frozen=True, slots=True)
class ProspectScore:
    total: int
    breakdown: dict[str, int]
    qualified: bool
    reasons: tuple[str, ...]


def _clamp(value: float) -> float:
    if value < 0.0:
        return 0.0
    if value > 1.0:
        return 1.0
    return value


def score_prospect(
    *,
    sector_fit: float,
    likely_lead_flow: float,
    decision_maker_clarity: float,
    pain_signal: float,
    payment_ability: float,
    personalization_signal: float,
    risk_low: float,
) -> ProspectScore:
    """Return a :class:`ProspectScore`. Inputs are 0.0..1.0 fitness fractions."""
    factors: dict[str, float] = {
        "sector_fit": sector_fit,
        "likely_lead_flow": likely_lead_flow,
        "decision_maker_clarity": decision_maker_clarity,
        "pain_signal": pain_signal,
        "payment_ability": payment_ability,
        "personalization_signal": personalization_signal,
        "risk_low": risk_low,
    }
    breakdown: dict[str, int] = {
        name: round(_clamp(frac) * WEIGHTS[name]) for name, frac in factors.items()
    }
    total = sum(breakdown.values())
    reasons: list[str] = []
    if breakdown["personalization_signal"] == 0:
        reasons.append("no_personalization_signal")
    if breakdown["pain_signal"] == 0:
        reasons.append("no_pain_signal")
    if breakdown["decision_maker_clarity"] == 0:
        reasons.append("unclear_decision_maker")
    if total < QUALIFY_THRESHOLD:
        reasons.append(f"below_threshold:{total}<{QUALIFY_THRESHOLD}")
    return ProspectScore(
        total=total,
        breakdown=breakdown,
        qualified=total >= QUALIFY_THRESHOLD,
        reasons=tuple(reasons),
    )


__all__ = ["QUALIFY_THRESHOLD", "WEIGHTS", "ProspectScore", "score_prospect"]
