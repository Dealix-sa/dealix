"""Tests for the Follow-up & Closing Engine.

Covers response handling, objection responses, deal progression,
closing plans, safety invariants, and bilingual output.
"""
from __future__ import annotations

import pytest

from dealix.company_intelligence.followup_engine import (
    ClosingPlan,
    ClosingSignal,
    DealProgression,
    DealStage,
    FollowUpAction,
    FollowUpUrgency,
    ObjectionCategory,
    ObjectionResponse,
    assess_deal_progression,
    generate_closing_plan,
    get_objection_response,
    handle_response,
)

TENANT = "tenant_test_followup"
SOURCE = "test_source"


# -----------------------------------------------------------------------
# Response handling
# -----------------------------------------------------------------------


class TestResponseHandling:
    def test_opt_out_response(self):
        action = handle_response(
            tenant_id=TENANT,
            prospect_name="Ahmad",
            prospect_company="TestCo",
            response_text="إيقاف",
            source_id=SOURCE,
        )
        assert action.action_type == "opt_out"
        assert action.urgency == FollowUpUrgency.IMMEDIATE
        assert action.deal_stage == DealStage.LOST
        assert action.auto_send is False

    def test_positive_response(self):
        action = handle_response(
            tenant_id=TENANT,
            prospect_name="Faisal",
            prospect_company="CloudSoft",
            response_text="Yes, sounds good! Let's talk",
            source_id=SOURCE,
        )
        assert action.action_type == "schedule_discovery"
        assert action.urgency == FollowUpUrgency.IMMEDIATE
        assert action.deal_stage == DealStage.INTERESTED

    def test_interested_response(self):
        action = handle_response(
            tenant_id=TENANT,
            prospect_name="Sara",
            prospect_company="TechCo",
            response_text="tell me more about pricing",
            source_id=SOURCE,
        )
        assert action.action_type == "provide_info"
        assert action.urgency == FollowUpUrgency.SAME_DAY

    def test_question_response(self):
        action = handle_response(
            tenant_id=TENANT,
            prospect_name="Khalid",
            prospect_company="DataCo",
            response_text="How does it work exactly?",
            source_id=SOURCE,
        )
        assert action.action_type == "answer_question"

    def test_objection_response(self):
        action = handle_response(
            tenant_id=TENANT,
            prospect_name="Nasser",
            prospect_company="BigCo",
            response_text="too expensive for our budget",
            source_id=SOURCE,
        )
        assert action.action_type == "handle_objection"
        assert "اعتراض" in action.reason

    def test_not_now_response(self):
        action = handle_response(
            tenant_id=TENANT,
            prospect_name="Ali",
            prospect_company="BusyCo",
            response_text="not now, maybe later",
            source_id=SOURCE,
        )
        assert action.action_type == "schedule_later"
        assert action.deal_stage == DealStage.DEFERRED

    def test_referral_response(self):
        action = handle_response(
            tenant_id=TENANT,
            prospect_name="Mona",
            prospect_company="RefCo",
            response_text="try reaching out to our VP Sales",
            source_id=SOURCE,
        )
        assert action.action_type == "follow_referral"

    def test_negative_response(self):
        action = handle_response(
            tenant_id=TENANT,
            prospect_name="Omar",
            prospect_company="NoCo",
            response_text="no",
            source_id=SOURCE,
        )
        assert action.action_type == "monitor"
        assert action.urgency == FollowUpUrgency.MONITOR

    def test_deterministic_id(self):
        a1 = handle_response(
            tenant_id=TENANT, prospect_name="Test",
            prospect_company="Co", response_text="yes",
            source_id=SOURCE,
        )
        a2 = handle_response(
            tenant_id=TENANT, prospect_name="Test",
            prospect_company="Co", response_text="yes",
            source_id=SOURCE,
        )
        assert a1.action_id == a2.action_id
        assert a1.action_id.startswith("followup_")

    def test_bilingual_drafts(self):
        action = handle_response(
            tenant_id=TENANT, prospect_name="Test",
            prospect_company="Co", response_text="yes sure",
            source_id=SOURCE,
        )
        assert action.draft_ar  # Arabic draft exists
        assert action.draft_en  # English draft exists


# -----------------------------------------------------------------------
# Objection handling
# -----------------------------------------------------------------------


