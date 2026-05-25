"""Funnel conversion computes per-step and overall conversion rates."""

from __future__ import annotations

from dealix.hermes.growth.revenue.funnel_conversion import FunnelStage, assess


def test_funnel_overall_rate() -> None:
    stages = [
        FunnelStage("leads", 1000),
        FunnelStage("qualified", 250),
        FunnelStage("proposal", 80),
        FunnelStage("closed_won", 20),
    ]
    rep = assess(stages)
    assert rep.overall_rate == 0.02
    assert rep.rates[0] == ("leads", "qualified", 0.25)
