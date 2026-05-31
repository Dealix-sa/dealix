"""
Unit tests for api/routers/pricing_psychology.py

Tests cover:
- 6 pricing principles with bilingual names and scripts
- 5 price anchor scripts with trap guidance
- 5 tier psychology entries
- _simulate_price_roi: ROI calculation, tier recommendation
- Router metadata
"""
from __future__ import annotations

import pytest

from api.routers.pricing_psychology import (
    _PRICING_PSYCHOLOGY,
    _PRICE_ANCHOR_SCRIPTS,
    _TIER_PSYCHOLOGY,
    _simulate_price_roi,
    PriceSimulatorInput,
    router,
)


class TestPricingPsychology:
    def test_six_principles(self):
        assert len(_PRICING_PSYCHOLOGY) == 6

    def test_all_bilingual(self):
        for k, v in _PRICING_PSYCHOLOGY.items():
            assert v.get("principle_en"), f"{k} missing principle_en"
            assert v.get("principle_ar"), f"{k} missing principle_ar"

    def test_all_have_script(self):
        for k, v in _PRICING_PSYCHOLOGY.items():
            assert v.get("script_en"), f"{k} missing script_en"

    def test_all_have_avoid(self):
        for k, v in _PRICING_PSYCHOLOGY.items():
            assert v.get("avoid_en"), f"{k} missing avoid_en"

    def test_anchor_high_first_present(self):
        assert "anchor_high_first" in _PRICING_PSYCHOLOGY

    def test_zatca_roi_anchor_present(self):
        assert "zatca_roi_anchor" in _PRICING_PSYCHOLOGY

    def test_ramadan_principle_present(self):
        assert "ramadan_sensitivity" in _PRICING_PSYCHOLOGY

    def test_zatca_avoid_says_reduces_not_guarantees(self):
        avoid = _PRICING_PSYCHOLOGY["zatca_roi_anchor"]["avoid_en"].lower()
        assert "guarantee" not in avoid or "do not" in avoid or "reduces" in avoid

    def test_ramadan_avoid_no_eid_invoices(self):
        avoid = _PRICING_PSYCHOLOGY["ramadan_sensitivity"]["avoid_en"].lower()
        assert "eid" in avoid or "ramadan" in avoid or "proposal" in avoid


class TestPriceAnchorScripts:
    def test_five_scripts(self):
        assert len(_PRICE_ANCHOR_SCRIPTS) == 5

    def test_all_bilingual(self):
        for s in _PRICE_ANCHOR_SCRIPTS:
            assert s.get("scenario_en"), "Missing scenario_en"
            assert s.get("scenario_ar"), "Missing scenario_ar"
            assert s.get("script_en"), "Missing script_en"
            assert s.get("script_ar"), "Missing script_ar"

    def test_all_have_trap_to_avoid(self):
        for s in _PRICE_ANCHOR_SCRIPTS:
            assert s.get("trap_to_avoid_en"), "Missing trap_to_avoid_en"

    def test_discount_script_avoids_discounting(self):
        discount_script = next(s for s in _PRICE_ANCHOR_SCRIPTS if "discount" in s["scenario_en"].lower())
        trap = discount_script["trap_to_avoid_en"].lower()
        assert "discount" in trap

    def test_too_high_script_mentions_roi(self):
        too_high = next(s for s in _PRICE_ANCHOR_SCRIPTS if "too high" in s["scenario_en"].lower())
        script = too_high["script_en"].lower()
        assert "roi" in script or "cost" in script or "savings" in script


