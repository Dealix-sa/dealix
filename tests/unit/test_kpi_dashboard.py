"""Unit tests for the /api/v1/kpi-dashboard router in api/routers/kpi_dashboard.py"""
from __future__ import annotations

import pytest

from api.routers.kpi_dashboard import (
    _KPI_DEFINITIONS,
    _DASHBOARD_VIEWS,
    _SAUDI_KPI_BENCHMARKS,
    KPISnapshotInput,
    _build_kpi_snapshot,
    router_v2 as router,
)


def _make_snapshot(**overrides) -> KPISnapshotInput:
    data = dict(
        company_name="Gulf Tech Solutions",
        period_label_en="Q1 2026",
        mrr_growth_pct=15.0,
        nrr_pct=110.0,
        churn_rate_pct=2.5,
        data_quality_score=75.0,
        pipeline_velocity_days=40.0,
        customer_health_score=72.0,
        saudization_pct=60.0,
        zatca_compliance_pct=90.0,
    )
    data.update(overrides)
    return KPISnapshotInput(**data)


def _make_high_performance_snapshot() -> KPISnapshotInput:
    """Input values that should produce grade A (>= 6 above median)."""
    return _make_snapshot(
        mrr_growth_pct=25.0,       # median=8  → above (up_is_good)
        nrr_pct=130.0,             # median=100 → above (up_is_good)
        churn_rate_pct=0.5,        # median=4   → above (down_is_good, lower is better)
        data_quality_score=85.0,   # median=65  → above (up_is_good)
        pipeline_velocity_days=20.0,  # median=55  → above (down_is_good)
        customer_health_score=80.0,   # median=68  → above (up_is_good)
        saudization_pct=70.0,         # median=55  → above (up_is_good)
        zatca_compliance_pct=95.0,    # median=85  → above (up_is_good)
    )


def _make_poor_performance_snapshot() -> KPISnapshotInput:
    """Input values that should produce grade D (< 2 above median)."""
    return _make_snapshot(
        mrr_growth_pct=2.0,        # median=8  → below
        nrr_pct=85.0,              # median=100 → below
        churn_rate_pct=8.0,        # median=4   → below (higher churn = worse)
        data_quality_score=40.0,   # median=65  → below
        pipeline_velocity_days=80.0,  # median=55  → below (higher days = worse)
        customer_health_score=50.0,   # median=68  → below
        saudization_pct=30.0,         # median=55  → below
        zatca_compliance_pct=60.0,    # median=85  → below
    )


# ---------------------------------------------------------------------------
# Static data: KPI definitions
# ---------------------------------------------------------------------------


class TestKPIDefinitions:
    def test_has_eight_definitions(self):
        assert len(_KPI_DEFINITIONS) == 8

    def test_all_have_kpi_id(self):
        for kpi_id, defn in _KPI_DEFINITIONS.items():
            assert defn.get("kpi_id") == kpi_id

    def test_all_have_name_en(self):
        for kpi_id, defn in _KPI_DEFINITIONS.items():
            assert defn.get("name_en"), f"{kpi_id} missing name_en"

    def test_all_have_name_ar(self):
        for kpi_id, defn in _KPI_DEFINITIONS.items():
            assert defn.get("name_ar"), f"{kpi_id} missing name_ar"

    def test_all_have_description_en(self):
        for kpi_id, defn in _KPI_DEFINITIONS.items():
            assert defn.get("description_en"), f"{kpi_id} missing description_en"

    def test_all_have_unit(self):
        valid_units = {"%", "SAR", "count", "days", "score"}
        for kpi_id, defn in _KPI_DEFINITIONS.items():
            assert defn.get("unit") in valid_units, f"{kpi_id} has invalid unit: {defn.get('unit')}"

    def test_all_have_direction(self):
        valid_directions = {"up_is_good", "down_is_good"}
        for kpi_id, defn in _KPI_DEFINITIONS.items():
            assert defn.get("direction") in valid_directions

    def test_all_have_target_source_en(self):
        for kpi_id, defn in _KPI_DEFINITIONS.items():
            assert defn.get("target_source_en"), f"{kpi_id} missing target_source_en"

    def test_expected_kpi_ids_present(self):
        expected = {
            "mrr_growth", "nrr", "churn_rate", "data_quality_score",
            "pipeline_velocity_days", "customer_health_score",
            "saudization_pct", "zatca_compliance_pct",
        }
        assert expected == set(_KPI_DEFINITIONS.keys())

    def test_churn_rate_is_down_is_good(self):
        assert _KPI_DEFINITIONS["churn_rate"]["direction"] == "down_is_good"

    def test_pipeline_velocity_is_down_is_good(self):
        assert _KPI_DEFINITIONS["pipeline_velocity_days"]["direction"] == "down_is_good"

    def test_nrr_is_up_is_good(self):
        assert _KPI_DEFINITIONS["nrr"]["direction"] == "up_is_good"


