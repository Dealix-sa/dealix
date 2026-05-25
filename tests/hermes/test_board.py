from __future__ import annotations

from dealix.hermes.board import (
    BoardMemo,
    build_traction_report,
    compute_executive_metrics,
    render_board_memo,
    render_investor_update,
)
from dealix.hermes.board.investor_update import InvestorUpdate


def _metrics():
    return compute_executive_metrics(
        verified_revenue_sar=120_000,
        pipeline_proposals_sar=500_000,
        pipeline_committed_sar=180_000,
        delivered_costs_sar=70_000,
        payment_count=20,
        retainer_active_count=8,
        customer_value_delivered_sar=300_000,
        assets_created=12,
        assets_reused=22,
        trust_incidents=0,
        approval_sla_p95_minutes=45,
        agent_attributable_revenue_sar=60_000,
        agent_cost_sar=10_000,
        partner_revenue_sar=30_000,
        founder_hours_period=180,
        founder_hours_strategic=110,
    )


def test_executive_metrics_compute_gm_and_quality():
    m = _metrics()
    assert m.gross_margin_pct > 0
    assert 0 <= m.revenue_quality_score <= 100
    assert m.headline_health() in ("green", "amber:trust", "amber:margin", "amber:retention", "amber:quality")


def test_investor_update_renders_markdown():
    update = InvestorUpdate(
        period="2026Q1",
        headline="Verified revenue up 30% quarter-over-quarter",
        metrics=_metrics(),
        highlights=["Closed 3 strategic accounts"],
        lowlights=["Founder time on delivery > target"],
        asks=["Intros to 2 enterprise CFOs"],
    )
    out = render_investor_update(update)
    assert "Verified revenue" in out
    assert "2026Q1" in out
    assert "Closed 3 strategic" in out


def test_board_memo_renders():
    memo = BoardMemo(
        period="2026Q1",
        decision_topic="Should we move agentic_control_plane to GA pricing?",
        recommendation="Yes, with strategic-tier guardrails",
        options_considered=["GA at SAR 65,000", "Custom-quoted only", "Delay one quarter"],
        metrics=_metrics(),
        risks=["Delivery margin compression at higher volume"],
        next_review_date="2026-07-01",
    )
    out = render_board_memo(memo)
    assert "GA pricing" in out
    assert "Verified revenue" in out


def test_traction_report():
    rep = build_traction_report(
        period="2026Q1",
        verified_revenue_sar=120_000,
        retainer_active_count=8,
        paying_customers=20,
        case_studies_published=3,
        partner_count=4,
        nps=42,
    )
    assert rep.verified_revenue_sar == 120_000
    assert rep.partner_count == 4
