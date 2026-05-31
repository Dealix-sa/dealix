"""
Saudi B2B AI market sizing intelligence.

TAM/SAM/SOM estimates for AI automation across Saudi sectors,
with Vision 2030 growth drivers and addressable segment sizes.
Estimates based on public MCIT, Monsha'at, and KPMG/McKinsey Saudi
digital economy reports. No guaranteed-outcome language.
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

router = APIRouter(prefix="/api/v1/market-sizing", tags=["Analytics"])

# ---------------------------------------------------------------------------
# Saudi B2B AI market data (2024-2030 estimates)
# ---------------------------------------------------------------------------

_MARKET_DATA: dict[str, dict[str, Any]] = {
    "ai_software_saas": {
        "sector": "ai_software_saas",
        "name_ar": "برمجيات الذكاء الاصطناعي وSaaS",
        "name_en": "AI Software & SaaS",
        "tam_sar_billion": 45.0,
        "sam_sar_billion": 12.0,
        "som_sar_million_5y": 180.0,
        "cagr_pct": 32,
        "vision2030_driver": "National AI Strategy: 14,500 AI specialists by 2030",
        "vision2030_driver_ar": "استراتيجية الذكاء الاصطناعي الوطنية: 14,500 متخصص بحلول 2030",
        "key_buyers": ["ARAMCO", "SABIC", "STC", "Public sector ministries", "Banks"],
        "typical_deal_size_sar": {"min": 50_000, "max": 5_000_000},
        "sales_cycle_days": {"min": 45, "max": 180},
        "decision_complexity": "high",
        "top_pain_points": [
            "Manual reporting and analytics",
            "ZATCA Phase 2 e-invoicing compliance",
            "Arabic NLP for customer-facing applications",
            "Data governance and PDPL compliance",
        ],
    },
    "fintech": {
        "sector": "fintech",
        "name_ar": "التقنية المالية",
        "name_en": "FinTech",
        "tam_sar_billion": 28.0,
        "sam_sar_billion": 7.5,
        "som_sar_million_5y": 95.0,
        "cagr_pct": 24,
        "vision2030_driver": "SAMA FinTech Lab + open banking mandate by 2025",
        "vision2030_driver_ar": "مختبر FinTech لمؤسسة النقد + تفويح الخدمات المصرفية المفتوحة بحلول 2025",
        "key_buyers": ["Islamic banks", "Payment fintechs", "Insurance (insurtech)", "BNPL providers"],
        "typical_deal_size_sar": {"min": 100_000, "max": 3_000_000},
        "sales_cycle_days": {"min": 60, "max": 240},
        "decision_complexity": "very_high",
        "top_pain_points": [
            "KYC/AML automation",
            "Islamic finance product pricing models",
            "Open banking API integration",
            "Fraud detection",
        ],
    },
    "healthcare": {
        "sector": "healthcare",
        "name_ar": "الرعاية الصحية",
        "name_en": "Healthcare",
        "tam_sar_billion": 22.0,
        "sam_sar_billion": 6.0,
        "som_sar_million_5y": 75.0,
        "cagr_pct": 19,
        "vision2030_driver": "Healthcare privatization: 290+ new hospitals by 2030",
        "vision2030_driver_ar": "خصخصة الرعاية الصحية: أكثر من 290 مستشفى جديد بحلول 2030",
        "key_buyers": ["Private hospital groups", "MOH suppliers", "Specialty clinics", "Pharma"],
        "typical_deal_size_sar": {"min": 75_000, "max": 2_000_000},
        "sales_cycle_days": {"min": 90, "max": 365},
        "decision_complexity": "high",
        "top_pain_points": [
            "Patient data management and PDPL compliance",
            "Appointment scheduling optimization",
            "Medical Arabic NLP",
            "Insurance claims automation",
        ],
    },
    "logistics": {
        "sector": "logistics",
        "name_ar": "اللوجستيات وسلاسل التوريد",
        "name_en": "Logistics & Supply Chain",
        "tam_sar_billion": 18.0,
        "sam_sar_billion": 5.5,
        "som_sar_million_5y": 65.0,
        "cagr_pct": 21,
        "vision2030_driver": "NEOM Smart Logistics + Red Sea Port expansion",
        "vision2030_driver_ar": "نيوم لوجستيك الذكي + توسعة ميناء البحر الأحمر",
        "key_buyers": ["Saudi Post", "Aramex KSA", "NEOM contractors", "Retail chains"],
        "typical_deal_size_sar": {"min": 50_000, "max": 1_500_000},
        "sales_cycle_days": {"min": 30, "max": 120},
        "decision_complexity": "medium",
        "top_pain_points": [
            "Last-mile delivery optimization",
            "Warehouse automation ROI",
            "Cross-border customs documentation",
            "Route optimization for prayer time breaks",
        ],
    },
    "real_estate": {
        "sector": "real_estate",
        "name_ar": "العقارات",
        "name_en": "Real Estate & PropTech",
        "tam_sar_billion": 15.0,
        "sam_sar_billion": 4.0,
        "som_sar_million_5y": 50.0,
        "cagr_pct": 18,
        "vision2030_driver": "70% homeownership target; NEOM + Diriyah + AlUla mega-projects",
        "vision2030_driver_ar": "هدف 70% تملّك المساكن؛ مشاريع نيوم والدرعية والعُلا العملاقة",
        "key_buyers": ["Dar Al Arkan", "Emaar KSA", "Retal Urban", "ROSHN", "Developers"],
        "typical_deal_size_sar": {"min": 30_000, "max": 800_000},
        "sales_cycle_days": {"min": 30, "max": 90},
        "decision_complexity": "medium",
        "top_pain_points": [
            "Property valuation automation",
            "Tenant management AI",
            "Mortgage document processing (ZATCA)",
            "Arabic chatbots for lead qualification",
        ],
    },
    "retail": {
        "sector": "retail",
        "name_ar": "تجارة التجزئة",
        "name_en": "Retail",
        "tam_sar_billion": 20.0,
        "sam_sar_billion": 5.0,
        "som_sar_million_5y": 60.0,
        "cagr_pct": 15,
        "vision2030_driver": "Retail modernization + 150M+ tourist influx driving demand",
        "vision2030_driver_ar": "تحديث التجزئة + أكثر من 150 مليون سائح يدفعون الطلب",
        "key_buyers": ["Panda Retail", "BinDawood", "Jarir Bookstore", "eCommerce players"],
        "typical_deal_size_sar": {"min": 25_000, "max": 500_000},
        "sales_cycle_days": {"min": 21, "max": 60},
        "decision_complexity": "low",
        "top_pain_points": [
            "Inventory forecasting for Ramadan/Eid spikes",
            "ZATCA POS integration",
            "Arabic product recommendation",
            "Supply chain visibility",
        ],
    },
    "government_public_sector": {
        "sector": "government_public_sector",
        "name_ar": "القطاع الحكومي",
        "name_en": "Government & Public Sector",
        "tam_sar_billion": 35.0,
        "sam_sar_billion": 4.5,
        "som_sar_million_5y": 55.0,
        "cagr_pct": 14,
        "vision2030_driver": "Government Digital Transformation (CITC, Yesser program)",
        "vision2030_driver_ar": "التحول الرقمي الحكومي (هيئة الاتصالات، برنامج ياسر)",
        "key_buyers": ["Ministries via Etimad portal", "MOMRA", "MOE", "MOH"],
        "typical_deal_size_sar": {"min": 200_000, "max": 10_000_000},
        "sales_cycle_days": {"min": 180, "max": 730},
        "decision_complexity": "very_high",
        "top_pain_points": [
            "Government process automation (G2C services)",
            "Arabic document processing",
            "NCA-compliant cybersecurity",
            "Vision 2030 KPI tracking",
        ],
    },
}

# ---------------------------------------------------------------------------
# Pydantic models
# ---------------------------------------------------------------------------

class SOMCalculatorInput(BaseModel):
    sector: str = Field(..., description="Sector ID from GET /api/v1/market-sizing/sectors")
    target_market_share_pct: float = Field(
        ..., gt=0, le=100, description="Target market share % in the SAM"
    )
    years: int = Field(3, ge=1, le=10)


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@router.get("/sectors", summary="Saudi B2B AI sector market sizes")
async def list_sectors() -> dict[str, Any]:
    return {
        "sectors": [
            {
                "sector": k,
                "name_ar": v["name_ar"],
                "name_en": v["name_en"],
                "tam_sar_billion": v["tam_sar_billion"],
                "sam_sar_billion": v["sam_sar_billion"],
                "cagr_pct": v["cagr_pct"],
                "decision_complexity": v["decision_complexity"],
            }
            for k, v in _MARKET_DATA.items()
        ],
        "total_tam_sar_billion": round(sum(v["tam_sar_billion"] for v in _MARKET_DATA.values()), 1),
        "total_sam_sar_billion": round(sum(v["sam_sar_billion"] for v in _MARKET_DATA.values()), 1),
        "methodology_note_en": (
            "TAM = Total Saudi B2B AI/automation software market. "
            "SAM = Serviceable portion via SaaS/managed services. "
            "Sources: MCIT Digital Economy Report 2023, Monsha'at SME Report 2024, "
            "KPMG Saudi AI Outlook 2024. Estimates are indicative."
        ),
        "methodology_note_ar": (
            "TAM = إجمالي السوق السعودي لبرامج الذكاء الاصطناعي B2B. "
            "SAM = الجزء القابل للخدمة عبر SaaS/العمليات المُدارة. "
            "المصادر: تقرير الاقتصاد الرقمي لوزارة الاتصالات 2023، تقرير منشآت 2024. "
            "التقديرات استرشادية."
        ),
        "governance_decision": "ALLOW_WITH_REVIEW",
    }


@router.get("/sectors/{sector_id}", summary="Detailed market intelligence for a sector")
async def get_sector(sector_id: str) -> dict[str, Any]:
    sector = _MARKET_DATA.get(sector_id)
    if not sector:
        raise HTTPException(
            status_code=404,
            detail=f"Sector '{sector_id}' not found. Use GET /api/v1/market-sizing/sectors.",
        )
    return {
        **sector,
        "disclaimer_en": (
            "Market estimates are indicative ranges based on public reports. "
            "Actual market size and addressable segments depend on go-to-market specifics."
        ),
        "disclaimer_ar": (
            "تقديرات السوق نطاقات استرشادية مستندة إلى تقارير عامة. "
            "حجم السوق الفعلي والشرائح القابلة للاستهداف تعتمد على تفاصيل الذهاب إلى السوق."
        ),
        "governance_decision": "ALLOW_WITH_REVIEW",
    }


@router.post("/calculate-som", summary="Calculate Serviceable Obtainable Market (SOM)")
async def calculate_som(body: SOMCalculatorInput) -> dict[str, Any]:
    sector = _MARKET_DATA.get(body.sector)
    if not sector:
        raise HTTPException(
            status_code=404,
            detail=f"Sector '{body.sector}' not found. Use GET /api/v1/market-sizing/sectors.",
        )

    sam_sar = sector["sam_sar_billion"] * 1_000_000_000
    som_sar = sam_sar * body.target_market_share_pct / 100

    # Project with CAGR
    cagr = sector["cagr_pct"] / 100
    future_sam = sam_sar * (1 + cagr) ** body.years
    future_som = future_sam * body.target_market_share_pct / 100

    return {
        "sector": body.sector,
        "sector_name_en": sector["name_en"],
        "target_market_share_pct": body.target_market_share_pct,
        "current_sam_sar": round(sam_sar, 0),
        "current_som_sar": round(som_sar, 0),
        "projected_sam_sar_in_n_years": round(future_sam, 0),
        "projected_som_sar_in_n_years": round(future_som, 0),
        "years": body.years,
        "assumed_cagr_pct": sector["cagr_pct"],
        "note_en": (
            f"At {body.target_market_share_pct}% of SAM, "
            f"your {body.years}-year SOM is approximately "
            f"SAR {future_som / 1_000_000:.1f}M — assuming {sector['cagr_pct']}% sector CAGR."
        ),
        "note_ar": (
            f"بحصة {body.target_market_share_pct}% من SAM، "
            f"إجمالي السوق القابل للحصول خلال {body.years} سنوات هو تقريباً "
            f"{future_som / 1_000_000:.1f} مليون ريال — بافتراض نمو سنوي {sector['cagr_pct']}%."
        ),
        "disclaimer_en": (
            "Market share projections are illustrative. "
            "Actual results depend on execution, competition, and market conditions."
        ),
        "disclaimer_ar": (
            "تسقطات حصة السوق استرشادية. "
            "النتائج الفعلية تعتمد على التنفيذ والمنافسة وظروف السوق."
        ),
        "governance_decision": "ALLOW_WITH_REVIEW",
    }


@router.get("/comparison", summary="Side-by-side comparison of top sectors by attractiveness")
async def compare_sectors(
    by: str = Query("cagr", description="Sort by: cagr | sam | tam | sales_cycle"),
) -> dict[str, Any]:
    sectors = list(_MARKET_DATA.values())

    sort_key = {
        "cagr": lambda s: s["cagr_pct"],
        "sam": lambda s: s["sam_sar_billion"],
        "tam": lambda s: s["tam_sar_billion"],
        "sales_cycle": lambda s: -s["sales_cycle_days"]["min"],  # shorter = better
    }.get(by, lambda s: s["cagr_pct"])

    ranked = sorted(sectors, key=sort_key, reverse=True)

    return {
        "ranked_by": by,
        "sectors": [
            {
                "rank": i + 1,
                "sector": s["sector"],
                "name_en": s["name_en"],
                "name_ar": s["name_ar"],
                "cagr_pct": s["cagr_pct"],
                "sam_sar_billion": s["sam_sar_billion"],
                "typical_deal_min_sar": s["typical_deal_size_sar"]["min"],
                "sales_cycle_min_days": s["sales_cycle_days"]["min"],
                "decision_complexity": s["decision_complexity"],
            }
            for i, s in enumerate(ranked)
        ],
        "governance_decision": "ALLOW_WITH_REVIEW",
    }
