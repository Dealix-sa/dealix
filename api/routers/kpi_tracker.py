"""
Saudi B2B KPI tracker for Dealix client engagements.

Provides a curated library of Saudi-market-relevant KPIs for B2B companies,
with benchmarks, calculation guides, and Vision 2030 alignment. Helps clients
understand which metrics matter most in their sector.
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

router = APIRouter(prefix="/api/v1/kpi-tracker", tags=["Analytics"])

# ---------------------------------------------------------------------------
# KPI Library
# ---------------------------------------------------------------------------

_KPI_LIBRARY: dict[str, Any] = {
    "revenue_growth_rate": {
        "name_en": "Revenue Growth Rate",
        "name_ar": "معدل نمو الإيرادات",
        "category": "revenue",
        "formula_en": "((Current Period Revenue - Prior Period Revenue) / Prior Period Revenue) × 100",
        "formula_ar": "((إيرادات الفترة الحالية - إيرادات الفترة السابقة) / إيرادات الفترة السابقة) × 100",
        "benchmark_saudi_b2b_pct": 20,
        "benchmark_context_en": "Saudi B2B SaaS companies targeting Vision 2030 sectors should target ≥20% YoY.",
        "vision_2030_relevance_en": "Directly supports Thriving Economy pillar — target 50% non-oil GDP by 2030.",
        "data_source_en": "Financial statements, CRM revenue reports",
        "frequency": "monthly",
        "alert_threshold_en": "Below 10% YoY is a red flag for Saudi B2B in growth sectors.",
    },
    "customer_acquisition_cost": {
        "name_en": "Customer Acquisition Cost (CAC)",
        "name_ar": "تكلفة اكتساب العملاء",
        "category": "sales_efficiency",
        "formula_en": "Total Sales & Marketing Spend / Number of New Customers Acquired",
        "formula_ar": "إجمالي إنفاق المبيعات والتسويق / عدد العملاء الجدد المكتسبين",
        "benchmark_saudi_b2b_pct": None,
        "benchmark_context_en": "Saudi B2B SaaS: SAR 2,000–8,000 CAC is typical for SME segment; SAR 15,000–50,000 for enterprise.",
        "vision_2030_relevance_en": "Lower CAC through digital channels supports Vision 2030 digital economy goals.",
        "data_source_en": "CRM, paid media dashboards, HR salary data",
        "frequency": "monthly",
        "alert_threshold_en": "CAC:LTV ratio above 1:3 is unsustainable.",
    },
    "customer_lifetime_value": {
        "name_en": "Customer Lifetime Value (LTV / CLV)",
        "name_ar": "قيمة عمر العميل",
        "category": "revenue",
        "formula_en": "Average Monthly Revenue per Customer × Gross Margin % / Monthly Churn Rate",
        "formula_ar": "متوسط الإيرادات الشهرية للعميل × نسبة هامش الربح الإجمالي / معدل التراجع الشهري",
        "benchmark_saudi_b2b_pct": None,
        "benchmark_context_en": "LTV:CAC ratio ≥3:1 is healthy. Saudi B2B managed services target LTV of SAR 50,000–200,000.",
        "vision_2030_relevance_en": "High LTV businesses build the stable private sector Saudi Vision 2030 requires.",
        "data_source_en": "Billing system, CRM, churn tracking",
        "frequency": "quarterly",
        "alert_threshold_en": "LTV:CAC below 2:1 requires immediate margin or retention intervention.",
    },
    "monthly_recurring_revenue": {
        "name_en": "Monthly Recurring Revenue (MRR)",
        "name_ar": "الإيرادات المتكررة الشهرية",
        "category": "revenue",
        "formula_en": "Sum of all active monthly subscription values",
        "formula_ar": "مجموع قيم جميع الاشتراكات الشهرية النشطة",
        "benchmark_saudi_b2b_pct": None,
        "benchmark_context_en": "Dealix managed ops tier adds SAR 2,999–4,999/mo per client. Target 20% MoM MRR growth in early stage.",
        "vision_2030_relevance_en": "Recurring revenue model supports stable, measurable GDP contribution.",
        "data_source_en": "Billing system, contract management",
        "frequency": "monthly",
        "alert_threshold_en": "MRR contraction (negative net MRR) for 2+ months requires executive review.",
    },
    "net_revenue_retention": {
        "name_en": "Net Revenue Retention (NRR)",
        "name_ar": "صافي احتفاظ الإيرادات",
        "category": "retention",
        "formula_en": "((Start MRR + Expansion MRR - Churned MRR - Contraction MRR) / Start MRR) × 100",
        "formula_ar": "((MRR البداية + MRR التوسع - MRR المتراجع - MRR الانكماش) / MRR البداية) × 100",
        "benchmark_saudi_b2b_pct": 110,
        "benchmark_context_en": "World-class SaaS NRR is >110%. Saudi B2B: ≥100% is target; ≥110% means expansion exceeds churn.",
        "vision_2030_relevance_en": "High NRR demonstrates sustainable value creation, key for Saudi IPO readiness (Tadawul).",
        "data_source_en": "Billing system, CRM expansion tracking",
        "frequency": "monthly",
        "alert_threshold_en": "NRR below 90% indicates systemic value delivery failure — escalate immediately.",
    },
    "pipeline_coverage_ratio": {
        "name_en": "Pipeline Coverage Ratio",
        "name_ar": "نسبة تغطية خط الأنابيب",
        "category": "sales_pipeline",
        "formula_en": "Total Qualified Pipeline Value / Revenue Target for the Period",
        "formula_ar": "إجمالي قيمة خط الأنابيب المؤهل / هدف الإيرادات للفترة",
        "benchmark_saudi_b2b_pct": None,
        "benchmark_context_en": "3:1 pipeline coverage is minimum. Saudi B2B with longer cycles (Ramadan/Eid effect) should target 4:1.",
        "vision_2030_relevance_en": "Healthy pipeline supports predictable revenue projections required for Vision 2030 partner reporting.",
        "data_source_en": "CRM pipeline reports",
        "frequency": "weekly",
        "alert_threshold_en": "Below 2:1 pipeline coverage 60 days before quarter-end is critical.",
    },
    "saudization_rate": {
        "name_en": "Saudization Rate (Nitaqat)",
        "name_ar": "نسبة السعودة (نطاقات)",
        "category": "compliance",
        "formula_en": "Saudi Employees / Total Employees × 100",
        "formula_ar": "الموظفون السعوديون / إجمالي الموظفين × 100",
        "benchmark_saudi_b2b_pct": None,
        "benchmark_context_en": "Varies by sector and company size. Target Platinum or High Green band. Checked against HRSD Nitaqat system.",
        "vision_2030_relevance_en": "Nitaqat compliance is mandatory. Vision 2030 targets 50% private sector Saudization by 2030.",
        "data_source_en": "HRSD Nitaqat portal, HR system",
        "frequency": "quarterly",
        "alert_threshold_en": "Yellow or Red band triggers work permit restrictions — immediate HR action required.",
    },
    "data_quality_score": {
        "name_en": "Data Quality Score",
        "name_ar": "درجة جودة البيانات",
        "category": "data_operations",
        "formula_en": "(Completeness % + Accuracy % + Freshness %) / 3",
        "formula_ar": "(نسبة الاكتمال + نسبة الدقة + نسبة الحداثة) / 3",
        "benchmark_saudi_b2b_pct": 75,
        "benchmark_context_en": "Dealix requires ≥70% data quality score before revenue intelligence is meaningful. Target ≥85%.",
        "vision_2030_relevance_en": "High data quality enables AI adoption — foundational for Saudi AI Strategy objectives.",
        "data_source_en": "CRM audit, Dealix data quality module",
        "frequency": "monthly",
        "alert_threshold_en": "Below 60% data quality makes revenue intelligence unreliable — trigger data remediation sprint.",
    },
}

_KPI_CATEGORIES: list[dict[str, Any]] = [
    {
        "category": "revenue",
        "name_en": "Revenue KPIs",
        "name_ar": "مؤشرات الإيرادات",
        "description_en": "Track top-line growth, recurring revenue, and lifetime value.",
    },
    {
        "category": "sales_efficiency",
        "name_en": "Sales Efficiency KPIs",
        "name_ar": "مؤشرات كفاءة المبيعات",
        "description_en": "Measure cost and velocity of acquiring new revenue.",
    },
    {
        "category": "sales_pipeline",
        "name_en": "Pipeline Health KPIs",
        "name_ar": "مؤشرات صحة خط الأنابيب",
        "description_en": "Monitor pipeline coverage, velocity, and stage conversion.",
    },
    {
        "category": "retention",
        "name_en": "Retention & Expansion KPIs",
        "name_ar": "مؤشرات الاحتفاظ والتوسع",
        "description_en": "Track churn, NRR, and expansion revenue.",
    },
    {
        "category": "compliance",
        "name_en": "Saudi Compliance KPIs",
        "name_ar": "مؤشرات الامتثال السعودي",
        "description_en": "Monitor Nitaqat, ZATCA, and PDPL compliance posture.",
    },
    {
        "category": "data_operations",
        "name_en": "Data & Operations KPIs",
        "name_ar": "مؤشرات البيانات والعمليات",
        "description_en": "Track data quality and operational efficiency metrics.",
    },
]


class KPIDashboardInput(BaseModel):
    company_name: str = Field(..., min_length=2)
    monthly_revenue_sar: float = Field(..., ge=0)
    prior_month_revenue_sar: float = Field(..., ge=0)
    total_customers: int = Field(..., ge=0)
    new_customers_this_month: int = Field(..., ge=0)
    churned_customers_this_month: int = Field(..., ge=0)
    total_pipeline_sar: float = Field(..., ge=0)
    monthly_sales_marketing_spend_sar: float = Field(..., ge=0)
    saudi_employees: int = Field(..., ge=0)
    total_employees: int = Field(..., ge=1)


def _compute_kpi_snapshot(inp: KPIDashboardInput) -> dict[str, Any]:
    revenue_growth_pct = (
        round((inp.monthly_revenue_sar - inp.prior_month_revenue_sar) / inp.prior_month_revenue_sar * 100, 1)
        if inp.prior_month_revenue_sar > 0 else 0.0
    )
    cac = (
        round(inp.monthly_sales_marketing_spend_sar / inp.new_customers_this_month, 0)
        if inp.new_customers_this_month > 0 else 0.0
    )
    churn_rate_pct = (
        round(inp.churned_customers_this_month / inp.total_customers * 100, 1)
        if inp.total_customers > 0 else 0.0
    )
    saudization_pct = round(inp.saudi_employees / inp.total_employees * 100, 1)
    pipeline_coverage = (
        round(inp.total_pipeline_sar / inp.monthly_revenue_sar, 1)
        if inp.monthly_revenue_sar > 0 else 0.0
    )

    alerts: list[str] = []
    if revenue_growth_pct < 0:
        alerts.append("Revenue declined MoM — investigate churn and pipeline gaps")
    if churn_rate_pct > 5:
        alerts.append(f"High churn rate {churn_rate_pct}% — trigger customer success intervention")
    if pipeline_coverage < 2.0:
        alerts.append(f"Pipeline coverage {pipeline_coverage}x below 2x threshold — build pipeline urgently")
    if saudization_pct < 30:
        alerts.append(f"Saudization {saudization_pct}% may be below sector threshold — check Nitaqat band")

    return {
        "company_name": inp.company_name,
        "kpis": {
            "revenue_growth_mom_pct": revenue_growth_pct,
            "customer_acquisition_cost_sar": cac,
            "churn_rate_pct": churn_rate_pct,
            "saudization_pct": saudization_pct,
            "pipeline_coverage_ratio": pipeline_coverage,
        },
        "alerts": alerts,
        "health_summary_en": "Healthy" if not alerts else f"{len(alerts)} alert(s) require attention",
        "governance_decision": "ALLOW_WITH_REVIEW",
    }


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@router.get("/library", summary="KPI library for Saudi B2B companies")
async def get_kpi_library(
    category: str | None = Query(None, description="Filter by category"),
) -> dict[str, Any]:
    kpis = _KPI_LIBRARY
    if category is not None:
        kpis = {k: v for k, v in _KPI_LIBRARY.items() if v.get("category") == category}
    return {
        "kpis": kpis,
        "total": len(kpis),
        "governance_decision": "ALLOW_WITH_REVIEW",
    }


@router.get("/library/{kpi_id}", summary="Detail for one KPI")
async def get_kpi(kpi_id: str) -> dict[str, Any]:
    kpi = _KPI_LIBRARY.get(kpi_id)
    if kpi is None:
        raise HTTPException(status_code=404, detail=f"KPI '{kpi_id}' not found.")
    return {**kpi, "kpi_id": kpi_id, "governance_decision": "ALLOW_WITH_REVIEW"}


@router.get("/categories", summary="KPI categories")
async def get_categories() -> dict[str, Any]:
    return {
        "categories": _KPI_CATEGORIES,
        "governance_decision": "ALLOW_WITH_REVIEW",
    }


@router.post("/snapshot", summary="Compute KPI snapshot from raw inputs")
async def compute_snapshot(inp: KPIDashboardInput) -> dict[str, Any]:
    return _compute_kpi_snapshot(inp)
