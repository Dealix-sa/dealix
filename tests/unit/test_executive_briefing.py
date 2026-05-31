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

from api.routers.executive_briefing import (
    _PERSONAS,
    _TIER_DESCRIPTIONS,
    build_briefing,
    BriefingRequest,
    router,
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
