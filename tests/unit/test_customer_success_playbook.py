"""
Unit tests for api/routers/customer_success_playbook.py

Tests cover:
- Playbook stages: 5 stages present, bilingual, goals
- Onboarding stage: 4-week plan, success metrics, churn signals
- _health_score: high/low/critical scoring, risk factor detection
- Health bands: Healthy/At Risk/Critical/Churning
- Recommended stage routing
- Router metadata
"""
from __future__ import annotations

import pytest

from api.routers.customer_success_playbook import (
    _PLAYBOOKS,
    _health_score,
    AccountHealthInput,
    router,
)


class TestPlaybookData:
    def test_five_stages(self):
        expected = {"onboarding", "value_realization", "expansion", "renewal", "churn_risk"}
        assert expected == set(_PLAYBOOKS.keys())

    def test_all_have_bilingual_names(self):
        for sid, s in _PLAYBOOKS.items():
            assert s.get("name_ar"), f"{sid} missing name_ar"
            assert s.get("name_en"), f"{sid} missing name_en"

    def test_all_have_goals(self):
        for sid, s in _PLAYBOOKS.items():
            assert s.get("goal_en"), f"{sid} missing goal_en"
            assert s.get("goal_ar"), f"{sid} missing goal_ar"

    def test_onboarding_has_weekly_actions(self):
        onboarding = _PLAYBOOKS["onboarding"]
        assert len(onboarding.get("weekly_actions", [])) == 4

    def test_onboarding_weeks_1_to_4(self):
        onboarding = _PLAYBOOKS["onboarding"]
        weeks = [w["week"] for w in onboarding["weekly_actions"]]
        assert weeks == [1, 2, 3, 4]

    def test_onboarding_has_pdpl_in_week1(self):
        week1 = _PLAYBOOKS["onboarding"]["weekly_actions"][0]
        actions_text = " ".join(week1["actions_en"]).lower()
        assert "pdpl" in actions_text or "data processing" in actions_text

    def test_renewal_has_saudi_timing(self):
        renewal = _PLAYBOOKS["renewal"]
        assert renewal.get("saudi_timing_en")
        assert renewal.get("saudi_timing_ar")

    def test_renewal_timing_mentions_ramadan(self):
        timing = _PLAYBOOKS["renewal"]["saudi_timing_en"].lower()
        assert "ramadan" in timing

    def test_churn_risk_has_risk_signals(self):
        churn = _PLAYBOOKS["churn_risk"]
        assert len(churn.get("risk_signals", [])) >= 5

    def test_expansion_has_upsell_paths(self):
        expansion = _PLAYBOOKS["expansion"]
        assert len(expansion.get("upsell_paths", [])) >= 3

    def test_all_stages_have_churn_warning_signs(self):
        for sid, s in _PLAYBOOKS.items():
            assert "churn_warning_signs" in s, f"{sid} missing churn_warning_signs"

    def test_onboarding_has_success_metrics(self):
        metrics = _PLAYBOOKS["onboarding"]["success_metrics"]
        assert len(metrics) >= 3


class TestHealthScoring:
    def _healthy_input(self, **overrides) -> AccountHealthInput:
        data = dict(
            account_name="ACME Saudi",
            months_active=6,
            last_login_days_ago=1,
            nps_score=9.0,
            roi_reports_opened_pct=80.0,
            check_ins_missed_last_30d=0,
            champion_active=True,
            competitor_poc_running=False,
        )
        data.update(overrides)
        return AccountHealthInput(**data)

    def test_healthy_account_scores_80_plus(self):
        result = _health_score(self._healthy_input())
        assert result["health_score"] >= 80

    def test_healthy_band_is_healthy(self):
        result = _health_score(self._healthy_input())
        assert result["health_band"] == "Healthy"

    def test_no_login_14_days_drops_score(self):
        healthy = _health_score(self._healthy_input())["health_score"]
        no_login = _health_score(self._healthy_input(last_login_days_ago=15))["health_score"]
        assert no_login < healthy

    def test_no_login_generates_risk_factor(self):
        result = _health_score(self._healthy_input(last_login_days_ago=15))
        risk_texts = " ".join(result["risk_factors"]).lower()
        assert "login" in risk_texts

    def test_low_nps_drops_score(self):
        healthy = _health_score(self._healthy_input())["health_score"]
        low_nps = _health_score(self._healthy_input(nps_score=5.0))["health_score"]
        assert low_nps < healthy

    def test_low_nps_generates_risk_factor(self):
        result = _health_score(self._healthy_input(nps_score=5.0))
        risk_texts = " ".join(result["risk_factors"]).lower()
        assert "nps" in risk_texts

    def test_missed_checkins_drop_score(self):
        healthy = _health_score(self._healthy_input())["health_score"]
        missed = _health_score(self._healthy_input(check_ins_missed_last_30d=2))["health_score"]
        assert missed < healthy

    def test_champion_inactive_is_critical_risk(self):
        result = _health_score(self._healthy_input(champion_active=False))
        risk_texts = " ".join(result["risk_factors"]).lower()
        assert "champion" in risk_texts

    def test_competitor_poc_drops_score(self):
        healthy = _health_score(self._healthy_input())["health_score"]
        with_poc = _health_score(self._healthy_input(competitor_poc_running=True))["health_score"]
        assert with_poc < healthy

    def test_all_risks_combined_is_critical(self):
        result = _health_score(self._healthy_input(
            last_login_days_ago=20,
            nps_score=4.0,
            roi_reports_opened_pct=10.0,
            check_ins_missed_last_30d=3,
            champion_active=False,
            competitor_poc_running=True,
        ))
        assert result["health_band"] in ("Critical", "Churning")
        assert result["immediate_action_needed"] is True

    def test_score_cannot_go_negative(self):
        result = _health_score(self._healthy_input(
            last_login_days_ago=30,
            nps_score=1.0,
            roi_reports_opened_pct=0.0,
            check_ins_missed_last_30d=5,
            champion_active=False,
            competitor_poc_running=True,
        ))
        assert result["health_score"] >= 0

    def test_expansion_recommended_for_very_healthy(self):
        result = _health_score(self._healthy_input())
        assert result["recommended_playbook_stage"] == "expansion"

    def test_churn_risk_recommended_for_low_score(self):
        result = _health_score(self._healthy_input(
            last_login_days_ago=20,
            nps_score=4.0,
            roi_reports_opened_pct=10.0,
            check_ins_missed_last_30d=3,
            champion_active=False,
        ))
        assert result["recommended_playbook_stage"] == "churn_risk"


class TestRouterMetadata:
    def test_router_prefix(self):
        assert router.prefix == "/api/v1/customer-success"

    def test_router_tags(self):
        assert "Analytics" in router.tags
