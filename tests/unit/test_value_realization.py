"""Unit tests for api/routers/value_realization.py"""
from __future__ import annotations

import pytest
from fastapi import HTTPException

from api.routers.value_realization import (
    _VALUE_MILESTONES,
    _VALUE_METRICS,
    _VALUE_FRAMEWORKS,
    _VALID_FRAMEWORKS,
    ValueCaseInput,
    _build_value_case,
    router,
)


def _make_input(**overrides) -> ValueCaseInput:
    data = dict(
        client_name="Acme Trading Co.",
        framework="efficiency",
        baseline_reporting_hours_per_week=20.0,
        current_reporting_hours_per_week=12.0,
        baseline_error_rate_pct=10.0,
        current_error_rate_pct=4.0,
        months_since_go_live=3,
    )
    data.update(overrides)
    return ValueCaseInput(**data)


# ---------------------------------------------------------------------------
# Static data: _VALUE_MILESTONES
# ---------------------------------------------------------------------------


class TestValueMilestones:
    def test_has_five_items(self):
        assert len(_VALUE_MILESTONES) == 5

    def test_ordered_one_through_five(self):
        orders = [m["order"] for m in _VALUE_MILESTONES]
        assert orders == [1, 2, 3, 4, 5]

    def test_all_have_milestone_id(self):
        for m in _VALUE_MILESTONES:
            assert m.get("milestone_id"), f"missing milestone_id in {m}"

    def test_all_have_milestone_name_en(self):
        for m in _VALUE_MILESTONES:
            assert m.get("milestone_name_en"), f"missing milestone_name_en in {m}"

    def test_all_have_milestone_name_ar(self):
        for m in _VALUE_MILESTONES:
            assert m.get("milestone_name_ar"), f"missing milestone_name_ar in {m}"

    def test_all_have_typical_days_to_achieve(self):
        for m in _VALUE_MILESTONES:
            assert isinstance(m.get("typical_days_to_achieve"), int)

    def test_all_have_proof_metric_en(self):
        for m in _VALUE_MILESTONES:
            assert m.get("proof_metric_en"), f"missing proof_metric_en in {m}"

    def test_all_have_proof_metric_ar(self):
        for m in _VALUE_MILESTONES:
            assert m.get("proof_metric_ar"), f"missing proof_metric_ar in {m}"

    def test_contains_first_login(self):
        ids = [m["milestone_id"] for m in _VALUE_MILESTONES]
        assert "first_login" in ids

    def test_contains_roi_demonstrated(self):
        ids = [m["milestone_id"] for m in _VALUE_MILESTONES]
        assert "roi_demonstrated" in ids

    def test_first_login_typical_days_is_7(self):
        m = next(x for x in _VALUE_MILESTONES if x["milestone_id"] == "first_login")
        assert m["typical_days_to_achieve"] == 7

    def test_roi_demonstrated_typical_days_is_90(self):
        m = next(x for x in _VALUE_MILESTONES if x["milestone_id"] == "roi_demonstrated")
        assert m["typical_days_to_achieve"] == 90


# ---------------------------------------------------------------------------
# Static data: _VALUE_METRICS
# ---------------------------------------------------------------------------


class TestValueMetrics:
    def test_has_six_items(self):
        assert len(_VALUE_METRICS) == 6

    def test_all_have_metric_id(self):
        for m in _VALUE_METRICS:
            assert m.get("metric_id"), f"missing metric_id in {m}"

    def test_all_have_metric_name_en(self):
        for m in _VALUE_METRICS:
            assert m.get("metric_name_en"), f"missing metric_name_en in {m}"

    def test_all_have_metric_name_ar(self):
        for m in _VALUE_METRICS:
            assert m.get("metric_name_ar"), f"missing metric_name_ar in {m}"

    def test_all_have_unit(self):
        for m in _VALUE_METRICS:
            assert m.get("unit"), f"missing unit in {m}"

    def test_all_have_calculation_method_en(self):
        for m in _VALUE_METRICS:
            assert m.get("calculation_method_en"), f"missing calculation_method_en in {m}"

    def test_contains_time_saved_hours(self):
        ids = [m["metric_id"] for m in _VALUE_METRICS]
        assert "time_saved_hours" in ids

    def test_contains_revenue_influenced_sar(self):
        ids = [m["metric_id"] for m in _VALUE_METRICS]
        assert "revenue_influenced_sar" in ids


# ---------------------------------------------------------------------------
# Static data: _VALUE_FRAMEWORKS
# ---------------------------------------------------------------------------


class TestValueFrameworks:
    def test_has_three_keys(self):
        assert len(_VALUE_FRAMEWORKS) == 3

    def test_contains_efficiency(self):
        assert "efficiency" in _VALUE_FRAMEWORKS

    def test_contains_compliance(self):
        assert "compliance" in _VALUE_FRAMEWORKS

    def test_contains_growth(self):
        assert "growth" in _VALUE_FRAMEWORKS

    def test_all_have_name_en(self):
        for key, fw in _VALUE_FRAMEWORKS.items():
            assert fw.get("name_en"), f"{key} missing name_en"

    def test_all_have_name_ar(self):
        for key, fw in _VALUE_FRAMEWORKS.items():
            assert fw.get("name_ar"), f"{key} missing name_ar"

    def test_all_have_primary_metrics_list_of_three(self):
        for key, fw in _VALUE_FRAMEWORKS.items():
            assert isinstance(fw.get("primary_metrics"), list), f"{key} missing primary_metrics"
            assert len(fw["primary_metrics"]) == 3, f"{key} primary_metrics length != 3"

    def test_all_have_headline_formula_en(self):
        for key, fw in _VALUE_FRAMEWORKS.items():
            assert fw.get("headline_formula_en"), f"{key} missing headline_formula_en"


