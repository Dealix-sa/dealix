"""Unit tests for api/routers/pricing_simulator.py"""
from __future__ import annotations

import pytest
from fastapi import HTTPException

from api.routers.pricing_simulator import (
    _DEAL_STRUCTURES,
    _PAYMENT_INCENTIVES,
    _VALID_DEAL_STRUCTURES,
    DealStructureInput,
    _simulate_deal,
    router,
)


def _make_input(**overrides) -> DealStructureInput:
    data = dict(
        base_price_sar=10_000.0,
        deal_structure="monthly",
        apply_incentives=[],
        headcount=1,
    )
    data.update(overrides)
    return DealStructureInput(**data)


# ---------------------------------------------------------------------------
# Static data: _DEAL_STRUCTURES
# ---------------------------------------------------------------------------


class TestDealStructures:
    def test_has_four_keys(self):
        assert len(_DEAL_STRUCTURES) == 4

    def test_contains_monthly(self):
        assert "monthly" in _DEAL_STRUCTURES

    def test_contains_quarterly(self):
        assert "quarterly" in _DEAL_STRUCTURES

    def test_contains_annual(self):
        assert "annual" in _DEAL_STRUCTURES

    def test_contains_multi_year(self):
        assert "multi_year" in _DEAL_STRUCTURES

    def test_all_have_name_en(self):
        for key, data in _DEAL_STRUCTURES.items():
            assert data.get("name_en"), f"{key} missing name_en"

    def test_all_have_name_ar(self):
        for key, data in _DEAL_STRUCTURES.items():
            assert data.get("name_ar"), f"{key} missing name_ar"

    def test_all_have_discount_pct(self):
        for key, data in _DEAL_STRUCTURES.items():
            assert "discount_pct" in data, f"{key} missing discount_pct"

    def test_all_have_commitment_months(self):
        for key, data in _DEAL_STRUCTURES.items():
            assert "commitment_months" in data, f"{key} missing commitment_months"

    def test_all_have_payment_terms_en(self):
        for key, data in _DEAL_STRUCTURES.items():
            assert data.get("payment_terms_en"), f"{key} missing payment_terms_en"

    def test_all_have_payment_terms_ar(self):
        for key, data in _DEAL_STRUCTURES.items():
            assert data.get("payment_terms_ar"), f"{key} missing payment_terms_ar"

    def test_multi_year_higher_discount_than_monthly(self):
        assert _DEAL_STRUCTURES["multi_year"]["discount_pct"] > _DEAL_STRUCTURES["monthly"]["discount_pct"]

    def test_monthly_discount_pct_is_zero(self):
        assert _DEAL_STRUCTURES["monthly"]["discount_pct"] == 0.0

    def test_annual_discount_pct_is_15(self):
        assert _DEAL_STRUCTURES["annual"]["discount_pct"] == 15.0

    def test_multi_year_discount_pct_is_25(self):
        assert _DEAL_STRUCTURES["multi_year"]["discount_pct"] == 25.0

    def test_monthly_commitment_months_is_1(self):
        assert _DEAL_STRUCTURES["monthly"]["commitment_months"] == 1

    def test_multi_year_commitment_months_is_24(self):
        assert _DEAL_STRUCTURES["multi_year"]["commitment_months"] == 24


# ---------------------------------------------------------------------------
# Static data: _PAYMENT_INCENTIVES
# ---------------------------------------------------------------------------


class TestPaymentIncentives:
    def test_has_four_items(self):
        assert len(_PAYMENT_INCENTIVES) == 4

    def test_all_have_incentive_en(self):
        for item in _PAYMENT_INCENTIVES:
            assert item.get("incentive_en"), f"Item missing incentive_en"

    def test_all_have_incentive_ar(self):
        for item in _PAYMENT_INCENTIVES:
            assert item.get("incentive_ar"), f"Item missing incentive_ar"

    def test_all_have_discount_addl_pct(self):
        for item in _PAYMENT_INCENTIVES:
            assert "discount_addl_pct" in item

    def test_early_payment_30d_discount(self):
        item = next(i for i in _PAYMENT_INCENTIVES if i["incentive_id"] == "early_payment_30d")
        assert item["discount_addl_pct"] == 3.0

    def test_reference_customer_discount(self):
        item = next(i for i in _PAYMENT_INCENTIVES if i["incentive_id"] == "reference_customer")
        assert item["discount_addl_pct"] == 5.0

    def test_case_study_rights_discount(self):
        item = next(i for i in _PAYMENT_INCENTIVES if i["incentive_id"] == "case_study_rights")
        assert item["discount_addl_pct"] == 3.0

    def test_visa_payment_discount(self):
        item = next(i for i in _PAYMENT_INCENTIVES if i["incentive_id"] == "visa_payment")
        assert item["discount_addl_pct"] == 2.0


