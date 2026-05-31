"""Unit tests for api/routers/health_score_explainer.py"""
from __future__ import annotations

import pytest

from api.routers.health_score_explainer import (
    _HEALTH_DIMENSIONS,
    _HEALTH_SCORE_BANDS,
    _HEALTH_IMPROVEMENT_LEVERS,
    HealthScoreBreakdownInput,
    _explain_health_score,
    router,
)


def _make_input(**overrides) -> HealthScoreBreakdownInput:
    data = dict(
        client_name="Acme Corp",
        product_usage_score=80.0,
        nps_score_normalized=70.0,
        support_health_score=85.0,
        engagement_score=75.0,
        expansion_signals_score=65.0,
        billing_health_score=95.0,
    )
    data.update(overrides)
    return HealthScoreBreakdownInput(**data)


def _make_all_100_input() -> HealthScoreBreakdownInput:
    return HealthScoreBreakdownInput(
        client_name="Perfect Client",
        product_usage_score=100.0,
        nps_score_normalized=100.0,
        support_health_score=100.0,
        engagement_score=100.0,
        expansion_signals_score=100.0,
        billing_health_score=100.0,
    )


def _make_all_zero_input() -> HealthScoreBreakdownInput:
    return HealthScoreBreakdownInput(
        client_name="Zero Client",
        product_usage_score=0.0,
        nps_score_normalized=0.0,
        support_health_score=0.0,
        engagement_score=0.0,
        expansion_signals_score=0.0,
        billing_health_score=0.0,
    )


# ---------------------------------------------------------------------------
# Static data: _HEALTH_DIMENSIONS
# ---------------------------------------------------------------------------


class TestHealthDimensions:
    def test_has_six_items(self):
        assert len(_HEALTH_DIMENSIONS) == 6

    def test_ordered_1_through_6(self):
        orders = [d["order"] for d in _HEALTH_DIMENSIONS]
        assert orders == list(range(1, 7))

    def test_weights_sum_to_100(self):
        total = sum(d["weight"] for d in _HEALTH_DIMENSIONS)
        assert total == 100

    def test_all_have_dimension_id(self):
        for d in _HEALTH_DIMENSIONS:
            assert d.get("dimension_id"), f"Dimension order {d['order']} missing dimension_id"

    def test_all_have_dimension_name_en(self):
        for d in _HEALTH_DIMENSIONS:
            assert d.get("dimension_name_en"), f"{d['dimension_id']} missing dimension_name_en"

    def test_all_have_dimension_name_ar(self):
        for d in _HEALTH_DIMENSIONS:
            assert d.get("dimension_name_ar"), f"{d['dimension_id']} missing dimension_name_ar"

    def test_all_have_weight(self):
        for d in _HEALTH_DIMENSIONS:
            assert isinstance(d.get("weight"), int), f"{d['dimension_id']} missing int weight"

    def test_all_have_description_en(self):
        for d in _HEALTH_DIMENSIONS:
            assert d.get("description_en"), f"{d['dimension_id']} missing description_en"

    def test_all_have_green_threshold(self):
        for d in _HEALTH_DIMENSIONS:
            assert "green_threshold" in d, f"{d['dimension_id']} missing green_threshold"

    def test_all_have_amber_threshold(self):
        for d in _HEALTH_DIMENSIONS:
            assert "amber_threshold" in d, f"{d['dimension_id']} missing amber_threshold"

    def test_product_usage_weight_is_25(self):
        dim = next(d for d in _HEALTH_DIMENSIONS if d["dimension_id"] == "product_usage")
        assert dim["weight"] == 25

    def test_billing_health_weight_is_10(self):
        dim = next(d for d in _HEALTH_DIMENSIONS if d["dimension_id"] == "billing_health")
        assert dim["weight"] == 10


# ---------------------------------------------------------------------------
# Static data: _HEALTH_SCORE_BANDS
# ---------------------------------------------------------------------------


class TestHealthScoreBands:
    def test_has_six_keys(self):
        assert len(_HEALTH_SCORE_BANDS) == 6

    def test_contains_expansion_ready(self):
        assert "expansion_ready" in _HEALTH_SCORE_BANDS

    def test_contains_healthy(self):
        assert "healthy" in _HEALTH_SCORE_BANDS

    def test_contains_stable(self):
        assert "stable" in _HEALTH_SCORE_BANDS

    def test_contains_at_risk(self):
        assert "at_risk" in _HEALTH_SCORE_BANDS

    def test_contains_critical(self):
        assert "critical" in _HEALTH_SCORE_BANDS

    def test_contains_blocked(self):
        assert "blocked" in _HEALTH_SCORE_BANDS

    def test_all_have_band_name_en(self):
        for key, data in _HEALTH_SCORE_BANDS.items():
            assert data.get("band_name_en"), f"{key} missing band_name_en"

    def test_all_have_band_name_ar(self):
        for key, data in _HEALTH_SCORE_BANDS.items():
            assert data.get("band_name_ar"), f"{key} missing band_name_ar"

    def test_all_have_score_range_en(self):
        for key, data in _HEALTH_SCORE_BANDS.items():
            assert data.get("score_range_en"), f"{key} missing score_range_en"

    def test_all_have_recommended_actions_en(self):
        for key, data in _HEALTH_SCORE_BANDS.items():
            assert isinstance(data.get("recommended_actions_en"), list), (
                f"{key} missing recommended_actions_en list"
            )

    def test_all_recommended_actions_have_2_items(self):
        for key, data in _HEALTH_SCORE_BANDS.items():
            assert len(data["recommended_actions_en"]) == 2, (
                f"{key} recommended_actions_en should have 2 items"
            )


