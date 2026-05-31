"""
Unit tests for api/routers/account_plan.py

Tests cover:
- Account plan template sections
- 3 account tiers (strategic, growth, standard)
- _build_account_plan: tier selection, milestones, client name
- Router metadata
"""
from __future__ import annotations

import pytest

from api.routers.account_plan import (
    _ACCOUNT_PLAN_TEMPLATE,
    _ACCOUNT_TIERS,
    _build_account_plan,
    AccountPlanInput,
    router,
)


class TestAccountPlanTemplate:
    def test_template_is_dict(self):
        assert isinstance(_ACCOUNT_PLAN_TEMPLATE, dict)

    def test_template_has_key_sections(self):
        keys = set(_ACCOUNT_PLAN_TEMPLATE.keys())
        # Should have at least stakeholder_map, milestones, risk_register
        assert len(keys) >= 4

    def test_template_has_milestones(self):
        assert any("milestone" in k.lower() for k in _ACCOUNT_PLAN_TEMPLATE.keys())

    def test_template_has_risk_register(self):
        keys = " ".join(_ACCOUNT_PLAN_TEMPLATE.keys()).lower()
        assert "risk" in keys


class TestAccountTiers:
    def test_three_tiers(self):
        assert len(_ACCOUNT_TIERS) == 3

    def test_tiers_are_strategic_growth_standard(self):
        assert set(_ACCOUNT_TIERS.keys()) == {"strategic", "growth", "standard"}

    def test_all_bilingual(self):
        for k, v in _ACCOUNT_TIERS.items():
            assert v.get("name_en"), f"{k} missing name_en"
            assert v.get("name_ar"), f"{k} missing name_ar"

    def test_strategic_has_highest_minimum(self):
        strategic_min = _ACCOUNT_TIERS["strategic"].get("annual_revenue_sar_min", 0)
        standard_min = _ACCOUNT_TIERS["standard"].get("annual_revenue_sar_min", 0)
        assert strategic_min > standard_min

    def test_all_have_cadence(self):
        for k, v in _ACCOUNT_TIERS.items():
            assert v.get("cadence_en"), f"{k} missing cadence_en"


class TestBuildAccountPlan:
    def _make_input(self, **overrides) -> AccountPlanInput:
        data = dict(
            client_name="ACME Saudi",
            client_sector="fintech",
            estimated_annual_revenue_sar=60_000.0,
            champion_name="Mohammed Al-Rashid",
            champion_title="VP Sales",
            identified_pains=["Manual reporting", "No pipeline visibility"],
            current_stage="onboarding",
            months_as_client=1,
        )
        data.update(overrides)
        return AccountPlanInput(**data)

    def test_returns_dict(self):
        result = _build_account_plan(self._make_input())
        assert isinstance(result, dict)

    def test_client_name_appears_in_plan(self):
        result = _build_account_plan(self._make_input())
        plan_text = str(result).lower()
        assert "acme saudi" in plan_text

    def test_has_milestones_section(self):
        result = _build_account_plan(self._make_input())
        assert "milestones" in result

    def test_has_risk_register(self):
        result = _build_account_plan(self._make_input())
        assert "risk_register" in result

    def test_has_stakeholder_map(self):
        result = _build_account_plan(self._make_input())
        assert "stakeholder_map" in result

    def test_has_success_metrics(self):
        result = _build_account_plan(self._make_input())
        assert "success_metrics" in result

    def test_has_executive_summary(self):
        result = _build_account_plan(self._make_input())
        assert "executive_summary" in result

    def test_high_revenue_gets_strategic_tier(self):
        result = _build_account_plan(self._make_input(estimated_annual_revenue_sar=75_000))
        tier_section = result.get("account_tier_detail") or result.get("plan_meta") or {}
        tier_text = str(tier_section).lower()
        assert "strategic" in tier_text

    def test_low_revenue_gets_standard_tier(self):
        result = _build_account_plan(self._make_input(estimated_annual_revenue_sar=8_000))
        tier_section = result.get("account_tier_detail") or result.get("plan_meta") or {}
        tier_text = str(tier_section).lower()
        assert "standard" in tier_text

    @pytest.mark.parametrize("stage", ["onboarding", "value_realization", "expansion", "renewal"])
    def test_all_stages_build_successfully(self, stage):
        result = _build_account_plan(self._make_input(current_stage=stage))
        assert isinstance(result, dict)
        assert len(result) > 0

    def test_valid_stages_all_accepted(self):
        for stage in ["onboarding", "value_realization", "expansion", "renewal"]:
            inp = AccountPlanInput(
                client_name="Test",
                client_sector="tech",
                estimated_annual_revenue_sar=5000.0,
                champion_name="Ahmed",
                champion_title="Manager",
                identified_pains=["pain"],
                current_stage=stage,
                months_as_client=0,
            )
            assert inp.current_stage == stage

    def test_empty_pains_rejected(self):
        with pytest.raises(Exception):
            AccountPlanInput(
                client_name="Test",
                client_sector="tech",
                estimated_annual_revenue_sar=5000.0,
                champion_name="Ahmed",
                champion_title="Manager",
                identified_pains=[],  # min_length=1
                current_stage="onboarding",
                months_as_client=0,
            )


class TestRouterMetadata:
    def test_router_prefix(self):
        assert router.prefix == "/api/v1/account-plan"

    def test_router_tags(self):
        assert "Sales" in router.tags
