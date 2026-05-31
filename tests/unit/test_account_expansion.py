"""Unit tests for api/routers/account_expansion.py"""
from __future__ import annotations

import pytest
from fastapi import HTTPException

from api.routers.account_expansion import (
    _EXPANSION_PLAYBOOKS,
    _EXPANSION_SIGNALS,
    _VALID_ACCOUNT_TIERS,
    ExpansionAssessmentInput,
    _assess_expansion,
    router,
)


def _make_input(**overrides) -> ExpansionAssessmentInput:
    data = dict(
        client_name="Tamimi Markets",
        current_tier="growth",
        mrr_sar=20_000.0,
        usage_score=60.0,
        nps_score=7.0,
        months_as_customer=12,
        champion_promoted=False,
        new_budget_cycle=False,
    )
    data.update(overrides)
    return ExpansionAssessmentInput(**data)


# ---------------------------------------------------------------------------
# Static data: signals
# ---------------------------------------------------------------------------


class TestExpansionSignals:
    def test_has_six_signals(self):
        assert len(_EXPANSION_SIGNALS) == 6

    def test_all_have_signal_id(self):
        for s in _EXPANSION_SIGNALS:
            assert s.get("signal_id"), f"Signal missing signal_id: {s}"

    def test_all_have_signal_en(self):
        for s in _EXPANSION_SIGNALS:
            assert s.get("signal_en"), f"Signal {s.get('signal_id')} missing signal_en"

    def test_all_have_signal_ar(self):
        for s in _EXPANSION_SIGNALS:
            assert s.get("signal_ar"), f"Signal {s.get('signal_id')} missing signal_ar"

    def test_all_have_weight(self):
        for s in _EXPANSION_SIGNALS:
            assert "weight" in s, f"Signal {s.get('signal_id')} missing weight"
            assert 0 <= s["weight"] <= 100

    def test_all_have_trigger_action_en(self):
        for s in _EXPANSION_SIGNALS:
            assert s.get("trigger_action_en"), f"Signal {s.get('signal_id')} missing trigger_action_en"

    def test_all_have_trigger_action_ar(self):
        for s in _EXPANSION_SIGNALS:
            assert s.get("trigger_action_ar"), f"Signal {s.get('signal_id')} missing trigger_action_ar"

    def test_expected_signal_ids_present(self):
        ids = {s["signal_id"] for s in _EXPANSION_SIGNALS}
        assert "high_usage_rate" in ids
        assert "champion_promotion" in ids
        assert "new_budget_cycle" in ids
        assert "positive_nps" in ids
        assert "team_growth" in ids
        assert "zatca_phase_expansion" in ids


# ---------------------------------------------------------------------------
# Static data: playbooks
# ---------------------------------------------------------------------------


class TestExpansionPlaybooks:
    def test_has_three_keys(self):
        assert len(_EXPANSION_PLAYBOOKS) == 3

    def test_expected_keys(self):
        assert "upsell_tier" in _EXPANSION_PLAYBOOKS
        assert "cross_sell_module" in _EXPANSION_PLAYBOOKS
        assert "seat_expansion" in _EXPANSION_PLAYBOOKS

    def test_all_have_name_en(self):
        for key, pb in _EXPANSION_PLAYBOOKS.items():
            assert pb.get("name_en"), f"Playbook '{key}' missing name_en"

    def test_all_have_name_ar(self):
        for key, pb in _EXPANSION_PLAYBOOKS.items():
            assert pb.get("name_ar"), f"Playbook '{key}' missing name_ar"

    def test_all_have_three_steps_en(self):
        for key, pb in _EXPANSION_PLAYBOOKS.items():
            assert len(pb.get("steps_en", [])) == 3, f"Playbook '{key}' does not have 3 steps_en"

    def test_all_have_three_steps_ar(self):
        for key, pb in _EXPANSION_PLAYBOOKS.items():
            assert len(pb.get("steps_ar", [])) == 3, f"Playbook '{key}' does not have 3 steps_ar"


# ---------------------------------------------------------------------------
# Valid tiers
# ---------------------------------------------------------------------------


class TestValidAccountTiers:
    def test_three_valid_tiers(self):
        assert _VALID_ACCOUNT_TIERS == {"standard", "growth", "strategic"}


# ---------------------------------------------------------------------------
# _assess_expansion
# ---------------------------------------------------------------------------


