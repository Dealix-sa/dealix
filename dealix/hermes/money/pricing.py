"""
Pricing — the 5-rung Dealix ladder.

The rungs are stable; the prices reflect the current published offers.
Enterprise pricing is intentionally a range and requires sovereign sign-off.
"""

from __future__ import annotations

from pydantic import BaseModel


class PricingRung(BaseModel):
    name: str
    min_sar: float
    max_sar: float | None
    sovereign_approval_required: bool


LADDER: tuple[PricingRung, ...] = (
    PricingRung(name="Free Diagnostic", min_sar=0, max_sar=0, sovereign_approval_required=False),
    PricingRung(name="Sprint", min_sar=499, max_sar=499, sovereign_approval_required=False),
    PricingRung(name="Data Pack", min_sar=1500, max_sar=1500, sovereign_approval_required=False),
    PricingRung(name="Managed Ops", min_sar=2999, max_sar=4999, sovereign_approval_required=False),
    PricingRung(name="Custom AI", min_sar=5000, max_sar=25000, sovereign_approval_required=True),
)


def recommend_rung(estimated_value_sar: float | None) -> PricingRung:
    """Pick the lowest rung that fits the buyer's stated value bracket."""
    if estimated_value_sar is None:
        return LADDER[0]
    for rung in LADDER:
        ceiling = rung.max_sar if rung.max_sar is not None else float("inf")
        if estimated_value_sar <= ceiling:
            return rung
    return LADDER[-1]
