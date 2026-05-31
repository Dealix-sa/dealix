"""
Unit tests for api/routers/champion_development.py

Tests cover:
- _CHAMPION_PROFILES: 4 archetypes, bilingual fields, motivators
- _CHAMPION_DEVELOPMENT_STAGES: 5 stages, bilingual names, activities
- _CHAMPION_HEALTH_INDICATORS: strong/weak lists with 5 each
- ChampionAssessmentInput: validation, archetype validation, field constraints
- _assess_champion: health score computation, label assignment, governance_decision
- Router metadata: prefix and tags
"""
from __future__ import annotations

import pytest

from api.routers.champion_development import (
    _CHAMPION_PROFILES,
    _CHAMPION_DEVELOPMENT_STAGES,
    _CHAMPION_HEALTH_INDICATORS,
    _assess_champion,
    ChampionAssessmentInput,
    router,
)


# ---------------------------------------------------------------------------
# Champion profiles
# ---------------------------------------------------------------------------


class TestChampionProfiles:
    def test_four_profiles(self):
        assert len(_CHAMPION_PROFILES) == 4

    def test_expected_archetype_keys(self):
        expected = {
            "operational_owner",
            "technology_lead",
            "financial_buyer",
            "executive_sponsor",
        }
        assert expected == set(_CHAMPION_PROFILES.keys())

    def test_all_have_name_en(self):
        for key, profile in _CHAMPION_PROFILES.items():
            assert profile.get("name_en"), f"{key} missing name_en"

    def test_all_have_name_ar(self):
        for key, profile in _CHAMPION_PROFILES.items():
            assert profile.get("name_ar"), f"{key} missing name_ar"

    def test_all_have_description_en(self):
        for key, profile in _CHAMPION_PROFILES.items():
            assert profile.get("description_en"), f"{key} missing description_en"

    def test_all_have_description_ar(self):
        for key, profile in _CHAMPION_PROFILES.items():
            assert profile.get("description_ar"), f"{key} missing description_ar"

    def test_technology_lead_mentions_pdpl_or_security(self):
        profile = _CHAMPION_PROFILES["technology_lead"]
        text = (profile["description_en"] + " " + profile.get("engagement_tip_en", "")).lower()
        assert "pdpl" in text or "security" in text or "integration" in text

    def test_financial_buyer_mentions_roi_or_zatca(self):
        profile = _CHAMPION_PROFILES["financial_buyer"]
        text = (profile["description_en"] + " " + profile.get("engagement_tip_en", "")).lower()
        assert "roi" in text or "zatca" in text or "cash" in text

    def test_executive_sponsor_mentions_vision_2030(self):
        profile = _CHAMPION_PROFILES["executive_sponsor"]
        text = (profile["description_en"] + " " + profile.get("engagement_tip_en", "")).lower()
        assert "vision 2030" in text or "saudization" in text or "strategic" in text


# ---------------------------------------------------------------------------
# Champion development stages
# ---------------------------------------------------------------------------