# ---------------------------------------------------------------------------
# Static data: dashboard views
# ---------------------------------------------------------------------------


class TestDashboardViews:
    def test_has_three_views(self):
        assert len(_DASHBOARD_VIEWS) == 3

    def test_view_ids(self):
        ids = {v["view_id"] for v in _DASHBOARD_VIEWS}
        assert ids == {"executive", "operations", "customer_success"}

    def test_all_have_name_en(self):
        for v in _DASHBOARD_VIEWS:
            assert v.get("name_en"), f"View {v.get('view_id')} missing name_en"

    def test_all_have_name_ar(self):
        for v in _DASHBOARD_VIEWS:
            assert v.get("name_ar"), f"View {v.get('view_id')} missing name_ar"

    def test_all_have_kpi_ids_list(self):
        for v in _DASHBOARD_VIEWS:
            assert isinstance(v.get("kpi_ids"), list)
            assert len(v["kpi_ids"]) > 0

    def test_all_have_audience_en(self):
        for v in _DASHBOARD_VIEWS:
            assert v.get("audience_en"), f"View {v.get('view_id')} missing audience_en"

    def test_all_have_audience_ar(self):
        for v in _DASHBOARD_VIEWS:
            assert v.get("audience_ar"), f"View {v.get('view_id')} missing audience_ar"

    def test_executive_view_kpi_ids(self):
        view = next(v for v in _DASHBOARD_VIEWS if v["view_id"] == "executive")
        assert "mrr_growth" in view["kpi_ids"]
        assert "nrr" in view["kpi_ids"]
        assert "churn_rate" in view["kpi_ids"]
        assert "saudization_pct" in view["kpi_ids"]

    def test_operations_view_kpi_ids(self):
        view = next(v for v in _DASHBOARD_VIEWS if v["view_id"] == "operations")
        assert "data_quality_score" in view["kpi_ids"]
        assert "pipeline_velocity_days" in view["kpi_ids"]
        assert "zatca_compliance_pct" in view["kpi_ids"]

    def test_customer_success_view_kpi_ids(self):
        view = next(v for v in _DASHBOARD_VIEWS if v["view_id"] == "customer_success")
        assert "customer_health_score" in view["kpi_ids"]
        assert "nrr" in view["kpi_ids"]

    def test_all_view_kpi_ids_are_valid(self):
        valid_kpi_ids = set(_KPI_DEFINITIONS.keys())
        for v in _DASHBOARD_VIEWS:
            for kpi_id in v["kpi_ids"]:
                assert kpi_id in valid_kpi_ids, f"Unknown kpi_id '{kpi_id}' in view '{v['view_id']}'"


# ---------------------------------------------------------------------------
# Static data: Saudi KPI benchmarks
# ---------------------------------------------------------------------------


class TestSaudiKPIBenchmarks:
    def test_has_eight_keys(self):
        assert len(_SAUDI_KPI_BENCHMARKS) == 8

    def test_keys_match_kpi_definitions(self):
        assert set(_SAUDI_KPI_BENCHMARKS.keys()) == set(_KPI_DEFINITIONS.keys())

    def test_all_have_world_class(self):
        for kpi_id, b in _SAUDI_KPI_BENCHMARKS.items():
            assert "world_class" in b, f"{kpi_id} missing world_class"

    def test_all_have_saudi_median(self):
        for kpi_id, b in _SAUDI_KPI_BENCHMARKS.items():
            assert "saudi_median" in b, f"{kpi_id} missing saudi_median"

    def test_all_have_unit(self):
        for kpi_id, b in _SAUDI_KPI_BENCHMARKS.items():
            assert "unit" in b, f"{kpi_id} missing unit"


# ---------------------------------------------------------------------------
# _build_kpi_snapshot
# ---------------------------------------------------------------------------


