"""Investor update markdown surfaces every KPI heading."""

from __future__ import annotations

from dealix.hermes.board.investor_update import render
from dealix.hermes.board.metrics import build


def test_render_contains_kpi_headings() -> None:
    m = build(
        period="2026-Q1",
        verified_revenue_sar=480_000,
        revenue_quality_grade="A",
        pipeline_quality_grade="B",
        gross_margin=0.72,
        retainer_conversion=0.55,
        agent_roi=4.5,
        trust_incidents=0,
        approvals_pending=2,
        assets_created=12,
        assets_reused=23,
        partner_revenue_sar=120_000,
        founder_time_leverage_hours=88.0,
    )
    out = render(m, narrative="Strong quarter")
    assert "Verified Outcomes" in out
    assert "Governance" in out
    assert "Strong quarter" in out