class TestChampionDevelopmentStages:
    def test_five_stages(self):
        assert len(_CHAMPION_DEVELOPMENT_STAGES) == 5

    def test_expected_stage_ids(self):
        stage_ids = [s["stage"] for s in _CHAMPION_DEVELOPMENT_STAGES]
        expected = ["identify", "educate", "arm", "test", "elevate"]
        assert stage_ids == expected

    def test_all_have_name_en_and_ar(self):
        for s in _CHAMPION_DEVELOPMENT_STAGES:
            assert s.get("name_en"), f"{s['stage']} missing name_en"
            assert s.get("name_ar"), f"{s['stage']} missing name_ar"

    def test_all_have_activities_en(self):
        for s in _CHAMPION_DEVELOPMENT_STAGES:
            acts = s.get("activities_en", [])
            assert isinstance(acts, list) and len(acts) > 0, (
                f"{s['stage']} missing activities_en"
            )

    def test_all_have_activities_ar(self):
        for s in _CHAMPION_DEVELOPMENT_STAGES:
            acts = s.get("activities_ar", [])
            assert isinstance(acts, list) and len(acts) > 0, (
                f"{s['stage']} missing activities_ar"
            )

    def test_identify_has_at_least_3_activities(self):
        identify = next(s for s in _CHAMPION_DEVELOPMENT_STAGES if s["stage"] == "identify")
        assert len(identify["activities_en"]) >= 3

    def test_arm_stage_mentions_proof_pack_or_roi(self):
        arm = next(s for s in _CHAMPION_DEVELOPMENT_STAGES if s["stage"] == "arm")
        all_text = " ".join(arm.get("activities_en", [])).lower()
        assert "proof" in all_text or "roi" in all_text or "deck" in all_text

    def test_test_stage_has_at_least_2_activities(self):
        test_stage = next(s for s in _CHAMPION_DEVELOPMENT_STAGES if s["stage"] == "test")
        assert len(test_stage["activities_en"]) >= 2

    def test_elevate_stage_has_at_least_2_activities(self):
        elevate = next(s for s in _CHAMPION_DEVELOPMENT_STAGES if s["stage"] == "elevate")
        assert len(elevate["activities_en"]) >= 2


# ---------------------------------------------------------------------------
# Champion health indicators
# ---------------------------------------------------------------------------


class TestChampionHealthIndicators:
    def test_has_strong_key(self):
        assert "strong" in _CHAMPION_HEALTH_INDICATORS

    def test_has_weak_key(self):
        assert "weak" in _CHAMPION_HEALTH_INDICATORS

    def test_five_strong_indicators(self):
        assert len(_CHAMPION_HEALTH_INDICATORS["strong"]) == 5

    def test_five_weak_indicators(self):
        assert len(_CHAMPION_HEALTH_INDICATORS["weak"]) == 5

    def test_strong_indicators_are_strings(self):
        for indicator in _CHAMPION_HEALTH_INDICATORS["strong"]:
            assert isinstance(indicator, str) and len(indicator) > 0

    def test_weak_indicators_are_strings(self):
        for indicator in _CHAMPION_HEALTH_INDICATORS["weak"]:
            assert isinstance(indicator, str) and len(indicator) > 0


# ---------------------------------------------------------------------------
# ChampionAssessmentInput validation
# ---------------------------------------------------------------------------


class TestChampionAssessmentInput:
    def _valid_data(self, **overrides) -> dict:
        data = {
            "contact_name": "Khaled Al-Otaibi",
            "contact_title": "IT Director",
            "archetype_guess": "technology_lead",
            "has_senior_access": True,
            "data_access_committed": True,
            "response_time_hours": 12.0,
            "introduced_senior": True,
        }
        data.update(overrides)
        return data

    def test_valid_input_accepted(self):
        inp = ChampionAssessmentInput(**self._valid_data())
        assert inp.contact_name == "Khaled Al-Otaibi"

    def test_empty_contact_name_rejected(self):
        with pytest.raises(Exception):
            ChampionAssessmentInput(**self._valid_data(contact_name=""))

    def test_empty_contact_title_rejected(self):
        with pytest.raises(Exception):
            ChampionAssessmentInput(**self._valid_data(contact_title=""))

    def test_invalid_archetype_rejected(self):
        with pytest.raises(Exception):
            ChampionAssessmentInput(**self._valid_data(archetype_guess="unknown_archetype"))

    def test_negative_response_time_rejected(self):
        with pytest.raises(Exception):
            ChampionAssessmentInput(**self._valid_data(response_time_hours=-1.0))

    @pytest.mark.parametrize("archetype", [
        "operational_owner", "technology_lead", "financial_buyer", "executive_sponsor",
    ])
    def test_all_valid_archetypes_accepted(self, archetype):
        inp = ChampionAssessmentInput(**self._valid_data(archetype_guess=archetype))
        assert inp.archetype_guess == archetype