class TestBuildKPISnapshot:
    def test_returns_dict(self):
        result = _build_kpi_snapshot(_make_snapshot())
        assert isinstance(result, dict)

    def test_has_company_name(self):
        result = _build_kpi_snapshot(_make_snapshot(company_name="Aramco Digital"))
        assert result["company_name"] == "Aramco Digital"

    def test_has_period_label_en(self):
        result = _build_kpi_snapshot(_make_snapshot(period_label_en="Q2 2026"))
        assert result["period_label_en"] == "Q2 2026"

    def test_kpi_scores_count_eight(self):
        result = _build_kpi_snapshot(_make_snapshot())
        assert len(result["kpi_scores"]) == 8

    def test_kpi_scores_each_have_kpi_id(self):
        result = _build_kpi_snapshot(_make_snapshot())
        for score in result["kpi_scores"]:
            assert "kpi_id" in score

    def test_kpi_scores_each_have_value(self):
        result = _build_kpi_snapshot(_make_snapshot())
        for score in result["kpi_scores"]:
            assert "value" in score

    def test_kpi_scores_each_have_vs_benchmark(self):
        result = _build_kpi_snapshot(_make_snapshot())
        for score in result["kpi_scores"]:
            assert score.get("vs_benchmark") in {"above_median", "at_median", "below_median"}

    def test_kpi_scores_each_have_unit(self):
        result = _build_kpi_snapshot(_make_snapshot())
        for score in result["kpi_scores"]:
            assert "unit" in score

    def test_has_top_performers(self):
        result = _build_kpi_snapshot(_make_snapshot())
        assert "top_performers" in result
        assert isinstance(result["top_performers"], list)

    def test_top_performers_max_three(self):
        result = _build_kpi_snapshot(_make_snapshot())
        assert len(result["top_performers"]) <= 3

    def test_has_needs_attention(self):
        result = _build_kpi_snapshot(_make_snapshot())
        assert "needs_attention" in result
        assert isinstance(result["needs_attention"], list)

    def test_needs_attention_max_three(self):
        result = _build_kpi_snapshot(_make_snapshot())
        assert len(result["needs_attention"]) <= 3

    def test_has_overall_grade(self):
        result = _build_kpi_snapshot(_make_snapshot())
        assert result.get("overall_grade") in {"A", "B", "C", "D"}

    def test_high_performance_grade_a(self):
        result = _build_kpi_snapshot(_make_high_performance_snapshot())
        assert result["overall_grade"] == "A"

    def test_poor_performance_grade_d(self):
        result = _build_kpi_snapshot(_make_poor_performance_snapshot())
        assert result["overall_grade"] == "D"

    def test_governance_decision_allow_with_review(self):
        result = _build_kpi_snapshot(_make_snapshot())
        assert result["governance_decision"] == "ALLOW_WITH_REVIEW"

    def test_has_disclaimer_en(self):
        result = _build_kpi_snapshot(_make_snapshot())
        assert result.get("disclaimer_en")

    def test_has_disclaimer_ar(self):
        result = _build_kpi_snapshot(_make_snapshot())
        assert result.get("disclaimer_ar")

    def test_above_median_up_is_good(self):
        # mrr_growth median=8; 25 > 8 => above_median
        result = _build_kpi_snapshot(_make_snapshot(mrr_growth_pct=25.0))
        mrr_score = next(s for s in result["kpi_scores"] if s["kpi_id"] == "mrr_growth")
        assert mrr_score["vs_benchmark"] == "above_median"

    def test_below_median_up_is_good(self):
        # mrr_growth median=8; 2 < 8 => below_median
        result = _build_kpi_snapshot(_make_snapshot(mrr_growth_pct=2.0))
        mrr_score = next(s for s in result["kpi_scores"] if s["kpi_id"] == "mrr_growth")
        assert mrr_score["vs_benchmark"] == "below_median"

    def test_above_median_down_is_good(self):
        # churn_rate median=4; 1.0 < 4 => above_median (lower is better)
        result = _build_kpi_snapshot(_make_snapshot(churn_rate_pct=1.0))
        churn_score = next(s for s in result["kpi_scores"] if s["kpi_id"] == "churn_rate")
        assert churn_score["vs_benchmark"] == "above_median"

    def test_below_median_down_is_good(self):
        # churn_rate median=4; 7.0 > 4 => below_median
        result = _build_kpi_snapshot(_make_snapshot(churn_rate_pct=7.0))
        churn_score = next(s for s in result["kpi_scores"] if s["kpi_id"] == "churn_rate")
        assert churn_score["vs_benchmark"] == "below_median"


# ---------------------------------------------------------------------------
# Router metadata
# ---------------------------------------------------------------------------


class TestRouterMetadata:
    def test_prefix(self):
        assert router.prefix == "/api/v1/kpi-dashboard"

    def test_tags_contain_analytics(self):
        assert "Analytics" in router.tags
