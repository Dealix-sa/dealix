"""Tests for the Autonomous Company Operator — the master orchestrator.

Covers the full operating cycle, founder action pack, stage outputs,
safety invariants, bilingual summaries, and cycle metrics.
"""
from __future__ import annotations

import pytest

from dealix.company_intelligence.autonomous_operator import (
    ActionCategory,
    ActionPriority,
    FounderActionPack,
    OperatingCycle,
    run_operating_cycle,
    summarize_cycle_for_founder,
)
from dealix.company_intelligence.fulfillment_engine import (
    ClientEngagement,
    EngagementStatus,
    create_engagement,
)
from dealix.company_intelligence.research_engine import (
    CompanyProfile,
    DecisionMaker,
    DecisionMakerRole,
    PainSignal,
)

TENANT = "tenant_test_operator"
SOURCE = "test_source"


# -----------------------------------------------------------------------
# Empty operating cycle
# -----------------------------------------------------------------------


class TestEmptyCycle:
    def test_empty_cycle(self):
        cycle = run_operating_cycle(
            tenant_id=TENANT, source_id=SOURCE,
        )
        assert isinstance(cycle, OperatingCycle)
        assert cycle.new_prospects_found == 0
        assert cycle.qualified_count == 0
        assert cycle.sequences_planned == 0
        assert cycle.responses_handled == 0
        assert cycle.deals_in_pipeline == 0
        assert cycle.autonomous_execution is False
        assert cycle.action_pack is not None

    def test_deterministic_id(self):
        c1 = run_operating_cycle(
            tenant_id=TENANT, cycle_date="2026-08-08",
            source_id=SOURCE,
        )
        c2 = run_operating_cycle(
            tenant_id=TENANT, cycle_date="2026-08-08",
            source_id=SOURCE,
        )
        assert c1.cycle_id == c2.cycle_id
        assert c1.cycle_id.startswith("cycle_")


# -----------------------------------------------------------------------
# Research & Qualify stages (1-2)
# -----------------------------------------------------------------------


class TestResearchQualifyStages:
    def _make_prospects(self):
        return [
            CompanyProfile(
                tenant_id=TENANT,
                company_name="HotCo",
                company_name_ar="هوت كو",
                sector="saas",
                employee_count=100,
                city="Riyadh",
                country="SA",
                website="https://hotco.sa",
                source_id=SOURCE,
                pain_signals=(PainSignal.REVENUE_LEAKAGE, PainSignal.FOLLOW_UP_GAPS),
                decision_makers=(
                    DecisionMaker(
                        name="Faisal", role=DecisionMakerRole.FOUNDER_CEO,
                        email="faisal@hotco.sa", is_primary=True,
                    ),
                ),
            ),
            CompanyProfile(
                tenant_id=TENANT,
                company_name="ColdCo",
                sector="agriculture",
                employee_count=5,
                country="SA",
                source_id=SOURCE,
            ),
        ]

    def test_researches_and_qualifies(self):
        cycle = run_operating_cycle(
            tenant_id=TENANT,
            new_prospects=self._make_prospects(),
            source_id=SOURCE,
        )
        assert cycle.new_prospects_found == 2
        assert len(cycle.research_briefs) == 2
        # HotCo should be qualified, ColdCo should not
        assert cycle.qualified_count >= 1

    def test_generates_outreach_for_qualified(self):
        cycle = run_operating_cycle(
            tenant_id=TENANT,
            new_prospects=self._make_prospects(),
            source_id=SOURCE,
        )
        assert cycle.sequences_planned >= 1
        assert len(cycle.outreach_sequences) >= 1

    def test_creates_founder_actions_for_qualified(self):
        cycle = run_operating_cycle(
            tenant_id=TENANT,
            new_prospects=self._make_prospects(),
            source_id=SOURCE,
        )
        assert cycle.action_pack is not None
        assert cycle.action_pack.total_actions >= 1
        # Should have approve_outreach actions
        categories = [a.category for a in cycle.action_pack.actions]
        assert ActionCategory.APPROVE_OUTREACH in categories


# -----------------------------------------------------------------------
# Response stage (7)
# -----------------------------------------------------------------------


class TestResponseStage:
    def test_handles_responses(self):
        responses = [
            {
                "prospect_name": "Ahmad",
                "prospect_company": "TestCo",
                "text": "Yes, sounds good! Let's talk.",
            },
            {
                "prospect_name": "Sara",
                "prospect_company": "NoCo",
                "text": "إيقاف",
            },
        ]
        cycle = run_operating_cycle(
            tenant_id=TENANT, responses=responses,
            source_id=SOURCE,
        )
        assert cycle.responses_handled == 2
        assert len(cycle.follow_up_actions) == 2

    def test_opt_out_creates_critical_action(self):
        responses = [
            {
                "prospect_name": "Sara",
                "prospect_company": "NoCo",
                "text": "stop please",
            },
        ]
        cycle = run_operating_cycle(
            tenant_id=TENANT, responses=responses,
            source_id=SOURCE,
        )
        assert cycle.action_pack is not None
        priorities = [a.priority for a in cycle.action_pack.actions]
        assert ActionPriority.CRITICAL in priorities

    def test_positive_response_creates_action(self):
        responses = [
            {
                "prospect_name": "Ahmad",
                "prospect_company": "TestCo",
                "text": "sure, let's do it",
            },
        ]
        cycle = run_operating_cycle(
            tenant_id=TENANT, responses=responses,
            source_id=SOURCE,
        )
        categories = [a.category for a in cycle.action_pack.actions]
        assert ActionCategory.RESPOND_TO_LEAD in categories


