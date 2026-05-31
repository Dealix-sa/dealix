"""
Unit tests for api/routers/kpi_tracker.py

Tests cover:
- 8 KPIs with bilingual names, formulas, benchmarks
- 6 KPI categories
- _compute_kpi_snapshot: revenue growth, churn, saudization alerts
- Router metadata
"""
from __future__ import annotations

import pytest

from api.routers.kpi_tracker import (
    _KPI_LIBRARY,
    _KPI_CATEGORIES,
    _compute_kpi_snapshot,
    KPIDashboardInput,
    router,
)


class TestKPILibrary:
    def test_eight_kpis(self):
        assert len(_KPI_LIBRARY) == 8

    def test_all_bilingual(self):
        for k, v in _KPI_LIBRARY.items():
            assert v.get("name_en"), f"{k} missing name_en"
            assert v.get("name_ar"), f"{k} missing name_ar"

    def test_all_have_formula(self):
        for k, v in _KPI_LIBRARY.items():
            assert v.get("formula_en"), f"{k} missing formula_en"
            assert v.get("formula_ar"), f"{k} missing formula_ar"

    def test_all_have_category(self):
        for k, v in _KPI_LIBRARY.items():
            assert v.get("category"), f"{k} missing category"

    def test_all_have_frequency(self):
        for k, v in _KPI_LIBRARY.items():
            assert v.get("frequency"), f"{k} missing frequency"

    def test_all_have_alert_threshold(self):
        for k, v in _KPI_LIBRARY.items():
            assert v.get("alert_threshold_en"), f"{k} missing alert_threshold_en"

    def test_revenue_kpis_present(self):
        revenue_kpis = [k for k, v in _KPI_LIBRARY.items() if v["category"] == "revenue"]
        assert len(revenue_kpis) >= 3

    def test_compliance_kpi_present(self):
        compliance_kpis = [k for k, v in _KPI_LIBRARY.items() if v["category"] == "compliance"]
        assert len(compliance_kpis) >= 1

    def test_saudization_kpi_present(self):
        assert "saudization_rate" in _KPI_LIBRARY

    def test_mrr_kpi_present(self):
        assert "monthly_recurring_revenue" in _KPI_LIBRARY

    def test_nrr_benchmark_110(self):
        nrr = _KPI_LIBRARY["net_revenue_retention"]
        assert nrr.get("benchmark_saudi_b2b_pct") == 110

    def test_data_quality_benchmark_75(self):
        dq = _KPI_LIBRARY["data_quality_score"]
        assert dq.get("benchmark_saudi_b2b_pct") == 75


class TestKPICategories:
    def test_six_categories(self):
        assert len(_KPI_CATEGORIES) == 6

    def test_all_bilingual(self):
        for c in _KPI_CATEGORIES:
            assert c.get("name_en"), f"{c['category']} missing name_en"
            assert c.get("name_ar"), f"{c['category']} missing name_ar"

    def test_compliance_category_present(self):
        cats = {c["category"] for c in _KPI_CATEGORIES}
        assert "compliance" in cats

    def test_revenue_category_present(self):
        cats = {c["category"] for c in _KPI_CATEGORIES}
        assert "revenue" in cats


class TestComputeKPISnapshot:
    def _healthy_input(self, **overrides) -> KPIDashboardInput:
        data = dict(
            company_name="ACME Saudi",
            monthly_revenue_sar=500_000.0,
            prior_month_revenue_sar=450_000.0,
            total_customers=50,
            new_customers_this_month=5,
            churned_customers_this_month=1,
            total_pipeline_sar=2_000_000.0,
            monthly_sales_marketing_spend_sar=25_000.0,
            saudi_employees=15,
            total_employees=30,
        )
        data.update(overrides)
        return KPIDashboardInput(**data)

    def test_healthy_snapshot_no_alerts(self):
        result = _compute_kpi_snapshot(self._healthy_input())
        assert result["alerts"] == []

    def test_revenue_growth_calculated(self):
        result = _compute_kpi_snapshot(self._healthy_input())
        # (500k - 450k) / 450k * 100 = 11.1%
        assert abs(result["kpis"]["revenue_growth_mom_pct"] - 11.1) < 0.5

    def test_revenue_decline_triggers_alert(self):
        result = _compute_kpi_snapshot(self._healthy_input(
            monthly_revenue_sar=400_000, prior_month_revenue_sar=500_000
        ))
        alert_text = " ".join(result["alerts"]).lower()
        assert "revenue" in alert_text or "decline" in alert_text

    def test_high_churn_triggers_alert(self):
        result = _compute_kpi_snapshot(self._healthy_input(
            churned_customers_this_month=5, total_customers=20
        ))
        assert len(result["alerts"]) > 0
        alert_text = " ".join(result["alerts"]).lower()
        assert "churn" in alert_text

    def test_low_pipeline_triggers_alert(self):
        result = _compute_kpi_snapshot(self._healthy_input(
            total_pipeline_sar=300_000, monthly_revenue_sar=500_000
        ))
        alert_text = " ".join(result["alerts"]).lower()
        assert "pipeline" in alert_text

    def test_low_saudization_triggers_alert(self):
        result = _compute_kpi_snapshot(self._healthy_input(
            saudi_employees=3, total_employees=30
        ))
        alert_text = " ".join(result["alerts"]).lower()
        assert "saudization" in alert_text or "nitaqat" in alert_text

    def test_cac_calculated(self):
        result = _compute_kpi_snapshot(self._healthy_input(
            monthly_sales_marketing_spend_sar=50_000, new_customers_this_month=5
        ))
        assert result["kpis"]["customer_acquisition_cost_sar"] == 10_000.0

    def test_zero_new_customers_no_division_error(self):
        result = _compute_kpi_snapshot(self._healthy_input(new_customers_this_month=0))
        assert result["kpis"]["customer_acquisition_cost_sar"] == 0.0

    def test_governance_allow_with_review(self):
        result = _compute_kpi_snapshot(self._healthy_input())
        assert result["governance_decision"] == "ALLOW_WITH_REVIEW"

    def test_company_name_in_result(self):
        result = _compute_kpi_snapshot(self._healthy_input())
        assert result["company_name"] == "ACME Saudi"


class TestRouterMetadata:
    def test_router_prefix(self):
        assert router.prefix == "/api/v1/kpi-tracker"

    def test_router_tags(self):
        assert "Analytics" in router.tags
