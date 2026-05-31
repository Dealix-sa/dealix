"""
Unit tests for api/routers/executive_briefing.py

Tests cover:
- Persona data: 6 personas, bilingual fields, concerns
- BriefingRequest validation
- build_briefing: structure, sections, cultural context
- All 6 personas generate valid briefings
- Tier descriptions
"""
from __future__ import annotations

import pytest

from fastapi import HTTPException

from api.routers.executive_briefing import (
    _PERSONAS,
    _TIER_DESCRIPTIONS,
    build_briefing,
    BriefingRequest,
    router,
    _BRIEFING_FORMATS,
    _EXECUTIVE_PROOF_POINTS,
    _VISION_2030_LINKAGES,
    _VALID_BRIEFING_FORMATS,
    ExecutiveBriefingInput,
    _build_executive_briefing,
)


class TestPersonaData:
    def test_six_personas(self):
        expected = {"cfo", "ceo", "cto", "cio", "coo", "chro"}
        assert expected == set(_PERSONAS.keys())

    def test_all_have_bilingual_titles(self):
        for pid, p in _PERSONAS.items():
            assert p.get("title_ar"), f"{pid} missing title_ar"
            assert p.get("title_en"), f"{pid} missing title_en"

    def test_all_have_five_plus_concerns(self):
        for pid, p in _PERSONAS.items():
            assert len(p["primary_concerns"]) >= 4, f"{pid} too few concerns"

    def test_all_have_ar_concerns(self):
        for pid, p in _PERSONAS.items():
            assert p.get("primary_concerns_ar"), f"{pid} missing primary_concerns_ar"
            assert len(p["primary_concerns_ar"]) == len(p["primary_concerns"])

    def test_cfo_mentions_roi(self):
        cfo = _PERSONAS["cfo"]
        concerns_text = " ".join(cfo["primary_concerns"]).lower()
        assert "roi" in concerns_text or "payback" in concerns_text or "cost" in concerns_text

    def test_cfo_mentions_zatca(self):
        cfo = _PERSONAS["cfo"]
        concerns_text = " ".join(cfo["primary_concerns"]).lower()
        assert "zatca" in concerns_text

    def test_cto_mentions_pdpl(self):
        cto = _PERSONAS["cto"]
        concerns_text = " ".join(cto["primary_concerns"]).lower()
        assert "pdpl" in concerns_text

    def test_chro_mentions_saudization(self):
        chro = _PERSONAS["chro"]
        concerns_text = " ".join(chro["primary_concerns"]).lower()
        assert "saudization" in concerns_text or "nitaqat" in concerns_text

    def test_all_have_proof_points(self):
        for pid, p in _PERSONAS.items():
            assert len(p.get("proof_points", [])) >= 3, f"{pid} insufficient proof points"

    def test_all_have_objection_anticipation(self):
        for pid, p in _PERSONAS.items():
            assert len(p.get("objection_anticipation", [])) >= 2, f"{pid} missing objections"


class TestTierDescriptions:
    def test_four_tiers(self):
        expected = {"sprint", "data_pack", "managed_ops", "custom_ai"}
        assert expected == set(_TIER_DESCRIPTIONS.keys())

    def test_all_have_bilingual_descriptions(self):
        for tier_id, tier in _TIER_DESCRIPTIONS.items():
            assert tier.get("en"), f"{tier_id} missing en"
            assert tier.get("ar"), f"{tier_id} missing ar"

    def test_sprint_has_price(self):
        assert "499" in _TIER_DESCRIPTIONS["sprint"]["en"]


class TestBuildBriefing:
    def _make_request(self, persona="cfo", **overrides) -> BriefingRequest:
        data = dict(
            persona=persona,
            company_name="ACME Saudi LLC",
            sector="Financial Services",
            primary_use_case="automate accounts payable reconciliation",
            estimated_roi_pct=180.0,
            estimated_payback_months=8.0,
            dealix_tier="managed_ops",
        )
        data.update(overrides)
        return BriefingRequest(**data)

    def test_briefing_has_executive_summary(self):
        result = build_briefing(self._make_request())
        assert result["executive_summary_en"]
        assert result["executive_summary_ar"]

    def test_company_name_in_summary(self):
        result = build_briefing(self._make_request(company_name="TestCo"))
        assert "TestCo" in result["executive_summary_en"]

    def test_roi_in_summary(self):
        result = build_briefing(self._make_request(estimated_roi_pct=150))
        assert "150" in result["executive_summary_en"]

    def test_briefing_has_five_sections(self):
        result = build_briefing(self._make_request())
        assert len(result["briefing_sections"]) == 5

    def test_all_sections_bilingual(self):
        result = build_briefing(self._make_request())
        for section in result["briefing_sections"]:
            assert section.get("content_en"), f"{section['section']} missing content_en"
            assert section.get("content_ar"), f"{section['section']} missing content_ar"

    def test_has_cultural_context(self):
        result = build_briefing(self._make_request())
        assert result["cultural_context_en"]
        assert result["cultural_context_ar"]

    def test_has_objection_anticipation(self):
        result = build_briefing(self._make_request())
        assert len(result["objection_anticipation"]) >= 2

    def test_has_recommended_tier(self):
        result = build_briefing(self._make_request())
        assert result["recommended_dealix_tier"]

    @pytest.mark.parametrize("persona", ["cfo", "ceo", "cto", "cio", "coo", "chro"])
    def test_all_six_personas_generate_briefings(self, persona):
        result = build_briefing(self._make_request(persona=persona))
        assert result["persona"] == persona
        assert result["executive_summary_en"]
        assert result["briefing_sections"]

    def test_persona_title_included(self):
        result = build_briefing(self._make_request(persona="cfo"))
        assert result["persona_title_en"] == _PERSONAS["cfo"]["title_en"]

    def test_primary_concerns_included(self):
        result = build_briefing(self._make_request())
        assert len(result["primary_concerns_en"]) >= 4
        assert len(result["primary_concerns_ar"]) >= 4


