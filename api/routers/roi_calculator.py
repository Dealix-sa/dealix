"""
AI automation ROI calculator for Saudi B2B companies.

Computes ROI, payback period, NPV, and IRR for AI/automation projects
based on Saudi market labor costs, productivity assumptions, and SAR
pricing. All amounts in SAR. Estimates only — no guarantees.
"""
from __future__ import annotations

import math
from typing import Any

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

router = APIRouter(prefix="/api/v1/roi-calculator", tags=["Analytics"])

# ---------------------------------------------------------------------------
# Saudi market labor cost benchmarks (SAR/month, 2024 midpoints)
# ---------------------------------------------------------------------------

_LABOR_BENCHMARKS: dict[str, dict[str, Any]] = {
    "data_entry_clerk": {
        "title_ar": "موظف إدخال بيانات",
        "title_en": "Data Entry Clerk",
        "monthly_salary_sar": 4_500,
        "fully_loaded_multiplier": 1.35,  # salary × 1.35 = total cost (GOSI, benefits)
        "automatable_pct": 85,
    },
    "accounts_payable_specialist": {
        "title_ar": "أخصائي حسابات دائنة",
        "title_en": "Accounts Payable Specialist",
        "monthly_salary_sar": 7_000,
        "fully_loaded_multiplier": 1.35,
        "automatable_pct": 60,
    },
    "customer_service_agent": {
        "title_ar": "موظف خدمة عملاء",
        "title_en": "Customer Service Agent",
        "monthly_salary_sar": 5_500,
        "fully_loaded_multiplier": 1.35,
        "automatable_pct": 45,
    },
    "sales_operations_analyst": {
        "title_ar": "محلل عمليات المبيعات",
        "title_en": "Sales Operations Analyst",
        "monthly_salary_sar": 10_000,
        "fully_loaded_multiplier": 1.40,
        "automatable_pct": 40,
    },
    "hr_generalist": {
        "title_ar": "أخصائي موارد بشرية",
        "title_en": "HR Generalist",
        "monthly_salary_sar": 8_500,
        "fully_loaded_multiplier": 1.38,
        "automatable_pct": 35,
    },
    "report_analyst": {
        "title_ar": "محلل تقارير",
        "title_en": "Reporting / BI Analyst",
        "monthly_salary_sar": 12_000,
        "fully_loaded_multiplier": 1.40,
        "automatable_pct": 50,
    },
}

# ---------------------------------------------------------------------------
# ROI calculation models
# ---------------------------------------------------------------------------

class AutomationROIInput(BaseModel):
    project_name: str = Field(..., max_length=120)
    implementation_cost_sar: float = Field(..., gt=0, description="One-time implementation cost SAR")
    annual_maintenance_cost_sar: float = Field(0, ge=0, description="Annual ongoing cost SAR")

    # Labor savings
    roles_automated: list[str] = Field(
        default_factory=list,
        description="Role IDs from GET /api/v1/roi-calculator/benchmarks",
    )
    headcount_per_role: dict[str, int] = Field(
        default_factory=dict,
        description="Number of employees per role ID being automated",
    )

    # Custom benefits (if not using benchmark roles)
    custom_annual_labor_saving_sar: float = Field(0, ge=0)
    custom_annual_revenue_uplift_sar: float = Field(0, ge=0)
    custom_annual_error_reduction_sar: float = Field(0, ge=0)

    # Analysis horizon
    projection_years: int = Field(3, ge=1, le=10, description="NPV projection years")
    discount_rate_pct: float = Field(10.0, ge=0, le=50, description="Discount rate % (WACC proxy)")


def _calculate_labor_savings(inp: AutomationROIInput) -> float:
    savings = 0.0
    for role_id in inp.roles_automated:
        bench = _LABOR_BENCHMARKS.get(role_id)
        if bench:
            count = inp.headcount_per_role.get(role_id, 1)
            monthly_fully_loaded = (
                bench["monthly_salary_sar"] * bench["fully_loaded_multiplier"]
            )
            annual_saving = (
                monthly_fully_loaded * 12 * count * bench["automatable_pct"] / 100
            )
            savings += annual_saving
    return savings


