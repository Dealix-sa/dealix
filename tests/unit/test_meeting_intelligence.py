"""Unit tests for api/routers/meeting_intelligence.py"""
from __future__ import annotations

import pytest
from fastapi import HTTPException

from api.routers.meeting_intelligence import (
    _MEETING_TYPES,
    _SAUDI_MEETING_ETIQUETTE,
    _MEETING_OUTCOME_TEMPLATES,
    _VALID_MEETING_TYPES,
    MeetingBriefInput,
    _build_meeting_brief,
    router,
)


def _make_input(**overrides) -> MeetingBriefInput:
    data = dict(
        meeting_type="discovery",
        prospect_company="Al-Falah Trading",
        prospect_name="Khalid Al-Shammari",
        prospect_title="Operations Director",
        known_pain_points=["manual monthly reporting"],
        is_first_meeting=True,
        arabic_primary=False,
    )
    data.update(overrides)
    return MeetingBriefInput(**data)


# ---------------------------------------------------------------------------
# Static data: _MEETING_TYPES
# ---------------------------------------------------------------------------


class TestMeetingTypes:
    def test_has_four_keys(self):
        assert len(_MEETING_TYPES) == 4

    def test_contains_discovery(self):
        assert "discovery" in _MEETING_TYPES

    def test_contains_demo(self):
        assert "demo" in _MEETING_TYPES

    def test_contains_proposal_review(self):
        assert "proposal_review" in _MEETING_TYPES

    def test_contains_qbr(self):
        assert "qbr" in _MEETING_TYPES

    def test_all_have_name_en(self):
        for key, mt in _MEETING_TYPES.items():
            assert mt.get("name_en"), f"{key} missing name_en"

    def test_all_have_name_ar(self):
        for key, mt in _MEETING_TYPES.items():
            assert mt.get("name_ar"), f"{key} missing name_ar"

    def test_all_have_duration_minutes_int(self):
        for key, mt in _MEETING_TYPES.items():
            assert isinstance(mt.get("duration_minutes"), int), f"{key} duration_minutes not int"

    def test_all_have_four_agenda_items_en(self):
        for key, mt in _MEETING_TYPES.items():
            assert isinstance(mt.get("agenda_items_en"), list), f"{key} missing agenda_items_en"
            assert len(mt["agenda_items_en"]) == 4, f"{key} agenda_items_en length != 4"

    def test_all_have_four_agenda_items_ar(self):
        for key, mt in _MEETING_TYPES.items():
            assert isinstance(mt.get("agenda_items_ar"), list), f"{key} missing agenda_items_ar"
            assert len(mt["agenda_items_ar"]) == 4, f"{key} agenda_items_ar length != 4"

    def test_all_have_success_criteria_en(self):
        for key, mt in _MEETING_TYPES.items():
            assert mt.get("success_criteria_en"), f"{key} missing success_criteria_en"

    def test_all_have_success_criteria_ar(self):
        for key, mt in _MEETING_TYPES.items():
            assert mt.get("success_criteria_ar"), f"{key} missing success_criteria_ar"


# ---------------------------------------------------------------------------
# Static data: _SAUDI_MEETING_ETIQUETTE
# ---------------------------------------------------------------------------


class TestSaudiMeetingEtiquette:
    def test_has_six_rules(self):
        assert len(_SAUDI_MEETING_ETIQUETTE) == 6

    def test_all_have_rule_en(self):
        for i, rule in enumerate(_SAUDI_MEETING_ETIQUETTE):
            assert rule.get("rule_en"), f"rule {i} missing rule_en"

    def test_all_have_rule_ar(self):
        for i, rule in enumerate(_SAUDI_MEETING_ETIQUETTE):
            assert rule.get("rule_ar"), f"rule {i} missing rule_ar"

    def test_all_have_applies_to(self):
        for i, rule in enumerate(_SAUDI_MEETING_ETIQUETTE):
            assert rule.get("applies_to"), f"rule {i} missing applies_to"

    def test_applies_to_values_are_valid(self):
        valid = {"all", "formal", "initial"}
        for rule in _SAUDI_MEETING_ETIQUETTE:
            assert rule["applies_to"] in valid, f"applies_to '{rule['applies_to']}' not in {valid}"


# ---------------------------------------------------------------------------
# Static data: _MEETING_OUTCOME_TEMPLATES
# ---------------------------------------------------------------------------


