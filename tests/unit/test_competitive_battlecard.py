"""Unit tests for api/routers/competitive_battlecard.py"""
from __future__ import annotations

import pytest
from fastapi import HTTPException

from api.routers.competitive_battlecard import (
    _BATTLECARD_SECTIONS,
    _DEALIX_DIFFERENTIATORS,
    _OBJECTION_COUNTER_SCRIPTS,
    _VALID_COMPETITIVE_CONTEXTS,
    BattlecardInput,
    _build_battlecard,
    router,
)


def _make_input(**overrides) -> BattlecardInput:
    data = dict(
        competitive_context="new_logo",
        prospect_sector="technology",
        deal_value_sar=25000.0,
        known_competitor_archetype="global_saas",
    )
    data.update(overrides)
    return BattlecardInput(**data)


# ---------------------------------------------------------------------------
# Static data: battlecard sections
# ---------------------------------------------------------------------------


class TestBattlecardSections:
    def test_has_five_sections(self):
        assert len(_BATTLECARD_SECTIONS) == 5

    def test_ordered_1_to_5(self):
        orders = [s["order"] for s in _BATTLECARD_SECTIONS]
        assert orders == [1, 2, 3, 4, 5]

    def test_all_have_section_name_en(self):
        for s in _BATTLECARD_SECTIONS:
            assert s.get("section_name_en"), f"Section order {s.get('order')} missing section_name_en"

    def test_all_have_section_name_ar(self):
        for s in _BATTLECARD_SECTIONS:
            assert s.get("section_name_ar"), f"Section order {s.get('order')} missing section_name_ar"

    def test_all_have_purpose_en(self):
        for s in _BATTLECARD_SECTIONS:
            assert s.get("purpose_en"), f"Section order {s.get('order')} missing purpose_en"

    def test_all_have_purpose_ar(self):
        for s in _BATTLECARD_SECTIONS:
            assert s.get("purpose_ar"), f"Section order {s.get('order')} missing purpose_ar"

    def test_first_section_is_positioning_statement(self):
        first = next(s for s in _BATTLECARD_SECTIONS if s["order"] == 1)
        assert "positioning" in first["section_name_en"].lower() or "Positioning" in first["section_name_en"]

    def test_last_section_is_proof_points(self):
        last = next(s for s in _BATTLECARD_SECTIONS if s["order"] == 5)
        assert "proof" in last["section_name_en"].lower() or "Proof" in last["section_name_en"]


# ---------------------------------------------------------------------------
# Static data: Dealix differentiators
# ---------------------------------------------------------------------------


class TestDealixDifferentiators:
    def test_has_six_differentiators(self):
        assert len(_DEALIX_DIFFERENTIATORS) == 6

    def test_all_have_differentiator_en(self):
        for d in _DEALIX_DIFFERENTIATORS:
            assert d.get("differentiator_en"), "Differentiator missing differentiator_en"

    def test_all_have_differentiator_ar(self):
        for d in _DEALIX_DIFFERENTIATORS:
            assert d.get("differentiator_ar"), "Differentiator missing differentiator_ar"

    def test_all_have_proof_data_en(self):
        for d in _DEALIX_DIFFERENTIATORS:
            assert d.get("proof_data_en"), "Differentiator missing proof_data_en"

    def test_all_have_applicable_competitors_en(self):
        for d in _DEALIX_DIFFERENTIATORS:
            assert d.get("applicable_competitors_en"), "Differentiator missing applicable_competitors_en"

    def test_saudi_native_differentiator_present(self):
        names_en = [d["differentiator_en"].lower() for d in _DEALIX_DIFFERENTIATORS]
        assert any("saudi" in n for n in names_en)

    def test_bilingual_ux_differentiator_present(self):
        names_en = [d["differentiator_en"].lower() for d in _DEALIX_DIFFERENTIATORS]
        assert any("bilingual" in n for n in names_en)


# ---------------------------------------------------------------------------
# Static data: objection counter scripts
# ---------------------------------------------------------------------------