class TestRouterMetadata:
    def test_router_prefix(self):
        assert router.prefix == "/api/v1/executive-briefing"

    def test_router_tags(self):
        assert "Sales" in router.tags


# ===========================================================================
# Tests for extended executive briefing: formats, proof points, linkages
# ===========================================================================


def _make_briefing_input(**overrides) -> ExecutiveBriefingInput:
    data = dict(
        briefing_format="c_level_summary",
        company_name="Aramco Digital",
        key_metric_1_label_en="Process Efficiency",
        key_metric_1_value="40% reduction",
        key_metric_2_label_en="Invoice Accuracy",
        key_metric_2_value="99.5%",
        primary_outcome_en="automate accounts payable reconciliation",
        primary_outcome_ar="أتمتة تسوية الحسابات الدائنة",
        audience_title_en="Chief Financial Officer",
    )
    data.update(overrides)
    return ExecutiveBriefingInput(**data)


class TestBriefingFormats:
    def test_has_three_formats(self):
        assert len(_BRIEFING_FORMATS) == 3

    def test_has_c_level_summary(self):
        assert "c_level_summary" in _BRIEFING_FORMATS

    def test_has_board_presentation(self):
        assert "board_presentation" in _BRIEFING_FORMATS

    def test_has_investor_update(self):
        assert "investor_update" in _BRIEFING_FORMATS

    def test_all_have_name_en(self):
        for key, fmt in _BRIEFING_FORMATS.items():
            assert fmt.get("name_en"), f"{key} missing name_en"

    def test_all_have_name_ar(self):
        for key, fmt in _BRIEFING_FORMATS.items():
            assert fmt.get("name_ar"), f"{key} missing name_ar"

    def test_all_have_max_pages(self):
        for key, fmt in _BRIEFING_FORMATS.items():
            assert isinstance(fmt.get("max_pages"), int), f"{key} missing max_pages"

    def test_all_have_duration_minutes(self):
        for key, fmt in _BRIEFING_FORMATS.items():
            assert isinstance(fmt.get("duration_minutes"), int), f"{key} missing duration_minutes"

    def test_c_level_summary_max_pages(self):
        assert _BRIEFING_FORMATS["c_level_summary"]["max_pages"] == 2

    def test_c_level_summary_duration(self):
        assert _BRIEFING_FORMATS["c_level_summary"]["duration_minutes"] == 15

    def test_board_presentation_max_pages(self):
        assert _BRIEFING_FORMATS["board_presentation"]["max_pages"] == 8

    def test_board_presentation_duration(self):
        assert _BRIEFING_FORMATS["board_presentation"]["duration_minutes"] == 45

    def test_investor_update_max_pages(self):
        assert _BRIEFING_FORMATS["investor_update"]["max_pages"] == 5

    def test_investor_update_duration(self):
        assert _BRIEFING_FORMATS["investor_update"]["duration_minutes"] == 30

    def test_all_have_key_sections_en(self):
        for key, fmt in _BRIEFING_FORMATS.items():
            assert len(fmt.get("key_sections_en", [])) >= 3, f"{key} needs at least 3 key_sections_en"

    def test_all_have_key_sections_ar(self):
        for key, fmt in _BRIEFING_FORMATS.items():
            sections_en = fmt.get("key_sections_en", [])
            sections_ar = fmt.get("key_sections_ar", [])
            assert len(sections_ar) == len(sections_en), f"{key} sections_ar length mismatch"


class TestExecutiveProofPoints:
    def test_has_five_proof_points(self):
        assert len(_EXECUTIVE_PROOF_POINTS) == 5

    def test_all_have_proof_en(self):
        for pp in _EXECUTIVE_PROOF_POINTS:
            assert pp.get("proof_en"), "Proof point missing proof_en"

    def test_all_have_proof_ar(self):
        for pp in _EXECUTIVE_PROOF_POINTS:
            assert pp.get("proof_ar"), "Proof point missing proof_ar"

    def test_all_have_metric_type(self):
        for pp in _EXECUTIVE_PROOF_POINTS:
            assert pp.get("metric_type"), "Proof point missing metric_type"

    def test_metric_types_are_valid(self):
        valid_types = {"efficiency", "revenue", "compliance", "growth", "quality"}
        for pp in _EXECUTIVE_PROOF_POINTS:
            assert pp["metric_type"] in valid_types, f"Invalid metric_type: {pp['metric_type']}"


