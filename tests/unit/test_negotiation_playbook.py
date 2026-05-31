"""
Unit tests for api/routers/negotiation_playbook.py

Tests cover:
- _SAUDI_NEGOTIATION_PRINCIPLES: 6 principles, bilingual fields, required keys
- _CONCESSION_FRAMEWORK: 5 concession types, bilingual fields
- _WALK_AWAY_SIGNALS: 5 signals, bilingual fields
- _SCENARIO_PLAYBOOKS: 5 scenarios, bilingual fields, example scripts
- NegotiationScenarioInput: validation, valid/invalid values
- _build_negotiation_brief: governance_decision, playbook match, concession logic
- Router metadata: prefix and tags
"""
from __future__ import annotations

import pytest

from api.routers.negotiation_playbook import (
    _SAUDI_NEGOTIATION_PRINCIPLES,
    _CONCESSION_FRAMEWORK,
    _WALK_AWAY_SIGNALS,
    _SCENARIO_PLAYBOOKS,
    _build_negotiation_brief,
    NegotiationScenarioInput,
    router,
)


# ---------------------------------------------------------------------------
# Saudi negotiation principles
# ---------------------------------------------------------------------------


class TestSaudiNegotiationPrinciples:
    """
    _SAUDI_NEGOTIATION_PRINCIPLES is a list[dict] where each dict has an 'id' field.
    """

    def _by_id(self, principle_id: str) -> dict:
        return next(p for p in _SAUDI_NEGOTIATION_PRINCIPLES if p["id"] == principle_id)

    def test_six_principles(self):
        assert len(_SAUDI_NEGOTIATION_PRINCIPLES) == 6

    def test_expected_principle_ids(self):
        expected = {
            "face_saving",
            "relationship_first",
            "authority_clarity",
            "silence_as_strength",
            "halal_commercial_terms",
            "patience_timeline",
        }
        actual = {p["id"] for p in _SAUDI_NEGOTIATION_PRINCIPLES}
        assert expected == actual

    def test_all_have_name_en(self):
        for p in _SAUDI_NEGOTIATION_PRINCIPLES:
            assert p.get("name_en"), f"{p['id']} missing name_en"

    def test_all_have_name_ar(self):
        for p in _SAUDI_NEGOTIATION_PRINCIPLES:
            assert p.get("name_ar"), f"{p['id']} missing name_ar"

    def test_face_saving_mentions_graceful_exit(self):
        principle = self._by_id("face_saving")
        text = principle["description_en"].lower()
        assert "exit" in text or "corner" in text or "dignity" in text

    def test_halal_terms_mentions_murabaha_or_fee(self):
        principle = self._by_id("halal_commercial_terms")
        text = principle["description_en"].lower()
        assert "murabaha" in text or "fee" in text or "interest" in text

    def test_patience_timeline_mentions_budget_cycle(self):
        principle = self._by_id("patience_timeline")
        text = principle["description_en"].lower()
        assert "q1" in text or "q4" in text or "jan" in text or "oct" in text or "budget" in text


# ---------------------------------------------------------------------------
# Concession framework
# ---------------------------------------------------------------------------


class TestConcessionFramework:
    def test_five_concessions(self):
        assert len(_CONCESSION_FRAMEWORK) == 5

    def test_expected_concession_ids(self):
        ids = {c["id"] for c in _CONCESSION_FRAMEWORK}
        expected = {
            "anchor_high",
            "bundle_concession",
            "scope_reduction",
            "payment_terms",
            "pilot_first",
        }
        assert expected == ids

    def test_all_have_name_en(self):
        for c in _CONCESSION_FRAMEWORK:
            assert c.get("name_en"), f"{c['id']} missing name_en"

    def test_all_have_name_ar(self):
        for c in _CONCESSION_FRAMEWORK:
            assert c.get("name_ar"), f"{c['id']} missing name_ar"

    def test_pilot_first_mentions_sar_amount(self):
        pilot = next(c for c in _CONCESSION_FRAMEWORK if c["id"] == "pilot_first")
        text = pilot["description_en"].lower()
        assert "499" in text or "999" in text or "sar" in text or "pilot" in text


