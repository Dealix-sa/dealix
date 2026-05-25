"""ABM tier assignment scales with fit_score and revenue potential."""

from __future__ import annotations

from dealix.hermes.growth.abm_engine import assign_tier


def test_high_fit_high_potential_gets_tier_1() -> None:
    plan = assign_tier("acc_1", fit_score=0.9, revenue_potential_sar=750_000)
    assert plan.tier == "tier_1"
    assert plan.contacts >= 5


def test_low_fit_drops_to_tier_4() -> None:
    plan = assign_tier("acc_2", fit_score=0.1, revenue_potential_sar=10_000)
    assert plan.tier == "tier_4"
