"""Unit tests for api/routers/proof_pack.py"""
from __future__ import annotations

import pytest

from api.routers.proof_pack import (
    _PROOF_CATEGORIES,
    _PROOF_PACK_SECTIONS,
    _PROOF_QUALITY_CHECKLIST,
    _VALID_ENGAGEMENT_TYPES,
    ProofPackInput,
    _build_proof_pack,
    _compute_metric_deltas,
    _nps_label,
    _top_improvements,
    router,
)


def _make_input(**overrides) -> ProofPackInput:
    data = dict(
        client_name="Almarai Group",
        client_sector="food_beverage",
        engagement_type="sprint",
        engagement_start_date="2025-01-15",
        baseline_metrics={
            "reporting_hours_per_week": 20.0,
            "data_errors_per_month": 50.0,
        },
        current_metrics={
            "reporting_hours_per_week": 8.0,
            "data_errors_per_month": 10.0,
        },
        champion_name="Fatima Al-Zahrani",
        champion_title="Head of Data",
        nps_score=9.0,
        testimonial_quote="Dealix transformed our reporting.",
    )
    data.update(overrides)
    return ProofPackInput(**data)


class TestProofCategories:
    def test_five_categories(self):
        assert len(_PROOF_CATEGORIES) == 5

    def test_all_bilingual(self):
        for key, cat in _PROOF_CATEGORIES.items():
            assert cat.get("name_en"), f"{key} missing name_en"
            assert cat.get("name_ar"), f"{key} missing name_ar"

    def test_all_have_template(self):
        for key, cat in _PROOF_CATEGORIES.items():
            assert cat.get("template_en"), f"{key} missing template_en"

    def test_all_have_strength_rating(self):
        for key, cat in _PROOF_CATEGORIES.items():
            assert cat.get("strength_rating"), f"{key} missing strength_rating"


class TestProofPackSections:
    def test_five_sections(self):
        assert len(_PROOF_PACK_SECTIONS) == 5

    def test_all_have_titles(self):
        for s in _PROOF_PACK_SECTIONS:
            assert s.get("title_en"), "Section missing title_en"
            assert s.get("title_ar"), "Section missing title_ar"


class TestProofQualityChecklist:
    def test_seven_items(self):
        assert len(_PROOF_QUALITY_CHECKLIST) == 7


class TestValidEngagementTypes:
    def test_four_types(self):
        assert _VALID_ENGAGEMENT_TYPES == {"sprint", "data_pack", "managed_ops", "custom_ai"}


class TestComputeMetricDeltas:
    def test_basic_delta(self):
        deltas = _compute_metric_deltas({"hours": 20.0}, {"hours": 8.0})
        assert len(deltas) == 1
        d = deltas[0]
        assert d["metric"] == "hours"
        assert d["before"] == 20.0
        assert d["after"] == 8.0
        assert d["delta"] == pytest.approx(-12.0)
        assert d["pct_change"] == pytest.approx(-60.0)

    def test_missing_metric_skipped(self):
        deltas = _compute_metric_deltas(
            {"a": 10.0, "b": 20.0},
            {"a": 8.0},  # b not in current
        )
        metrics = [d["metric"] for d in deltas]
        assert "b" not in metrics
        assert "a" in metrics

    def test_zero_baseline_handled(self):
        deltas = _compute_metric_deltas({"x": 0.0}, {"x": 5.0})
        assert deltas[0]["pct_change"] == 100.0

    def test_zero_zero_handled(self):
        deltas = _compute_metric_deltas({"x": 0.0}, {"x": 0.0})
        assert deltas[0]["pct_change"] == 0.0


class TestTopImprovements:
    def test_returns_top_two(self):
        deltas = [
            {"metric": "a", "pct_change": -20.0},
            {"metric": "b", "pct_change": -60.0},
            {"metric": "c", "pct_change": -10.0},
        ]
        top = _top_improvements(deltas, n=2)
        assert len(top) == 2
        assert top[0]["metric"] == "b"

    def test_respects_n(self):
        deltas = [{"metric": str(i), "pct_change": float(i)} for i in range(5)]
        assert len(_top_improvements(deltas, n=3)) == 3


class TestNpsLabel:
    def test_promoter_at_9(self):
        assert _nps_label(9.0) == "Promoter"

    def test_promoter_at_10(self):
        assert _nps_label(10.0) == "Promoter"

    def test_passive_at_7(self):
        assert _nps_label(7.0) == "Passive"

    def test_detractor_at_6(self):
        assert _nps_label(6.0) == "Detractor"

    def test_detractor_at_0(self):
        assert _nps_label(0.0) == "Detractor"


class TestBuildProofPack:
    def test_returns_dict(self):
        result = _build_proof_pack(_make_input())
        assert isinstance(result, dict)

    def test_has_five_sections(self):
        result = _build_proof_pack(_make_input())
        assert len(result.get("sections", [])) == 5

    def test_governance_approval_first(self):
        result = _build_proof_pack(_make_input())
        assert result["governance_decision"] == "APPROVAL_FIRST"

    def test_has_client_name(self):
        result = _build_proof_pack(_make_input())
        assert result["client_name"] == "Almarai Group"

    def test_metric_deltas_computed(self):
        result = _build_proof_pack(_make_input())
        results_section = result["sections"][2]  # Section 3 = results after Dealix
        assert results_section.get("metric_deltas") is not None
        assert len(results_section["metric_deltas"]) == 2

    def test_top_improvements_in_result(self):
        result = _build_proof_pack(_make_input())
        assert result.get("top_improvements") is not None

    def test_has_nps_label(self):
        result = _build_proof_pack(_make_input(nps_score=9.0))
        testimonial_section = result["sections"][3]  # Section 4 = testimonial
        assert testimonial_section.get("nps_label") == "Promoter"

    def test_detractor_nps(self):
        result = _build_proof_pack(_make_input(nps_score=5.0))
        testimonial_section = result["sections"][3]
        assert testimonial_section.get("nps_label") == "Detractor"

    def test_invalid_engagement_type_raises(self):
        from fastapi import HTTPException
        with pytest.raises(HTTPException):
            _build_proof_pack(_make_input(engagement_type="invalid_type"))

    def test_all_valid_engagement_types_work(self):
        for etype in _VALID_ENGAGEMENT_TYPES:
            result = _build_proof_pack(_make_input(engagement_type=etype))
            assert isinstance(result, dict)

    def test_has_bilingual_disclaimer(self):
        result = _build_proof_pack(_make_input())
        assert result.get("disclaimer_en")
        assert result.get("disclaimer_ar")

    def test_sections_bilingual(self):
        result = _build_proof_pack(_make_input())
        for s in result["sections"]:
            assert s.get("title_en"), f"Section missing title_en: {s}"
            assert s.get("title_ar"), f"Section missing title_ar: {s}"

    def test_empty_metrics_handled(self):
        result = _build_proof_pack(_make_input(baseline_metrics={}, current_metrics={}))
        results_section = result["sections"][2]
        assert results_section.get("metric_deltas") == []


class TestRouterMetadata:
    def test_prefix(self):
        assert router.prefix == "/api/v1/proof-pack"

    def test_tags_contain_sales(self):
        assert "Sales" in router.tags
