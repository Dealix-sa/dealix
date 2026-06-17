"""Verify company scoring produces correct scores and buckets."""
from __future__ import annotations

from os_runtime.scorer import score_company


def test_empty_dict_returns_low_score() -> None:
    result = score_company({})
    assert result["score"] <= 10, f"Empty company should score <= 10, got {result['score']}"


def test_empty_dict_bucket_is_string() -> None:
    result = score_company({})
    assert isinstance(result["bucket"], str)
    assert len(result["bucket"]) > 0


def test_all_max_values_returns_high_score() -> None:
    # maintenance_or_field_ops uses YAML boolean True (YAML parses 'yes' as True)
    full_company = {
        "operations_complexity": "high",
        "reporting_burden": "high",
        "maintenance_or_field_ops": True,
        "multi_branch_or_scale": "many",
        "operations_data_roles": "strong",
        "growth_expansion_signals": "strong",
        "reachable_decision_maker": "clear",
        "founder_background_fit": "strong",
    }
    result = score_company(full_company)
    assert result["score"] >= 70, f"Full-scoring company should score >= 70, got {result['score']}"


def test_all_max_values_bucket_is_priority() -> None:
    # maintenance_or_field_ops uses YAML boolean True (YAML parses 'yes' as True)
    full_company = {
        "operations_complexity": "high",
        "reporting_burden": "high",
        "maintenance_or_field_ops": True,
        "multi_branch_or_scale": "many",
        "operations_data_roles": "strong",
        "growth_expansion_signals": "strong",
        "reachable_decision_maker": "clear",
        "founder_background_fit": "strong",
    }
    result = score_company(full_company)
    assert result["bucket"] in {"priority_high", "priority_medium"}


def test_result_always_has_bucket_field() -> None:
    for data in [{}, {"operations_complexity": "low"}, {"reporting_burden": "high"}]:
        result = score_company(data)
        assert "bucket" in result
        assert isinstance(result["bucket"], str)


def test_result_has_dimensions_field() -> None:
    result = score_company({})
    assert "dimensions" in result
    assert isinstance(result["dimensions"], dict)


def test_result_has_recommendation_field() -> None:
    result = score_company({})
    assert "recommendation" in result
    assert isinstance(result["recommendation"], str)


def test_missing_dimension_scores_zero() -> None:
    result = score_company({})
    for dim_score in result["dimensions"].values():
        assert dim_score == 0, f"Missing dimension should score 0, got {dim_score}"


def test_partial_input_scores_correctly() -> None:
    result_partial = score_company({"operations_complexity": "high"})
    result_empty = score_company({})
    assert result_partial["score"] > result_empty["score"]


def test_score_is_numeric() -> None:
    result = score_company({"operations_complexity": "medium"})
    assert isinstance(result["score"], (int, float))


def test_disqualified_bucket_for_zero_score() -> None:
    result = score_company({})
    assert result["bucket"] == "disqualified"
