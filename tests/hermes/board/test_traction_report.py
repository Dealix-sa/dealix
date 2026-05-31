"""Traction report computes deltas between consecutive board snapshots."""

from __future__ import annotations

from dealix.hermes.board.metrics import build
from dealix.hermes.board.traction_report import delta, render


def _snap(period: str, revenue: float, margin: float, retainer: float) -> object:
    return build(
        period=period,
        verified_revenue_sar=revenue,
        revenue_quality_grade="A",
        pipeline_quality_grade="B",
        gross_margin=margin,
        retainer_conversion=retainer,
        agent_roi=3.0,
        trust_incidents=0,
        approvals_pending=0,
        assets_created=0,
        assets_reused=0,
        partner_revenue_sar=0,
        founder_time_leverage_hours=0,
    )


def test_delta_between_periods() -> None:
    prev = _snap("2026-Q1", 400_000, 0.6, 0.4)
    cur = _snap("2026-Q2", 600_000, 0.68, 0.5)
    d = delta(prev, cur)
    assert d.revenue_delta_sar == 200_000
    assert "Traction Report" in render(prev, cur)
