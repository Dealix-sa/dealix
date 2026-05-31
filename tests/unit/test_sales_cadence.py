"""Unit tests for api/routers/sales_cadence.py"""
from __future__ import annotations

import pytest
from fastapi import HTTPException

from api.routers.sales_cadence import (
    _CADENCE_TEMPLATES,
    _SAUDI_COMMUNICATION_RULES,
    _VALID_CADENCE_TYPES,
    CadencePlanInput,
    _build_cadence_plan,
    router,
)


def _make_input(**overrides) -> CadencePlanInput:
    data = dict(
        cadence_type="warm_intro",
        prospect_name="Ahmad Al-Rashidi",
        prospect_company="AlRashidi Trading Co.",
        preferred_channel="whatsapp",
        arabic_primary=False,
    )
    data.update(overrides)
    return CadencePlanInput(**data)


# ---------------------------------------------------------------------------
# Static data: _CADENCE_TEMPLATES
# ---------------------------------------------------------------------------


class TestCadenceTemplates:
    def test_has_four_keys(self):
        assert len(_CADENCE_TEMPLATES) == 4

    def test_has_cold_outreach(self):
        assert "cold_outreach" in _CADENCE_TEMPLATES

    def test_has_warm_intro(self):
        assert "warm_intro" in _CADENCE_TEMPLATES

    def test_has_post_demo(self):
        assert "post_demo" in _CADENCE_TEMPLATES

    def test_has_renewal_touch(self):
        assert "renewal_touch" in _CADENCE_TEMPLATES

    def test_all_templates_have_name_en(self):
        for key, val in _CADENCE_TEMPLATES.items():
            assert val.get("name_en"), f"{key} missing name_en"

    def test_all_templates_have_name_ar(self):
        for key, val in _CADENCE_TEMPLATES.items():
            assert val.get("name_ar"), f"{key} missing name_ar"

    def test_all_templates_have_total_touches(self):
        for key, val in _CADENCE_TEMPLATES.items():
            assert isinstance(val.get("total_touches"), int), f"{key} missing total_touches"
            assert val["total_touches"] > 0

    def test_all_templates_have_duration_days(self):
        for key, val in _CADENCE_TEMPLATES.items():
            assert isinstance(val.get("duration_days"), int), f"{key} missing duration_days"
            assert val["duration_days"] > 0

    def test_all_templates_have_touch_sequence(self):
        for key, val in _CADENCE_TEMPLATES.items():
            assert isinstance(val.get("touch_sequence"), list), f"{key} missing touch_sequence"
            assert len(val["touch_sequence"]) > 0

    def test_touch_sequence_length_matches_total_touches(self):
        for key, val in _CADENCE_TEMPLATES.items():
            assert len(val["touch_sequence"]) == val["total_touches"], (
                f"{key}: touch_sequence length {len(val['touch_sequence'])} "
                f"!= total_touches {val['total_touches']}"
            )

    def test_cold_outreach_total_touches(self):
        assert _CADENCE_TEMPLATES["cold_outreach"]["total_touches"] == 5

    def test_cold_outreach_duration_days(self):
        assert _CADENCE_TEMPLATES["cold_outreach"]["duration_days"] == 14

    def test_warm_intro_total_touches(self):
        assert _CADENCE_TEMPLATES["warm_intro"]["total_touches"] == 4

    def test_warm_intro_duration_days(self):
        assert _CADENCE_TEMPLATES["warm_intro"]["duration_days"] == 7

    def test_post_demo_total_touches(self):
        assert _CADENCE_TEMPLATES["post_demo"]["total_touches"] == 6

    def test_post_demo_duration_days(self):
        assert _CADENCE_TEMPLATES["post_demo"]["duration_days"] == 21

    def test_renewal_touch_total_touches(self):
        assert _CADENCE_TEMPLATES["renewal_touch"]["total_touches"] == 5

    def test_renewal_touch_duration_days(self):
        assert _CADENCE_TEMPLATES["renewal_touch"]["duration_days"] == 30

    def test_all_touch_sequence_items_have_day(self):
        for key, val in _CADENCE_TEMPLATES.items():
            for touch in val["touch_sequence"]:
                assert "day" in touch, f"{key} touch missing 'day'"

    def test_all_touch_sequence_items_have_channel(self):
        for key, val in _CADENCE_TEMPLATES.items():
            for touch in val["touch_sequence"]:
                assert "channel" in touch, f"{key} touch missing 'channel'"

    def test_all_touch_sequence_items_have_message_hook_en(self):
        for key, val in _CADENCE_TEMPLATES.items():
            for touch in val["touch_sequence"]:
                assert touch.get("message_hook_en"), f"{key} touch missing 'message_hook_en'"

    def test_all_touch_sequence_items_have_message_hook_ar(self):
        for key, val in _CADENCE_TEMPLATES.items():
            for touch in val["touch_sequence"]:
                assert touch.get("message_hook_ar"), f"{key} touch missing 'message_hook_ar'"