class TestTierPsychology:
    def test_five_tiers(self):
        assert len(_TIER_PSYCHOLOGY) == 5

    def test_expected_tiers(self):
        expected = {"free_diagnostic", "sprint_499", "data_pack_1500", "managed_ops_2999_4999", "custom_ai_5k_25k"}
        assert expected == set(_TIER_PSYCHOLOGY.keys())

    def test_all_bilingual(self):
        for k, v in _TIER_PSYCHOLOGY.items():
            assert v.get("tier_en"), f"{k} missing tier_en"
            assert v.get("tier_ar"), f"{k} missing tier_ar"

    def test_all_have_psychology(self):
        for k, v in _TIER_PSYCHOLOGY.items():
            assert v.get("psychology_en"), f"{k} missing psychology_en"

    def test_free_diagnostic_zero_price(self):
        assert "0" in _TIER_PSYCHOLOGY["free_diagnostic"]["price_display"]

    def test_sprint_499_price(self):
        assert "499" in _TIER_PSYCHOLOGY["sprint_499"]["price_display"]

    def test_managed_ops_mentions_analyst_comparison(self):
        psych = _TIER_PSYCHOLOGY["managed_ops_2999_4999"]["psychology_en"].lower()
        assert "analyst" in psych or "employee" in psych or "headcount" in psych


class TestSimulatePriceROI:
    def _base_input(self, **overrides) -> PriceSimulatorInput:
        data = dict(
            annual_manual_reporting_hours=500.0,
            hourly_fully_loaded_cost_sar=100.0,
            zatca_non_compliance_risk_sar=20_000.0,
            missed_deals_per_year=3,
            avg_deal_size_sar=5_000.0,
        )
        data.update(overrides)
        return PriceSimulatorInput(**data)

    def test_total_value_positive(self):
        result = _simulate_price_roi(self._base_input())
        assert result["total_annual_value_sar"] > 0

    def test_reporting_savings_70_pct_of_hours_cost(self):
        result = _simulate_price_roi(self._base_input(
            annual_manual_reporting_hours=100.0,
            hourly_fully_loaded_cost_sar=100.0,
            zatca_non_compliance_risk_sar=0.0,
            missed_deals_per_year=0,
        ))
        # 100 * 100 * 0.7 = 7000
        assert result["annual_reporting_savings_sar"] == pytest.approx(7_000.0)

    def test_zatca_savings_80_pct(self):
        result = _simulate_price_roi(self._base_input(
            annual_manual_reporting_hours=0.0,
            zatca_non_compliance_risk_sar=10_000.0,
            missed_deals_per_year=0,
        ))
        assert result["compliance_savings_sar"] == pytest.approx(8_000.0)

    def test_pipeline_uplift_30_pct(self):
        result = _simulate_price_roi(self._base_input(
            annual_manual_reporting_hours=0.0,
            zatca_non_compliance_risk_sar=0.0,
            missed_deals_per_year=10,
            avg_deal_size_sar=1_000.0,
        ))
        assert result["pipeline_uplift_sar"] == pytest.approx(3_000.0)

    def test_has_recommended_tier(self):
        result = _simulate_price_roi(self._base_input())
        assert result["recommended_tier"] in (
            "free_diagnostic", "sprint_499", "data_pack_1500",
            "managed_ops_2999_4999", "custom_ai"
        )

    def test_high_value_recommends_managed_ops_or_higher(self):
        result = _simulate_price_roi(self._base_input(
            annual_manual_reporting_hours=2000.0,
            zatca_non_compliance_risk_sar=100_000.0,
        ))
        assert result["recommended_tier"] in ("managed_ops_2999_4999", "custom_ai")

    def test_zero_inputs_recommends_free_diagnostic(self):
        result = _simulate_price_roi(PriceSimulatorInput(
            annual_manual_reporting_hours=0.0,
            zatca_non_compliance_risk_sar=0.0,
            missed_deals_per_year=0,
        ))
        assert result["recommended_tier"] == "free_diagnostic"

    def test_payback_months_sprint_positive(self):
        result = _simulate_price_roi(self._base_input())
        assert result["payback_months_sprint"] > 0

    def test_governance_allow_with_review(self):
        result = _simulate_price_roi(self._base_input())
        assert result["governance_decision"] == "ALLOW_WITH_REVIEW"


class TestRouterMetadata:
    def test_router_prefix(self):
        assert router.prefix == "/api/v1/pricing-psychology"

    def test_router_tags(self):
        assert "Sales" in router.tags