class TestObjectionHandling:
    def test_price_objection(self):
        resp = get_objection_response(ObjectionCategory.PRICE, "too expensive")
        assert isinstance(resp, ObjectionResponse)
        assert resp.category == ObjectionCategory.PRICE
        assert resp.response_ar  # Has Arabic response
        assert resp.response_en  # Has English response
        assert resp.reframe_ar  # Has Arabic reframe
        assert resp.reframe_en  # Has English reframe
        assert resp.auto_send is False

    def test_all_categories_have_responses(self):
        for cat in [
            ObjectionCategory.PRICE,
            ObjectionCategory.TIMING,
            ObjectionCategory.AUTHORITY,
            ObjectionCategory.NEED,
            ObjectionCategory.TRUST,
            ObjectionCategory.COMPETITOR,
            ObjectionCategory.COMPLEXITY,
        ]:
            resp = get_objection_response(cat)
            assert resp.response_ar
            assert resp.response_en

    def test_custom_category_has_fallback(self):
        resp = get_objection_response(ObjectionCategory.CUSTOM, "some random objection")
        assert resp.response_ar
        assert resp.response_en

    def test_deterministic_id(self):
        r1 = get_objection_response(ObjectionCategory.PRICE, "expensive")
        r2 = get_objection_response(ObjectionCategory.PRICE, "expensive")
        assert r1.response_id == r2.response_id
        assert r1.response_id.startswith("objection_")


# -----------------------------------------------------------------------
# Deal progression
# -----------------------------------------------------------------------


class TestDealProgression:
    def test_basic_progression(self):
        prog = assess_deal_progression(
            tenant_id=TENANT,
            prospect_name="Ahmad",
            prospect_company="TestCo",
            current_stage=DealStage.DISCOVERY,
            source_id=SOURCE,
        )
        assert isinstance(prog, DealProgression)
        assert prog.current_stage == DealStage.DISCOVERY
        assert 0 <= prog.closing_probability <= 100
        assert prog.auto_close is False

    def test_won_deal_full_probability(self):
        prog = assess_deal_progression(
            tenant_id=TENANT,
            prospect_name="Test",
            prospect_company="Co",
            current_stage=DealStage.WON,
            source_id=SOURCE,
        )
        assert prog.closing_probability == 100.0

    def test_lost_deal_zero_probability(self):
        prog = assess_deal_progression(
            tenant_id=TENANT,
            prospect_name="Test",
            prospect_company="Co",
            current_stage=DealStage.LOST,
            source_id=SOURCE,
        )
        assert prog.closing_probability == 0.0

    def test_closing_signals_increase_probability(self):
        without = assess_deal_progression(
            tenant_id=TENANT, prospect_name="Test",
            prospect_company="Co",
            current_stage=DealStage.PROPOSAL,
            source_id=SOURCE,
        )
        with_signals = assess_deal_progression(
            tenant_id=TENANT, prospect_name="Test",
            prospect_company="Co",
            current_stage=DealStage.PROPOSAL,
            closing_signals=(
                ClosingSignal.ASKED_PRICING,
                ClosingSignal.REQUESTED_PROPOSAL,
            ),
            source_id=SOURCE,
        )
        assert with_signals.closing_probability > without.closing_probability

    def test_unresolved_objections_decrease_probability(self):
        clean = assess_deal_progression(
            tenant_id=TENANT, prospect_name="Test",
            prospect_company="Co",
            current_stage=DealStage.NEGOTIATION,
            source_id=SOURCE,
        )
        with_objections = assess_deal_progression(
            tenant_id=TENANT, prospect_name="Test",
            prospect_company="Co",
            current_stage=DealStage.NEGOTIATION,
            objections_raised=(ObjectionCategory.PRICE, ObjectionCategory.TIMING),
            source_id=SOURCE,
        )
        assert with_objections.closing_probability < clean.closing_probability

    def test_staleness_decreases_probability(self):
        fresh = assess_deal_progression(
            tenant_id=TENANT, prospect_name="Test",
            prospect_company="Co",
            current_stage=DealStage.PROPOSAL,
            days_in_stage=1,
            source_id=SOURCE,
        )
        stale = assess_deal_progression(
            tenant_id=TENANT, prospect_name="Test",
            prospect_company="Co",
            current_stage=DealStage.PROPOSAL,
            days_in_stage=30,
            source_id=SOURCE,
        )
        assert stale.closing_probability < fresh.closing_probability

    def test_next_action_determined(self):
        prog = assess_deal_progression(
            tenant_id=TENANT, prospect_name="Test",
            prospect_company="Co",
            current_stage=DealStage.PROSPECT,
            source_id=SOURCE,
        )
        assert prog.next_action == "initiate_contact"
        assert prog.next_action_ar  # Arabic action exists

    def test_deterministic_id(self):
        d1 = assess_deal_progression(
            tenant_id=TENANT, prospect_name="Test",
            prospect_company="Co",
            current_stage=DealStage.DISCOVERY,
            source_id=SOURCE,
        )
        d2 = assess_deal_progression(
            tenant_id=TENANT, prospect_name="Test",
            prospect_company="Co",
            current_stage=DealStage.DISCOVERY,
            source_id=SOURCE,
        )
        assert d1.deal_id == d2.deal_id
        assert d1.deal_id.startswith("deal_")


