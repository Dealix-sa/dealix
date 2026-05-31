"""Account-Based Marketing tier matrix."""

from __future__ import annotations

from dataclasses import dataclass

_TIER_PLAYBOOK = {
    "tier_1": {"contacts": 8, "touches_per_quarter": 12, "investment_sar": 25000},
    "tier_2": {"contacts": 5, "touches_per_quarter": 8, "investment_sar": 12000},
    "tier_3": {"contacts": 3, "touches_per_quarter": 5, "investment_sar": 5000},
    "tier_4": {"contacts": 1, "touches_per_quarter": 2, "investment_sar": 1500},
}


@dataclass(frozen=True)
class AccountPlan:
    account_id: str
    tier: str
    contacts: int
    touches_per_quarter: int
    investment_sar: int


def assign_tier(account_id: str, fit_score: float, revenue_potential_sar: float) -> AccountPlan:
    """Assign an ABM tier from fit_score and revenue potential and return its playbook."""
    if fit_score >= 0.8 and revenue_potential_sar >= 500_000:
        tier = "tier_1"
    elif fit_score >= 0.6 and revenue_potential_sar >= 150_000:
        tier = "tier_2"
    elif fit_score >= 0.4:
        tier = "tier_3"
    else:
        tier = "tier_4"
    playbook = _TIER_PLAYBOOK[tier]
    return AccountPlan(
        account_id=account_id,
        tier=tier,
        contacts=playbook["contacts"],
        touches_per_quarter=playbook["touches_per_quarter"],
        investment_sar=playbook["investment_sar"],
    )
