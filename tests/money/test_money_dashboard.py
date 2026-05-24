"""Tests for `dealix.money.dashboard.MoneyDashboard`."""

from __future__ import annotations

from datetime import datetime, timedelta

from dealix.hermes.core.opportunities import Opportunity, OpportunityType
from dealix.hermes.core.outcomes import Outcome, OutcomeKind
from dealix.hermes.core.schemas import Money, utcnow
from dealix.money.dashboard import MoneyDashboard
from dealix.trust.approvals import ApprovalQueue, ApprovalTicket
from dealix.hermes.sovereignty import SovereigntyLevel


def _outcome(amount: float, created_at: datetime | None = None) -> Outcome:
    o = Outcome(
        execution_id="plan_x",
        kind=OutcomeKind.MONEY,
        summary="paid",
        value=Money.sar(amount),
    )
    if created_at is not None:
        # Pydantic models with extra=forbid won't accept arbitrary attrs;
        # use model_copy to swap created_at for the deterministic value.
        return o.model_copy(update={"created_at": created_at})
    return o


def test_cash_today_sums_money_outcomes_from_today() -> None:
    now = utcnow()
    yesterday = now - timedelta(days=1)
    dashboard = MoneyDashboard(
        outcomes=[
            _outcome(1000, created_at=now),
            _outcome(500, created_at=now),
            _outcome(9999, created_at=yesterday),  # ignored
        ]
    )
    assert dashboard.cash_today(now=now).amount == Money.sar(1500).amount


def test_top_opportunity_today_picks_highest_score() -> None:
    opps = [
        Opportunity(
            signal_id="s1",
            opp_type=OpportunityType.KNOWLEDGE,
            title="Knowledge ask",
            narrative="how do you...",
            urgency=2,
            fit_score=2,
        ),
        Opportunity(
            signal_id="s2",
            opp_type=OpportunityType.REVENUE,
            title="Revenue lead",
            narrative="proposal request",
            expected_value=Money.sar(20000),
            urgency=5,
            fit_score=5,
        ),
    ]
    dashboard = MoneyDashboard()
    top = dashboard.top_opportunity_today(opps)
    assert top is not None
    assert top.opp_type == OpportunityType.REVENUE


def test_approvals_pending_lists_active_tickets() -> None:
    dashboard = MoneyDashboard()
    queue = ApprovalQueue()
    queue.submit(
        ApprovalTicket(
            decision_id="hdec_x",
            summary="please approve",
            sovereignty_level=SovereigntyLevel.S2_SAMI_APPROVAL,
        )
    )
    pending = dashboard.approvals_pending(queue)
    assert len(pending) == 1
    assert pending[0].summary == "please approve"


def test_weekly_snapshot_returns_full_kpi_set() -> None:
    now = utcnow()
    dashboard = MoneyDashboard(
        outcomes=[
            _outcome(7500, created_at=now),
            _outcome(2500, created_at=now),
        ]
    )
    queue = ApprovalQueue()
    snap = dashboard.weekly_snapshot(
        opportunities=[],
        queue=queue,
        proposals_drafted=4,
        pilots_active=2,
        cash_at_risk=Money.sar(1500),
        top_offer_name="AI Trust Kit",
    )
    assert snap.cash_collected.amount == Money.sar(10000).amount
    assert snap.cash_at_risk.amount == Money.sar(1500).amount
    assert snap.approvals_pending == 0
    assert snap.proposals_drafted == 4
    assert snap.pilots_active == 2
    assert snap.top_offer_name == "AI Trust Kit"
    assert 0.0 <= snap.win_rate_pct <= 1.0
