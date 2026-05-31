"""Unit tests for api/routers/onboarding_playbook.py"""
from __future__ import annotations

import pytest
from fastapi import HTTPException

from api.routers.onboarding_playbook import (
    _ONBOARDING_PHASES,
    _ONBOARDING_RISKS,
    _VALID_ENGAGEMENT_TYPES,
    OnboardingPlanInput,
    _build_onboarding_plan,
    router,
)


def _make_input(**overrides) -> OnboardingPlanInput:
    data = dict(
        client_name="Saudi Telecom",
        engagement_type="sprint",
        start_date="2026-06-01",
        primary_contact_name="Ahmed Al-Rashidi",
        primary_contact_title="Head of Digital Transformation",
        data_systems=["SAP", "Oracle"],
        arabic_primary=False,
    )
    data.update(overrides)
    return OnboardingPlanInput(**data)


# ---------------------------------------------------------------------------
# Static data: phases
# ---------------------------------------------------------------------------


class TestOnboardingPhases:
    def test_has_five_phases(self):
        assert len(_ONBOARDING_PHASES) == 5

    def test_phases_ordered_1_to_5(self):
        orders = [p["order"] for p in _ONBOARDING_PHASES]
        assert orders == list(range(1, 6))

    def test_all_have_phase_name_en(self):
        for p in _ONBOARDING_PHASES:
            assert p.get("phase_name_en"), f"Phase {p.get('order')} missing phase_name_en"

    def test_all_have_phase_name_ar(self):
        for p in _ONBOARDING_PHASES:
            assert p.get("phase_name_ar"), f"Phase {p.get('order')} missing phase_name_ar"

    def test_all_have_duration_days(self):
        for p in _ONBOARDING_PHASES:
            assert "duration_days" in p
            assert p["duration_days"] > 0

    def test_all_have_three_milestones_en(self):
        for p in _ONBOARDING_PHASES:
            assert len(p.get("key_milestones_en", [])) == 3, (
                f"Phase {p.get('order')} does not have 3 milestones_en"
            )

    def test_all_have_three_milestones_ar(self):
        for p in _ONBOARDING_PHASES:
            assert len(p.get("key_milestones_ar", [])) == 3, (
                f"Phase {p.get('order')} does not have 3 milestones_ar"
            )

    def test_all_have_success_criteria_en(self):
        for p in _ONBOARDING_PHASES:
            assert p.get("success_criteria_en"), f"Phase {p.get('order')} missing success_criteria_en"

    def test_all_have_success_criteria_ar(self):
        for p in _ONBOARDING_PHASES:
            assert p.get("success_criteria_ar"), f"Phase {p.get('order')} missing success_criteria_ar"

    def test_total_duration_is_20(self):
        total = sum(p["duration_days"] for p in _ONBOARDING_PHASES)
        assert total == 20

    def test_first_phase_is_kickoff(self):
        assert _ONBOARDING_PHASES[0]["phase_name_en"] == "Kickoff"

    def test_last_phase_is_go_live(self):
        assert _ONBOARDING_PHASES[4]["phase_name_en"] == "Go Live"


# ---------------------------------------------------------------------------
# Static data: risks
# ---------------------------------------------------------------------------


class TestOnboardingRisks:
    def test_has_five_risks(self):
        assert len(_ONBOARDING_RISKS) == 5

    def test_all_have_risk_en(self):
        for r in _ONBOARDING_RISKS:
            assert r.get("risk_en"), "Risk missing risk_en"

    def test_all_have_risk_ar(self):
        for r in _ONBOARDING_RISKS:
            assert r.get("risk_ar"), "Risk missing risk_ar"

    def test_all_have_mitigation_en(self):
        for r in _ONBOARDING_RISKS:
            assert r.get("mitigation_en"), "Risk missing mitigation_en"

    def test_all_have_mitigation_ar(self):
        for r in _ONBOARDING_RISKS:
            assert r.get("mitigation_ar"), "Risk missing mitigation_ar"

    def test_all_have_probability(self):
        for r in _ONBOARDING_RISKS:
            assert r.get("probability") in {"high", "medium", "low"}, (
                f"Risk has invalid probability: {r.get('probability')}"
            )


# ---------------------------------------------------------------------------
# Valid engagement types
# ---------------------------------------------------------------------------