# ---------------------------------------------------------------------------
# Static data: _SAUDI_COMMUNICATION_RULES
# ---------------------------------------------------------------------------


class TestSaudiCommunicationRules:
    def test_has_six_rules(self):
        assert len(_SAUDI_COMMUNICATION_RULES) == 6

    def test_all_rules_have_rule_en(self):
        for r in _SAUDI_COMMUNICATION_RULES:
            assert r.get("rule_en"), "Rule missing rule_en"

    def test_all_rules_have_rule_ar(self):
        for r in _SAUDI_COMMUNICATION_RULES:
            assert r.get("rule_ar"), "Rule missing rule_ar"


# ---------------------------------------------------------------------------
# _build_cadence_plan
# ---------------------------------------------------------------------------


class TestBuildCadencePlan:
    def test_returns_dict(self):
        result = _build_cadence_plan(_make_input())
        assert isinstance(result, dict)

    def test_has_cadence_type(self):
        result = _build_cadence_plan(_make_input(cadence_type="post_demo"))
        assert result["cadence_type"] == "post_demo"

    def test_has_prospect_name(self):
        result = _build_cadence_plan(_make_input(prospect_name="Khalid"))
        assert result["prospect_name"] == "Khalid"

    def test_has_prospect_company(self):
        result = _build_cadence_plan(_make_input(prospect_company="Acme KSA"))
        assert result["prospect_company"] == "Acme KSA"

    def test_has_template_name_en(self):
        result = _build_cadence_plan(_make_input())
        assert result.get("template_name_en")

    def test_has_template_name_ar(self):
        result = _build_cadence_plan(_make_input())
        assert result.get("template_name_ar")

    def test_has_total_touches(self):
        result = _build_cadence_plan(_make_input())
        assert isinstance(result["total_touches"], int)
        assert result["total_touches"] > 0

    def test_has_duration_days(self):
        result = _build_cadence_plan(_make_input())
        assert isinstance(result["duration_days"], int)
        assert result["duration_days"] > 0

    def test_has_touch_sequence(self):
        result = _build_cadence_plan(_make_input())
        assert isinstance(result["touch_sequence"], list)
        assert len(result["touch_sequence"]) > 0

    def test_touch_sequence_length_matches_total_touches(self):
        result = _build_cadence_plan(_make_input())
        assert len(result["touch_sequence"]) == result["total_touches"]

    def test_has_saudi_rules_to_observe(self):
        result = _build_cadence_plan(_make_input())
        assert "saudi_rules_to_observe" in result

    def test_saudi_rules_to_observe_count_is_six(self):
        result = _build_cadence_plan(_make_input())
        assert len(result["saudi_rules_to_observe"]) == 6

    def test_language_preference_en_when_not_arabic_primary(self):
        result = _build_cadence_plan(_make_input(arabic_primary=False))
        assert result["language_preference"] == "en"

    def test_language_preference_ar_when_arabic_primary(self):
        result = _build_cadence_plan(_make_input(arabic_primary=True))
        assert result["language_preference"] == "ar"

    def test_governance_decision_is_approval_first(self):
        result = _build_cadence_plan(_make_input())
        assert result["governance_decision"] == "APPROVAL_FIRST"

    def test_all_four_valid_types_work(self):
        for ct in _VALID_CADENCE_TYPES:
            result = _build_cadence_plan(_make_input(cadence_type=ct))
            assert result["cadence_type"] == ct

    def test_invalid_cadence_type_raises_http_422(self):
        with pytest.raises(HTTPException) as exc_info:
            _build_cadence_plan(_make_input(cadence_type="unknown_type"))
        assert exc_info.value.status_code == 422

    def test_invalid_cadence_type_message_contains_value(self):
        with pytest.raises(HTTPException) as exc_info:
            _build_cadence_plan(_make_input(cadence_type="bad_value"))
        assert "bad_value" in str(exc_info.value.detail)


# ---------------------------------------------------------------------------
# _VALID_CADENCE_TYPES
# ---------------------------------------------------------------------------


class TestValidCadenceTypes:
    def test_has_four_values(self):
        assert len(_VALID_CADENCE_TYPES) == 4

    def test_contains_cold_outreach(self):
        assert "cold_outreach" in _VALID_CADENCE_TYPES

    def test_contains_warm_intro(self):
        assert "warm_intro" in _VALID_CADENCE_TYPES

    def test_contains_post_demo(self):
        assert "post_demo" in _VALID_CADENCE_TYPES

    def test_contains_renewal_touch(self):
        assert "renewal_touch" in _VALID_CADENCE_TYPES


# ---------------------------------------------------------------------------
# Router metadata
# ---------------------------------------------------------------------------


class TestRouterMetadata:
    def test_prefix(self):
        assert router.prefix == "/api/v1/sales-cadence"

    def test_tags_contain_sales(self):
        assert "Sales" in router.tags
