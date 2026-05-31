"""BoardMetrics is constructed with the documented KPI fields."""

from __future__ import annotations

from dealix.hermes.board.metrics import build


def test_build_board_metrics() -> None:
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
    assert m.period == "2026-Q1"
    assert m.gross_margin == 0.72
    assert m.trust_incidents == 0