def _npv(cash_flows: list[float], rate: float) -> float:
    return sum(cf / (1 + rate) ** i for i, cf in enumerate(cash_flows))


def _irr(cash_flows: list[float]) -> float | None:
    """Newton-Raphson IRR estimate. Returns None if no solution found."""
    if not cash_flows or cash_flows[0] >= 0:
        return None
    rate = 0.1
    for _ in range(100):
        npv = _npv(cash_flows, rate)
        npv_deriv = sum(
            -i * cf / (1 + rate) ** (i + 1)
            for i, cf in enumerate(cash_flows)
            if i > 0
        )
        if abs(npv_deriv) < 1e-10:
            break
        rate_new = rate - npv / npv_deriv
        if abs(rate_new - rate) < 1e-8:
            return round(rate_new * 100, 2)
        rate = rate_new
    return round(rate * 100, 2)


def _payback_months(initial_cost: float, annual_net_benefit: float) -> float | None:
    if annual_net_benefit <= 0:
        return None
    return round(initial_cost / annual_net_benefit * 12, 1)


def calculate_roi(inp: AutomationROIInput) -> dict[str, Any]:
    labor_savings = _calculate_labor_savings(inp)
    total_annual_benefit = (
        labor_savings
        + inp.custom_annual_labor_saving_sar
        + inp.custom_annual_revenue_uplift_sar
        + inp.custom_annual_error_reduction_sar
    )
    annual_net_benefit = total_annual_benefit - inp.annual_maintenance_cost_sar

    # Cash flows: year 0 = -implementation_cost; years 1..n = annual_net_benefit
    cash_flows = [-inp.implementation_cost_sar] + [annual_net_benefit] * inp.projection_years
    discount_rate = inp.discount_rate_pct / 100

    npv_value = _npv(cash_flows, discount_rate)
    irr_value = _irr(cash_flows)
    payback = _payback_months(inp.implementation_cost_sar, annual_net_benefit)

    # 3-year cumulative return
    total_return_3y = annual_net_benefit * min(3, inp.projection_years) - inp.implementation_cost_sar
    roi_pct = (
        total_return_3y / inp.implementation_cost_sar * 100
        if inp.implementation_cost_sar > 0
        else 0
    )

    # Per-role breakdown
    role_breakdown = []
    for role_id in inp.roles_automated:
        bench = _LABOR_BENCHMARKS.get(role_id)
        if bench:
            count = inp.headcount_per_role.get(role_id, 1)
            monthly_fl = bench["monthly_salary_sar"] * bench["fully_loaded_multiplier"]
            role_saving = monthly_fl * 12 * count * bench["automatable_pct"] / 100
            role_breakdown.append({
                "role_id": role_id,
                "role_en": bench["title_en"],
                "role_ar": bench["title_ar"],
                "headcount": count,
                "automatable_pct": bench["automatable_pct"],
                "annual_saving_sar": round(role_saving, 0),
            })

    return {
        "project_name": inp.project_name,
        "inputs_summary": {
            "implementation_cost_sar": inp.implementation_cost_sar,
            "annual_maintenance_cost_sar": inp.annual_maintenance_cost_sar,
            "projection_years": inp.projection_years,
            "discount_rate_pct": inp.discount_rate_pct,
        },
        "annual_benefits": {
            "labor_savings_sar": round(labor_savings, 0),
            "custom_labor_saving_sar": inp.custom_annual_labor_saving_sar,
            "custom_revenue_uplift_sar": inp.custom_annual_revenue_uplift_sar,
            "custom_error_reduction_sar": inp.custom_annual_error_reduction_sar,
            "total_annual_benefit_sar": round(total_annual_benefit, 0),
            "net_annual_benefit_sar": round(annual_net_benefit, 0),
        },
        "financial_metrics": {
            "npv_sar": round(npv_value, 0),
            "irr_pct": irr_value,
            "payback_months": payback,
            "roi_3year_pct": round(roi_pct, 1),
            "cumulative_3year_net_sar": round(total_return_3y, 0),
        },
        "role_breakdown": role_breakdown,
        "rating": (
            "Excellent" if roi_pct >= 200
            else "Strong" if roi_pct >= 100
            else "Good" if roi_pct >= 50
            else "Marginal" if roi_pct >= 0
            else "Negative"
        ),
    }


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@router.get("/benchmarks", summary="Saudi market labor cost benchmarks for ROI modelling")
async def get_benchmarks() -> dict[str, Any]:
    return {
        "benchmarks": [
            {"id": k, **v}
            for k, v in _LABOR_BENCHMARKS.items()
        ],
        "note_en": (
            "Fully-loaded cost = salary × multiplier (includes GOSI, benefits, "
            "overhead). Based on 2024 Saudi market midpoints."
        ),
        "note_ar": (
            "التكلفة الشاملة = الراتب × معامل (يشمل التأمينات الاجتماعية والمزايا والعبء). "
            "مستند إلى متوسطات السوق السعودي 2024."
        ),
        "disclaimer_en": "Indicative benchmarks. Actual costs vary by company size and location.",
        "disclaimer_ar": "معايير استرشادية. تتفاوت التكاليف الفعلية بحسب حجم الشركة والموقع.",
        "governance_decision": "ALLOW_WITH_REVIEW",
    }