# ---------------------------------------------------------------------------
# _simulate_deal
# ---------------------------------------------------------------------------


class TestSimulateDeal:
    def test_returns_dict(self):
        result = _simulate_deal(_make_input())
        assert isinstance(result, dict)

    def test_has_total_contract_value_sar(self):
        result = _simulate_deal(_make_input())
        assert "total_contract_value_sar" in result

    def test_has_discounted_price_sar(self):
        result = _simulate_deal(_make_input())
        assert "discounted_price_sar" in result

    def test_has_total_discount_pct(self):
        result = _simulate_deal(_make_input())
        assert "total_discount_pct" in result

    def test_has_savings_vs_monthly_sar(self):
        result = _simulate_deal(_make_input())
        assert "savings_vs_monthly_sar" in result

    def test_monthly_no_base_discount(self):
        result = _simulate_deal(_make_input(deal_structure="monthly"))
        assert result["base_discount_pct"] == 0.0

    def test_annual_base_discount_15_pct(self):
        result = _simulate_deal(_make_input(deal_structure="annual"))
        assert result["base_discount_pct"] == 15.0

    def test_applying_incentive_reduces_price(self):
        without = _simulate_deal(_make_input(deal_structure="monthly"))
        with_ = _simulate_deal(_make_input(deal_structure="monthly", apply_incentives=["early_payment_30d"]))
        assert with_["discounted_price_sar"] < without["discounted_price_sar"]

    def test_total_discount_pct_caps_at_40(self):
        result = _simulate_deal(
            _make_input(
                deal_structure="multi_year",
                apply_incentives=["early_payment_30d", "reference_customer", "case_study_rights", "visa_payment"],
            )
        )
        assert result["total_discount_pct"] <= 40.0

    def test_savings_vs_monthly_sar_non_negative(self):
        result = _simulate_deal(_make_input(deal_structure="annual"))
        assert result["savings_vs_monthly_sar"] >= 0

    def test_monthly_savings_vs_monthly_is_zero(self):
        result = _simulate_deal(_make_input(deal_structure="monthly"))
        assert result["savings_vs_monthly_sar"] == 0.0

    def test_total_contract_value_matches_formula(self):
        inp = _make_input(deal_structure="annual", headcount=3)
        result = _simulate_deal(inp)
        expected = result["discounted_price_sar"] * 3 * 12
        assert abs(result["total_contract_value_sar"] - expected) < 0.01

    def test_unknown_incentive_ids_ignored(self):
        result = _simulate_deal(_make_input(apply_incentives=["nonexistent_incentive"]))
        assert result["incentive_discount_pct"] == 0.0

    def test_invalid_deal_structure_raises_http_422(self):
        with pytest.raises(HTTPException) as exc_info:
            _simulate_deal(_make_input(deal_structure="biennial"))
        assert exc_info.value.status_code == 422

    def test_all_four_valid_structures_work(self):
        for structure in _VALID_DEAL_STRUCTURES:
            result = _simulate_deal(_make_input(deal_structure=structure))
            assert result["deal_structure"] == structure

    def test_governance_decision_is_approval_first(self):
        result = _simulate_deal(_make_input())
        assert result["governance_decision"] == "APPROVAL_FIRST"

    def test_headcount_multiplies_contract_value(self):
        result_1 = _simulate_deal(_make_input(deal_structure="annual", headcount=1))
        result_5 = _simulate_deal(_make_input(deal_structure="annual", headcount=5))
        assert abs(result_5["total_contract_value_sar"] - result_1["total_contract_value_sar"] * 5) < 0.01

    def test_multi_year_higher_savings_than_annual(self):
        result_annual = _simulate_deal(
            _make_input(deal_structure="annual", base_price_sar=1000.0)
        )
        result_multi = _simulate_deal(
            _make_input(deal_structure="multi_year", base_price_sar=1000.0)
        )
        assert result_multi["savings_vs_monthly_sar"] > result_annual["savings_vs_monthly_sar"]

    def test_incentives_sum_correctly(self):
        result = _simulate_deal(
            _make_input(
                deal_structure="monthly",
                apply_incentives=["early_payment_30d", "visa_payment"],
            )
        )
        assert result["incentive_discount_pct"] == 5.0


# ---------------------------------------------------------------------------
# Router metadata
# ---------------------------------------------------------------------------


class TestRouterMetadata:
    def test_prefix(self):
        assert router.prefix == "/api/v1/pricing-simulator"

    def test_tags_contain_sales(self):
        assert "Sales" in router.tags