# ---------------------------------------------------------------------------
# Static data: _HEALTH_IMPROVEMENT_LEVERS
# ---------------------------------------------------------------------------


class TestHealthImprovementLevers:
    def test_has_five_items(self):
        assert len(_HEALTH_IMPROVEMENT_LEVERS) == 5

    def test_all_have_lever_en(self):
        for lever in _HEALTH_IMPROVEMENT_LEVERS:
            assert lever.get("lever_en"), "Lever missing lever_en"

    def test_all_have_lever_ar(self):
        for lever in _HEALTH_IMPROVEMENT_LEVERS:
            assert lever.get("lever_ar"), "Lever missing lever_ar"

    def test_all_have_typical_score_improvement(self):
        for lever in _HEALTH_IMPROVEMENT_LEVERS:
            assert "typical_score_improvement" in lever

    def test_all_have_time_to_impact_weeks(self):
        for lever in _HEALTH_IMPROVEMENT_LEVERS:
            assert "time_to_impact_weeks" in lever


# ---------------------------------------------------------------------------
# _explain_health_score
# ---------------------------------------------------------------------------


class TestExplainHealthScore:
    def test_returns_dict(self):
        result = _explain_health_score(_make_input())
        assert isinstance(result, dict)

    def test_has_overall_score(self):
        result = _explain_health_score(_make_input())
        assert "overall_score" in result

    def test_has_score_band(self):
        result = _explain_health_score(_make_input())
        assert "score_band" in result

    def test_has_dimension_breakdown(self):
        result = _explain_health_score(_make_input())
        assert "dimension_breakdown" in result

    def test_dimension_breakdown_has_6_items(self):
        result = _explain_health_score(_make_input())
        assert len(result["dimension_breakdown"]) == 6

    def test_has_weakest_dimensions(self):
        result = _explain_health_score(_make_input())
        assert "weakest_dimensions" in result

    def test_has_client_name(self):
        result = _explain_health_score(_make_input(client_name="Test Co"))
        assert result["client_name"] == "Test Co"

    def test_all_100_gives_expansion_ready_band(self):
        result = _explain_health_score(_make_all_100_input())
        assert result["score_band"] == "expansion_ready"

    def test_all_100_gives_overall_score_100(self):
        result = _explain_health_score(_make_all_100_input())
        assert abs(result["overall_score"] - 100.0) < 0.01

    def test_all_zero_gives_blocked_band(self):
        result = _explain_health_score(_make_all_zero_input())
        assert result["score_band"] == "blocked"

    def test_all_zero_gives_overall_score_0(self):
        result = _explain_health_score(_make_all_zero_input())
        assert result["overall_score"] == 0.0

    def test_dimension_breakdown_has_status_field(self):
        result = _explain_health_score(_make_input())
        for dim in result["dimension_breakdown"]:
            assert dim.get("status") in {"green", "amber", "red"}, (
                f"Dimension {dim.get('dimension_id')} has invalid status"
            )

    def test_high_usage_high_nps_status_green(self):
        result = _explain_health_score(
            _make_input(product_usage_score=90.0, nps_score_normalized=90.0)
        )
        breakdown = {d["dimension_id"]: d for d in result["dimension_breakdown"]}
        assert breakdown["product_usage"]["status"] == "green"
        assert breakdown["nps"]["status"] == "green"

    def test_low_usage_status_red(self):
        result = _explain_health_score(_make_input(product_usage_score=10.0))
        breakdown = {d["dimension_id"]: d for d in result["dimension_breakdown"]}
        assert breakdown["product_usage"]["status"] == "red"

    def test_weakest_dimensions_max_length_3(self):
        result = _explain_health_score(_make_all_zero_input())
        assert len(result["weakest_dimensions"]) <= 3

    def test_weakest_dimensions_are_red_only(self):
        result = _explain_health_score(_make_input())
        red_ids = {
            d["dimension_id"]
            for d in result["dimension_breakdown"]
            if d["status"] == "red"
        }
        for wk in result["weakest_dimensions"]:
            assert wk in red_ids

    def test_governance_decision_is_allow_with_review(self):
        result = _explain_health_score(_make_input())
        assert result["governance_decision"] == "ALLOW_WITH_REVIEW"

    def test_improvement_levers_count_is_5(self):
        result = _explain_health_score(_make_input())
        assert len(result["improvement_levers"]) == 5

    def test_weighted_contribution_calculation(self):
        result = _explain_health_score(_make_input(product_usage_score=80.0))
        breakdown = {d["dimension_id"]: d for d in result["dimension_breakdown"]}
        expected = 80.0 * (25 / 100)
        assert abs(breakdown["product_usage"]["weighted_contribution"] - expected) < 0.01

    def test_overall_score_weighted_average(self):
        inp = _make_input(
            product_usage_score=60.0,
            nps_score_normalized=60.0,
            support_health_score=60.0,
            engagement_score=60.0,
            expansion_signals_score=60.0,
            billing_health_score=60.0,
        )
        result = _explain_health_score(inp)
        assert abs(result["overall_score"] - 60.0) < 0.01


# ---------------------------------------------------------------------------
# Router metadata
# ---------------------------------------------------------------------------


class TestRouterMetadata:
    def test_prefix(self):
        assert router.prefix == "/api/v1/health-score-explainer"

    def test_tags_contain_analytics(self):
        assert "Analytics" in router.tags
