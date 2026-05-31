"""Unit tests for api/routers/renewal_management.py"""
from __future__ import annotations

import pytest

from api.routers.renewal_management import (
    _RENEWAL_RISK_THRESHOLDS,
    _RENEWAL_TIMELINE,
    _UPSELL_TRIGGERS_AT_RENEWAL,
    RenewalAssessmentInput,
    _assess_renewal,
    router,
)


def _make_input(**overrides) -> RenewalAssessmentInput:
    data = dict(
        client_name="Aramco Digital",
        current_arr_sar=120_000.0,
        contract_end_date="2026-09-30",
        nrr_pct=115.0,
        health_score=80.0,
        champion_engaged=True,
        decision_maker_met=False,
        has_open_support_issues=False,
    )
    data.update(overrides)
    return RenewalAssessmentInput(**data)


# ---------------------------------------------------------------------------
# Static data: renewal timeline
# ---------------------------------------------------------------------------


class TestRenewalTimeline:
    def test_has_five_milestones(self):
        assert len(_RENEWAL_TIMELINE) == 5

    def test_ordered_1_to_5(self):
        orders = [m["order"] for m in _RENEWAL_TIMELINE]
        assert orders == [1, 2, 3, 4, 5]

    def test_all_have_weeks_before_renewal(self):
        for m in _RENEWAL_TIMELINE:
            assert "weeks_before_renewal" in m
            assert isinstance(m["weeks_before_renewal"], int)

    def test_all_have_milestone_en(self):
        for m in _RENEWAL_TIMELINE:
            assert m.get("milestone_en"), f"Milestone order {m.get('order')} missing milestone_en"

    def test_all_have_milestone_ar(self):
        for m in _RENEWAL_TIMELINE:
            assert m.get("milestone_ar"), f"Milestone order {m.get('order')} missing milestone_ar"

    def test_all_have_owner_en(self):
        for m in _RENEWAL_TIMELINE:
            assert m.get("owner_en"), f"Milestone order {m.get('order')} missing owner_en"

    def test_all_have_owner_ar(self):
        for m in _RENEWAL_TIMELINE:
            assert m.get("owner_ar"), f"Milestone order {m.get('order')} missing owner_ar"

    def test_all_have_action_items_en(self):
        for m in _RENEWAL_TIMELINE:
            assert isinstance(m.get("action_items_en"), list)
            assert len(m["action_items_en"]) == 2, (
                f"Milestone order {m.get('order')} must have 2 action_items_en"
            )

    def test_all_have_action_items_ar(self):
        for m in _RENEWAL_TIMELINE:
            assert isinstance(m.get("action_items_ar"), list)
            assert len(m["action_items_ar"]) == 2, (
                f"Milestone order {m.get('order')} must have 2 action_items_ar"
            )

    def test_first_milestone_12_weeks(self):
        first = next(m for m in _RENEWAL_TIMELINE if m["order"] == 1)
        assert first["weeks_before_renewal"] == 12

    def test_last_milestone_2_weeks(self):
        last = next(m for m in _RENEWAL_TIMELINE if m["order"] == 5)
        assert last["weeks_before_renewal"] == 2

    def test_milestones_decreasing_weeks(self):
        weeks = [m["weeks_before_renewal"] for m in _RENEWAL_TIMELINE]
        assert weeks == sorted(weeks, reverse=True)


# ---------------------------------------------------------------------------
# Static data: renewal risk thresholds
# ---------------------------------------------------------------------------