# -----------------------------------------------------------------------
# Closing plan
# -----------------------------------------------------------------------


class TestClosingPlan:
    def test_basic_plan(self):
        deal = assess_deal_progression(
            tenant_id=TENANT, prospect_name="Ahmad",
            prospect_company="TestCo",
            current_stage=DealStage.DISCOVERY,
            source_id=SOURCE,
        )
        plan = generate_closing_plan(
            tenant_id=TENANT, deal=deal, source_id=SOURCE,
        )
        assert isinstance(plan, ClosingPlan)
        assert plan.auto_close is False
        assert plan.approval_required is True
        assert len(plan.steps) > 0
        assert len(plan.steps_ar) > 0

    def test_plan_has_bilingual_steps(self):
        deal = assess_deal_progression(
            tenant_id=TENANT, prospect_name="Test",
            prospect_company="Co",
            current_stage=DealStage.PROSPECT,
            source_id=SOURCE,
        )
        plan = generate_closing_plan(
            tenant_id=TENANT, deal=deal, source_id=SOURCE,
        )
        assert len(plan.steps) == len(plan.steps_ar)

    def test_deterministic_id(self):
        deal = assess_deal_progression(
            tenant_id=TENANT, prospect_name="Test",
            prospect_company="Co",
            current_stage=DealStage.DISCOVERY,
            source_id=SOURCE,
        )
        p1 = generate_closing_plan(
            tenant_id=TENANT, deal=deal, source_id=SOURCE,
        )
        p2 = generate_closing_plan(
            tenant_id=TENANT, deal=deal, source_id=SOURCE,
        )
        assert p1.plan_id == p2.plan_id
        assert p1.plan_id.startswith("closingplan_")


# -----------------------------------------------------------------------
# Safety invariants
# -----------------------------------------------------------------------


class TestFollowUpEngineSafety:
    def test_follow_up_never_auto_send(self):
        with pytest.raises(ValueError, match="auto_send must be False"):
            FollowUpAction(
                tenant_id=TENANT, auto_send=True,
                approval_required=True, source_id=SOURCE,
            )

    def test_follow_up_requires_approval(self):
        with pytest.raises(ValueError, match="approval_required must be True"):
            FollowUpAction(
                tenant_id=TENANT, auto_send=False,
                approval_required=False, source_id=SOURCE,
            )

    def test_objection_response_never_auto_send(self):
        with pytest.raises(ValueError, match="auto_send must be False"):
            ObjectionResponse(auto_send=True)

    def test_deal_progression_never_auto_close(self):
        with pytest.raises(ValueError, match="auto_close must be False"):
            DealProgression(
                tenant_id=TENANT, auto_close=True,
                source_id=SOURCE,
            )

    def test_closing_plan_never_auto_close(self):
        with pytest.raises(ValueError, match="auto_close must be False"):
            ClosingPlan(
                tenant_id=TENANT, auto_close=True,
                approval_required=True, source_id=SOURCE,
            )

    def test_closing_plan_requires_approval(self):
        with pytest.raises(ValueError, match="approval_required must be True"):
            ClosingPlan(
                tenant_id=TENANT, auto_close=False,
                approval_required=False, source_id=SOURCE,
            )
