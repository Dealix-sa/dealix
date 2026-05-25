"""
PricingEngine — recommend a price band for an offer given buyer type,
complexity, urgency, proof, risk, and partner involvement.

All pricing decisions are S2: the engine produces a recommendation,
``approve_pricing`` capability is still required to execute it.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class PricingInputs:
    offer_id: str
    buyer_type: str  # "smb" | "enterprise" | "agency" | "venture"
    sector: str
    urgency: str  # "low" | "medium" | "high"
    delivery_complexity: str  # "low" | "medium" | "high"
    proof_level: str  # "weak" | "medium" | "strong"
    risk_level: str  # "low" | "medium" | "high"
    retainer_potential: bool
    partner_involved: bool


@dataclass
class PricingRecommendation:
    offer_id: str
    recommended_price_sar: float
    floor_price_sar: float
    target_price_sar: float
    pricing_confidence: float
    requires_approval: bool
    reason: str


_BASE = {
    "smb": 6000,
    "enterprise": 30000,
    "agency": 12000,
    "venture": 9000,
}

_COMPLEXITY = {"low": 1.0, "medium": 1.4, "high": 2.0}
_URGENCY = {"low": 1.0, "medium": 1.1, "high": 1.25}
_PROOF = {"weak": 0.9, "medium": 1.0, "strong": 1.15}
_RISK = {"low": 1.0, "medium": 0.95, "high": 0.85}


def recommend_price(inputs: PricingInputs) -> PricingRecommendation:
    base = _BASE.get(inputs.buyer_type, 8000)
    multiplier = (
        _COMPLEXITY[inputs.delivery_complexity]
        * _URGENCY[inputs.urgency]
        * _PROOF[inputs.proof_level]
        * _RISK[inputs.risk_level]
    )
    if inputs.retainer_potential:
        multiplier *= 1.1
    if inputs.partner_involved:
        multiplier *= 0.95
    target = round(base * multiplier, -2)
    floor = round(target * 0.6, -2)
    recommended = round(target * 0.9, -2)
    confidence = round(0.5 + 0.05 * (1 if inputs.proof_level == "strong" else 0) + 0.05 * (1 if inputs.retainer_potential else 0), 2)
    reason_parts = [
        f"{inputs.buyer_type}/{inputs.sector}",
        f"complexity={inputs.delivery_complexity}",
        f"urgency={inputs.urgency}",
        f"risk={inputs.risk_level}",
    ]
    return PricingRecommendation(
        offer_id=inputs.offer_id,
        recommended_price_sar=recommended,
        floor_price_sar=floor,
        target_price_sar=target,
        pricing_confidence=confidence,
        requires_approval=True,
        reason=", ".join(reason_parts),
    )