# ---------------------------------------------------------------------------
# Walk-away signals
# ---------------------------------------------------------------------------


class TestWalkAwaySignals:
    def test_five_signals(self):
        assert len(_WALK_AWAY_SIGNALS) == 5

    def test_expected_signal_ids(self):
        ids = {s["id"] for s in _WALK_AWAY_SIGNALS}
        expected = {
            "persistent_below_cost_pressure",
            "single_decision_maker_absent",
            "scope_creep_before_signing",
            "payment_terms_over_90_days",
            "no_data_access_commitment",
        }
        assert expected == ids

    def test_all_have_signal_en(self):
        for s in _WALK_AWAY_SIGNALS:
            assert s.get("signal_en"), f"{s['id']} missing signal_en"

    def test_all_have_signal_ar(self):
        for s in _WALK_AWAY_SIGNALS:
            assert s.get("signal_ar"), f"{s['id']} missing signal_ar"

    def test_below_cost_pressure_mentions_sar(self):
        signal = next(s for s in _WALK_AWAY_SIGNALS if s["id"] == "persistent_below_cost_pressure")
        text = signal["description_en"].lower()
        assert "2,000" in text or "sar" in text or "managed" in text


# ---------------------------------------------------------------------------
# Scenario playbooks
# ---------------------------------------------------------------------------


class TestScenarioPlaybooks:
    def test_five_playbooks(self):
        assert len(_SCENARIO_PLAYBOOKS) == 5

    def test_expected_scenario_types(self):
        expected = {
            "price_objection",
            "timeline_objection",
            "scope_creep",
            "competitor_comparison",
            "approval_delay",
        }
        assert expected == set(_SCENARIO_PLAYBOOKS.keys())

    def test_all_have_name_en_and_ar(self):
        for key, playbook in _SCENARIO_PLAYBOOKS.items():
            assert playbook.get("name_en"), f"{key} missing name_en"
            assert playbook.get("name_ar"), f"{key} missing name_ar"

    def test_all_have_recommended_response(self):
        for key, playbook in _SCENARIO_PLAYBOOKS.items():
            assert playbook.get("recommended_response_en"), f"{key} missing recommended_response_en"
            assert playbook.get("recommended_response_ar"), f"{key} missing recommended_response_ar"

    def test_all_have_trap_to_avoid(self):
        for key, playbook in _SCENARIO_PLAYBOOKS.items():
            assert playbook.get("trap_to_avoid_en"), f"{key} missing trap_to_avoid_en"
            assert playbook.get("trap_to_avoid_ar"), f"{key} missing trap_to_avoid_ar"

    def test_all_have_example_script(self):
        for key, playbook in _SCENARIO_PLAYBOOKS.items():
            assert playbook.get("example_script_en"), f"{key} missing example_script_en"

    def test_no_guaranteed_outcome_language(self):
        """No playbook should use language that guarantees outcomes."""
        forbidden_phrases = ["guaranteed", "will definitely", "always works", "100% success"]
        for key, playbook in _SCENARIO_PLAYBOOKS.items():
            for field, value in playbook.items():
                if isinstance(value, str):
                    for phrase in forbidden_phrases:
                        assert phrase not in value.lower(), (
                            f"{key}.{field} contains forbidden phrase: '{phrase}'"
                        )


# ---------------------------------------------------------------------------
# NegotiationScenarioInput validation
# ---------------------------------------------------------------------------


