"""خادم Hermes — pure scoring functions.

Three exposed functions:
  * opportunity_score(opp)   → float in [0, 5]
  * risk_score(context)      → RiskLevel
  * partner_fit_score(p, o)  → float in [0, 5]

These are deliberately pure: no I/O, no globals, no LLM calls. Weighting
constants live at module scope so tests can pin them or rebalance.
"""

from __future__ import annotations

from decimal import Decimal
from typing import Any

from dealix.hermes.core.opportunities import Opportunity, OpportunityType
from dealix.hermes.core.schemas import RiskLevel


# ─────────────────────────────────────────────────────────────
# Weighting constants
# ─────────────────────────────────────────────────────────────

# Spec: revenue 0.3, urgency 0.2, fit 0.3, effort_inverse 0.2
OPPORTUNITY_WEIGHTS: dict[str, float] = {
    "revenue": 0.30,
    "urgency": 0.20,
    "fit": 0.30,
    "effort_inverse": 0.20,
}

# Revenue normalisation: 25,000 SAR maps to a full 5-point component.
_REVENUE_CAP_SAR: Decimal = Decimal("25000")

# Partner-fit weights
PARTNER_FIT_WEIGHTS: dict[str, float] = {
    "category_alignment": 0.40,
    "value_overlap": 0.30,
    "trust_score": 0.30,
}


def _revenue_component(opp: Opportunity) -> float:
    """Normalise expected_value to a 0–5 scale; missing money → 0."""
    if opp.expected_value is None:
        return 0.0
    amount = opp.expected_value.amount
    if amount <= 0:
        return 0.0
    capped = min(amount, _REVENUE_CAP_SAR)
    return float(capped / _REVENUE_CAP_SAR) * 5.0


def opportunity_score(opp: Opportunity) -> float:
    """Weighted aggregate score in [0, 5].

    components:
      revenue          = expected_value normalised to 25k SAR
      urgency          = urgency (1..5 → 1..5)
      fit              = fit_score (1..5 → 1..5)
      effort_inverse   = 6 - effort_score (5 means trivial)
    """
    revenue = _revenue_component(opp)
    urgency = float(opp.urgency)
    fit = float(opp.fit_score)
    effort_inv = float(6 - opp.effort_score)

    score = (
        OPPORTUNITY_WEIGHTS["revenue"] * revenue
        + OPPORTUNITY_WEIGHTS["urgency"] * urgency
        + OPPORTUNITY_WEIGHTS["fit"] * fit
        + OPPORTUNITY_WEIGHTS["effort_inverse"] * effort_inv
    )
    # Clamp & round to 3dp for stable comparison.
    return max(0.0, min(5.0, round(score, 3)))


def opportunity_score_components(opp: Opportunity) -> dict[str, float]:
    """Expose per-component contribution for evidence/audit trails."""
    return {
        "revenue": _revenue_component(opp),
        "urgency": float(opp.urgency),
        "fit": float(opp.fit_score),
        "effort_inverse": float(6 - opp.effort_score),
    }


# ─────────────────────────────────────────────────────────────
# Risk scoring
# ─────────────────────────────────────────────────────────────


_RISK_FLAGS = (
    "monetary_amount",
    "external_visibility",
    "sensitive_data",
    "legal_commitment",
    "regulator_facing",
)


def risk_score(context: dict[str, Any]) -> RiskLevel:
    """Coarse risk classifier driven by a small flag dictionary.

    Accepts keys: sensitive_data, legal_commitment, regulator_facing,
    external_visibility, monetary_amount (Money|int|float|None),
    public_api, mcp_external, financial_transfer.

    Returns RiskLevel; CRITICAL trumps everything else.
    """
    critical_keys = (
        "sensitive_data",
        "legal_commitment",
        "regulator_facing",
        "public_api",
        "mcp_external",
        "financial_transfer",
    )
    if any(bool(context.get(k)) for k in critical_keys):
        return RiskLevel.CRITICAL

    monetary = context.get("monetary_amount")
    amount = _coerce_amount(monetary)

    if amount is not None and amount >= Decimal("100000"):
        return RiskLevel.CRITICAL
    if amount is not None and amount >= Decimal("25000"):
        return RiskLevel.HIGH

    high_flags = sum(1 for k in _RISK_FLAGS if context.get(k))
    if high_flags >= 2 or context.get("external_visibility"):
        return RiskLevel.HIGH

    if amount is not None and amount >= Decimal("2500"):
        return RiskLevel.MEDIUM
    if context.get("strategic_partnership"):
        return RiskLevel.MEDIUM
    return RiskLevel.LOW


def _coerce_amount(value: Any) -> Decimal | None:
    if value is None:
        return None
    if hasattr(value, "amount"):
        try:
            return Decimal(str(value.amount))
        except Exception:  # pragma: no cover - defensive
            return None
    try:
        return Decimal(str(value))
    except Exception:  # pragma: no cover - defensive
        return None


# ─────────────────────────────────────────────────────────────
# Partner fit
# ─────────────────────────────────────────────────────────────


def partner_fit_score(partner: dict[str, Any], opportunity: Opportunity) -> float:
    """Score a partner against an opportunity in [0, 5].

    partner dict accepts: categories (list[str]), trust_score (0..5),
    value_overlap (0..1), region (str). Missing fields are treated as
    neutral (0).
    """
    categories = set(partner.get("categories") or [])
    same_category = (
        opportunity.opp_type.value in categories
        or "partnership" in categories
        or partner.get("any_match")
    )
    category_component = 5.0 if same_category else 1.5

    value_overlap_raw = float(partner.get("value_overlap") or 0.0)
    value_overlap = max(0.0, min(1.0, value_overlap_raw)) * 5.0

    trust_raw = float(partner.get("trust_score") or 0.0)
    trust_component = max(0.0, min(5.0, trust_raw))

    score = (
        PARTNER_FIT_WEIGHTS["category_alignment"] * category_component
        + PARTNER_FIT_WEIGHTS["value_overlap"] * value_overlap
        + PARTNER_FIT_WEIGHTS["trust_score"] * trust_component
    )
    return max(0.0, min(5.0, round(score, 3)))


__all__ = [
    "OPPORTUNITY_WEIGHTS",
    "PARTNER_FIT_WEIGHTS",
    "opportunity_score",
    "opportunity_score_components",
    "partner_fit_score",
    "risk_score",
]
