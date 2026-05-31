"""Unit tests for api/routers/revenue_forecast.py"""
from __future__ import annotations

import pytest

from api.routers.revenue_forecast import (
    _FORECAST_MODELS,
    _SEASONALITY_FACTORS,
    ForecastInput,
    _run_forecast,
    router,
)


def _make_input(**overrides) -> ForecastInput:
    data = dict(
        company_name="Test Co",
        current_mrr_sar=100_000.0,
        historical_monthly_growth_rate_pct=5.0,
        forecast_months=6,
        model="linear_trend",
        include_new_pipeline_sar=0.0,
    )
    data.update(overrides)
    return ForecastInput(**data)


class TestSeasonalityFactors:
    def test_twelve_months(self):
        assert len(_SEASONALITY_FACTORS) == 12

    def test_all_months_present(self):
        assert set(_SEASONALITY_FACTORS.keys()) == set(range(1, 13))

    def test_all_have_multiplier(self):
        for month, data in _SEASONALITY_FACTORS.items():
            assert "multiplier" in data, f"Month {month} missing multiplier"
            assert data["multiplier"] > 0

    def test_all_bilingual(self):
        for month, data in _SEASONALITY_FACTORS.items():
            assert data.get("month_name_en"), f"Month {month} missing month_name_en"
            assert data.get("month_name_ar"), f"Month {month} missing month_name_ar"

    def test_ramadan_period_lower_multiplier(self):
        # March is typically Ramadan → multiplier below 1.0
        march = _SEASONALITY_FACTORS[3]["multiplier"]
        assert march < 1.0

    def test_post_eid_higher_multiplier(self):
        # April is post-Eid → multiplier above 1.0
        april = _SEASONALITY_FACTORS[4]["multiplier"]
        assert april > 1.0


class TestForecastModels:
    def test_three_models(self):
        assert len(_FORECAST_MODELS) == 3

    def test_expected_models(self):
        assert set(_FORECAST_MODELS.keys()) == {"linear_trend", "seasonality_adjusted", "conservative"}

    def test_all_bilingual(self):
        for model_id, model_data in _FORECAST_MODELS.items():
            assert model_data.get("name_en"), f"{model_id} missing name_en"
            assert model_data.get("name_ar"), f"{model_id} missing name_ar"


class TestRunForecast:
    def test_returns_dict(self):
        result = _run_forecast(_make_input())
        assert isinstance(result, dict)

    def test_monthly_forecast_correct_length(self):
        result = _run_forecast(_make_input(forecast_months=6))
        assert len(result["monthly_forecast"]) == 6

    def test_24_month_forecast(self):
        result = _run_forecast(_make_input(forecast_months=24))
        assert len(result["monthly_forecast"]) == 24

    def test_has_peak_and_trough(self):
        result = _run_forecast(_make_input())
        assert "peak_month" in result
        assert "trough_month" in result

    def test_peak_mrr_gte_trough(self):
        result = _run_forecast(_make_input(model="seasonality_adjusted"))
        assert result["peak_month"]["mrr_sar"] >= result["trough_month"]["mrr_sar"]

    def test_conservative_model_lower_than_linear(self):
        linear = _run_forecast(_make_input(model="linear_trend", forecast_months=6))
        conservative = _run_forecast(_make_input(model="conservative", forecast_months=6))
        assert conservative["total_forecast_arr_sar"] < linear["total_forecast_arr_sar"]

    def test_has_arr(self):
        result = _run_forecast(_make_input())
        assert result.get("total_forecast_arr_sar", 0) > 0

    def test_pipeline_adds_to_base(self):
        no_pipeline = _run_forecast(_make_input(include_new_pipeline_sar=0))
        with_pipeline = _run_forecast(_make_input(include_new_pipeline_sar=50_000))
        assert with_pipeline["total_forecast_arr_sar"] > no_pipeline["total_forecast_arr_sar"]

    def test_governance_allow_with_review(self):
        result = _run_forecast(_make_input())
        assert result["governance_decision"] == "ALLOW_WITH_REVIEW"

    def test_has_disclaimer(self):
        result = _run_forecast(_make_input())
        assert result.get("disclaimer_en")
        assert result.get("disclaimer_ar")

    def test_has_company_name(self):
        result = _run_forecast(_make_input(company_name="Acme SA"))
        assert result["company_name"] == "Acme SA"

    def test_monthly_entries_bilingual(self):
        result = _run_forecast(_make_input(forecast_months=3))
        for entry in result["monthly_forecast"]:
            assert "month_name_en" in entry
            assert "month_name_ar" in entry
            assert entry["mrr_sar"] > 0

    def test_positive_growth_increases_mrr(self):
        result = _run_forecast(_make_input(
            model="linear_trend",
            historical_monthly_growth_rate_pct=10.0,
            forecast_months=3,
        ))
        mrr_values = [e["mrr_sar"] for e in result["monthly_forecast"]]
        assert mrr_values[-1] > mrr_values[0]


class TestRouterMetadata:
    def test_prefix(self):
        assert router.prefix == "/api/v1/revenue-forecast"

    def test_tags_contain_analytics(self):
        assert "Analytics" in router.tags
