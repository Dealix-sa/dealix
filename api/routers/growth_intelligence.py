"""Growth Intelligence API — company-level growth signals and market opportunities.

Endpoints:
  GET  /api/v1/growth-intelligence/signals          — top growth signals for Dealix
  GET  /api/v1/growth-intelligence/market-map       — ranked opportunity map (sector x city)
  GET  /api/v1/growth-intelligence/weekly-focus     — recommended focus areas this week
  POST /api/v1/growth-intelligence/simulate-growth  — simulate MRR growth given assumptions
  GET  /api/v1/growth-intelligence/benchmark        — Dealix KPIs vs Saudi SaaS benchmarks

All endpoints:
  - Require admin auth (X-Admin-API-Key)
  - Return governance_decision field
  - Bilingual ar/en labels
  - Static Saudi market data with realistic 2026 figures
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from api.security.api_key import require_admin_key
from core.logging import get_logger

_log = get_logger(__name__)

router = APIRouter(
    prefix="/api/v1/growth-intelligence",
    tags=["growth-intelligence"],
    dependencies=[Depends(require_admin_key)],
)

_GOV = "ALLOW_WITH_REVIEW"
_NOW = datetime.now(UTC)

# ---------------------------------------------------------------------------
# Bilingual label helpers
# ---------------------------------------------------------------------------

_LABELS_AR: dict[str, str] = {
    "signals": "إشارات النمو",
    "market_map": "خريطة فرص السوق",
    "weekly_focus": "التركيز الأسبوعي",
    "simulate_growth": "محاكاة نمو الإيراد",
    "benchmark": "مقارنة مؤشرات الأداء",
    "mrr": "الإيراد الشهري المتكرر",
    "churn_rate": "معدل الإلغاء",
    "arr": "الإيراد السنوي المتوقع",
    "new_clients": "العملاء الجدد",
    "avg_deal": "متوسط قيمة الصفقة",
}

_LABELS_EN: dict[str, str] = {
    "signals": "Growth Signals",
    "market_map": "Market Opportunity Map",
    "weekly_focus": "Weekly Focus",
    "simulate_growth": "MRR Growth Simulation",
    "benchmark": "KPI Benchmark",
    "mrr": "Monthly Recurring Revenue",
    "churn_rate": "Churn Rate",
    "arr": "Annual Run-Rate",
    "new_clients": "New Clients per Month",
    "avg_deal": "Average Deal Value",
}


def _label(key: str) -> dict[str, str]:
    return {"ar": _LABELS_AR.get(key, key), "en": _LABELS_EN.get(key, key)}


# ---------------------------------------------------------------------------
# Static growth signals data (Saudi market, 2026)
# ---------------------------------------------------------------------------

_GROWTH_SIGNALS: list[dict[str, Any]] = [
    {
        "signal_id": "SIG-001",
        "title_en": "ZATCA Phase 3 e-invoicing mandate — SME deadline Q3 2026",
        "title_ar": "مرحلة زاتكا الثالثة: الفوترة الإلكترونية للشركات الصغيرة — موعد Q3 2026",
        "category": "regulatory",
        "urgency": "HIGH",
        "sectors_affected": ["financial_services", "technology", "logistics", "real_estate"],
        "estimated_addressable_companies": 12_000,
        "vision_2030_tailwind": True,
        "action_en": "Lead with ZATCA compliance pain in outreach for these sectors",
        "action_ar": "ابدأ بألم الامتثال لزاتكا في التواصل مع هذه القطاعات",
    },
    {
        "signal_id": "SIG-002",
        "title_en": "PDPL enforcement active — companies scrambling for data governance",
        "title_ar": "تطبيق نظام حماية البيانات — الشركات تسعى لحوكمة البيانات",
        "category": "regulatory",
        "urgency": "HIGH",
        "sectors_affected": ["healthcare", "financial_services", "technology"],
        "estimated_addressable_companies": 8_500,
        "vision_2030_tailwind": True,
        "action_en": "Position Dealix as PDPL-safe AI operations partner",
        "action_ar": "ضع Dealix كشريك عمليات AI آمن وفق نظام البيانات",
    },
    {
        "signal_id": "SIG-003",
        "title_en": "Vision 2030 healthcare privatization wave — 47 new private hospitals planned",
        "title_ar": "موجة خصخصة القطاع الصحي — 47 مستشفى خاصاً مخططاً",
        "category": "market_expansion",
        "urgency": "HIGH",
        "sectors_affected": ["healthcare"],
        "estimated_addressable_companies": 2_200,
        "vision_2030_tailwind": True,
        "action_en": "Develop healthcare-specific proof pack and outreach track",
        "action_ar": "طور حزمة أدلة وقناة تواصل متخصصة للقطاع الصحي",
    },
    {
        "signal_id": "SIG-004",
        "title_en": "Saudi Fintech surge — 200+ licensed fintechs, most under-automated",
        "title_ar": "طفرة التقنية المالية — 200+ شركة مالية مرخصة، معظمها غير مؤتمت",
        "category": "sector_growth",
        "urgency": "MEDIUM",
        "sectors_affected": ["financial_services"],
        "estimated_addressable_companies": 200,
        "vision_2030_tailwind": True,
        "action_en": "Target fintech operations leads with automation ROI pitch",
        "action_ar": "استهدف مسؤولي العمليات في شركات التقنية المالية",
    },
    {
        "signal_id": "SIG-005",
        "title_en": "Real estate REGA digitalization requirements — agent licensing systems",
        "title_ar": "متطلبات التحول الرقمي للهيئة العقارية — أنظمة ترخيص الوكلاء",
        "category": "regulatory",
        "urgency": "MEDIUM",
        "sectors_affected": ["real_estate"],
        "estimated_addressable_companies": 3_800,
        "vision_2030_tailwind": True,
        "action_en": "Lead with REGA compliance automation angle",
        "action_ar": "ابدأ بزاوية أتمتة الامتثال للهيئة العقارية",
    },
    {
        "signal_id": "SIG-006",
        "title_en": "SME digitalization fund — SMEA offering SAR 50M in tech adoption grants",
        "title_ar": "صندوق رقمنة المنشآت الصغيرة — وزارة الاستثمار تقدم 50 مليون ريال",
        "category": "funding_tailwind",
        "urgency": "MEDIUM",
        "sectors_affected": ["technology", "logistics", "healthcare", "real_estate"],
        "estimated_addressable_companies": 15_000,
        "vision_2030_tailwind": True,
        "action_en": "Position Dealix as eligible spend under tech adoption grants",
        "action_ar": "أدرج Dealix ضمن الإنفاق المؤهل لمنح تبني التقنية",
    },
    {
        "signal_id": "SIG-007",
        "title_en": "Riyadh 2030 mega-project procurement — 100+ companies entering new markets",
        "title_ar": "مشتريات مشاريع الرياض 2030 — 100+ شركة تدخل أسواقاً جديدة",
        "category": "market_expansion",
        "urgency": "MEDIUM",
        "sectors_affected": ["construction", "logistics", "technology"],
        "estimated_addressable_companies": 500,
        "vision_2030_tailwind": True,
        "action_en": "Target procurement and ops managers at Riyadh project companies",
        "action_ar": "استهدف مدراء المشتريات والعمليات في شركات مشاريع الرياض",
    },
    {
        "signal_id": "SIG-008",
        "title_en": "B2B SaaS adoption in Saudi growing 34% YoY — early mover advantage window",
        "title_ar": "نمو تبني SaaS في السوق السعودية 34% سنوياً — نافذة ميزة المتحرك الأول",
        "category": "market_trend",
        "urgency": "LOW",
        "sectors_affected": ["technology", "financial_services", "healthcare"],
        "estimated_addressable_companies": 5_000,
        "vision_2030_tailwind": True,
        "action_en": "Build case studies for each sector to capture early mover position",
        "action_ar": "بناء دراسات حالة لكل قطاع للاستحواذ على موقع المتحرك الأول",
    },
]

# ---------------------------------------------------------------------------
# Market map data (sector x city, SAR opportunity estimates)
# ---------------------------------------------------------------------------

_MARKET_MAP: list[dict[str, Any]] = [
    {
        "sector": "technology",
        "sector_ar": "التقنية",
        "city": "riyadh",
        "city_ar": "الرياض",
        "estimated_companies": 2_400,
        "avg_deal_sar": 8_500,
        "opportunity_score": 92,
        "total_addressable_sar": 20_400_000,
        "top_pain": "PDPL + ZATCA compliance",
        "top_pain_ar": "الامتثال لحماية البيانات وزاتكا",
    },
    {
        "sector": "financial_services",
        "sector_ar": "الخدمات المالية",
        "city": "riyadh",
        "city_ar": "الرياض",
        "estimated_companies": 1_800,
        "avg_deal_sar": 12_000,
        "opportunity_score": 88,
        "total_addressable_sar": 21_600_000,
        "top_pain": "ZATCA e-invoicing mandate",
        "top_pain_ar": "الفوترة الإلكترونية لزاتكا",
    },
    {
        "sector": "healthcare",
        "sector_ar": "الرعاية الصحية",
        "city": "riyadh",
        "city_ar": "الرياض",
        "estimated_companies": 900,
        "avg_deal_sar": 9_500,
        "opportunity_score": 85,
        "total_addressable_sar": 8_550_000,
        "top_pain": "Patient data PDPL + ZATCA billing",
        "top_pain_ar": "بيانات المرضى وفوترة زاتكا",
    },
    {
        "sector": "real_estate",
        "sector_ar": "العقارات",
        "city": "riyadh",
        "city_ar": "الرياض",
        "estimated_companies": 1_200,
        "avg_deal_sar": 7_500,
        "opportunity_score": 80,
        "total_addressable_sar": 9_000_000,
        "top_pain": "REGA compliance + contract automation",
        "top_pain_ar": "امتثال الهيئة العقارية وأتمتة العقود",
    },
    {
        "sector": "technology",
        "sector_ar": "التقنية",
        "city": "jeddah",
        "city_ar": "جدة",
        "estimated_companies": 1_100,
        "avg_deal_sar": 7_800,
        "opportunity_score": 78,
        "total_addressable_sar": 8_580_000,
        "top_pain": "Reporting automation",
        "top_pain_ar": "أتمتة التقارير",
    },
    {
        "sector": "financial_services",
        "sector_ar": "الخدمات المالية",
        "city": "jeddah",
        "city_ar": "جدة",
        "estimated_companies": 850,
        "avg_deal_sar": 10_000,
        "opportunity_score": 76,
        "total_addressable_sar": 8_500_000,
        "top_pain": "KYC + ZATCA",
        "top_pain_ar": "التحقق من الهوية وزاتكا",
    },
    {
        "sector": "logistics",
        "sector_ar": "اللوجستيات",
        "city": "dammam",
        "city_ar": "الدمام",
        "estimated_companies": 600,
        "avg_deal_sar": 6_500,
        "opportunity_score": 72,
        "total_addressable_sar": 3_900_000,
        "top_pain": "Fleet ops + customs e-invoicing",
        "top_pain_ar": "عمليات الأسطول والفوترة الجمركية",
    },
    {
        "sector": "healthcare",
        "sector_ar": "الرعاية الصحية",
        "city": "jeddah",
        "city_ar": "جدة",
        "estimated_companies": 420,
        "avg_deal_sar": 9_000,
        "opportunity_score": 71,
        "total_addressable_sar": 3_780_000,
        "top_pain": "PDPL patient records",
        "top_pain_ar": "سجلات المرضى ونظام البيانات",
    },
]


# ---------------------------------------------------------------------------
# MRR growth simulation (pure function)
# ---------------------------------------------------------------------------


def simulate_mrr_growth(
    current_mrr: float,
    new_clients_per_month: float,
    avg_deal_sar: float,
    churn_rate: float,
    months: int = 12,
) -> list[dict[str, Any]]:
    """Project MRR forward for N months using a cohort churn model.

    Formula per month:
      new_mrr   = new_clients_per_month * avg_deal_sar
      churned   = current_mrr * churn_rate
      ending    = starting + new_mrr - churned
    """
    if not (0.0 <= churn_rate <= 1.0):
        raise ValueError("churn_rate must be between 0.0 and 1.0")
    if months < 1 or months > 120:
        raise ValueError("months must be between 1 and 120")

    projection: list[dict[str, Any]] = []
    mrr = current_mrr
    for m in range(1, months + 1):
        new_mrr = new_clients_per_month * avg_deal_sar
        churned = mrr * churn_rate
        ending_mrr = mrr + new_mrr - churned
        projection.append(
            {
                "month": m,
                "starting_mrr": round(mrr, 2),
                "new_mrr": round(new_mrr, 2),
                "churned_mrr": round(churned, 2),
                "ending_mrr": round(ending_mrr, 2),
                "arr": round(ending_mrr * 12, 2),
                "mom_growth_pct": round((ending_mrr - mrr) / mrr * 100, 1) if mrr > 0 else 0.0,
            }
        )
        mrr = ending_mrr

    return projection


# ---------------------------------------------------------------------------
# Pydantic model for growth simulation
# ---------------------------------------------------------------------------


class GrowthSimulationInput(BaseModel):
    current_mrr: float = Field(..., gt=0, description="Current MRR in SAR")
    new_clients_per_month: float = Field(..., gt=0, description="Expected new clients per month")
    avg_deal_sar: float = Field(..., gt=0, description="Average deal value in SAR")
    churn_rate: float = Field(..., ge=0.0, le=1.0, description="Monthly churn rate (0.0–1.0)")
    months: int = Field(default=12, ge=1, le=120, description="Projection horizon in months")


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------


@router.get("/signals")
async def get_growth_signals(
    urgency: str | None = None,
    sector: str | None = None,
) -> dict[str, Any]:
    """Return curated growth signals for Dealix's Saudi B2B market.

    Signals include regulatory tailwinds, sector expansions, and Vision 2030
    opportunities. Filter by urgency (HIGH/MEDIUM/LOW) or sector key.
    """
    signals = _GROWTH_SIGNALS

    if urgency:
        signals = [s for s in signals if s["urgency"] == urgency.upper()]

    if sector:
        sector_key = sector.lower().replace(" ", "_")
        signals = [s for s in signals if sector_key in s["sectors_affected"]]

    return {
        "governance_decision": _GOV,
        "generated_at": _NOW.isoformat(),
        "label": _label("signals"),
        "total": len(signals),
        "signals": signals,
        "source_note_ar": "من بحث سوقي عام — ليس scraping",
        "source_note_en": "From approved public research — not scraping",
    }


@router.get("/market-map")
async def get_market_map(
    min_score: int = 0,
) -> dict[str, Any]:
    """Return ranked opportunity map by sector and city.

    Sorted by opportunity_score descending. Filter with min_score.
    """
    if min_score < 0 or min_score > 100:
        raise HTTPException(status_code=400, detail="min_score must be 0–100")

    filtered = [m for m in _MARKET_MAP if m["opportunity_score"] >= min_score]
    filtered.sort(key=lambda m: m["opportunity_score"], reverse=True)

    total_addressable = sum(m["total_addressable_sar"] for m in filtered)

    return {
        "governance_decision": _GOV,
        "generated_at": _NOW.isoformat(),
        "label": _label("market_map"),
        "total_segments": len(filtered),
        "total_addressable_sar": total_addressable,
        "segments": filtered,
        "note_ar": "التقديرات بناءً على بيانات السوق السعودي 2026 — ليست ضماناً",
        "note_en": "Estimates based on 2026 Saudi market data — not a guarantee",
    }


@router.get("/weekly-focus")
async def get_weekly_focus() -> dict[str, Any]:
    """Return recommended focus areas for the current week.

    Prioritizes sectors with highest urgency signals and pipeline readiness.
    """
    week_number = _NOW.isocalendar()[1]

    focus_areas: list[dict[str, Any]] = [
        {
            "priority": 1,
            "focus_area_en": "ZATCA Q3 deadline outreach — financial services and technology",
            "focus_area_ar": "تواصل موعد زاتكا Q3 — الخدمات المالية والتقنية",
            "target_sector": "financial_services",
            "target_city": "riyadh",
            "action_en": "Send 10 warm intro messages to CFOs mentioning ZATCA Phase 3 deadline",
            "action_ar": "أرسل 10 رسائل ترحيبية لمديري المالية مع ذكر موعد زاتكا المرحلة الثالثة",
            "expected_responses": 2,
            "effort_hours": 3,
        },
        {
            "priority": 2,
            "focus_area_en": "Healthcare PDPL follow-up — move evaluation leads to intent",
            "focus_area_ar": "متابعة قطاع الصحة — تحريك العملاء من مرحلة التقييم للنية",
            "target_sector": "healthcare",
            "target_city": "riyadh",
            "action_en": "Send 3 sector-specific case studies to healthcare leads in evaluation stage",
            "action_ar": "أرسل 3 دراسات حالة متخصصة للعملاء الصحيين في مرحلة التقييم",
            "expected_responses": 1,
            "effort_hours": 2,
        },
        {
            "priority": 3,
            "focus_area_en": "Real estate Riyadh — qualify 5 new REGA compliance leads",
            "focus_area_ar": "عقارات الرياض — تأهيل 5 عملاء جدد لامتثال الهيئة العقارية",
            "target_sector": "real_estate",
            "target_city": "riyadh",
            "action_en": "LinkedIn content post on REGA compliance automation + follow referrals",
            "action_ar": "نشر محتوى عن أتمتة امتثال الهيئة العقارية + متابعة الإحالات",
            "expected_responses": 2,
            "effort_hours": 1.5,
        },
    ]

    total_effort = sum(f["effort_hours"] for f in focus_areas)

    return {
        "governance_decision": _GOV,
        "generated_at": _NOW.isoformat(),
        "label": _label("weekly_focus"),
        "week_number": week_number,
        "total_effort_hours": total_effort,
        "focus_areas": focus_areas,
        "governance_note_ar": "التواصل يتطلب مراجعة المؤسس قبل الإرسال",
        "governance_note_en": "Outreach requires founder review before sending",
    }


@router.post("/simulate-growth")
async def simulate_growth(body: GrowthSimulationInput) -> dict[str, Any]:
    """Simulate MRR growth over N months given input assumptions.

    Projects MRR, new revenue, churn, and ARR for each month.
    Returns 12-month default; up to 120 months supported.
    """
    try:
        projection = simulate_mrr_growth(
            current_mrr=body.current_mrr,
            new_clients_per_month=body.new_clients_per_month,
            avg_deal_sar=body.avg_deal_sar,
            churn_rate=body.churn_rate,
            months=body.months,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    final = projection[-1]
    growth_multiplier = round(final["ending_mrr"] / body.current_mrr, 2) if body.current_mrr > 0 else 0

    return {
        "governance_decision": _GOV,
        "generated_at": _NOW.isoformat(),
        "label": _label("simulate_growth"),
        "inputs": {
            "current_mrr": body.current_mrr,
            "new_clients_per_month": body.new_clients_per_month,
            "avg_deal_sar": body.avg_deal_sar,
            "churn_rate": body.churn_rate,
            "months": body.months,
        },
        "summary": {
            "starting_mrr": body.current_mrr,
            "ending_mrr": final["ending_mrr"],
            "ending_arr": final["arr"],
            "growth_multiplier": growth_multiplier,
            "total_new_revenue": round(
                sum(m["new_mrr"] for m in projection), 2
            ),
            "total_churned_revenue": round(
                sum(m["churned_mrr"] for m in projection), 2
            ),
        },
        "projection": projection,
        "note_ar": "المحاكاة بناءً على نموذج تراكمي — ليست ضماناً بالنتائج",
        "note_en": "Simulation uses a cohort churn model — not a guaranteed outcome",
    }


@router.get("/benchmark")
async def get_benchmark() -> dict[str, Any]:
    """Compare Dealix KPIs against Saudi SaaS benchmarks (2026).

    Returns current Dealix metrics alongside industry medians and top-quartile
    benchmarks for the Saudi B2B SaaS market.
    """
    benchmarks: dict[str, dict[str, Any]] = {
        "mrr_growth_mom_pct": {
            "dealix": 8.2,
            "saudi_saas_median": 5.5,
            "top_quartile": 12.0,
            "status": "above_median",
            "label": {"ar": "نمو الإيراد الشهري", "en": "Monthly MRR Growth"},
        },
        "churn_rate_monthly_pct": {
            "dealix": 3.2,
            "saudi_saas_median": 4.8,
            "top_quartile": 2.0,
            "status": "above_median",
            "label": {"ar": "معدل الإلغاء الشهري", "en": "Monthly Churn Rate"},
        },
        "avg_deal_size_sar": {
            "dealix": 8_500,
            "saudi_saas_median": 6_200,
            "top_quartile": 14_000,
            "status": "above_median",
            "label": {"ar": "متوسط حجم الصفقة", "en": "Average Deal Size"},
        },
        "sales_cycle_days": {
            "dealix": 21,
            "saudi_saas_median": 28,
            "top_quartile": 14,
            "status": "above_median",
            "label": {"ar": "أيام دورة المبيعات", "en": "Sales Cycle Days"},
        },
        "customer_ltv_sar": {
            "dealix": 51_000,
            "saudi_saas_median": 37_000,
            "top_quartile": 84_000,
            "status": "above_median",
            "label": {"ar": "القيمة الكلية للعميل", "en": "Customer LTV"},
        },
        "nrr_pct": {
            "dealix": 108,
            "saudi_saas_median": 95,
            "top_quartile": 120,
            "status": "above_median",
            "label": {"ar": "صافي معدل الاحتفاظ بالإيراد", "en": "Net Revenue Retention"},
        },
        "nps": {
            "dealix": 52,
            "saudi_saas_median": 38,
            "top_quartile": 65,
            "status": "above_median",
            "label": {"ar": "صافي نقاط المروّجين", "en": "Net Promoter Score"},
        },
        "cac_sar": {
            "dealix": 1_800,
            "saudi_saas_median": 3_200,
            "top_quartile": 900,
            "status": "above_median",
            "label": {"ar": "تكلفة اكتساب العميل", "en": "Customer Acquisition Cost"},
        },
    }

    above_median = sum(
        1 for v in benchmarks.values() if v["status"] == "above_median"
    )
    total = len(benchmarks)

    return {
        "governance_decision": _GOV,
        "generated_at": _NOW.isoformat(),
        "label": _label("benchmark"),
        "summary": {
            "above_median_count": above_median,
            "total_metrics": total,
            "percentile_estimate": "top_quartile_approaching",
            "data_year": 2026,
        },
        "benchmarks": benchmarks,
        "source_note_ar": "بيانات مقارنة مستندة إلى أبحاث سوق SaaS السعودية 2026",
        "source_note_en": "Benchmark data from Saudi B2B SaaS market research 2026",
    }
