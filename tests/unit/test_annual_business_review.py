"""Unit tests for api/routers/annual_business_review.py"""
from __future__ import annotations

import pytest

from api.routers.annual_business_review import (
    _ABR_BENCHMARKS,
    _ABR_SECTIONS,
    _PREPARATION_GUIDE,
    _VALID_ACCOUNT_TIERS,
    ABRGenerateInput,
    _generate_abr,
    router,
)


def _make_input(**overrides) -> ABRGenerateInput:
    data = dict(
        client_name="AlRajhi Capital",
        client_sector="banking_finance",
        account_tier="strategic",
        year=2025,
        mrr_start_sar=50_000.0,
        mrr_end_sar=65_000.0,
        nrr_pct=115.0,
        churn_rate_pct=1.5,
        data_quality_score=88.0,
        saudization_pct=55.0,
        notable_wins=["Closed ZATCA Phase 2", "5 new enterprise users"],
        challenges=["Q3 integration delay"],
    )
    data.update(overrides)
    return ABRGenerateInput(**data)


class TestABRSections:
    def test_seven_sections(self):
        assert len(_ABR_SECTIONS) == 7

    def test_sections_ordered(self):
        orders = [s["order"] for s in _ABR_SECTIONS]
        assert orders == list(range(1, 8))

    def test_all_bilingual(self):
        for s in _ABR_SECTIONS:
            assert s.get("title_en"), f"Section {s['order']} missing title_en"
            assert s.get("title_ar"), f"Section {s['order']} missing title_ar"

    def test_all_have_key_questions(self):
        for s in _ABR_SECTIONS:
            assert s.get("key_questions_en"), f"Section {s['order']} missing key_questions_en"


class TestABRBenchmarks:
    def test_world_class_nrr_is_120(self):
        assert _ABR_BENCHMARKS["world_class_nrr_pct"] == 120

    def test_saudi_median_revenue_growth_is_18(self):
        assert _ABR_BENCHMARKS["saudi_median_revenue_growth_pct"] == 18

    def test_saudization_target_is_50(self):
        assert _ABR_BENCHMARKS["vision_2030_saudization_target_pct"] == 50

    def test_acceptable_churn_is_2_5(self):
        assert _ABR_BENCHMARKS["acceptable_churn_rate_monthly_pct"] == 2.5

    def test_top_quartile_dq_is_85(self):
        assert _ABR_BENCHMARKS["top_quartile_data_quality_score"] == 85


class TestValidAccountTiers:
    def test_three_valid_tiers(self):
        assert _VALID_ACCOUNT_TIERS == {"strategic", "growth", "standard"}


class TestGenerateABR:
    def test_returns_dict(self):
        result = _generate_abr(_make_input())
        assert isinstance(result, dict)

    def test_has_client_name(self):
        result = _generate_abr(_make_input())
        assert result["client_name"] == "AlRajhi Capital"

    def test_has_seven_sections(self):
        result = _generate_abr(_make_input())
        assert len(result["sections"]) == 7

    def test_sections_bilingual(self):
        result = _generate_abr(_make_input())
        for s in result["sections"]:
            assert s.get("draft_content_en"), f"Section {s['order']} missing draft_content_en"
            assert s.get("draft_content_ar"), f"Section {s['order']} missing draft_content_ar"

    def test_expand_recommendation(self):
        result = _generate_abr(_make_input(nrr_pct=115.0, churn_rate_pct=1.5, mrr_start_sar=50_000, mrr_end_sar=55_000))
        assert result["renewal_recommendation"] == "expand"

    def test_renew_recommendation(self):
        result = _generate_abr(_make_input(nrr_pct=95.0, churn_rate_pct=2.0))
        assert result["renewal_recommendation"] == "renew"

    def test_at_risk_recommendation(self):
        result = _generate_abr(_make_input(nrr_pct=70.0, churn_rate_pct=8.0))
        assert result["renewal_recommendation"] == "at_risk"

    def test_governance_approval_first(self):
        result = _generate_abr(_make_input())
        assert result["governance_decision"] == "APPROVAL_FIRST"

    def test_computed_metrics_present(self):
        result = _generate_abr(_make_input())
        metrics = result["computed_metrics"]
        assert "mrr_growth_pct" in metrics
        assert "vs_world_class_nrr" in metrics
        assert "vs_saudi_median_revenue_growth" in metrics
        assert "vs_acceptable_churn" in metrics
        assert "vs_vision2030_saudization_target" in metrics

    def test_mrr_growth_computed_correctly(self):
        result = _generate_abr(_make_input(mrr_start_sar=100_000, mrr_end_sar=120_000))
        assert result["computed_metrics"]["mrr_growth_pct"] == pytest.approx(20.0, abs=0.1)

    def test_above_median_vs_revenue_growth(self):
        result = _generate_abr(_make_input(mrr_start_sar=100_000, mrr_end_sar=125_000))
        assert result["computed_metrics"]["vs_saudi_median_revenue_growth"] == "above_median"

    def test_below_median_vs_revenue_growth(self):
        result = _generate_abr(_make_input(mrr_start_sar=100_000, mrr_end_sar=105_000))
        assert result["computed_metrics"]["vs_saudi_median_revenue_growth"] == "below_median"

    def test_has_disclaimer(self):
        result = _generate_abr(_make_input())
        assert result.get("disclaimer_en")
        assert result.get("disclaimer_ar")

    def test_executive_highlights_not_empty(self):
        result = _generate_abr(_make_input())
        assert result.get("executive_highlights")

    def test_notable_wins_in_first_section(self):
        result = _generate_abr(_make_input(notable_wins=["Win A"]))
        first_section = result["sections"][0]
        assert "Win A" in first_section["draft_content_en"]

    def test_zero_mrr_start_handled(self):
        result = _generate_abr(_make_input(mrr_start_sar=0.0, mrr_end_sar=10_000.0))
        assert result["computed_metrics"]["mrr_growth_pct"] == 0.0


class TestPreparationGuide:
    def test_has_recommended_timing(self):
        assert "recommended_timing_en" in _PREPARATION_GUIDE

    def test_has_who_to_invite(self):
        assert "who_to_invite_en" in _PREPARATION_GUIDE
        assert len(_PREPARATION_GUIDE["who_to_invite_en"]) >= 3


class TestRouterMetadata:
    def test_prefix(self):
        assert router.prefix == "/api/v1/annual-business-review"

    def test_tags_contain_analytics(self):
        assert "Analytics" in router.tags
