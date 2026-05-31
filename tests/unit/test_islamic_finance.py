"""
Unit tests for api/routers/islamic_finance.py

Tests cover:
- Structure list: 4 structures present, bilingual descriptions
- Compliance checklist: 7 items, riba/gharar/SAMA present
- Murabaha calculator: principal + profit = total, monthly installment math
- Ijara calculator: monthly rental calculation, purchase option
- Router metadata
"""
from __future__ import annotations

import pytest

from api.routers.islamic_finance import (
    _STRUCTURES,
    _STRUCTURE_BY_ID,
    _COMPLIANCE_CHECKLIST,
    _calculate_murabaha,
    _calculate_ijara,
    MurabahaInput,
    IjaraInput,
    router,
)


class TestStructureData:
    def test_four_structures(self):
        assert len(_STRUCTURES) == 4

    def test_has_murabaha(self):
        assert "murabaha" in _STRUCTURE_BY_ID

    def test_has_ijara(self):
        assert "ijara" in _STRUCTURE_BY_ID

    def test_has_musharaka(self):
        assert "musharaka" in _STRUCTURE_BY_ID

    def test_has_istisna(self):
        assert "istisna" in _STRUCTURE_BY_ID

    def test_all_have_bilingual_descriptions(self):
        for s in _STRUCTURES:
            assert s.get("description_ar"), f"{s['id']} missing description_ar"
            assert s.get("description_en"), f"{s['id']} missing description_en"

    def test_all_have_sharia_requirements(self):
        for s in _STRUCTURES:
            assert s.get("sharia_requirements"), f"{s['id']} missing requirements"
            assert len(s["sharia_requirements"]) >= 2

    def test_murabaha_no_interest_mentioned(self):
        # Should emphasize no-riba
        murabaha = _STRUCTURE_BY_ID["murabaha"]
        desc = murabaha["description_en"].lower()
        assert "no interest" in desc or "profit" in desc

    def test_all_have_saudi_banks(self):
        for s in _STRUCTURES:
            assert s.get("saudi_banks_offering"), f"{s['id']} missing banks"


class TestComplianceChecklist:
    def test_at_least_six_items(self):
        assert len(_COMPLIANCE_CHECKLIST) >= 6

    def test_riba_item_present(self):
        items = [c["item"].lower() for c in _COMPLIANCE_CHECKLIST]
        assert any("riba" in i or "interest" in i for i in items)

    def test_gharar_item_present(self):
        items = [c["item"].lower() for c in _COMPLIANCE_CHECKLIST]
        assert any("gharar" in i or "uncertainty" in i for i in items)

    def test_sama_item_present(self):
        items = [c["item"].lower() for c in _COMPLIANCE_CHECKLIST]
        assert any("sama" in i for i in items)

    def test_all_items_have_bilingual_checks(self):
        for item in _COMPLIANCE_CHECKLIST:
            assert item.get("check_en"), f"Missing check_en for {item['item']}"
            assert item.get("check_ar"), f"Missing check_ar for {item['item']}"

    def test_all_items_have_arabic_name(self):
        for item in _COMPLIANCE_CHECKLIST:
            assert item.get("item_ar"), f"Missing item_ar for {item['item']}"


class TestMurabahaCalculator:
    def _basic_input(self, **overrides) -> MurabahaInput:
        data = dict(
            principal_sar=100_000,
            profit_rate_annual_pct=5.0,
            term_months=12,
        )
        data.update(overrides)
        return MurabahaInput(**data)

    def test_total_amount_equals_principal_plus_profit(self):
        result = _calculate_murabaha(self._basic_input())
        expected_total = 100_000 + 100_000 * 0.05 * (12 / 12)
        assert abs(result["total_amount_sar"] - expected_total) < 0.01

    def test_monthly_installment_times_months_equals_total(self):
        result = _calculate_murabaha(self._basic_input())
        computed = result["monthly_installment_sar"] * 12
        assert abs(computed - result["total_amount_sar"]) < 1.0

    def test_longer_term_larger_total_profit(self):
        short = _calculate_murabaha(self._basic_input(term_months=12))
        long_ = _calculate_murabaha(self._basic_input(term_months=60))
        assert long_["total_profit_sar"] > short["total_profit_sar"]

    def test_higher_rate_larger_profit(self):
        low = _calculate_murabaha(self._basic_input(profit_rate_annual_pct=3.0))
        high = _calculate_murabaha(self._basic_input(profit_rate_annual_pct=8.0))
        assert high["total_profit_sar"] > low["total_profit_sar"]

    def test_structure_field_is_murabaha(self):
        result = _calculate_murabaha(self._basic_input())
        assert result["structure"] == "murabaha"

    def test_schedule_sample_present(self):
        result = _calculate_murabaha(self._basic_input())
        assert "schedule_sample" in result
        assert len(result["schedule_sample"]) >= 3

    def test_first_period_is_1(self):
        result = _calculate_murabaha(self._basic_input())
        first = result["schedule_sample"][0]
        assert first["period"] == 1

    def test_500k_sar_5pct_12m(self):
        result = _calculate_murabaha(self._basic_input(
            principal_sar=500_000, profit_rate_annual_pct=5.0, term_months=12
        ))
        expected_profit = 500_000 * 0.05
        assert abs(result["total_profit_sar"] - expected_profit) < 0.01

    def test_zero_profit_impossible(self):
        # profit_rate must be > 0
        with pytest.raises(Exception):
            MurabahaInput(principal_sar=100_000, profit_rate_annual_pct=0, term_months=12)


class TestIjaraCalculator:
    def _basic_input(self, **overrides) -> IjaraInput:
        data = dict(
            asset_value_sar=500_000,
            rental_rate_annual_pct=6.0,
            term_months=24,
            purchase_option=False,
            residual_value_pct=10.0,
        )
        data.update(overrides)
        return IjaraInput(**data)

    def test_monthly_rental_calculation(self):
        result = _calculate_ijara(self._basic_input())
        expected = 500_000 * 0.06 / 12
        assert abs(result["monthly_rental_sar"] - expected) < 0.01

    def test_total_rentals_equals_monthly_times_term(self):
        result = _calculate_ijara(self._basic_input())
        assert abs(result["total_rentals_sar"] - result["monthly_rental_sar"] * 24) < 0.01

    def test_no_purchase_option(self):
        result = _calculate_ijara(self._basic_input(purchase_option=False))
        assert result["purchase_price_at_end_sar"] is None
        assert result["total_cost_if_purchased_sar"] is None

    def test_with_purchase_option(self):
        result = _calculate_ijara(self._basic_input(
            purchase_option=True, residual_value_pct=10.0
        ))
        expected_purchase = 500_000 * 0.10
        assert abs(result["purchase_price_at_end_sar"] - expected_purchase) < 0.01

    def test_total_cost_with_purchase(self):
        result = _calculate_ijara(self._basic_input(
            purchase_option=True, residual_value_pct=10.0
        ))
        expected = result["total_rentals_sar"] + result["purchase_price_at_end_sar"]
        assert abs(result["total_cost_if_purchased_sar"] - expected) < 0.01

    def test_structure_field_is_ijara(self):
        result = _calculate_ijara(self._basic_input())
        assert result["structure"] == "ijara"


class TestRouterMetadata:
    def test_router_prefix(self):
        assert router.prefix == "/api/v1/islamic-finance"

    def test_router_tags(self):
        assert "Saudi Market" in router.tags
