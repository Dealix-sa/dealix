"""Fit score for a candidate partner (section 118)."""

from __future__ import annotations

from dataclasses import dataclass


def _clip(x: float) -> float:
    return max(0.0, min(1.0, x))


@dataclass
class PartnerFitInputs:
    client_base: float
    sales_capability: float
    delivery_capability: float
    trust_level: float
    sector_fit: float
    risk_level: float


class PartnerFitScorer:
    def compute(self, inputs: PartnerFitInputs) -> tuple[float, dict[str, float]]:
        b = {
            "client_base": 0.25 * _clip(inputs.client_base),
            "sales_capability": 0.20 * _clip(inputs.sales_capability),
            "delivery_capability": 0.20 * _clip(inputs.delivery_capability),
            "trust_level": 0.15 * _clip(inputs.trust_level),
            "sector_fit": 0.15 * _clip(inputs.sector_fit),
            "risk_penalty": -0.15 * _clip(inputs.risk_level),
        }
        return _clip(sum(b.values())), b


__all__ = ["PartnerFitInputs", "PartnerFitScorer"]