class TestValidEngagementTypes:
    def test_four_valid_types(self):
        assert _VALID_ENGAGEMENT_TYPES == {"sprint", "data_pack", "managed_ops", "custom_ai"}


# ---------------------------------------------------------------------------
# _build_onboarding_plan
# ---------------------------------------------------------------------------


class TestBuildOnboardingPlan:
    def test_returns_dict(self):
        result = _build_onboarding_plan(_make_input())
        assert isinstance(result, dict)

    def test_has_client_name(self):
        result = _build_onboarding_plan(_make_input(client_name="ACME"))
        assert result["client_name"] == "ACME"

    def test_has_five_phases(self):
        result = _build_onboarding_plan(_make_input())
        assert len(result["phases"]) == 5

    def test_total_duration_days_is_20(self):
        result = _build_onboarding_plan(_make_input())
        assert result["total_duration_days"] == 20

    def test_has_primary_contact(self):
        result = _build_onboarding_plan(_make_input())
        assert "primary_contact" in result
        assert "name" in result["primary_contact"]
        assert "title" in result["primary_contact"]

    def test_primary_contact_name(self):
        result = _build_onboarding_plan(_make_input(primary_contact_name="Noura Al-Ali"))
        assert result["primary_contact"]["name"] == "Noura Al-Ali"

    def test_primary_contact_title(self):
        result = _build_onboarding_plan(_make_input(primary_contact_title="CTO"))
        assert result["primary_contact"]["title"] == "CTO"

    def test_has_data_systems_count(self):
        result = _build_onboarding_plan(_make_input(data_systems=["SAP", "Oracle", "Salesforce"]))
        assert result["data_systems_count"] == 3

    def test_empty_data_systems_count_zero(self):
        result = _build_onboarding_plan(_make_input(data_systems=[]))
        assert result["data_systems_count"] == 0

    def test_language_primary_en_by_default(self):
        result = _build_onboarding_plan(_make_input(arabic_primary=False))
        assert result["language_primary"] == "en"

    def test_language_primary_ar_when_set(self):
        result = _build_onboarding_plan(_make_input(arabic_primary=True))
        assert result["language_primary"] == "ar"

    def test_has_five_risks(self):
        result = _build_onboarding_plan(_make_input())
        assert len(result["risks"]) == 5

    def test_governance_decision_approval_first(self):
        result = _build_onboarding_plan(_make_input())
        assert result["governance_decision"] == "APPROVAL_FIRST"

    def test_has_disclaimer_en(self):
        result = _build_onboarding_plan(_make_input())
        assert result.get("disclaimer_en")

    def test_has_disclaimer_ar(self):
        result = _build_onboarding_plan(_make_input())
        assert result.get("disclaimer_ar")

    def test_invalid_engagement_type_raises_422(self):
        with pytest.raises(HTTPException) as exc_info:
            _build_onboarding_plan(_make_input(engagement_type="unknown_type"))
        assert exc_info.value.status_code == 422

    def test_invalid_engagement_type_error_message(self):
        with pytest.raises(HTTPException) as exc_info:
            _build_onboarding_plan(_make_input(engagement_type="invalid"))
        assert "invalid" in str(exc_info.value.detail).lower()

    def test_valid_engagement_sprint(self):
        result = _build_onboarding_plan(_make_input(engagement_type="sprint"))
        assert result["engagement_type"] == "sprint"

    def test_valid_engagement_data_pack(self):
        result = _build_onboarding_plan(_make_input(engagement_type="data_pack"))
        assert result["engagement_type"] == "data_pack"

    def test_valid_engagement_managed_ops(self):
        result = _build_onboarding_plan(_make_input(engagement_type="managed_ops"))
        assert result["engagement_type"] == "managed_ops"

    def test_valid_engagement_custom_ai(self):
        result = _build_onboarding_plan(_make_input(engagement_type="custom_ai"))
        assert result["engagement_type"] == "custom_ai"

    def test_phases_include_all_names(self):
        result = _build_onboarding_plan(_make_input())
        phase_names = [p["phase_name_en"] for p in result["phases"]]
        assert "Kickoff" in phase_names
        assert "Go Live" in phase_names


# ---------------------------------------------------------------------------
# Router metadata
# ---------------------------------------------------------------------------


class TestRouterMetadata:
    def test_prefix(self):
        assert router.prefix == "/api/v1/onboarding-playbook"

    def test_tags_contain_sales(self):
        assert "Sales" in router.tags
