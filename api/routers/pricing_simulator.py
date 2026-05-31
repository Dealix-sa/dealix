"""Pricing simulator for custom deal structuring and multi-year scenarios.

Provides deal structure options, payment incentives, and a simulation
function for calculating total contract value with applied discounts.
All data is static; no LLM or external API calls are made.

Prefix: /api/v1/pricing-simulator
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

router = APIRouter(
    prefix="/api/v1/pricing-simulator",
    tags=["Sales"],
)

# ---------------------------------------------------------------------------
# Governance constants
# ---------------------------------------------------------------------------

_GOV_REVIEW = "ALLOW_WITH_REVIEW"
_GOV_APPROVAL = "APPROVAL_FIRST"

# ---------------------------------------------------------------------------
# Static data: deal structures
# ---------------------------------------------------------------------------

_DEAL_STRUCTURES: dict[str, Any] = {
    "monthly": {
        "name_en": "Monthly",
        "name_ar": "شهري",
        "discount_pct": 0.0,
        "commitment_months": 1,
        "payment_terms_en": "Invoiced monthly. No long-term commitment required.",
        "payment_terms_ar": "يُفوتر شهرياً. لا يلزم الالتزام طويل الأمد.",
    },
    "quarterly": {
        "name_en": "Quarterly",
        "name_ar": "ربع سنوي",
        "discount_pct": 5.0,
        "commitment_months": 3,
        "payment_terms_en": "Invoiced quarterly in advance. 5% discount applied.",
        "payment_terms_ar": "يُفوتر ربع سنوياً مقدماً. يُطبق خصم 5%.",
    },
    "annual": {
        "name_en": "Annual",
        "name_ar": "سنوي",
        "discount_pct": 15.0,
        "commitment_months": 12,
        "payment_terms_en": "Invoiced annually in advance. 15% discount applied.",
        "payment_terms_ar": "يُفوتر سنوياً مقدماً. يُطبق خصم 15%.",
    },
    "multi_year": {
        "name_en": "Multi-Year",
        "name_ar": "متعدد السنوات",
        "discount_pct": 25.0,
        "commitment_months": 24,
        "payment_terms_en": "Invoiced annually over a 24-month term. 25% discount applied.",
        "payment_terms_ar": "يُفوتر سنوياً على مدى 24 شهراً. يُطبق خصم 25%.",
    },
}

# ---------------------------------------------------------------------------
# Static data: payment incentives
# ---------------------------------------------------------------------------

_PAYMENT_INCENTIVES: list[dict[str, Any]] = [
    {
        "incentive_id": "early_payment_30d",
        "incentive_en": "Early Payment (30 days)",
        "incentive_ar": "الدفع المبكر (30 يوماً)",
        "discount_addl_pct": 3.0,
    },
    {
        "incentive_id": "reference_customer",
        "incentive_en": "Reference Customer",
        "incentive_ar": "عميل مرجعي",
        "discount_addl_pct": 5.0,
    },
    {
        "incentive_id": "case_study_rights",
        "incentive_en": "Case Study Rights",
        "incentive_ar": "حقوق دراسة الحالة",
        "discount_addl_pct": 3.0,
    },
    {
        "incentive_id": "visa_payment",
        "incentive_en": "Visa Payment",
        "incentive_ar": "الدفع عبر فيزا",
        "discount_addl_pct": 2.0,
    },
]

# ---------------------------------------------------------------------------
# Valid deal structures
# ---------------------------------------------------------------------------

_VALID_DEAL_STRUCTURES: set[str] = {"monthly", "quarterly", "annual", "multi_year"}

# ---------------------------------------------------------------------------
# Pydantic models
# ---------------------------------------------------------------------------


class DealStructureInput(BaseModel):
    base_price_sar: float = Field(..., ge=0)
    deal_structure: str
    apply_incentives: list[str] = Field(default_factory=list)
    headcount: int = Field(default=1, ge=1)


# ---------------------------------------------------------------------------
# Pure-function core
# ---------------------------------------------------------------------------


def _simulate_deal(inp: DealStructureInput) -> dict[str, Any]:
    """Simulate deal pricing with discounts and payment incentives.

    Returns total contract value, discounted price, and savings vs monthly.
    Governance decision: APPROVAL_FIRST.
    """
    if inp.deal_structure not in _VALID_DEAL_STRUCTURES:
        raise HTTPException(
            status_code=422,
            detail=(
                f"Invalid deal_structure '{inp.deal_structure}'. "
                f"Valid values: {sorted(_VALID_DEAL_STRUCTURES)}"
            ),
        )

    structure_data = _DEAL_STRUCTURES[inp.deal_structure]
    base_discount_pct: float = structure_data["discount_pct"]

    incentive_lookup: dict[str, float] = {
        item["incentive_id"]: item["discount_addl_pct"] for item in _PAYMENT_INCENTIVES
    }
    incentive_discount_pct: float = sum(
        incentive_lookup[incentive_id]
        for incentive_id in inp.apply_incentives
        if incentive_id in incentive_lookup
    )

    total_discount_pct: float = min(base_discount_pct + incentive_discount_pct, 40.0)
    discounted_price_sar: float = inp.base_price_sar * (1 - total_discount_pct / 100)
    commitment_months: int = structure_data["commitment_months"]
    total_contract_value_sar: float = discounted_price_sar * inp.headcount * commitment_months
    monthly_equivalent_sar: float = total_contract_value_sar / commitment_months
    savings_vs_monthly_sar: float = max(
        0.0,
        inp.base_price_sar * inp.headcount * commitment_months - total_contract_value_sar,
    )

    return {
        "deal_structure": inp.deal_structure,
        "base_price_sar": inp.base_price_sar,
        "headcount": inp.headcount,
        "base_discount_pct": base_discount_pct,
        "incentive_discount_pct": incentive_discount_pct,
        "total_discount_pct": total_discount_pct,
        "discounted_price_sar": discounted_price_sar,
        "total_contract_value_sar": total_contract_value_sar,
        "monthly_equivalent_sar": monthly_equivalent_sar,
        "savings_vs_monthly_sar": savings_vs_monthly_sar,
        "commitment_months": commitment_months,
        "governance_decision": _GOV_APPROVAL,
    }


# ---------------------------------------------------------------------------
# Router endpoints
# ---------------------------------------------------------------------------


@router.get("/structures", summary="All 4 deal structures")
def get_structures() -> dict[str, Any]:
    """Return all deal structures with discount percentages and commitment terms."""
    return {
        "structures": _DEAL_STRUCTURES,
        "governance_decision": _GOV_REVIEW,
    }


@router.get("/payment-incentives", summary="All 4 payment incentives")
def get_payment_incentives() -> dict[str, Any]:
    """Return all payment incentives with additional discount percentages."""
    return {
        "payment_incentives": _PAYMENT_INCENTIVES,
        "governance_decision": _GOV_REVIEW,
    }


@router.post("/simulate", summary="Simulate a deal with custom structure and incentives")
def simulate_deal(body: DealStructureInput) -> dict[str, Any]:
    """Accept deal parameters and return a full pricing simulation.

    Governance decision: APPROVAL_FIRST.
    """
    return _simulate_deal(body)