class TestAssessExpansion:
    def test_returns_dict(self):
        result = _assess_expansion(_make_input())
        assert isinstance(result, dict)

    def test_has_expansion_score(self):
        result = _assess_expansion(_make_input())
        assert "expansion_score" in result

    def test_expansion_score_is_numeric(self):
        result = _assess_expansion(_make_input())
        assert isinstance(result["expansion_score"], (int, float))

    def test_has_expansion_label(self):
        result = _assess_expansion(_make_input())
        assert "expansion_label" in result

    def test_expansion_label_valid_values(self):
        result = _assess_expansion(_make_input())
        assert result["expansion_label"] in {"high", "medium", "low"}

    def test_has_recommended_playbook(self):
        result = _assess_expansion(_make_input())
        assert "recommended_playbook" in result

    def test_recommended_playbook_valid_values(self):
        result = _assess_expansion(_make_input())
        assert result["recommended_playbook"] in _EXPANSION_PLAYBOOKS

    def test_has_top_signals(self):
        result = _assess_expansion(_make_input())
        assert "top_signals" in result
        assert isinstance(result["top_signals"], list)

    def test_has_next_mrr_target_sar(self):
        result = _assess_expansion(_make_input())
        assert "next_mrr_target_sar" in result

    def test_has_governance_decision(self):
        result = _assess_expansion(_make_input())
        assert result["governance_decision"] == "APPROVAL_FIRST"

    def test_has_client_name(self):
        result = _assess_expansion(_make_input(client_name="ACME Corp"))
        assert result["client_name"] == "ACME Corp"

    def test_high_label_high_score(self):
        result = _assess_expansion(
            _make_input(
                usage_score=90,
                nps_score=9,
                months_as_customer=24,
                champion_promoted=True,
            )
        )
        assert result["expansion_label"] == "high"

    def test_high_label_maps_to_upsell_tier(self):
        result = _assess_expansion(
            _make_input(
                usage_score=90,
                nps_score=9,
                months_as_customer=24,
                champion_promoted=True,
            )
        )
        assert result["recommended_playbook"] == "upsell_tier"

    def test_low_label_low_score(self):
        result = _assess_expansion(
            _make_input(
                usage_score=20,
                nps_score=5,
                months_as_customer=3,
                champion_promoted=False,
                new_budget_cycle=False,
            )
        )
        assert result["expansion_label"] == "low"

    def test_low_label_maps_to_seat_expansion(self):
        result = _assess_expansion(
            _make_input(
                usage_score=20,
                nps_score=5,
                months_as_customer=3,
            )
        )
        assert result["recommended_playbook"] == "seat_expansion"

    def test_medium_label(self):
        # usage=50*0.3=15, nps=6*10*0.2=12, tenure=min(6/12,1)*100*0.2=10 = 37 → low
        # Nudge with new_budget_cycle to push to 52 → medium
        result = _assess_expansion(
            _make_input(
                usage_score=50,
                nps_score=6,
                months_as_customer=6,
                new_budget_cycle=True,
            )
        )
        assert result["expansion_label"] == "medium"

    def test_medium_label_maps_to_cross_sell_module(self):
        result = _assess_expansion(
            _make_input(
                usage_score=50,
                nps_score=6,
                months_as_customer=6,
                new_budget_cycle=True,
            )
        )
        assert result["recommended_playbook"] == "cross_sell_module"

    def test_invalid_current_tier_raises_422(self):
        with pytest.raises(HTTPException) as exc_info:
            _assess_expansion(_make_input(current_tier="enterprise"))
        assert exc_info.value.status_code == 422

    def test_invalid_current_tier_error_message(self):
        with pytest.raises(HTTPException) as exc_info:
            _assess_expansion(_make_input(current_tier="invalid"))
        assert "invalid_tier" in str(exc_info.value.detail).lower() or "invalid" in str(exc_info.value.detail).lower()

    def test_valid_tier_standard(self):
        result = _assess_expansion(_make_input(current_tier="standard"))
        assert result["expansion_label"] in {"high", "medium", "low"}

    def test_valid_tier_growth(self):
        result = _assess_expansion(_make_input(current_tier="growth"))
        assert result["expansion_label"] in {"high", "medium", "low"}

    def test_valid_tier_strategic(self):
        result = _assess_expansion(_make_input(current_tier="strategic"))
        assert result["expansion_label"] in {"high", "medium", "low"}

    def test_next_mrr_target_greater_than_mrr(self):
        result = _assess_expansion(_make_input(mrr_sar=10_000.0))
        assert result["next_mrr_target_sar"] > 10_000.0

    def test_next_mrr_high_multiplier(self):
        result = _assess_expansion(
            _make_input(
                mrr_sar=10_000.0,
                usage_score=90,
                nps_score=9,
                months_as_customer=24,
                champion_promoted=True,
            )
        )
        assert result["next_mrr_target_sar"] == pytest.approx(13_000.0, abs=1.0)

    def test_next_mrr_low_multiplier(self):
        result = _assess_expansion(
            _make_input(
                mrr_sar=10_000.0,
                usage_score=20,
                nps_score=5,
                months_as_customer=3,
            )
        )
        assert result["next_mrr_target_sar"] == pytest.approx(10_500.0, abs=1.0)

    def test_top_signals_high_usage(self):
        result = _assess_expansion(_make_input(usage_score=80))
        assert "high_usage_rate" in result["top_signals"]

    def test_top_signals_champion_promotion(self):
        result = _assess_expansion(_make_input(champion_promoted=True))
        assert "champion_promotion" in result["top_signals"]

    def test_top_signals_new_budget_cycle(self):
        result = _assess_expansion(_make_input(new_budget_cycle=True))
        assert "new_budget_cycle" in result["top_signals"]

    def test_top_signals_positive_nps(self):
        result = _assess_expansion(_make_input(nps_score=8.5))
        assert "positive_nps" in result["top_signals"]

    def test_low_usage_not_in_signals(self):
        result = _assess_expansion(_make_input(usage_score=30))
        assert "high_usage_rate" not in result["top_signals"]

    def test_zero_mrr_returns_nonzero_target(self):
        result = _assess_expansion(_make_input(mrr_sar=0.0))
        assert result["next_mrr_target_sar"] == 0.0


# ---------------------------------------------------------------------------
# Router metadata
# ---------------------------------------------------------------------------


class TestRouterMetadata:
    def test_prefix(self):
        assert router.prefix == "/api/v1/account-expansion"

    def test_tags_contain_sales(self):
        assert "Sales" in router.tags