class TestObjectionCounterScripts:
    def test_has_five_scripts(self):
        assert len(_OBJECTION_COUNTER_SCRIPTS) == 5

    def test_all_have_objection_en(self):
        for s in _OBJECTION_COUNTER_SCRIPTS:
            assert s.get("objection_en"), "Script missing objection_en"

    def test_all_have_objection_ar(self):
        for s in _OBJECTION_COUNTER_SCRIPTS:
            assert s.get("objection_ar"), "Script missing objection_ar"

    def test_all_have_counter_en(self):
        for s in _OBJECTION_COUNTER_SCRIPTS:
            assert s.get("counter_en"), "Script missing counter_en"

    def test_all_have_counter_ar(self):
        for s in _OBJECTION_COUNTER_SCRIPTS:
            assert s.get("counter_ar"), "Script missing counter_ar"

    def test_already_have_system_objection_present(self):
        objections = [s["objection_en"].lower() for s in _OBJECTION_COUNTER_SCRIPTS]
        assert any("already have" in o or "system" in o for o in objections)

    def test_expensive_objection_present(self):
        objections = [s["objection_en"].lower() for s in _OBJECTION_COUNTER_SCRIPTS]
        assert any("expensive" in o for o in objections)


# ---------------------------------------------------------------------------
# Valid competitive contexts
# ---------------------------------------------------------------------------


class TestValidCompetitiveContexts:
    def test_has_four_contexts(self):
        assert len(_VALID_COMPETITIVE_CONTEXTS) == 4

    def test_contains_head_to_head(self):
        assert "head_to_head" in _VALID_COMPETITIVE_CONTEXTS

    def test_contains_rfp_response(self):
        assert "rfp_response" in _VALID_COMPETITIVE_CONTEXTS

    def test_contains_renewal_defense(self):
        assert "renewal_defense" in _VALID_COMPETITIVE_CONTEXTS

    def test_contains_new_logo(self):
        assert "new_logo" in _VALID_COMPETITIVE_CONTEXTS


# ---------------------------------------------------------------------------
# _build_battlecard
# ---------------------------------------------------------------------------


class TestBuildBattlecard:
    def test_returns_dict(self):
        result = _build_battlecard(_make_input())
        assert isinstance(result, dict)

    def test_has_sections(self):
        result = _build_battlecard(_make_input())
        assert "sections" in result

    def test_sections_has_five_items(self):
        result = _build_battlecard(_make_input())
        assert len(result["sections"]) == 5

    def test_has_dealix_differentiators(self):
        result = _build_battlecard(_make_input())
        assert "dealix_differentiators" in result

    def test_differentiators_has_six_items(self):
        result = _build_battlecard(_make_input())
        assert len(result["dealix_differentiators"]) == 6

    def test_has_objection_counters(self):
        result = _build_battlecard(_make_input())
        assert "objection_counters" in result

    def test_objection_counters_has_five_items(self):
        result = _build_battlecard(_make_input())
        assert len(result["objection_counters"]) == 5

    def test_has_talk_track_en(self):
        result = _build_battlecard(_make_input())
        assert result.get("talk_track_en")

    def test_has_talk_track_ar(self):
        result = _build_battlecard(_make_input())
        assert result.get("talk_track_ar")

    def test_has_competitive_context(self):
        result = _build_battlecard(_make_input(competitive_context="rfp_response"))
        assert result["competitive_context"] == "rfp_response"

    def test_governance_decision_approval_first(self):
        result = _build_battlecard(_make_input())
        assert result["governance_decision"] == "APPROVAL_FIRST"

    def test_invalid_context_raises_422(self):
        with pytest.raises(HTTPException) as exc_info:
            _build_battlecard(_make_input(competitive_context="invalid_context"))
        assert exc_info.value.status_code == 422

    @pytest.mark.parametrize(
        "context",
        ["head_to_head", "rfp_response", "renewal_defense", "new_logo"],
    )
    def test_all_valid_contexts_work(self, context):
        result = _build_battlecard(_make_input(competitive_context=context))
        assert result["governance_decision"] == "APPROVAL_FIRST"

    def test_talk_track_varies_by_context(self):
        result_new_logo = _build_battlecard(_make_input(competitive_context="new_logo"))
        result_rfp = _build_battlecard(_make_input(competitive_context="rfp_response"))
        assert result_new_logo["talk_track_en"] != result_rfp["talk_track_en"]

    def test_talk_track_ar_varies_by_context(self):
        result_head_to_head = _build_battlecard(_make_input(competitive_context="head_to_head"))
        result_renewal = _build_battlecard(_make_input(competitive_context="renewal_defense"))
        assert result_head_to_head["talk_track_ar"] != result_renewal["talk_track_ar"]


# ---------------------------------------------------------------------------
# Router metadata
# ---------------------------------------------------------------------------


class TestRouterMetadata:
    def test_prefix(self):
        assert router.prefix == "/api/v1/competitive-battlecard"

    def test_tags_contain_sales(self):
        assert "Sales" in router.tags