# -----------------------------------------------------------------------
# Deal stages (8-9)
# -----------------------------------------------------------------------


class TestDealStages:
    def test_assesses_deals(self):
        deals = [
            {
                "prospect_name": "Khalid",
                "prospect_company": "BigDealCo",
                "stage": "negotiation",
                "closing_signals": ["asked_pricing", "requested_proposal"],
                "days_in_stage": 3,
                "total_touches": 5,
                "total_replies": 3,
                "estimated_value": 15000.0,
            },
        ]
        cycle = run_operating_cycle(
            tenant_id=TENANT, active_deals=deals,
            source_id=SOURCE,
        )
        assert cycle.deals_in_pipeline == 1
        assert len(cycle.deal_progressions) == 1
        prog = cycle.deal_progressions[0]
        assert prog.closing_probability > 0

    def test_high_probability_deal_gets_critical_action(self):
        deals = [
            {
                "prospect_name": "Winner",
                "prospect_company": "WinCo",
                "stage": "verbal_yes",
                "closing_signals": ["verbal_agreement"],
                "total_replies": 5,
            },
        ]
        cycle = run_operating_cycle(
            tenant_id=TENANT, active_deals=deals,
            source_id=SOURCE,
        )
        # Verbal yes with signal should be critical
        priorities = [a.priority for a in cycle.action_pack.actions]
        assert ActionPriority.CRITICAL in priorities


# -----------------------------------------------------------------------
# Delivery & Growth stages (10-11)
# -----------------------------------------------------------------------


class TestDeliveryGrowthStages:
    def test_assesses_engagements(self):
        # Create an active engagement
        active_eng = ClientEngagement(
            tenant_id=TENANT, client_name="Client1",
            client_company="ClientCo",
            offer_type="revenue_command_pilot",
            status=EngagementStatus.ACTIVE,
            auto_charge=False, auto_renew=False,
            source_id=SOURCE,
        )
        cycle = run_operating_cycle(
            tenant_id=TENANT, engagements=[active_eng],
            source_id=SOURCE,
        )
        assert cycle.active_clients == 1
        assert len(cycle.renewal_assessments) == 1

    def test_at_risk_engagement_gets_critical_action(self):
        eng = ClientEngagement(
            tenant_id=TENANT, client_name="Risky",
            client_company="RiskCo",
            offer_type="revenue_command_pilot",
            status=EngagementStatus.AT_RISK,
            auto_charge=False, auto_renew=False,
            source_id=SOURCE,
        )
        cycle = run_operating_cycle(
            tenant_id=TENANT, engagements=[eng],
            source_id=SOURCE,
        )
        priorities = [a.priority for a in cycle.action_pack.actions]
        assert ActionPriority.CRITICAL in priorities


# -----------------------------------------------------------------------
# Full cycle with all inputs
# -----------------------------------------------------------------------


class TestFullCycle:
    def test_full_cycle(self):
        prospects = [
            CompanyProfile(
                tenant_id=TENANT,
                company_name="FullCo",
                sector="saas",
                employee_count=80,
                country="SA",
                source_id=SOURCE,
                pain_signals=(PainSignal.REVENUE_LEAKAGE,),
                decision_makers=(
                    DecisionMaker(
                        name="Ali", role=DecisionMakerRole.FOUNDER_CEO,
                        email="ali@fullco.sa", is_primary=True,
                    ),
                ),
            ),
        ]
        responses = [
            {"prospect_name": "Sara", "prospect_company": "OldCo", "text": "interested"},
        ]
        deals = [
            {
                "prospect_name": "Omar",
                "prospect_company": "DealCo",
                "stage": "proposal",
                "estimated_value": 5000.0,
            },
        ]
        eng = ClientEngagement(
            tenant_id=TENANT, client_name="Existing",
            client_company="ExistCo",
            offer_type="revenue_command_pilot",
            status=EngagementStatus.ACTIVE,
            auto_charge=False, auto_renew=False,
            source_id=SOURCE,
        )

        cycle = run_operating_cycle(
            tenant_id=TENANT,
            cycle_date="2026-08-08",
            new_prospects=prospects,
            responses=responses,
            active_deals=deals,
            engagements=[eng],
            source_id=SOURCE,
        )

        assert cycle.new_prospects_found == 1
        assert cycle.responses_handled == 1
        assert cycle.deals_in_pipeline == 1
        assert cycle.active_clients == 1
        assert cycle.action_pack is not None
        assert cycle.action_pack.total_actions >= 3  # At least one per stage

    def test_actions_sorted_by_priority(self):
        responses = [
            {"prospect_name": "Urgent", "prospect_company": "UrgCo", "text": "stop"},
            {"prospect_name": "Normal", "prospect_company": "NormCo", "text": "maybe later"},
        ]
        cycle = run_operating_cycle(
            tenant_id=TENANT, responses=responses,
            source_id=SOURCE,
        )
        actions = cycle.action_pack.actions
        if len(actions) >= 2:
            priority_order = {
                ActionPriority.CRITICAL: 0,
                ActionPriority.HIGH: 1,
                ActionPriority.MEDIUM: 2,
                ActionPriority.LOW: 3,
                ActionPriority.INFO: 4,
            }
            for i in range(len(actions) - 1):
                assert priority_order[actions[i].priority] <= priority_order[actions[i + 1].priority]


