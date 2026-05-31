"""Unit tests for api/routers/retention_risk.py"""
from __future__ import annotations

import pytest

from api.routers.retention_risk import (
    _CHURN_RISK_FACTORS,
    _EARLY_WARNING_INDICATORS,
    _RETENTION_PLAYBOOKS,
    RetentionRiskInput,
    _assess_retention_risk,
    router,
)


def _make_input(**overrides) -> RetentionRiskInput:
    data = dict(
        client_name="Riyadh Tech",
        usage_score=70.0,
        nps_score=8.0,
        months_since_last_expansion=3,
        support_escalations_last_90d=1,
        champion_left=False,
        missed_payments=False,
        contract_expiring_within_90d=False,
        competitor_engaged=False,
    )
    data.update(overrides)
    return RetentionRiskInput(**data)


# ---------------------------------------------------------------------------
# Static data: churn risk factors
# ---------------------------------------------------------------------------


class TestChurnRiskFactors:
    def test_has_eight_factors(self):
        assert len(_CHURN_RISK_FACTORS) == 8

    def test_all_have_factor_id(self):
        for f in _CHURN_RISK_FACTORS:
            assert f.get("factor_id"), f"Factor missing factor_id: {f}"

    def test_all_have_factor_en(self):
        for f in _CHURN_RISK_FACTORS:
            assert f.get("factor_en"), f"Factor {f.get('factor_id')} missing factor_en"

    def test_all_have_factor_ar(self):
        for f in _CHURN_RISK_FACTORS:
            assert f.get("factor_ar"), f"Factor {f.get('factor_id')} missing factor_ar"

    def test_all_have_weight(self):
        for f in _CHURN_RISK_FACTORS:
            assert "weight" in f, f"Factor {f.get('factor_id')} missing weight"

    def test_weights_sum_to_100(self):
        total = sum(f["weight"] for f in _CHURN_RISK_FACTORS)
        assert total == 100

    def test_expected_factor_ids_present(self):
        ids = {f["factor_id"] for f in _CHURN_RISK_FACTORS}
        assert "low_usage" in ids
        assert "champion_left" in ids
        assert "missed_payments" in ids
        assert "no_expansion" in ids
        assert "low_nps" in ids
        assert "support_escalations" in ids
        assert "competitor_engaged" in ids
        assert "contract_expiring_soon" in ids

    def test_low_usage_weight_is_20(self):
        factor = next(f for f in _CHURN_RISK_FACTORS if f["factor_id"] == "low_usage")
        assert factor["weight"] == 20

    def test_champion_left_weight_is_20(self):
        factor = next(f for f in _CHURN_RISK_FACTORS if f["factor_id"] == "champion_left")
        assert factor["weight"] == 20

    def test_missed_payments_weight_is_15(self):
        factor = next(f for f in _CHURN_RISK_FACTORS if f["factor_id"] == "missed_payments")
        assert factor["weight"] == 15


# ---------------------------------------------------------------------------
# Static data: retention playbooks
# ---------------------------------------------------------------------------


class TestRetentionPlaybooks:
    def test_has_three_keys(self):
        assert len(_RETENTION_PLAYBOOKS) == 3

    def test_has_red_key(self):
        assert "red" in _RETENTION_PLAYBOOKS

    def test_has_amber_key(self):
        assert "amber" in _RETENTION_PLAYBOOKS

    def test_has_green_key(self):
        assert "green" in _RETENTION_PLAYBOOKS

    def test_all_have_label_en(self):
        for key, pb in _RETENTION_PLAYBOOKS.items():
            assert pb.get("label_en"), f"Playbook '{key}' missing label_en"

    def test_all_have_label_ar(self):
        for key, pb in _RETENTION_PLAYBOOKS.items():
            assert pb.get("label_ar"), f"Playbook '{key}' missing label_ar"

    def test_all_have_three_actions_en(self):
        for key, pb in _RETENTION_PLAYBOOKS.items():
            assert len(pb.get("actions_en", [])) == 3, f"Playbook '{key}' does not have 3 actions_en"

    def test_all_have_three_actions_ar(self):
        for key, pb in _RETENTION_PLAYBOOKS.items():
            assert len(pb.get("actions_ar", [])) == 3, f"Playbook '{key}' does not have 3 actions_ar"


# ---------------------------------------------------------------------------
# Static data: early warning indicators
# ---------------------------------------------------------------------------


class TestEarlyWarningIndicators:
    def test_has_five_indicators(self):
        assert len(_EARLY_WARNING_INDICATORS) == 5

    def test_all_have_indicator_en(self):
        for i in _EARLY_WARNING_INDICATORS:
            assert i.get("indicator_en"), "Indicator missing indicator_en"

    def test_all_have_indicator_ar(self):
        for i in _EARLY_WARNING_INDICATORS:
            assert i.get("indicator_ar"), "Indicator missing indicator_ar"

    def test_all_have_detection_method_en(self):
        for i in _EARLY_WARNING_INDICATORS:
            assert i.get("detection_method_en"), "Indicator missing detection_method_en"


# ---------------------------------------------------------------------------
# _assess_retention_risk
# ---------------------------------------------------------------------------