class TestRenewalRiskThresholds:
    def test_has_three_keys(self):
        assert len(_RENEWAL_RISK_THRESHOLDS) == 3

    def test_has_red_key(self):
        assert "red" in _RENEWAL_RISK_THRESHOLDS

    def test_has_amber_key(self):
        assert "amber" in _RENEWAL_RISK_THRESHOLDS

    def test_has_green_key(self):
        assert "green" in _RENEWAL_RISK_THRESHOLDS

    def test_red_has_label_en(self):
        assert _RENEWAL_RISK_THRESHOLDS["red"].get("label_en")

    def test_red_has_label_ar(self):
        assert _RENEWAL_RISK_THRESHOLDS["red"].get("label_ar")

    def test_amber_has_action_en(self):
        assert _RENEWAL_RISK_THRESHOLDS["amber"].get("action_en")

    def test_green_has_action_ar(self):
        assert _RENEWAL_RISK_THRESHOLDS["green"].get("action_ar")

    def test_red_nrr_threshold(self):
        assert _RENEWAL_RISK_THRESHOLDS["red"]["nrr_below"] == 90

    def test_red_health_score_threshold(self):
        assert _RENEWAL_RISK_THRESHOLDS["red"]["health_score_below"] == 40

    def test_amber_nrr_threshold(self):
        assert _RENEWAL_RISK_THRESHOLDS["amber"]["nrr_below"] == 105

    def test_amber_health_score_threshold(self):
        assert _RENEWAL_RISK_THRESHOLDS["amber"]["health_score_below"] == 65


# ---------------------------------------------------------------------------
# Static data: upsell triggers
# ---------------------------------------------------------------------------


class TestUpsellTriggers:
    def test_has_four_triggers(self):
        assert len(_UPSELL_TRIGGERS_AT_RENEWAL) == 4

    def test_all_have_trigger_en(self):
        for t in _UPSELL_TRIGGERS_AT_RENEWAL:
            assert t.get("trigger_en"), "Trigger missing trigger_en"

    def test_all_have_trigger_ar(self):
        for t in _UPSELL_TRIGGERS_AT_RENEWAL:
            assert t.get("trigger_ar"), "Trigger missing trigger_ar"

    def test_all_have_upsell_path_en(self):
        for t in _UPSELL_TRIGGERS_AT_RENEWAL:
            assert t.get("upsell_path_en"), "Trigger missing upsell_path_en"


# ---------------------------------------------------------------------------
# _assess_renewal
# ---------------------------------------------------------------------------


