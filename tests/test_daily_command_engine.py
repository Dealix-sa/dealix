"""Tests for the Daily Command Engine — capstone executive brief.

Covers daily command generation, attention prioritization, founder
summary, health scoring, and safety invariants.
"""
from __future__ import annotations

from datetime import date

import pytest

from dealix.company_intelligence.company_operator import (
    DepartmentSnapshot,
    OperatingHealth,
    generate_operating_snapshot,
)
from dealix.company_intelligence.daily_command_engine import (
    AttentionItem,
    AttentionUrgency,
    CommandSection,
    DailyCommandBrief,
    DailyHealthAssessment,
    generate_daily_command,
    prioritize_attention_items,
    summarize_for_founder,
)
from dealix.company_intelligence.department_contracts import Department
from dealix.company_intelligence.execution_contracts import OpportunityStage
from dealix.company_intelligence.outcome_contracts import EvidenceState
from dealix.company_intelligence.pipeline_engine import (
    analyze_pipeline,
    forecast_revenue,
    score_opportunity,
)

TENANT = "tenant_test_daily"
SOURCE = "test_source"
TODAY = date(2026, 8, 8)


# -----------------------------------------------------------------------
# Basic daily command
# -----------------------------------------------------------------------


class TestDailyCommand:
    def test_basic_command(self):
        brief = generate_daily_command(
            tenant_id=TENANT,
            brief_date=TODAY,
            source_id=SOURCE,
        )
        assert isinstance(brief, DailyCommandBrief)
        assert brief.tenant_id == TENANT
        assert brief.brief_date == TODAY
        assert brief.execution_allowed is False

    def test_deterministic_id(self):
        b1 = generate_daily_command(
            tenant_id=TENANT, brief_date=TODAY, source_id=SOURCE,
        )
        b2 = generate_daily_command(
            tenant_id=TENANT, brief_date=TODAY, source_id=SOURCE,
        )
        assert b1.brief_id == b2.brief_id
        assert b1.brief_id.startswith("dailybrief_")

    def test_with_blockers(self):
        brief = generate_daily_command(
            tenant_id=TENANT,
            brief_date=TODAY,
            blockers=("database migration pending", "API key expired"),
            source_id=SOURCE,
        )
        assert brief.blocker_count == 2
        blocker_items = [
            i for i in brief.attention_items
            if i.section == CommandSection.BLOCKERS
        ]
        assert len(blocker_items) == 2
        assert all(i.urgency == AttentionUrgency.CRITICAL for i in blocker_items)
        assert "resolve 2 blocker(s)" in brief.top_priorities

    def test_with_approvals(self):
        brief = generate_daily_command(
            tenant_id=TENANT,
            brief_date=TODAY,
            pending_approvals=("approve_001", "approve_002"),
            external_approvals=("approve_001",),
            high_risk_approvals=("approve_002",),
            source_id=SOURCE,
        )
        assert brief.approval_queue.total_pending == 2
        assert brief.approval_queue.external_pending == 1
        assert brief.approval_queue.high_risk_pending == 1
        assert "review 2 pending approval(s)" in brief.top_priorities

    def test_with_operating_snapshot(self):
        dept_snapshots = [
            DepartmentSnapshot(
                department=Department.SALES,
                health=OperatingHealth.GOOD,
                active_actions=5,
                completed_today=10,
                failed_today=0,
            ),
        ]
        snapshot = generate_operating_snapshot(
            tenant_id=TENANT,
            snapshot_date="2026-08-08",
            source_id=SOURCE,
            department_snapshots=dept_snapshots,
        )
        brief = generate_daily_command(
            tenant_id=TENANT,
            brief_date=TODAY,
            operating_snapshot=snapshot,
            source_id=SOURCE,
        )
        assert brief.completed_today == 10
        assert brief.failed_today == 0

    def test_critical_operations_flagged(self):
        dept_snapshots = [
            DepartmentSnapshot(
                department=Department.FINANCE,
                health=OperatingHealth.CRITICAL,
                failed_today=5,
            ),
        ]
        snapshot = generate_operating_snapshot(
            tenant_id=TENANT,
            snapshot_date="2026-08-08",
            source_id=SOURCE,
            department_snapshots=dept_snapshots,
        )
        brief = generate_daily_command(
            tenant_id=TENANT,
            brief_date=TODAY,
            operating_snapshot=snapshot,
            source_id=SOURCE,
        )
        ops_items = [
            i for i in brief.attention_items
            if i.section == CommandSection.OPERATIONS
        ]
        assert len(ops_items) >= 1
        assert ops_items[0].urgency == AttentionUrgency.CRITICAL

    def test_with_pipeline_analysis(self):
        scores = [
            score_opportunity(
                tenant_id=TENANT,
                opportunity_id=f"opp_{i}",
                stage=OpportunityStage.CONVERSATION,
                source_id=SOURCE,
            )
            for i in range(3)
        ]
        analysis = analyze_pipeline(
            tenant_id=TENANT, scores=scores, source_id=SOURCE,
        )
        forecast = forecast_revenue(
            tenant_id=TENANT,
            scores=scores,
            deal_values={f"opp_{i}": 50000.0 for i in range(3)},
            source_id=SOURCE,
        )
        brief = generate_daily_command(
            tenant_id=TENANT,
            brief_date=TODAY,
            pipeline_analysis=analysis,
            revenue_forecast=forecast,
            source_id=SOURCE,
        )
        assert brief.active_opportunities == 3
        assert brief.pipeline_value_weighted > 0

    def test_at_risk_pipeline_flagged(self):
        scores = [
            score_opportunity(
                tenant_id=TENANT,
                opportunity_id=f"opp_{i}",
                days_in_stage=50,
                source_id=SOURCE,
            )
            for i in range(4)
        ]
        analysis = analyze_pipeline(
            tenant_id=TENANT, scores=scores, source_id=SOURCE,
        )
        brief = generate_daily_command(
            tenant_id=TENANT,
            brief_date=TODAY,
            pipeline_analysis=analysis,
            source_id=SOURCE,
        )
        pipe_items = [
            i for i in brief.attention_items
            if i.section == CommandSection.PIPELINE
        ]
        assert len(pipe_items) >= 1

    def test_learning_events_noted(self):
        brief = generate_daily_command(
            tenant_id=TENANT,
            brief_date=TODAY,
            learning_events_count=3,
            source_id=SOURCE,
        )
        assert brief.learning_events_count == 3
        learn_items = [
            i for i in brief.attention_items
            if i.section == CommandSection.LEARNING
        ]
        assert len(learn_items) == 1

    def test_proof_events_noted(self):
        brief = generate_daily_command(
            tenant_id=TENANT,
            brief_date=TODAY,
            proof_events_count=2,
            source_id=SOURCE,
        )
        assert brief.proof_events_count == 2

    def test_revenue_state_passed_through(self):
        brief = generate_daily_command(
            tenant_id=TENANT,
            brief_date=TODAY,
            revenue_state=EvidenceState.PAYMENT_EVIDENCED,
            source_id=SOURCE,
        )
        assert brief.health.revenue_state == EvidenceState.PAYMENT_EVIDENCED