class TestVision2030Linkages:
    def test_has_four_linkages(self):
        assert len(_VISION_2030_LINKAGES) == 4

    def test_all_have_initiative_en(self):
        for lnk in _VISION_2030_LINKAGES:
            assert lnk.get("initiative_en"), "Linkage missing initiative_en"

    def test_all_have_initiative_ar(self):
        for lnk in _VISION_2030_LINKAGES:
            assert lnk.get("initiative_ar"), "Linkage missing initiative_ar"

    def test_all_have_dealix_contribution_en(self):
        for lnk in _VISION_2030_LINKAGES:
            assert lnk.get("dealix_contribution_en"), "Linkage missing dealix_contribution_en"

    def test_all_have_dealix_contribution_ar(self):
        for lnk in _VISION_2030_LINKAGES:
            assert lnk.get("dealix_contribution_ar"), "Linkage missing dealix_contribution_ar"

    def test_neom_linkage_present(self):
        initiatives = [lnk["initiative_en"] for lnk in _VISION_2030_LINKAGES]
        assert any("NEOM" in i for i in initiatives)

    def test_zatca_linkage_present(self):
        initiatives = [lnk["initiative_en"] for lnk in _VISION_2030_LINKAGES]
        assert any("ZATCA" in i for i in initiatives)


class TestBuildExecutiveBriefing:
    def test_returns_dict(self):
        result = _build_executive_briefing(_make_briefing_input())
        assert isinstance(result, dict)

    def test_has_company_name(self):
        result = _build_executive_briefing(_make_briefing_input(company_name="SABIC"))
        assert result["company_name"] == "SABIC"

    def test_has_briefing_format(self):
        result = _build_executive_briefing(_make_briefing_input())
        assert "briefing_format" in result

    def test_has_format_meta(self):
        result = _build_executive_briefing(_make_briefing_input())
        assert "format_meta" in result
        meta = result["format_meta"]
        assert "name_en" in meta
        assert "name_ar" in meta
        assert "max_pages" in meta
        assert "duration_minutes" in meta

    def test_has_sections(self):
        result = _build_executive_briefing(_make_briefing_input())
        assert "sections" in result

    def test_sections_count_matches_format(self):
        result = _build_executive_briefing(_make_briefing_input(briefing_format="c_level_summary"))
        assert len(result["sections"]) == len(_BRIEFING_FORMATS["c_level_summary"]["key_sections_en"])

    def test_each_section_has_summary_hook_en_with_company_name(self):
        result = _build_executive_briefing(_make_briefing_input(company_name="TestCo Ltd"))
        for section in result["sections"]:
            assert "TestCo Ltd" in section["summary_hook_en"]

    def test_each_section_has_summary_hook_ar(self):
        result = _build_executive_briefing(_make_briefing_input())
        for section in result["sections"]:
            assert section.get("summary_hook_ar")

    def test_has_proof_points_five(self):
        result = _build_executive_briefing(_make_briefing_input())
        assert len(result["proof_points"]) == 5

    def test_has_vision_2030_linkages_four(self):
        result = _build_executive_briefing(_make_briefing_input())
        assert len(result["vision_2030_linkages"]) == 4

    def test_has_custom_metrics_two(self):
        result = _build_executive_briefing(_make_briefing_input())
        assert len(result["custom_metrics"]) == 2

    def test_custom_metrics_include_labels(self):
        result = _build_executive_briefing(_make_briefing_input(
            key_metric_1_label_en="Cost Savings",
            key_metric_1_value="30%",
            key_metric_2_label_en="Time Saved",
            key_metric_2_value="2 hours/day",
        ))
        assert result["custom_metrics"][0]["label_en"] == "Cost Savings"
        assert result["custom_metrics"][1]["label_en"] == "Time Saved"

    def test_governance_decision_approval_first(self):
        result = _build_executive_briefing(_make_briefing_input())
        assert result["governance_decision"] == "APPROVAL_FIRST"

    def test_has_disclaimer_en(self):
        result = _build_executive_briefing(_make_briefing_input())
        assert result.get("disclaimer_en")

    def test_has_disclaimer_ar(self):
        result = _build_executive_briefing(_make_briefing_input())
        assert result.get("disclaimer_ar")

    def test_invalid_briefing_format_raises_http_422(self):
        with pytest.raises(HTTPException) as exc_info:
            _build_executive_briefing(_make_briefing_input(briefing_format="quarterly_report"))
        assert exc_info.value.status_code == 422

    @pytest.mark.parametrize("fmt", ["c_level_summary", "board_presentation", "investor_update"])
    def test_all_three_valid_formats_work(self, fmt):
        result = _build_executive_briefing(_make_briefing_input(briefing_format=fmt))
        assert result["briefing_format"] == fmt
        assert result["sections"]

    def test_valid_briefing_formats_set(self):
        assert _VALID_BRIEFING_FORMATS == {"c_level_summary", "board_presentation", "investor_update"}
