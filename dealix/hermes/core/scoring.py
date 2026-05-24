"""Opportunity scoring.

The default scorer matches the Money Score formula in section 116:

    score =
        + 0.30 cash_speed
        + 0.25 close_probability
        + 0.20 deal_value     (normalized)
        + 0.15 strategic_value
        - 0.10 risk

Inputs are clamped to [0,1]; ``deal_value_sar`` is normalized by the
configured ``deal_value_anchor_sar`` (default 100,000 SAR ≈ 1.0).
"""

from __future__ import annotations

from dataclasses import dataclass

from dealix.hermes.core.schemas import Opportunity


def _clip(x: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, x))


@dataclass
class ScoreInputs:
    cash_speed: float = 0.0
    close_probability: float = 0.0
    deal_value_sar: float = 0.0
    strategic_value: float = 0.0
    risk: float = 0.0


class OpportunityScorer:
    def __init__(self, deal_value_anchor_sar: float = 100_000.0) -> None:
        if deal_value_anchor_sar <= 0:
            raise ValueError("deal_value_anchor_sar must be > 0.")
        self.anchor = deal_value_anchor_sar

    def compute(self, inputs: ScoreInputs) -> tuple[float, dict[str, float]]:
        cs = _clip(inputs.cash_speed)
        cp = _clip(inputs.close_probability)
        dv = _clip(inputs.deal_value_sar / self.anchor)
        sv = _clip(inputs.strategic_value)
        rk = _clip(inputs.risk)
        breakdown = {
            "cash_speed": 0.30 * cs,
            "close_probability": 0.25 * cp,
            "deal_value": 0.20 * dv,
            "strategic_value": 0.15 * sv,
            "risk_penalty": -0.10 * rk,
        }
        total = sum(breakdown.values())
        return _clip(total), breakdown

    def score(self, opp: Opportunity, inputs: ScoreInputs) -> Opportunity:
        total, breakdown = self.compute(inputs)
        opp.score = total
        opp.score_breakdown = breakdown
        opp.estimated_value_sar = inputs.deal_value_sar
        opp.touch()
        return opp


__all__ = ["OpportunityScorer", "ScoreInputs"]
