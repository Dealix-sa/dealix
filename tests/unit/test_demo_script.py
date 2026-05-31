"""
Unit tests for api/routers/demo_script.py

Coverage:
- _DEMO_FLOW: 6 phases, bilingual names, total 50 minutes
- _DEMO_TYPES: 4 types, correct durations and audience fields
- _CULTURAL_DEMO_RULES: 7 rules, bilingual content
- _OBJECTION_RESPONSES: 5 objections, bilingual responses
- DemoConfigInput: field validation
- _configure_demo: phase filtering, language guidance, opening hook, governance
- Router metadata: prefix and tags
"""
from __future__ import annotations

import pytest

from api.routers.demo_script import (
    _DEMO_FLOW,
    _DEMO_FLOW_TOTAL_MINUTES,
    _DEMO_TYPES,
    _CULTURAL_DEMO_RULES,
    _OBJECTION_RESPONSES,
    _configure_demo,
    DemoConfigInput,
    router,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_config(**overrides) -> DemoConfigInput:
    """Return a valid DemoConfigInput unless overridden."""
    data: dict = dict(
        demo_type="champion_deep_dive",
        audience_seniority="manager_team_lead",
        known_pains=["manual ZATCA reporting"],
        is_arabic_primary=False,
    )
    data.update(overrides)
    return DemoConfigInput(**data)


# ---------------------------------------------------------------------------
# Demo flow structure
# ---------------------------------------------------------------------------

class TestDemoFlow:
    def test_six_phases(self):
        assert len(_DEMO_FLOW) == 6

    def test_total_duration_fifty_minutes(self):
        assert _DEMO_FLOW_TOTAL_MINUTES == 50

    def test_expected_phase_ids(self):
        ids = [p["id"] for p in _DEMO_FLOW]
        expected = [
            "opening",
            "pain_discovery",
            "solution_fit",
            "roi_moment",
            "proof_point",
            "next_step",
        ]
        assert ids == expected

    def test_all_phases_have_bilingual_names(self):
        for phase in _DEMO_FLOW:
            assert phase.get("name_en"), f"phase {phase['id']} missing name_en"
            assert phase.get("name_ar"), f"phase {phase['id']} missing name_ar"

    def test_all_phases_have_duration(self):
        for phase in _DEMO_FLOW:
            assert isinstance(phase["duration_minutes"], int)
            assert phase["duration_minutes"] > 0

    def test_all_phases_have_bilingual_purpose(self):
        for phase in _DEMO_FLOW:
            assert phase.get("purpose_en"), f"phase {phase['id']} missing purpose_en"
            assert phase.get("purpose_ar"), f"phase {phase['id']} missing purpose_ar"

    def test_opening_is_five_minutes(self):
        opening = next(p for p in _DEMO_FLOW if p["id"] == "opening")
        assert opening["duration_minutes"] == 5

    def test_solution_fit_is_fifteen_minutes(self):
        sf = next(p for p in _DEMO_FLOW if p["id"] == "solution_fit")
        assert sf["duration_minutes"] == 15


# ---------------------------------------------------------------------------
# Demo types structure
# ---------------------------------------------------------------------------

class TestDemoTypes:
    def test_four_demo_types(self):
        assert len(_DEMO_TYPES) == 4

    def test_expected_demo_type_keys(self):
        expected = {
            "executive_overview",
            "champion_deep_dive",
            "proposal_validation",
            "pilot_kickoff",
        }
        assert set(_DEMO_TYPES.keys()) == expected

    def test_executive_overview_duration_twenty(self):
        assert _DEMO_TYPES["executive_overview"]["duration_minutes"] == 20

    def test_champion_deep_dive_duration_fifty(self):
        assert _DEMO_TYPES["champion_deep_dive"]["duration_minutes"] == 50

    def test_all_have_bilingual_audience(self):
        for tid, tmeta in _DEMO_TYPES.items():
            assert tmeta.get("audience_en"), f"{tid} missing audience_en"
            assert tmeta.get("audience_ar"), f"{tid} missing audience_ar"

    def test_executive_overview_no_technical_detail(self):
        assert _DEMO_TYPES["executive_overview"]["technical_detail"] is False

    def test_champion_deep_dive_has_technical_detail(self):
        assert _DEMO_TYPES["champion_deep_dive"]["technical_detail"] is True


# ---------------------------------------------------------------------------
# Cultural demo rules structure
# ---------------------------------------------------------------------------

class TestCulturalDemoRules:
    def test_seven_rules(self):
        assert len(_CULTURAL_DEMO_RULES) == 7

    def test_all_have_bilingual_rule(self):
        for rule in _CULTURAL_DEMO_RULES:
            assert rule.get("rule_en"), f"rule {rule.get('id')} missing rule_en"
            assert rule.get("rule_ar"), f"rule {rule.get('id')} missing rule_ar"

    def test_friday_rule_present(self):
        combined = " ".join(r["rule_en"].lower() for r in _CULTURAL_DEMO_RULES)
        assert "friday" in combined

    def test_sar_currency_rule_present(self):
        combined = " ".join(r["rule_en"].lower() for r in _CULTURAL_DEMO_RULES)
        assert "sar" in combined or "currency" in combined or "usd" in combined


# ---------------------------------------------------------------------------
# Objection responses structure
# ---------------------------------------------------------------------------

class TestObjectionResponses:
    def test_five_objections(self):
        assert len(_OBJECTION_RESPONSES) == 5

    def test_expected_objection_ids(self):
        ids = {obj["id"] for obj in _OBJECTION_RESPONSES}
        expected = {
            "we_already_have_crm",
            "our_it_team_can_build",
            "show_me_the_price",
            "we_need_arabic_first",
            "what_about_data_security",
        }
        assert ids == expected

    def test_all_have_bilingual_responses(self):
        for obj in _OBJECTION_RESPONSES:
            assert obj.get("response_en"), f"{obj['id']} missing response_en"
            assert obj.get("response_ar"), f"{obj['id']} missing response_ar"

    def test_crm_objection_mentions_integration(self):
        crm_obj = next(o for o in _OBJECTION_RESPONSES if o["id"] == "we_already_have_crm")
        assert "integrat" in crm_obj["response_en"].lower()

    def test_security_objection_mentions_pdpl(self):
        sec_obj = next(o for o in _OBJECTION_RESPONSES if o["id"] == "what_about_data_security")
        assert "pdpl" in sec_obj["response_en"].lower()

    def test_arabic_objection_mentions_bilingual(self):
        ar_obj = next(o for o in _OBJECTION_RESPONSES if o["id"] == "we_need_arabic_first")
        assert "arabic" in ar_obj["response_en"].lower() or "bilingual" in ar_obj["response_en"].lower()


# ---------------------------------------------------------------------------
# DemoConfigInput validation
# ---------------------------------------------------------------------------

class TestDemoConfigInputValidation:
    def test_valid_config_created(self):
        inp = _make_config()
        assert inp.demo_type == "champion_deep_dive"
        assert inp.is_arabic_primary is False

    def test_arabic_primary_true(self):
        inp = _make_config(is_arabic_primary=True)
        assert inp.is_arabic_primary is True

    def test_known_pains_required_at_least_one(self):
        with pytest.raises(Exception):
            _make_config(known_pains=[])

    def test_known_pains_max_three(self):
        with pytest.raises(Exception):
            _make_config(known_pains=["a", "b", "c", "d"])

    def test_three_known_pains_accepted(self):
        inp = _make_config(known_pains=["pain_a", "pain_b", "pain_c"])
        assert len(inp.known_pains) == 3


# ---------------------------------------------------------------------------
# _configure_demo core logic
# ---------------------------------------------------------------------------

class TestConfigureDemo:
    def test_returns_demo_type_in_output(self):
        result = _configure_demo(_make_config(demo_type="executive_overview"))
        assert result["demo_type"] == "executive_overview"

    def test_executive_overview_duration_twenty(self):
        result = _configure_demo(_make_config(demo_type="executive_overview"))
        assert result["duration_minutes"] == 20

    def test_executive_overview_phases_fit_within_20_min(self):
        result = _configure_demo(_make_config(demo_type="executive_overview"))
        total = sum(p["duration_minutes"] for p in result["recommended_flow"])
        assert total <= 20

    def test_champion_deep_dive_includes_all_phases(self):
        result = _configure_demo(_make_config(demo_type="champion_deep_dive"))
        assert len(result["recommended_flow"]) == 6

    def test_arabic_primary_sets_arabic_guidance(self):
        result = _configure_demo(_make_config(is_arabic_primary=True))
        assert "arabic" in result["language_guidance_en"].lower()

    def test_english_primary_sets_english_guidance(self):
        result = _configure_demo(_make_config(is_arabic_primary=False))
        assert "english" in result["language_guidance_en"].lower()

    def test_opening_hook_references_first_pain(self):
        result = _configure_demo(_make_config(known_pains=["ZATCA overdue"]))
        assert "ZATCA overdue" in result["opening_hook_en"]

    def test_governance_decision_is_allow_with_review(self):
        result = _configure_demo(_make_config())
        assert result["governance_decision"] == "ALLOW_WITH_REVIEW"

    def test_invalid_demo_type_raises_value_error(self):
        with pytest.raises(ValueError):
            _configure_demo(_make_config(demo_type="nonexistent_type"))

    def test_invalid_seniority_raises_value_error(self):
        with pytest.raises(ValueError):
            _configure_demo(_make_config(audience_seniority="intern"))

    def test_bilingual_audience_returned(self):
        result = _configure_demo(_make_config(demo_type="executive_overview"))
        assert result.get("audience_en")
        assert result.get("audience_ar")

    def test_pilot_kickoff_config(self):
        result = _configure_demo(_make_config(demo_type="pilot_kickoff"))
        assert result["duration_minutes"] == 45

    def test_proposal_validation_config(self):
        result = _configure_demo(_make_config(demo_type="proposal_validation"))
        assert result["duration_minutes"] == 30


# ---------------------------------------------------------------------------
# Router metadata
# ---------------------------------------------------------------------------

class TestRouterMetadata:
    def test_router_prefix(self):
        assert router.prefix == "/api/v1/demo-script"

    def test_router_tags_include_sales(self):
        assert "Sales" in router.tags
