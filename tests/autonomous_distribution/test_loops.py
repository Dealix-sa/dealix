"""Tests for the unified Autonomous Distribution Loops."""

from __future__ import annotations

import pytest

from auto_client_acquisition.autonomous_distribution import (
    evening_loop,
    monthly_loop,
    morning_loop,
    weekly_loop,
)
from auto_client_acquisition.compliance_trust_os.approval_engine import (
    GovernanceDecision,
)
from auto_client_acquisition.friction_log import FrictionAggregate


class TestMorningLoop:
    def test_zero_state_returns_warm_list_action(self):
        m = morning_loop()
        assert m.governance_decision is GovernanceDecision.REQUIRE_APPROVAL
        assert m.drafts_queued == 0
        assert any("warm_list" in a or "founder_approve" in a for a in m.high_priority_actions)

    def test_with_pending_drafts(self):
        m = morning_loop(leads_inbound=5, leads_scored=4, drafts_pending=3)
        assert m.drafts_queued == 3
        assert any("founder_approve_3" in a for a in m.high_priority_actions)
        assert "5 new leads" in m.founder_digest_en

    def test_bilingual_digest(self):
        m = morning_loop(leads_inbound=2)
        assert m.founder_digest_ar
        assert m.founder_digest_en
        # Bilingual sanity: Arabic digest must contain Arabic chars.
        assert any("؀" <= ch <= "ۿ" for ch in m.founder_digest_ar)


class TestEveningLoop:
    def test_zero_state_allow(self):
        e = evening_loop()
        assert e.governance_decision is GovernanceDecision.ALLOW
        assert e.tomorrow_top_4

    def test_friction_high_severity_surfaces(self):
        agg = FrictionAggregate(
            customer_id="x",
            window_days=14,
            total=3,
            by_kind={"approval_blocked": 3},
            by_severity={"high": 2, "medium": 1},
            top_3_kinds=[("approval_blocked", 3)],
            total_cost_minutes=120,
            week_over_week_delta=2,
        )
        e = evening_loop(friction=agg)
        assert e.friction_events_today == 3
        assert e.high_severity_frictions == 2
        assert any("resolve_2" in a for a in e.tomorrow_top_4)

    def test_revenue_in_digest(self):
        e = evening_loop(revenue_today_sar=1499.0, leads_in_pipeline=12)
        assert "1499" in e.founder_digest_en
        assert "12" in e.founder_digest_en


class TestWeeklyLoop:
    def test_first_week_zero_revenue(self):
        w = weekly_loop()
        assert w.governance_decision is GovernanceDecision.REQUIRE_APPROVAL
        assert w.next_week_focus_en
        assert "Moyasar" in w.next_week_focus_en

    def test_wow_calculation_positive(self):
        w = weekly_loop(revenue_week_sar=2000.0, revenue_last_week_sar=1000.0)
        assert w.week_over_week_pct == 100.0

    def test_wow_calculation_zero_base(self):
        w = weekly_loop(revenue_week_sar=500.0, revenue_last_week_sar=0.0)
        assert w.week_over_week_pct == 100.0

    def test_retainer_eligible_focus(self):
        w = weekly_loop(retainers_eligible=2, revenue_week_sar=3000.0, revenue_last_week_sar=2000.0)
        assert "retainer" in w.next_week_focus_en


class TestMonthlyLoop:
    def test_day_15_activation_phase_behind(self):
        m = monthly_loop(day_count_since_launch=15, cumulative_revenue_sar=200.0)
        assert m.month_phase == "activation"
        assert m.milestone_verdict == "behind"

    def test_day_45_expansion_on_track(self):
        m = monthly_loop(day_count_since_launch=45, cumulative_revenue_sar=18000.0, active_retainers=1)
        assert m.month_phase == "expansion"
        assert m.milestone_verdict == "on_track"

    def test_day_75_compounding_ahead(self):
        m = monthly_loop(
            day_count_since_launch=75,
            cumulative_revenue_sar=55000.0,
            active_retainers=4,
            capital_assets_total=8,
        )
        assert m.month_phase == "compounding"
        assert m.milestone_verdict == "ahead"
        assert any("wave_3" in d for d in m.decisions_for_founder)

    def test_doctrine_violation_blocks_governance(self):
        m = monthly_loop(day_count_since_launch=20, doctrine_violations=2)
        assert m.governance_decision is GovernanceDecision.BLOCK
        assert any("doctrine" in d for d in m.decisions_for_founder)

    def test_behind_at_day_60_triggers_halt(self):
        m = monthly_loop(day_count_since_launch=60, cumulative_revenue_sar=5000.0)
        assert m.milestone_verdict == "behind"
        assert any("halt" in d for d in m.decisions_for_founder)