class TestMeetingOutcomeTemplates:
    def test_has_three_keys(self):
        assert len(_MEETING_OUTCOME_TEMPLATES) == 3

    def test_contains_positive(self):
        assert "positive" in _MEETING_OUTCOME_TEMPLATES

    def test_contains_neutral(self):
        assert "neutral" in _MEETING_OUTCOME_TEMPLATES

    def test_contains_needs_follow_up(self):
        assert "needs_follow_up" in _MEETING_OUTCOME_TEMPLATES

    def test_all_have_label_en(self):
        for key, tpl in _MEETING_OUTCOME_TEMPLATES.items():
            assert tpl.get("label_en"), f"{key} missing label_en"

    def test_all_have_label_ar(self):
        for key, tpl in _MEETING_OUTCOME_TEMPLATES.items():
            assert tpl.get("label_ar"), f"{key} missing label_ar"

    def test_all_have_next_step_en(self):
        for key, tpl in _MEETING_OUTCOME_TEMPLATES.items():
            assert tpl.get("next_step_en"), f"{key} missing next_step_en"

    def test_all_have_next_step_ar(self):
        for key, tpl in _MEETING_OUTCOME_TEMPLATES.items():
            assert tpl.get("next_step_ar"), f"{key} missing next_step_ar"


# ---------------------------------------------------------------------------
# _build_meeting_brief
# ---------------------------------------------------------------------------


class TestBuildMeetingBrief:
    def test_returns_dict(self):
        result = _build_meeting_brief(_make_input())
        assert isinstance(result, dict)

    def test_has_meeting_type(self):
        result = _build_meeting_brief(_make_input())
        assert "meeting_type" in result

    def test_has_agenda_items_en_with_four_items(self):
        result = _build_meeting_brief(_make_input())
        assert isinstance(result.get("agenda_items_en"), list)
        assert len(result["agenda_items_en"]) == 4

    def test_has_agenda_items_ar_with_four_items(self):
        result = _build_meeting_brief(_make_input())
        assert isinstance(result.get("agenda_items_ar"), list)
        assert len(result["agenda_items_ar"]) == 4

    def test_has_etiquette_rules_with_six_items(self):
        result = _build_meeting_brief(_make_input())
        assert isinstance(result.get("etiquette_rules"), list)
        assert len(result["etiquette_rules"]) == 6

    def test_has_opening_hook_en(self):
        result = _build_meeting_brief(_make_input())
        assert result.get("opening_hook_en")

    def test_has_opening_hook_ar(self):
        result = _build_meeting_brief(_make_input())
        assert result.get("opening_hook_ar")

    def test_opening_hook_en_contains_prospect_name(self):
        result = _build_meeting_brief(_make_input(prospect_name="Nora Al-Zahrani"))
        assert "Nora Al-Zahrani" in result["opening_hook_en"]

    def test_opening_hook_en_contains_prospect_company(self):
        result = _build_meeting_brief(_make_input(prospect_company="Gulf Motors"))
        assert "Gulf Motors" in result["opening_hook_en"]

    def test_opening_hook_en_contains_first_pain_point(self):
        result = _build_meeting_brief(_make_input(known_pain_points=["slow approvals"]))
        assert "slow approvals" in result["opening_hook_en"]

    def test_opening_hook_en_generic_when_no_pain_points(self):
        result = _build_meeting_brief(_make_input(known_pain_points=[]))
        assert result.get("opening_hook_en")

    def test_has_success_criteria_en(self):
        result = _build_meeting_brief(_make_input())
        assert result.get("success_criteria_en")

    def test_has_success_criteria_ar(self):
        result = _build_meeting_brief(_make_input())
        assert result.get("success_criteria_ar")

    def test_has_duration_minutes(self):
        result = _build_meeting_brief(_make_input())
        assert "duration_minutes" in result

    def test_meeting_type_in_result(self):
        result = _build_meeting_brief(_make_input(meeting_type="demo"))
        assert result["meeting_type"] == "demo"

    def test_invalid_meeting_type_raises_http_422(self):
        with pytest.raises(HTTPException) as exc_info:
            _build_meeting_brief(_make_input(meeting_type="board_dinner"))
        assert exc_info.value.status_code == 422

    def test_all_four_valid_types_work(self):
        for mt in _VALID_MEETING_TYPES:
            result = _build_meeting_brief(_make_input(meeting_type=mt))
            assert result["meeting_type"] == mt

    def test_governance_decision_is_approval_first(self):
        result = _build_meeting_brief(_make_input())
        assert result["governance_decision"] == "APPROVAL_FIRST"

    def test_is_first_meeting_preserved(self):
        result = _build_meeting_brief(_make_input(is_first_meeting=False))
        assert result["is_first_meeting"] is False

    def test_prospect_company_in_result(self):
        result = _build_meeting_brief(_make_input(prospect_company="Riyadh Logistics"))
        assert result["prospect_company"] == "Riyadh Logistics"

    def test_prospect_name_in_result(self):
        result = _build_meeting_brief(_make_input(prospect_name="Faisal Al-Dosari"))
        assert result["prospect_name"] == "Faisal Al-Dosari"


# ---------------------------------------------------------------------------
# Router metadata
# ---------------------------------------------------------------------------


class TestRouterMetadata:
    def test_prefix(self):
        assert router.prefix == "/api/v1/meeting-intelligence"

    def test_tags_contain_sales(self):
        assert "Sales" in router.tags