# -----------------------------------------------------------------------
# Founder summary
# -----------------------------------------------------------------------


class TestFounderSummary:
    def test_summary_bilingual(self):
        cycle = run_operating_cycle(
            tenant_id=TENANT,
            cycle_date="2026-08-08",
            responses=[
                {"prospect_name": "Test", "prospect_company": "Co", "text": "yes"},
            ],
            source_id=SOURCE,
        )
        summary = summarize_cycle_for_founder(cycle)
        assert isinstance(summary, str)
        # Should contain Arabic
        assert "دورة التشغيل" in summary
        # Should contain English
        assert "Daily Operating Cycle" in summary
        # Should contain date
        assert "2026-08-08" in summary
        # Should contain metrics
        assert "Metrics" in summary or "المقاييس" in summary

    def test_empty_cycle_summary(self):
        cycle = run_operating_cycle(
            tenant_id=TENANT, source_id=SOURCE,
        )
        summary = summarize_cycle_for_founder(cycle)
        assert "0" in summary  # Zero metrics


# -----------------------------------------------------------------------
# Action pack
# -----------------------------------------------------------------------


class TestFounderActionPack:
    def test_action_pack_metrics(self):
        cycle = run_operating_cycle(
            tenant_id=TENANT,
            responses=[
                {"prospect_name": "A", "prospect_company": "Co1", "text": "stop"},
                {"prospect_name": "B", "prospect_company": "Co2", "text": "yes"},
                {"prospect_name": "C", "prospect_company": "Co3", "text": "maybe later"},
            ],
            source_id=SOURCE,
        )
        pack = cycle.action_pack
        assert pack.total_actions == 3
        assert pack.estimated_total_minutes > 0
        assert pack.summary_ar
        assert pack.summary_en
        assert str(pack.total_actions) in pack.summary_ar
        assert str(pack.total_actions) in pack.summary_en

    def test_deterministic_pack_id(self):
        c1 = run_operating_cycle(
            tenant_id=TENANT, cycle_date="2026-08-08",
            source_id=SOURCE,
        )
        c2 = run_operating_cycle(
            tenant_id=TENANT, cycle_date="2026-08-08",
            source_id=SOURCE,
        )
        assert c1.action_pack.pack_id == c2.action_pack.pack_id
        assert c1.action_pack.pack_id.startswith("actionpack_")


# -----------------------------------------------------------------------
# Safety invariants
# -----------------------------------------------------------------------


class TestAutonomousOperatorSafety:
    def test_action_pack_never_autonomous(self):
        with pytest.raises(ValueError, match="autonomous_execution must be False"):
            FounderActionPack(
                tenant_id=TENANT,
                autonomous_execution=True,
                source_id=SOURCE,
            )

    def test_operating_cycle_never_autonomous(self):
        with pytest.raises(ValueError, match="autonomous_execution must be False"):
            OperatingCycle(
                tenant_id=TENANT,
                autonomous_execution=True,
                source_id=SOURCE,
            )

    def test_cycle_output_always_safe(self):
        """Every output of run_operating_cycle must have safe defaults."""
        cycle = run_operating_cycle(
            tenant_id=TENANT,
            new_prospects=[
                CompanyProfile(
                    tenant_id=TENANT, company_name="SafetyCo",
                    sector="saas", employee_count=100,
                    country="SA", source_id=SOURCE,
                    decision_makers=(
                        DecisionMaker(
                            name="Safe", role=DecisionMakerRole.FOUNDER_CEO,
                            email="safe@co.sa", is_primary=True,
                        ),
                    ),
                ),
            ],
            responses=[
                {"prospect_name": "Test", "prospect_company": "Co", "text": "yes"},
            ],
            source_id=SOURCE,
        )
        # Cycle itself
        assert cycle.autonomous_execution is False
        # Action pack
        assert cycle.action_pack.autonomous_execution is False
        # Research briefs
        for brief in cycle.research_briefs:
            assert brief.auto_contact_allowed is False
            assert brief.approval_required is True
        # Outreach sequences
        for seq in cycle.outreach_sequences:
            assert seq.auto_send is False
            assert seq.approval_required is True
        # Follow-up actions
        for action in cycle.follow_up_actions:
            assert action.auto_send is False
            assert action.approval_required is True
