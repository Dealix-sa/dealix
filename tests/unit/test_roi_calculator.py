"""
Unit tests for api/routers/roi_calculator.py

Tests cover:
- Labor benchmark data structure
- _calculate_labor_savings with known inputs
- _npv correctness
- _irr convergence on known case
- _payback_months arithmetic
- calculate_roi end-to-end with benchmark roles
- Quick estimate math
"""
from __future__ import annotations

import pytest

from api.routers.roi_calculator import (
    _LABOR_BENCHMARKS,
    _calculate_labor_savings,
    _npv,
    _irr,
    _payback_months,
    calculate_roi,
    AutomationROIInput,
    router,
)


class TestLaborBenchmarks:
    def test_has_data_entry(self):
        assert "data_entry_clerk" in _LABOR_BENCHMARKS

    def test_all_have_required_fields(self):
        for role_id, bench in _LABOR_BENCHMARKS.items():
            assert bench.get("title_ar"), f"{role_id} missing title_ar"
            assert bench.get("title_en"), f"{role_id} missing title_en"
            assert bench.get("monthly_salary_sar", 0) > 0
            assert bench.get("fully_loaded_multiplier", 0) > 1
            assert 0 < bench.get("automatable_pct", 0) <= 100

    def test_data_entry_highest_automatable(self):
        data_entry_pct = _LABOR_BENCHMARKS["data_entry_clerk"]["automatable_pct"]
        assert data_entry_pct >= 80

    def test_fully_loaded_multiplier_range(self):
        for bench in _LABOR_BENCHMARKS.values():
            assert 1.2 <= bench["fully_loaded_multiplier"] <= 2.0


class TestLaborSavingsCalculation:
    def test_single_role_calculation(self):
        inp = AutomationROIInput(
            project_name="Test",
            implementation_cost_sar=100_000,
            annual_maintenance_cost_sar=0,
            roles_automated=["data_entry_clerk"],
            headcount_per_role={"data_entry_clerk": 1},
            projection_years=3,
            discount_rate_pct=10,
        )
        bench = _LABOR_BENCHMARKS["data_entry_clerk"]
        expected = (
            bench["monthly_salary_sar"]
            * bench["fully_loaded_multiplier"]
            * 12
            * bench["automatable_pct"]
            / 100
        )
        savings = _calculate_labor_savings(inp)
        assert abs(savings - expected) < 1.0

    def test_two_roles_adds_up(self):
        inp = AutomationROIInput(
            project_name="Test",
            implementation_cost_sar=100_000,
            roles_automated=["data_entry_clerk", "customer_service_agent"],
            headcount_per_role={"data_entry_clerk": 2, "customer_service_agent": 1},
            projection_years=3,
            discount_rate_pct=10,
        )
        savings = _calculate_labor_savings(inp)
        assert savings > 0

    def test_more_headcount_means_more_savings(self):
        def make_inp(count):
            return AutomationROIInput(
                project_name="Test",
                implementation_cost_sar=100_000,
                roles_automated=["data_entry_clerk"],
                headcount_per_role={"data_entry_clerk": count},
                projection_years=3,
                discount_rate_pct=10,
            )
        assert _calculate_labor_savings(make_inp(2)) > _calculate_labor_savings(make_inp(1))

    def test_empty_roles_zero_savings(self):
        inp = AutomationROIInput(
            project_name="Test",
            implementation_cost_sar=100_000,
            roles_automated=[],
            projection_years=3,
            discount_rate_pct=10,
        )
        assert _calculate_labor_savings(inp) == 0.0


class TestNPV:
    def test_zero_rate_equals_sum(self):
        cash_flows = [-100, 50, 50, 50]
        assert abs(_npv(cash_flows, 0.0) - 50) < 0.01

    def test_positive_npv_for_good_project(self):
        # Invest 100, get 200 in year 1 at 10% rate
        assert _npv([-100, 200], 0.10) > 0

    def test_negative_npv_for_bad_project(self):
        assert _npv([-100, 10], 0.10) < 0

    def test_higher_rate_lower_npv(self):
        flows = [-100, 40, 40, 40]
        assert _npv(flows, 0.05) > _npv(flows, 0.15)


class TestIRR:
    def test_known_irr(self):
        # -100, +121 in year 1 → IRR = 21%
        irr = _irr([-100, 121])
        assert irr is not None
        assert abs(irr - 21.0) < 0.5

    def test_all_positive_returns_none(self):
        assert _irr([100, 200]) is None

    def test_typical_project_irr(self):
        # -1000, +400, +400, +400
        irr = _irr([-1000, 400, 400, 400])
        assert irr is not None
        assert 0 < irr < 50


class TestPayback:
    def test_simple_case(self):
        result = _payback_months(120_000, 60_000)
        assert abs(result - 24.0) < 0.1

    def test_zero_benefit_returns_none(self):
        assert _payback_months(100_000, 0) is None

    def test_negative_benefit_returns_none(self):
        assert _payback_months(100_000, -1) is None


class TestCalculateROI:
    def _strong_input(self) -> AutomationROIInput:
        return AutomationROIInput(
            project_name="Data Entry Automation",
            implementation_cost_sar=100_000,
            annual_maintenance_cost_sar=12_000,
            roles_automated=["data_entry_clerk"],
            headcount_per_role={"data_entry_clerk": 3},
            projection_years=3,
            discount_rate_pct=10,
        )

    def test_has_financial_metrics(self):
        result = calculate_roi(self._strong_input())
        assert "financial_metrics" in result
        fm = result["financial_metrics"]
        assert "npv_sar" in fm
        assert "payback_months" in fm
        assert "roi_3year_pct" in fm

    def test_has_role_breakdown(self):
        result = calculate_roi(self._strong_input())
        assert len(result["role_breakdown"]) == 1
        rb = result["role_breakdown"][0]
        assert rb["role_id"] == "data_entry_clerk"
        assert rb["headcount"] == 3

    def test_custom_savings_add_to_total(self):
        inp = AutomationROIInput(
            project_name="Test",
            implementation_cost_sar=100_000,
            custom_annual_labor_saving_sar=50_000,
            projection_years=3,
            discount_rate_pct=10,
        )
        result = calculate_roi(inp)
        assert result["annual_benefits"]["total_annual_benefit_sar"] == 50_000

    def test_rating_excellent_for_high_roi(self):
        inp = AutomationROIInput(
            project_name="Test",
            implementation_cost_sar=10_000,
            custom_annual_labor_saving_sar=50_000,
            projection_years=3,
            discount_rate_pct=10,
        )
        result = calculate_roi(inp)
        assert result["rating"] == "Excellent"

    def test_rating_negative_for_bad_project(self):
        inp = AutomationROIInput(
            project_name="Test",
            implementation_cost_sar=1_000_000,
            custom_annual_labor_saving_sar=1_000,
            projection_years=3,
            discount_rate_pct=10,
        )
        result = calculate_roi(inp)
        assert result["rating"] == "Negative"


class TestRouterMetadata:
    def test_router_prefix(self):
        assert router.prefix == "/api/v1/roi-calculator"

    def test_router_tags(self):
        assert "Analytics" in router.tags