# ---------------------------------------------------------------------------
# _assess_champion
# ---------------------------------------------------------------------------


class TestAssessChampion:
    def _make_input(self, **overrides) -> ChampionAssessmentInput:
        data = {
            "contact_name": "Sara Al-Ghamdi",
            "contact_title": "Operations Manager",
            "archetype_guess": "operational_owner",
            "has_senior_access": True,
            "data_access_committed": True,
            "response_time_hours": 10.0,
            "introduced_senior": True,
        }
        data.update(overrides)
        return ChampionAssessmentInput(**data)

    def test_returns_dict(self):
        result = _assess_champion(self._make_input())
        assert isinstance(result, dict)

    def test_governance_decision_is_allow_with_review(self):
        result = _assess_champion(self._make_input())
        assert result["governance_decision"] == "ALLOW_WITH_REVIEW"

    def test_perfect_inputs_give_strong_label(self):
        result = _assess_champion(self._make_input(
            has_senior_access=True,
            data_access_committed=True,
            response_time_hours=5.0,
            introduced_senior=True,
        ))
        assert result["health_score"] >= 70
        assert result["health_label"] == "Strong"

    def test_all_false_gives_weak_label(self):
        result = _assess_champion(self._make_input(
            has_senior_access=False,
            data_access_committed=False,
            response_time_hours=100.0,
            introduced_senior=False,
        ))
        assert result["health_score"] < 40
        assert result["health_label"] == "Weak"

    def test_moderate_score_gives_moderate_label(self):
        # has_senior_access=True (+25), no data (+0), 30h response (+10), no senior (+0) = 35 — Weak
        # has_senior_access=True (+25), data=True (+20), 30h (+10), no senior (+0) = 55 — Moderate
        result = _assess_champion(self._make_input(
            has_senior_access=True,
            data_access_committed=True,
            response_time_hours=30.0,
            introduced_senior=False,
        ))
        assert 40 <= result["health_score"] < 70
        assert result["health_label"] == "Moderate"

    def test_result_includes_archetype_profile(self):
        result = _assess_champion(self._make_input(archetype_guess="financial_buyer"))
        profile = result.get("archetype_profile")
        assert profile is not None
        assert profile.get("id") == "financial_buyer"

    def test_result_includes_recommended_actions_en(self):
        result = _assess_champion(self._make_input())
        actions = result.get("recommended_actions_en")
        assert isinstance(actions, list)
        assert len(actions) == 3

    def test_result_includes_recommended_actions_ar(self):
        result = _assess_champion(self._make_input())
        actions = result.get("recommended_actions_ar")
        assert isinstance(actions, list)
        assert len(actions) == 3

    def test_score_breakdown_present(self):
        result = _assess_champion(self._make_input())
        breakdown = result.get("score_breakdown")
        assert isinstance(breakdown, dict)
        assert "has_senior_access" in breakdown

    def test_response_time_48h_gives_10_points(self):
        result = _assess_champion(self._make_input(
            has_senior_access=False,
            data_access_committed=False,
            response_time_hours=48.0,
            introduced_senior=False,
        ))
        breakdown = result.get("score_breakdown", {})
        assert breakdown.get("response_time_hours_points") == 10

    def test_response_time_over_48h_gives_0_points(self):
        result = _assess_champion(self._make_input(
            has_senior_access=False,
            data_access_committed=False,
            response_time_hours=72.0,
            introduced_senior=False,
        ))
        breakdown = result.get("score_breakdown", {})
        assert breakdown.get("response_time_hours_points") == 0

    def test_contact_name_in_result(self):
        result = _assess_champion(self._make_input(contact_name="Faisal Al-Dosari"))
        assert result["contact_name"] == "Faisal Al-Dosari"


# ---------------------------------------------------------------------------
# Router metadata
# ---------------------------------------------------------------------------


class TestRouterMetadata:
    def test_router_prefix(self):
        assert router.prefix == "/api/v1/champion-development"

    def test_router_tags(self):
        assert "Sales" in router.tags
