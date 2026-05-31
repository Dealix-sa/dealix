"""Unit tests for api/routers/sales_forecasting.py"""
from __future__ import annotations

import pytest
from fastapi import HTTPException

from api.routers.sales_forecasting import (
    _FORECAST_METHODOLOGIES,
    _STAGE_WIN_RATES,
    _QUOTA_ATTAINMENT_BENCHMARKS,
    _VALID_METHODOLOGIES,
    ForecastInput,
    _run_sales_forecast,
    router,
)


def _make_input(**overrides) -> ForecastInput:
    data = dict(
        rep_name="Ahmed Al-Rashidi",
        quota_sar=100_000.0,
        methodology="stage_weighted",
        pipeline_deals=[],
    )
    data.update(overrides)
    return ForecastInput(**data)


# ---------------------------------------------------------------------------
# Static data: _FORECAST_METHODOLOGIES
# ---------------------------------------------------------------------------


class TestForecastMethodologies:
    def test_has_three_keys(self):
        assert len(_FORECAST_METHODOLOGIES) == 3

    def test_contains_pipeline_coverage(self):
        assert "pipeline_coverage" in _FORECAST_METHODOLOGIES

    def test_contains_stage_weighted(self):
        assert "stage_weighted" in _FORECAST_METHODOLOGIES

    def test_contains_ai_guided(self):
        assert "ai_guided" in _FORECAST_METHODOLOGIES

    def test_all_have_name_en(self):
        for key, data in _FORECAST_METHODOLOGIES.items():
            assert data.get("name_en"), f"{key} missing name_en"

    def test_all_have_name_ar(self):
        for key, data in _FORECAST_METHODOLOGIES.items():
            assert data.get("name_ar"), f"{key} missing name_ar"

    def test_all_have_description_en(self):
        for key, data in _FORECAST_METHODOLOGIES.items():
            assert data.get("description_en"), f"{key} missing description_en"

    def test_all_have_accuracy_claim_en(self):
        for key, data in _FORECAST_METHODOLOGIES.items():
            assert data.get("accuracy_claim_en"), f"{key} missing accuracy_claim_en"

    def test_all_have_best_for_en(self):
        for key, data in _FORECAST_METHODOLOGIES.items():
            assert data.get("best_for_en"), f"{key} missing best_for_en"


# ---------------------------------------------------------------------------
# Static data: _STAGE_WIN_RATES
# ---------------------------------------------------------------------------


class TestStageWinRates:
    def test_has_six_stages(self):
        assert len(_STAGE_WIN_RATES) == 6

    def test_contains_discovery(self):
        assert "discovery" in _STAGE_WIN_RATES

    def test_contains_qualification(self):
        assert "qualification" in _STAGE_WIN_RATES

    def test_contains_demo(self):
        assert "demo" in _STAGE_WIN_RATES

    def test_contains_proposal(self):
        assert "proposal" in _STAGE_WIN_RATES

    def test_contains_negotiation(self):
        assert "negotiation" in _STAGE_WIN_RATES

    def test_contains_closed(self):
        assert "closed" in _STAGE_WIN_RATES

    def test_closed_stage_win_rate_is_100(self):
        assert _STAGE_WIN_RATES["closed"] == 100.0

    def test_discovery_stage_win_rate_is_10(self):
        assert _STAGE_WIN_RATES["discovery"] == 10.0

    def test_win_rates_increase_across_stages(self):
        ordered = ["discovery", "qualification", "demo", "proposal", "negotiation", "closed"]
        for i in range(len(ordered) - 1):
            assert _STAGE_WIN_RATES[ordered[i]] < _STAGE_WIN_RATES[ordered[i + 1]]


# ---------------------------------------------------------------------------
# _run_sales_forecast
# ---------------------------------------------------------------------------


