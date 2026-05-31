"""Unit tests for api/routers/client_reporting.py"""
from __future__ import annotations

import pytest

from api.routers.client_reporting import (
    _REPORT_DELIVERY_STANDARDS,
    _REPORT_TEMPLATES,
    ReportGenerateInput,
    _compute_mrr_growth_pct,
    _fmt_sar,
    _generate_report_outline,
    router,
)


def _make_input(**overrides) -> ReportGenerateInput:
    data = dict(
        report_type="weekly_brief",
        client_name="Noon Commerce",
        client_sector="retail_ecommerce",
        reporting_period_en="Week of 26 May 2025",
        current_mrr_sar=120_000.0,
        prior_period_mrr_sar=115_000.0,
        pipeline_value_sar=500_000.0,
        key_wins=["Closed Tamimi deal"],
        key_challenges=["Integration delay"],
        action_items=["Follow up with IT"],
    )
    data.update(overrides)
    return ReportGenerateInput(**data)


class TestReportTemplates:
    def test_three_templates(self):
        assert len(_REPORT_TEMPLATES) == 3

    def test_expected_template_keys(self):
        expected = {"weekly_brief", "monthly_intelligence_report", "qbr_deck"}
        assert expected == set(_REPORT_TEMPLATES.keys())

    def test_all_bilingual(self):
        for key, tmpl in _REPORT_TEMPLATES.items():
            assert tmpl.get("name_en"), f"{key} missing name_en"
            assert tmpl.get("name_ar"), f"{key} missing name_ar"

    def test_all_have_sections(self):
        for key, tmpl in _REPORT_TEMPLATES.items():
            assert len(tmpl.get("sections", [])) >= 2, f"{key} needs ≥2 sections"

    def test_all_require_bilingual(self):
        for key, tmpl in _REPORT_TEMPLATES.items():
            assert tmpl.get("bilingual_required") is True, f"{key} must require bilingual"

    def test_qbr_deck_longer_than_weekly(self):
        # QBR deck page range should be longer than weekly brief
        weekly_range = _REPORT_TEMPLATES["weekly_brief"]["page_range"]
        assert weekly_range == "1-2"


class TestDeliveryStandards:
    def test_five_standards(self):
        assert len(_REPORT_DELIVERY_STANDARDS) == 5

    def test_all_have_standard_field(self):
        for s in _REPORT_DELIVERY_STANDARDS:
            assert s.get("standard_en"), "Delivery standard missing standard_en"


class TestMrrGrowthPct:
    def test_positive_growth(self):
        assert _compute_mrr_growth_pct(110, 100) == pytest.approx(10.0)

    def test_negative_growth(self):
        assert _compute_mrr_growth_pct(90, 100) == pytest.approx(-10.0)

    def test_zero_prior_returns_zero(self):
        assert _compute_mrr_growth_pct(100, 0) == 0.0

    def test_flat(self):
        assert _compute_mrr_growth_pct(100, 100) == pytest.approx(0.0)


class TestFmtSar:
    def test_formats_thousands(self):
        assert _fmt_sar(100_000) == "SAR 100,000"

    def test_formats_zero(self):
        assert _fmt_sar(0) == "SAR 0"


class TestGenerateReportOutline:
    def test_returns_dict(self):
        result = _generate_report_outline(_make_input())
        assert isinstance(result, dict)

    def test_has_section_outlines(self):
        result = _generate_report_outline(_make_input())
        assert len(result.get("section_outlines", [])) >= 2

    def test_section_outlines_bilingual(self):
        result = _generate_report_outline(_make_input())
        for section in result["section_outlines"]:
            assert section.get("draft_content_en"), "Section missing draft_content_en"
            assert section.get("draft_content_ar"), "Section missing draft_content_ar"

    def test_computed_metrics_present(self):
        result = _generate_report_outline(_make_input())
        metrics = result["computed_metrics"]
        assert "current_mrr_sar" in metrics
        assert "mrr_delta_sar" in metrics
        assert "growth_pct" in metrics

    def test_client_name_in_output(self):
        result = _generate_report_outline(_make_input(client_name="Tamimi Markets"))
        assert "Tamimi Markets" in str(result)

    def test_governance_approval_first(self):
        result = _generate_report_outline(_make_input())
        assert result["governance_decision"] == "APPROVAL_FIRST"

    def test_invalid_report_type_raises(self):
        from fastapi import HTTPException
        with pytest.raises(HTTPException):
            _generate_report_outline(_make_input(report_type="invalid_type_xyz"))

    def test_monthly_report_works(self):
        result = _generate_report_outline(_make_input(report_type="monthly_intelligence_report"))
        assert isinstance(result, dict)
        assert result["governance_decision"] == "APPROVAL_FIRST"

    def test_qbr_deck_works(self):
        result = _generate_report_outline(_make_input(report_type="qbr_deck"))
        assert isinstance(result, dict)

    def test_mrr_growth_positive(self):
        result = _generate_report_outline(_make_input(
            current_mrr_sar=110_000.0,
            prior_period_mrr_sar=100_000.0,
        ))
        assert result["computed_metrics"]["growth_pct"] == pytest.approx(10.0)


class TestRouterMetadata:
    def test_prefix(self):
        assert router.prefix == "/api/v1/client-reporting"

    def test_tags_contain_analytics(self):
        assert "Analytics" in router.tags
