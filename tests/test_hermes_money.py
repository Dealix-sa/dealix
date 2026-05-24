"""Money engine tests."""

from __future__ import annotations

import pytest

from dealix.hermes.core.opportunities import OpportunityStore
from dealix.hermes.core.outcomes import OutcomeStore
from dealix.hermes.core.schemas import OpportunityType, OutcomeStatus, SignalType
from dealix.hermes.core.scoring import score_money, score_opportunity
from dealix.hermes.core.signals import SignalStore
from dealix.hermes.money.cash_scout import CashScout
from dealix.hermes.money.cashflow import CashflowBrief
from dealix.hermes.money.dashboard import MoneyDashboard
from dealix.hermes.money.pricing import PricingIntelligence


@pytest.fixture(autouse=True)
def _isolate(monkeypatch):
    import dealix.hermes.core.opportunities as o_mod
    import dealix.hermes.core.outcomes as out_mod
    import dealix.hermes.core.signals as s_mod

    s_mod._default_store = SignalStore()
    o_mod._default_store = OpportunityStore()
    out_mod._default_store = OutcomeStore()
    yield
    for m in (s_mod, o_mod, out_mod):
        m._default_store = None


def test_opportunity_score_formula():
    from dealix.hermes.core.schemas import Opportunity

    opp = Opportunity(
        signal_id="sig_x",
        opportunity_type=OpportunityType.CUSTOMER,
        title="t",
        cash_speed_score=4,
        strategic_score=5,
        repeatability_score=5,
        data_moat_score=4,
        difficulty_score=2,
        risk_score=2,
    )
    expected = round(
        0.25 * 4 + 0.20 * 5 + 0.20 * 5 + 0.15 * 4 - 0.10 * 2 - 0.10 * 2,
        4,
    )
    assert score_opportunity(opp) == expected


def test_money_score_clamps_value_at_cap():
    score = score_money(
        cash_speed=5,
        close_probability=1.0,
        deal_value_sar=10_000_000,
        strategic=5,
        risk=0,
        value_cap_sar=100_000,
    )
    # value normalized to 5; perfect close probability scaled to 5
    assert score == round(0.30 * 5 + 0.25 * 5 + 0.20 * 5 + 0.15 * 5 - 0.0, 4)


def test_pricing_recommends_band():
    sig = SignalStore().ingest(source="x", signal_type=SignalType.CUSTOMER, title="t")
    opp = OpportunityStore().evaluate(sig, estimated_value_sar=10_000, strategic=5)
    rec = PricingIntelligence().recommend(opp)
    assert rec.floor_sar < rec.target_sar < rec.ceiling_sar


def test_cash_scout_returns_top_paths():
    from dealix.hermes.core.opportunities import get_opportunity_store
    from dealix.hermes.core.signals import get_signal_store

    s = get_signal_store()
    o = get_opportunity_store()
    for i in range(3):
        sig = s.ingest(source="x", signal_type=SignalType.CUSTOMER, title=f"lead {i}")
        o.evaluate(sig, estimated_value_sar=5_000 * (i + 1))
    items = CashScout().fastest_paths(top=2)
    assert len(items) == 2
    assert items[0]["money_score"] >= items[1]["money_score"]


def test_cashflow_summary_classifies_risk():
    from dealix.hermes.core.outcomes import get_outcome_store
    from dealix.hermes.core.schemas import Execution

    exe = Execution(decision_id="d", agent_id="a", action_type="x")
    get_outcome_store().record(exe, status=OutcomeStatus.PAID, revenue_sar=2_000)
    summary = CashflowBrief().summary()
    assert summary.paid_sar == 2_000
    assert summary.cash_risk in {"high", "medium", "low"}


def test_money_dashboard_snapshot_has_required_fields():
    snap = MoneyDashboard().snapshot()
    keys = snap.as_dict().keys()
    for field in (
        "fastest_cash_action",
        "highest_value_deal",
        "open_proposals",
        "follow_ups_due",
        "expected_revenue_sar",
        "best_next_action",
    ):
        assert field in keys