# -----------------------------------------------------------------------
# Attention prioritization
# -----------------------------------------------------------------------


class TestAttentionPrioritization:
    def test_critical_first(self):
        items = [
            AttentionItem(
                section=CommandSection.LEARNING,
                urgency=AttentionUrgency.LOW,
                title="learning",
            ),
            AttentionItem(
                section=CommandSection.BLOCKERS,
                urgency=AttentionUrgency.CRITICAL,
                title="blocker",
            ),
            AttentionItem(
                section=CommandSection.APPROVALS,
                urgency=AttentionUrgency.HIGH,
                title="approval",
            ),
        ]
        sorted_items = prioritize_attention_items(items)
        assert sorted_items[0].urgency == AttentionUrgency.CRITICAL
        assert sorted_items[1].urgency == AttentionUrgency.HIGH
        assert sorted_items[2].urgency == AttentionUrgency.LOW

    def test_action_required_first_within_urgency(self):
        items = [
            AttentionItem(
                section=CommandSection.PIPELINE,
                urgency=AttentionUrgency.HIGH,
                title="info",
                action_required=False,
            ),
            AttentionItem(
                section=CommandSection.PIPELINE,
                urgency=AttentionUrgency.HIGH,
                title="action",
                action_required=True,
            ),
        ]
        sorted_items = prioritize_attention_items(items)
        assert sorted_items[0].action_required is True


# -----------------------------------------------------------------------
# Founder summary
# -----------------------------------------------------------------------


class TestFounderSummary:
    def test_basic_summary(self):
        brief = generate_daily_command(
            tenant_id=TENANT,
            brief_date=TODAY,
            source_id=SOURCE,
        )
        summary = summarize_for_founder(brief)
        assert "Daily Command" in summary
        assert "2026-08-08" in summary

    def test_bilingual_format(self):
        brief = generate_daily_command(
            tenant_id=TENANT,
            brief_date=TODAY,
            pending_approvals=("a1",),
            source_id=SOURCE,
        )
        summary = summarize_for_founder(brief)
        # Arabic and English present
        assert "موافقات" in summary
        assert "Pending Approvals" in summary

    def test_blockers_in_summary(self):
        brief = generate_daily_command(
            tenant_id=TENANT,
            brief_date=TODAY,
            blockers=("critical issue",),
            source_id=SOURCE,
        )
        summary = summarize_for_founder(brief)
        assert "عوائق" in summary
        assert "critical issue" in summary

    def test_pipeline_in_summary(self):
        scores = [
            score_opportunity(
                tenant_id=TENANT,
                opportunity_id="opp_1",
                stage=OpportunityStage.PILOT,
                source_id=SOURCE,
            ),
        ]
        analysis = analyze_pipeline(
            tenant_id=TENANT, scores=scores, source_id=SOURCE,
        )
        forecast = forecast_revenue(
            tenant_id=TENANT,
            scores=scores,
            deal_values={"opp_1": 100000.0},
            source_id=SOURCE,
        )
        brief = generate_daily_command(
            tenant_id=TENANT,
            brief_date=TODAY,
            pipeline_analysis=analysis,
            revenue_forecast=forecast,
            source_id=SOURCE,
        )
        summary = summarize_for_founder(brief)
        assert "فرص نشطة" in summary
        assert "SAR" in summary


# -----------------------------------------------------------------------
# Safety invariants
# -----------------------------------------------------------------------


class TestDailyCommandSafety:
    def test_never_allows_execution(self):
        with pytest.raises(ValueError, match="never authorize execution"):
            DailyCommandBrief(
                tenant_id=TENANT,
                brief_id="dailybrief_fake",
                brief_date=TODAY,
                health=DailyHealthAssessment(),
                execution_allowed=True,
                source_id=SOURCE,
            )

    def test_generated_brief_always_safe(self):
        brief = generate_daily_command(
            tenant_id=TENANT,
            brief_date=TODAY,
            blockers=("b1",),
            pending_approvals=("a1", "a2"),
            learning_events_count=5,
            proof_events_count=3,
            source_id=SOURCE,
        )
        assert brief.execution_allowed is False