# ---------------------------------------------------------------------------
# _build_value_case
# ---------------------------------------------------------------------------


class TestBuildValueCase:
    def test_returns_dict(self):
        result = _build_value_case(_make_input())
        assert isinstance(result, dict)

    def test_has_hours_saved_per_week(self):
        result = _build_value_case(_make_input())
        assert "hours_saved_per_week" in result

    def test_has_hours_saved_pct(self):
        result = _build_value_case(_make_input())
        assert "hours_saved_pct" in result

    def test_has_error_reduction_pct(self):
        result = _build_value_case(_make_input())
        assert "error_reduction_pct" in result

    def test_has_annualized_hours_saved(self):
        result = _build_value_case(_make_input())
        assert "annualized_hours_saved" in result

    def test_has_estimated_sar_value(self):
        result = _build_value_case(_make_input())
        assert "estimated_sar_value" in result

    def test_has_milestones_likely_achieved(self):
        result = _build_value_case(_make_input())
        assert "milestones_likely_achieved" in result

    def test_has_client_name(self):
        result = _build_value_case(_make_input(client_name="Beta Corp"))
        assert result["client_name"] == "Beta Corp"

    def test_hours_saved_per_week_correct(self):
        result = _build_value_case(_make_input(
            baseline_reporting_hours_per_week=20.0,
            current_reporting_hours_per_week=12.0,
        ))
        assert abs(result["hours_saved_per_week"] - 8.0) < 0.001

    def test_hours_saved_pct_correct(self):
        result = _build_value_case(_make_input(
            baseline_reporting_hours_per_week=20.0,
            current_reporting_hours_per_week=12.0,
        ))
        assert abs(result["hours_saved_pct"] - 40.0) < 0.001

    def test_zero_baseline_hours_saved_pct_is_zero(self):
        result = _build_value_case(_make_input(
            baseline_reporting_hours_per_week=0.0,
            current_reporting_hours_per_week=0.0,
        ))
        assert result["hours_saved_pct"] == 0.0

    def test_error_reduction_pct_correct(self):
        result = _build_value_case(_make_input(
            baseline_error_rate_pct=10.0,
            current_error_rate_pct=4.0,
        ))
        assert abs(result["error_reduction_pct"] - 6.0) < 0.001

    def test_annualized_hours_saved_is_52x_weekly(self):
        result = _build_value_case(_make_input(
            baseline_reporting_hours_per_week=20.0,
            current_reporting_hours_per_week=12.0,
        ))
        expected = 8.0 * 52
        assert abs(result["annualized_hours_saved"] - expected) < 0.001

    def test_estimated_sar_value_is_75_times_annualized(self):
        result = _build_value_case(_make_input(
            baseline_reporting_hours_per_week=20.0,
            current_reporting_hours_per_week=12.0,
        ))
        assert abs(result["estimated_sar_value"] - result["annualized_hours_saved"] * 75) < 0.001

    def test_six_months_all_milestones_up_to_180_days(self):
        result = _build_value_case(_make_input(months_since_go_live=6))
        achieved_ids = result["milestones_likely_achieved"]
        for m in _VALUE_MILESTONES:
            if m["typical_days_to_achieve"] <= 180:
                assert m["milestone_id"] in achieved_ids, (
                    f"{m['milestone_id']} should be in achieved milestones at 6 months"
                )

    def test_zero_months_no_milestones(self):
        result = _build_value_case(_make_input(months_since_go_live=0))
        assert result["milestones_likely_achieved"] == []

    def test_hours_saved_per_week_cannot_be_negative(self):
        result = _build_value_case(_make_input(
            baseline_reporting_hours_per_week=5.0,
            current_reporting_hours_per_week=20.0,
        ))
        assert result["hours_saved_per_week"] == 0.0

    def test_error_reduction_pct_cannot_be_negative(self):
        result = _build_value_case(_make_input(
            baseline_error_rate_pct=2.0,
            current_error_rate_pct=8.0,
        ))
        assert result["error_reduction_pct"] == 0.0

    def test_invalid_framework_raises_http_422(self):
        with pytest.raises(HTTPException) as exc_info:
            _build_value_case(_make_input(framework="invalid_framework"))
        assert exc_info.value.status_code == 422

    def test_all_three_valid_frameworks_work(self):
        for fw in _VALID_FRAMEWORKS:
            result = _build_value_case(_make_input(framework=fw))
            assert result["framework"] == fw

    def test_governance_decision_is_approval_first(self):
        result = _build_value_case(_make_input())
        assert result["governance_decision"] == "APPROVAL_FIRST"

    def test_has_disclaimer_en(self):
        result = _build_value_case(_make_input())
        assert result.get("disclaimer_en")

    def test_has_disclaimer_ar(self):
        result = _build_value_case(_make_input())
        assert result.get("disclaimer_ar")

    def test_framework_data_matches_selected_framework(self):
        result = _build_value_case(_make_input(framework="compliance"))
        assert result["framework_data"] == _VALUE_FRAMEWORKS["compliance"]


# ---------------------------------------------------------------------------
# Router metadata
# ---------------------------------------------------------------------------


class TestRouterMetadata:
    def test_prefix(self):
        assert router.prefix == "/api/v1/value-realization"

    def test_tags_contain_analytics(self):
        assert "Analytics" in router.tags
