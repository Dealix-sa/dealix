"""
Productisation packaging — §108.

Three commercial tiers, each with an offer name and a heuristic
recommender that maps a customer profile to the right tier.
"""

from __future__ import annotations

from typing import Any


TIER_ENTRY = "Entry"
TIER_EXPANSION = "Expansion"
TIER_ENTERPRISE = "Enterprise"


TIERS: dict[str, dict[str, Any]] = {
    TIER_ENTRY: {
        "offer_name": "Trust-Pilot Sprint",
        "monthly_price_sar_floor": 4_900,
        "ideal_employees_max": 50,
        "ideal_revenue_sar_max": 5_000_000,
    },
    TIER_EXPANSION: {
        "offer_name": "Value Engine Retainer",
        "monthly_price_sar_floor": 19_900,
        "ideal_employees_max": 250,
        "ideal_revenue_sar_max": 50_000_000,
    },
    TIER_ENTERPRISE: {
        "offer_name": "Sovereign Control Plane",
        "monthly_price_sar_floor": 75_000,
        "ideal_employees_max": 10_000,
        "ideal_revenue_sar_max": 5_000_000_000,
    },
}


def recommend_offer_tier(customer_profile: dict[str, Any]) -> str:
    revenue = float(customer_profile.get("annual_revenue_sar", 0))
    employees = int(customer_profile.get("employees", 0))
    sector = str(customer_profile.get("sector", "")).lower()
    regulated = sector in {"bank", "fintech", "insurance", "government", "energy"}
    if regulated or revenue >= 50_000_000 or employees >= 250:
        return TIER_ENTERPRISE
    if revenue >= 5_000_000 or employees >= 50:
        return TIER_EXPANSION
    return TIER_ENTRY
