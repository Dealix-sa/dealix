"""
Finance
=======
Unit economics, pricing guardrails, and margin calculations.
Floor prices and margin targets for all Dealix offer types.
"""

FLOOR_PRICES_SAR: dict[str, int] = {
    "ai_workflow_audit": 5_000,
    "legal_regulated_audit": 15_000,
    "pilot_no_api": 30_000,
    "pilot_with_api": 60_000,
    "multi_system_pilot": 100_000,
    "production_system": 150_000,
    "command_center": 250_000,
    "retainer_monthly": 8_000,
}

MARGIN_TARGETS: dict[str, float] = {
    "minimum_acceptable": 0.50,
    "healthy_target": 0.65,
    "excellent": 0.80,
}

COST_CATEGORIES: list[str] = [
    "model_api",
    "hosting",
    "tools",
    "contractor_hours",
    "founder_hours",
    "support_hours",
]


def compute_margin(revenue: float, direct_costs: float) -> dict:
    """Compute gross margin and whether it meets targets."""
    if revenue <= 0:
        return {"error": "Revenue must be positive", "margin": 0.0, "acceptable": False}
    gross_profit = revenue - direct_costs
    margin = gross_profit / revenue
    return {
        "revenue_sar": revenue,
        "direct_costs_sar": direct_costs,
        "gross_profit_sar": gross_profit,
        "gross_margin": round(margin, 4),
        "gross_margin_pct": f"{margin:.1%}",
        "acceptable": margin >= MARGIN_TARGETS["minimum_acceptable"],
        "healthy": margin >= MARGIN_TARGETS["healthy_target"],
        "target": f"{MARGIN_TARGETS['healthy_target']:.0%}",
        "minimum": f"{MARGIN_TARGETS['minimum_acceptable']:.0%}",
    }


def check_floor_price(offer_type: str, proposed_price: float) -> dict:
    """Verify proposed price meets floor for the given offer type."""
    floor = FLOOR_PRICES_SAR.get(offer_type)
    if floor is None:
        return {"error": f"Unknown offer type: {offer_type}", "meets_floor": False}
    meets = proposed_price >= floor
    return {
        "offer_type": offer_type,
        "proposed_price_sar": proposed_price,
        "floor_price_sar": floor,
        "meets_floor": meets,
        "shortfall_sar": max(0.0, floor - proposed_price) if not meets else 0.0,
    }


def estimate_project_economics(
    offer_type: str,
    price_sar: float,
    model_api_cost: float = 0,
    hosting_cost: float = 0,
    contractor_hours: float = 0,
    contractor_rate_sar: float = 150,
    founder_hours: float = 0,
    founder_rate_sar: float = 300,
) -> dict:
    """Estimate unit economics for a project."""
    direct_costs = (
        model_api_cost
        + hosting_cost
        + (contractor_hours * contractor_rate_sar)
        + (founder_hours * founder_rate_sar)
    )
    floor_check = check_floor_price(offer_type, price_sar)
    margin_result = compute_margin(price_sar, direct_costs)
    return {
        "offer_type": offer_type,
        "floor_check": floor_check,
        "margin": margin_result,
        "cost_breakdown": {
            "model_api": model_api_cost,
            "hosting": hosting_cost,
            "contractor": contractor_hours * contractor_rate_sar,
            "founder": founder_hours * founder_rate_sar,
            "total_direct": direct_costs,
        },
    }
