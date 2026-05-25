"""Board memo composer surfaces a decision request."""

from __future__ import annotations

from dealix.hermes.board.board_memo import compose
from dealix.hermes.board.metrics import build


def test_compose_board_memo() -> None:
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
    memo = compose(metrics=m, title="Approve hiring plan", narrative="Pipeline is healthy.", decision_requested="Approve")
    assert memo.title == "Approve hiring plan"
    assert "Verified revenue" in memo.body
    assert memo.decision_requested == "Approve"