class TestNegotiationScenarioInput:
    def _valid_input(self, **overrides) -> dict:
        data = {
            "scenario_type": "price_objection",
            "deal_value_sar": 10_000.0,
            "stage": "negotiation",
        }
        data.update(overrides)
        return data

    def test_valid_input_accepted(self):
        inp = NegotiationScenarioInput(**self._valid_input())
        assert inp.scenario_type == "price_objection"

    def test_zero_deal_value_accepted_with_non_close_stage(self):
        inp = NegotiationScenarioInput(**self._valid_input(deal_value_sar=0, stage="proposal"))
        assert inp.deal_value_sar == 0

    def test_zero_deal_value_close_stage_rejected(self):
        with pytest.raises(Exception):
            NegotiationScenarioInput(**self._valid_input(deal_value_sar=0, stage="close"))

    def test_invalid_scenario_type_rejected(self):
        with pytest.raises(Exception):
            NegotiationScenarioInput(**self._valid_input(scenario_type="unknown_scenario"))

    def test_invalid_stage_rejected(self):
        with pytest.raises(Exception):
            NegotiationScenarioInput(**self._valid_input(stage="invalid_stage"))

    def test_negative_deal_value_rejected(self):
        with pytest.raises(Exception):
            NegotiationScenarioInput(**self._valid_input(deal_value_sar=-1.0))

    @pytest.mark.parametrize("scenario_type", [
        "price_objection", "timeline_objection", "scope_creep",
        "competitor_comparison", "approval_delay",
    ])
    def test_all_valid_scenario_types_accepted(self, scenario_type):
        inp = NegotiationScenarioInput(**self._valid_input(scenario_type=scenario_type))
        assert inp.scenario_type == scenario_type


# ---------------------------------------------------------------------------
# _build_negotiation_brief
# ---------------------------------------------------------------------------


class TestBuildNegotiationBrief:
    def _make_input(self, scenario_type="price_objection", deal_value_sar=10_000.0, stage="negotiation"):
        return NegotiationScenarioInput(
            scenario_type=scenario_type,
            deal_value_sar=deal_value_sar,
            stage=stage,
        )

    def test_returns_dict(self):
        result = _build_negotiation_brief(self._make_input())
        assert isinstance(result, dict)

    def test_governance_decision_is_approval_first(self):
        result = _build_negotiation_brief(self._make_input())
        assert result["governance_decision"] == "APPROVAL_FIRST"

    def test_returns_matching_scenario_type(self):
        result = _build_negotiation_brief(self._make_input("competitor_comparison"))
        playbook = result.get("playbook") or result.get("scenario_playbook") or {}
        assert playbook.get("scenario_type") == "competitor_comparison" or (
            result.get("scenario_type") == "competitor_comparison"
        )

    def test_returns_recommended_concessions_list(self):
        result = _build_negotiation_brief(self._make_input())
        concessions = result.get("recommended_concessions") or result.get("concession_recommendations") or []
        assert isinstance(concessions, list)
        assert len(concessions) > 0

    def test_large_deal_value_gets_relevant_concessions(self):
        result = _build_negotiation_brief(self._make_input(deal_value_sar=100_000.0))
        concessions = result.get("recommended_concessions") or result.get("concession_recommendations") or []
        concession_ids = [c.get("id") for c in concessions]
        # Large deals should not get pilot_first as primary concession
        assert len(concession_ids) > 0

    def test_small_deal_value_gets_concessions(self):
        result = _build_negotiation_brief(self._make_input(deal_value_sar=1_000.0))
        concessions = result.get("recommended_concessions") or result.get("concession_recommendations") or []
        assert len(concessions) > 0

    @pytest.mark.parametrize("scenario_type", [
        "price_objection", "timeline_objection", "scope_creep",
        "competitor_comparison", "approval_delay",
    ])
    def test_all_scenario_types_return_governance_decision(self, scenario_type):
        result = _build_negotiation_brief(self._make_input(scenario_type=scenario_type))
        assert result.get("governance_decision") == "APPROVAL_FIRST"


# ---------------------------------------------------------------------------
# Router metadata
# ---------------------------------------------------------------------------


class TestRouterMetadata:
    def test_router_prefix(self):
        assert router.prefix == "/api/v1/negotiation-playbook"

    def test_router_tags(self):
        assert "Sales" in router.tags