class TestRunSalesForecast:
    def test_returns_dict(self):
        result = _run_sales_forecast(_make_input())
        assert isinstance(result, dict)

    def test_has_total_pipeline_sar(self):
        result = _run_sales_forecast(_make_input())
        assert "total_pipeline_sar" in result

    def test_has_weighted_forecast_sar(self):
        result = _run_sales_forecast(_make_input())
        assert "weighted_forecast_sar" in result

    def test_has_pipeline_coverage_ratio(self):
        result = _run_sales_forecast(_make_input())
        assert "pipeline_coverage_ratio" in result

    def test_has_forecast_attainment_pct(self):
        result = _run_sales_forecast(_make_input())
        assert "forecast_attainment_pct" in result

    def test_has_attainment_label(self):
        result = _run_sales_forecast(_make_input())
        assert "attainment_label" in result

    def test_empty_pipeline_total_is_zero(self):
        result = _run_sales_forecast(_make_input(pipeline_deals=[]))
        assert result["total_pipeline_sar"] == 0.0

    def test_empty_pipeline_weighted_is_zero(self):
        result = _run_sales_forecast(_make_input(pipeline_deals=[]))
        assert result["weighted_forecast_sar"] == 0.0

    def test_closed_deal_weighted_equals_full_value(self):
        deal = {"stage": "closed", "deal_value_sar": 50_000.0}
        result = _run_sales_forecast(_make_input(pipeline_deals=[deal]))
        assert abs(result["weighted_forecast_sar"] - 50_000.0) < 0.01

    def test_discovery_deal_weighted_is_10_pct(self):
        deal = {"stage": "discovery", "deal_value_sar": 100_000.0}
        result = _run_sales_forecast(_make_input(pipeline_deals=[deal]))
        assert abs(result["weighted_forecast_sar"] - 10_000.0) < 0.01

    def test_zero_quota_no_division_by_zero(self):
        result = _run_sales_forecast(_make_input(quota_sar=0.0))
        assert result["pipeline_coverage_ratio"] == 0.0
        assert result["forecast_attainment_pct"] == 0.0

    def test_attainment_label_world_class(self):
        deals = [{"stage": "closed", "deal_value_sar": 200_000.0}]
        result = _run_sales_forecast(_make_input(quota_sar=100_000.0, pipeline_deals=deals))
        assert result["attainment_label"] == "world_class"

    def test_attainment_label_good(self):
        deals = [{"stage": "closed", "deal_value_sar": 100_000.0}]
        result = _run_sales_forecast(_make_input(quota_sar=100_000.0, pipeline_deals=deals))
        assert result["attainment_label"] == "good"

    def test_attainment_label_at_risk(self):
        deals = [{"stage": "closed", "deal_value_sar": 85_000.0}]
        result = _run_sales_forecast(_make_input(quota_sar=100_000.0, pipeline_deals=deals))
        assert result["attainment_label"] == "at_risk"

    def test_attainment_label_below_target(self):
        deals = [{"stage": "discovery", "deal_value_sar": 10_000.0}]
        result = _run_sales_forecast(_make_input(quota_sar=100_000.0, pipeline_deals=deals))
        assert result["attainment_label"] == "below_target"

    def test_invalid_methodology_raises_http_422(self):
        with pytest.raises(HTTPException) as exc_info:
            _run_sales_forecast(_make_input(methodology="magic_method"))
        assert exc_info.value.status_code == 422

    def test_all_three_valid_methodologies_work(self):
        for method in _VALID_METHODOLOGIES:
            result = _run_sales_forecast(_make_input(methodology=method))
            assert result["methodology"] == method

    def test_governance_decision_is_allow_with_review(self):
        result = _run_sales_forecast(_make_input())
        assert result["governance_decision"] == "ALLOW_WITH_REVIEW"

    def test_deals_count_matches_pipeline_length(self):
        deals = [
            {"stage": "demo", "deal_value_sar": 10_000.0},
            {"stage": "proposal", "deal_value_sar": 20_000.0},
        ]
        result = _run_sales_forecast(_make_input(pipeline_deals=deals))
        assert result["deals_count"] == 2

    def test_unknown_stage_defaults_to_10_pct_win_rate(self):
        deal = {"stage": "unknown_stage", "deal_value_sar": 100_000.0}
        result = _run_sales_forecast(_make_input(pipeline_deals=[deal]))
        assert abs(result["weighted_forecast_sar"] - 10_000.0) < 0.01

    def test_pipeline_coverage_ratio_correct(self):
        deals = [{"stage": "closed", "deal_value_sar": 300_000.0}]
        result = _run_sales_forecast(_make_input(quota_sar=100_000.0, pipeline_deals=deals))
        assert abs(result["pipeline_coverage_ratio"] - 3.0) < 0.01

    def test_rep_name_in_result(self):
        result = _run_sales_forecast(_make_input(rep_name="Sara Al-Mutairi"))
        assert result["rep_name"] == "Sara Al-Mutairi"

    def test_multiple_deals_total_pipeline_sums_correctly(self):
        deals = [
            {"stage": "demo", "deal_value_sar": 30_000.0},
            {"stage": "proposal", "deal_value_sar": 70_000.0},
        ]
        result = _run_sales_forecast(_make_input(pipeline_deals=deals))
        assert abs(result["total_pipeline_sar"] - 100_000.0) < 0.01


# ---------------------------------------------------------------------------
# Router metadata
# ---------------------------------------------------------------------------


class TestRouterMetadata:
    def test_prefix(self):
        assert router.prefix == "/api/v1/sales-forecasting"

    def test_tags_contain_analytics(self):
        assert "Analytics" in router.tags