@router.post("/calculate", summary="Calculate ROI for an AI automation project")
async def calculate_roi_endpoint(body: AutomationROIInput) -> dict[str, Any]:
    if body.roles_automated:
        unknown = [r for r in body.roles_automated if r not in _LABOR_BENCHMARKS]
        if unknown:
            raise HTTPException(
                status_code=422,
                detail=f"Unknown role IDs: {unknown}. Use GET /api/v1/roi-calculator/benchmarks.",
            )

    result = calculate_roi(body)
    return {
        **result,
        "disclaimer_en": (
            "This ROI estimate is illustrative. Actual results depend on implementation "
            "quality, change management, and business context. Not a guarantee of savings."
        ),
        "disclaimer_ar": (
            "هذا التقدير للعائد على الاستثمار استرشادي. النتائج الفعلية تعتمد على جودة "
            "التنفيذ وإدارة التغيير والسياق التجاري. ليس ضماناً للوفورات."
        ),
        "governance_decision": "ALLOW_WITH_REVIEW",
    }


@router.get("/quick-estimate", summary="Quick ROI estimate without detailed inputs")
async def quick_estimate(
    implementation_cost_sar: float = Query(..., gt=0, description="Project cost in SAR"),
    annual_saving_sar: float = Query(..., gt=0, description="Expected annual saving in SAR"),
    years: int = Query(3, ge=1, le=10),
) -> dict[str, Any]:
    payback = _payback_months(implementation_cost_sar, annual_saving_sar)
    cumulative = annual_saving_sar * years - implementation_cost_sar
    roi_pct = cumulative / implementation_cost_sar * 100

    return {
        "implementation_cost_sar": implementation_cost_sar,
        "annual_saving_sar": annual_saving_sar,
        "projection_years": years,
        "payback_months": payback,
        "cumulative_net_sar": round(cumulative, 0),
        "roi_pct": round(roi_pct, 1),
        "rating": (
            "Excellent" if roi_pct >= 200
            else "Strong" if roi_pct >= 100
            else "Good" if roi_pct >= 50
            else "Marginal" if roi_pct >= 0
            else "Negative"
        ),
        "disclaimer_en": "Quick estimate — use POST /calculate for detailed modelling.",
        "disclaimer_ar": "تقدير سريع — استخدم POST /calculate للنمذجة التفصيلية.",
        "governance_decision": "ALLOW_WITH_REVIEW",
    }