class TestAssessRetentionRisk:
    def test_returns_dict(self):
        result = _assess_retention_risk(_make_input())
        assert isinstance(result, dict)

    def test_has_risk_score(self):
        result = _assess_retention_risk(_make_input())
        assert "risk_score" in result

    def test_risk_score_is_numeric(self):
        result = _assess_retention_risk(_make_input())
        assert isinstance(result["risk_score"], (int, float))

    def test_risk_score_in_range_0_100(self):
        result = _assess_retention_risk(_make_input())
        assert 0 <= result["risk_score"] <= 100

    def test_has_risk_label(self):
        result = _assess_retention_risk(_make_input())
        assert "risk_label" in result

    def test_risk_label_valid_values(self):
        result = _assess_retention_risk(_make_input())
        assert result["risk_label"] in {"red", "amber", "green"}

    def test_has_playbook(self):
        result = _assess_retention_risk(_make_input())
        assert "playbook" in result
        assert isinstance(result["playbook"], dict)

    def test_has_top_risk_factors(self):
        result = _assess_retention_risk(_make_input())
        assert "top_risk_factors" in result
        assert isinstance(result["top_risk_factors"], list)

    def test_has_governance_decision(self):
        result = _assess_retention_risk(_make_input())
        assert result["governance_decision"] == "APPROVAL_FIRST"

    def test_has_client_name(self):
        result = _assess_retention_risk(_make_input(client_name="Gulf Bank"))
        assert result["client_name"] == "Gulf Bank"

    def test_has_disclaimer_en(self):
        result = _assess_retention_risk(_make_input())
        assert result.get("disclaimer_en")

    def test_has_disclaimer_ar(self):
        result = _assess_retention_risk(_make_input())
        assert result.get("disclaimer_ar")

    def test_high_risk_scenario_red(self):
        # usage=20 → +20, champion_left → +20, missed_payments → +15, nps=4 → +15 = 70
        result = _assess_retention_risk(
            _make_input(
                usage_score=20,
                nps_score=4,
                champion_left=True,
                missed_payments=True,
            )
        )
        assert result["risk_label"] == "red"

    def test_high_risk_score_above_60(self):
        # usage=20 → +20, champion_left → +20, missed_payments → +15, nps=4 → +15 = 70
        result = _assess_retention_risk(
            _make_input(
                usage_score=20,
                nps_score=4,
                champion_left=True,
                missed_payments=True,
            )
        )
        assert result["risk_score"] >= 60

    def test_low_risk_scenario_green(self):
        result = _assess_retention_risk(
            _make_input(
                usage_score=90,
                nps_score=9,
                months_since_last_expansion=1,
                support_escalations_last_90d=0,
                champion_left=False,
                missed_payments=False,
                contract_expiring_within_90d=False,
                competitor_engaged=False,
            )
        )
        assert result["risk_label"] == "green"

    def test_low_risk_score_below_30(self):
        result = _assess_retention_risk(
            _make_input(
                usage_score=90,
                nps_score=9,
                months_since_last_expansion=1,
                support_escalations_last_90d=0,
            )
        )
        assert result["risk_score"] < 30

    def test_medium_risk_scenario_amber(self):
        # usage=50 → +10, no expansion >6m → +10, nps=7.5 → +7 = 27 → amber (≥30 needed)
        # Add support escalations: 2*3=6 → total 33 → amber
        result = _assess_retention_risk(
            _make_input(
                usage_score=50,
                nps_score=7.5,
                months_since_last_expansion=8,
                support_escalations_last_90d=2,
                champion_left=False,
                missed_payments=False,
            )
        )
        assert result["risk_label"] == "amber"

    def test_playbook_matches_label(self):
        result = _assess_retention_risk(
            _make_input(
                usage_score=20,
                champion_left=True,
                missed_payments=True,
            )
        )
        label = result["risk_label"]
        assert result["playbook"] == _RETENTION_PLAYBOOKS[label]

    def test_top_risk_factors_low_usage(self):
        result = _assess_retention_risk(_make_input(usage_score=30))
        assert "low_usage" in result["top_risk_factors"]

    def test_top_risk_factors_champion_left(self):
        result = _assess_retention_risk(_make_input(champion_left=True))
        assert "champion_left" in result["top_risk_factors"]

    def test_top_risk_factors_missed_payments(self):
        result = _assess_retention_risk(_make_input(missed_payments=True))
        assert "missed_payments" in result["top_risk_factors"]

    def test_top_risk_factors_competitor_engaged(self):
        result = _assess_retention_risk(_make_input(competitor_engaged=True))
        assert "competitor_engaged" in result["top_risk_factors"]

    def test_top_risk_factors_contract_expiring(self):
        result = _assess_retention_risk(_make_input(contract_expiring_within_90d=True))
        assert "contract_expiring_soon" in result["top_risk_factors"]

    def test_support_escalations_contribute(self):
        result_zero = _assess_retention_risk(_make_input(support_escalations_last_90d=0))
        result_three = _assess_retention_risk(_make_input(support_escalations_last_90d=3))
        assert result_three["risk_score"] > result_zero["risk_score"]

    def test_risk_score_capped_at_100(self):
        result = _assess_retention_risk(
            _make_input(
                usage_score=10,
                nps_score=4,
                months_since_last_expansion=12,
                support_escalations_last_90d=10,
                champion_left=True,
                missed_payments=True,
                contract_expiring_within_90d=True,
                competitor_engaged=True,
            )
        )
        assert result["risk_score"] <= 100

    def test_no_factors_healthy_account(self):
        result = _assess_retention_risk(
            _make_input(
                usage_score=95,
                nps_score=9,
                months_since_last_expansion=2,
                support_escalations_last_90d=0,
            )
        )
        assert result["risk_label"] == "green"
        assert result["risk_score"] == 0


# ---------------------------------------------------------------------------
# Router metadata
# ---------------------------------------------------------------------------


class TestRouterMetadata:
    def test_prefix(self):
        assert router.prefix == "/api/v1/retention-risk"

    def test_tags_contain_analytics(self):
        assert "Analytics" in router.tags