class TestAssessRenewal:
    def test_returns_dict(self):
        result = _assess_renewal(_make_input())
        assert isinstance(result, dict)

    def test_has_risk_category(self):
        result = _assess_renewal(_make_input())
        assert "risk_category" in result

    def test_has_renewal_probability_pct(self):
        result = _assess_renewal(_make_input())
        assert "renewal_probability_pct" in result

    def test_has_recommended_arr_target_sar(self):
        result = _assess_renewal(_make_input())
        assert "recommended_arr_target_sar" in result

    def test_has_upsell_eligible(self):
        result = _assess_renewal(_make_input())
        assert "upsell_eligible" in result

    def test_has_client_name(self):
        result = _assess_renewal(_make_input(client_name="SABIC"))
        assert result["client_name"] == "SABIC"

    def test_green_case_risk_category(self):
        result = _assess_renewal(_make_input(nrr_pct=115.0, health_score=80.0))
        assert result["risk_category"] == "green"

    def test_green_case_upsell_eligible_true(self):
        result = _assess_renewal(_make_input(nrr_pct=115.0, health_score=80.0))
        assert result["upsell_eligible"] is True

    def test_red_case_nrr_below_90(self):
        result = _assess_renewal(_make_input(nrr_pct=80.0, health_score=50.0))
        assert result["risk_category"] == "red"

    def test_red_case_health_below_40(self):
        result = _assess_renewal(_make_input(nrr_pct=100.0, health_score=30.0))
        assert result["risk_category"] == "red"

    def test_red_case_upsell_eligible_false(self):
        result = _assess_renewal(_make_input(nrr_pct=80.0, health_score=30.0))
        assert result["upsell_eligible"] is False

    def test_amber_case(self):
        result = _assess_renewal(_make_input(nrr_pct=100.0, health_score=60.0))
        assert result["risk_category"] == "amber"

    def test_amber_nrr_below_105_health_above_65(self):
        result = _assess_renewal(_make_input(nrr_pct=104.0, health_score=70.0))
        assert result["risk_category"] == "amber"

    def test_renewal_probability_in_range_0_100(self):
        for nrr, health in [(80, 30), (100, 60), (115, 80)]:
            result = _assess_renewal(_make_input(nrr_pct=nrr, health_score=health))
            assert 0 <= result["renewal_probability_pct"] <= 100

    def test_champion_engaged_adds_to_probability(self):
        base = _assess_renewal(_make_input(champion_engaged=False, decision_maker_met=False))
        with_champion = _assess_renewal(_make_input(champion_engaged=True, decision_maker_met=False))
        assert with_champion["renewal_probability_pct"] > base["renewal_probability_pct"]

    def test_decision_maker_met_adds_to_probability(self):
        base = _assess_renewal(_make_input(champion_engaged=False, decision_maker_met=False))
        with_dm = _assess_renewal(_make_input(champion_engaged=False, decision_maker_met=True))
        assert with_dm["renewal_probability_pct"] > base["renewal_probability_pct"]

    def test_open_support_issues_reduces_probability(self):
        clean = _assess_renewal(_make_input(has_open_support_issues=False))
        with_issues = _assess_renewal(_make_input(has_open_support_issues=True))
        assert with_issues["renewal_probability_pct"] < clean["renewal_probability_pct"]

    def test_green_arr_target_multiplier(self):
        inp = _make_input(nrr_pct=115.0, health_score=80.0, current_arr_sar=100_000.0)
        result = _assess_renewal(inp)
        assert result["recommended_arr_target_sar"] == pytest.approx(120_000.0)

    def test_amber_arr_target_multiplier(self):
        inp = _make_input(nrr_pct=100.0, health_score=60.0, current_arr_sar=100_000.0)
        result = _assess_renewal(inp)
        assert result["recommended_arr_target_sar"] == pytest.approx(100_000.0)

    def test_red_arr_target_multiplier(self):
        inp = _make_input(nrr_pct=80.0, health_score=30.0, current_arr_sar=100_000.0)
        result = _assess_renewal(inp)
        assert result["recommended_arr_target_sar"] == pytest.approx(90_000.0)

    def test_governance_decision_approval_first(self):
        result = _assess_renewal(_make_input())
        assert result["governance_decision"] == "APPROVAL_FIRST"

    def test_has_disclaimer_en(self):
        result = _assess_renewal(_make_input())
        assert result.get("disclaimer_en")

    def test_has_disclaimer_ar(self):
        result = _assess_renewal(_make_input())
        assert result.get("disclaimer_ar")

    def test_probability_clamped_at_100(self):
        # Best possible scenario: green + champion + dm met, no issues
        result = _assess_renewal(
            _make_input(
                nrr_pct=200.0,
                health_score=100.0,
                champion_engaged=True,
                decision_maker_met=True,
                has_open_support_issues=False,
            )
        )
        assert result["renewal_probability_pct"] <= 100

    def test_probability_clamped_at_0(self):
        # Worst case: red + no champion + no dm + open issues
        result = _assess_renewal(
            _make_input(
                nrr_pct=0.0,
                health_score=0.0,
                champion_engaged=False,
                decision_maker_met=False,
                has_open_support_issues=True,
            )
        )
        assert result["renewal_probability_pct"] >= 0

    def test_has_risk_threshold_data(self):
        result = _assess_renewal(_make_input())
        assert "risk_threshold_data" in result
        assert result["risk_threshold_data"].get("label_en")


# ---------------------------------------------------------------------------
# Router metadata
# ---------------------------------------------------------------------------


class TestRouterMetadata:
    def test_prefix(self):
        assert router.prefix == "/api/v1/renewal-management"

    def test_tags_contain_sales(self):
        assert "Sales" in router.tags
