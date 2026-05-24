"""Customer Health Score.

Inputs are normalised to [0, 1]; the score weights usage, outcomes, and
communication, then layers a churn-risk and upsell-potential signal on top.
"""

from __future__ import annotations

from dataclasses import dataclass

from dealix.hermes.core.scoring import clip01, weighted_score


@dataclass(slots=True)
class CustomerSignals:
    usage_score: float
    outcome_score: float
    communication_score: float
    value_score: float
    renewal_risk: float  # higher = worse
    upsell_potential: float


_WEIGHTS = {
    "usage_score": 0.3,
    "outcome_score": 0.35,
    "communication_score": 0.2,
    "value_score": 0.15,
}


@dataclass(slots=True)
class HealthVerdict:
    score: float
    label: str  # "thriving" | "ok" | "at_risk" | "lost"
    renewal_risk: float
    upsell_potential: float
    rationale: str


def evaluate(signals: CustomerSignals) -> HealthVerdict:
    values = {
        "usage_score": signals.usage_score,
        "outcome_score": signals.outcome_score,
        "communication_score": signals.communication_score,
        "value_score": signals.value_score,
    }
    base = weighted_score(_WEIGHTS, values)
    risk = clip01(signals.renewal_risk)
    upsell = clip01(signals.upsell_potential)
    score = clip01(base - 0.4 * risk)

    if score >= 0.75:
        label = "thriving"
    elif score >= 0.55:
        label = "ok"
    elif score >= 0.3:
        label = "at_risk"
    else:
        label = "lost"

    rationale = (
        f"base={base:.2f} risk={risk:.2f} upsell={upsell:.2f} → {score:.2f}"
    )
    return HealthVerdict(
        score=round(score, 3),
        label=label,
        renewal_risk=risk,
        upsell_potential=upsell,
        rationale=rationale,
    )


__all__ = ["CustomerSignals", "HealthVerdict", "evaluate"]
