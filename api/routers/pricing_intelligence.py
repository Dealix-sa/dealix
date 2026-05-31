"""Pricing Intelligence API — Saudi B2B market rates, competitor landscape,
win-rate simulation, tier optimisation, and discount policy.

Endpoints:
  GET  /api/v1/pricing-intelligence/market-rates         — avg deal sizes by sector
  GET  /api/v1/pricing-intelligence/competitor-landscape — competitor pricing overview
  POST /api/v1/pricing-intelligence/win-rate-simulator   — win-rate prediction
  GET  /api/v1/pricing-intelligence/tier-optimization    — per-tier floor/ceiling/upsell
  GET  /api/v1/pricing-intelligence/discount-policy      — max discount rules per tier

All endpoints:
  - Require admin auth (X-Admin-API-Key)
  - governance_decision: ALLOW_WITH_REVIEW (except discount-policy: APPROVAL_FIRST)
  - Bilingual ar/en labels
  - Prices in SAR
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
    prefix="/api/v1/pricing-intelligence",
    tags=["pricing-intelligence"],
    dependencies=[Depends(require_admin_key)],
)

_GOV = "ALLOW_WITH_REVIEW"
_GOV_APPROVAL = "APPROVAL_FIRST"
_NOW = datetime.now(UTC)

# ---------------------------------------------------------------------------
# Saudi B2B deal size benchmarks by sector (SAR)
# ---------------------------------------------------------------------------

_SECTOR_DEAL_SIZES: dict[str, int] = {
    "technology": 4_500,
    "logistics": 3_200,
    "healthcare": 5_500,
    "financial_services": 6_000,
    "retail": 2_800,
    "real_estate": 4_200,
    "manufacturing": 3_800,
    "education": 2_500,
}

_SECTOR_LABELS_AR: dict[str, str] = {
    "technology": "التقنية",
    "logistics": "اللوجستيات",
    "healthcare": "الرعاية الصحية",
    "financial_services": "الخدمات المالية",
    "retail": "التجزئة",
    "real_estate": "العقارات",
    "manufacturing": "التصنيع",
    "education": "التعليم",
}

# ---------------------------------------------------------------------------
# Dealix product tiers
# ---------------------------------------------------------------------------

_TIERS: list[dict[str, Any]] = [
    {
        "tier_id": "sprint_499",
        "name_en": "Revenue Proof Sprint",
        "name_ar": "سبرنت إثبات الإيرادات",
        "current_price_sar": 499,
        "floor_sar": 399,
        "ceiling_sar": 699,
        "upsell_trigger_score": 72,
        "upsell_target_en": "Data-to-Revenue Pack",
        "upsell_target_ar": "حزمة البيانات والإيرادات",
        "kind": "one_off",
    },
    {
        "tier_id": "data_pack_1500",
        "name_en": "Data-to-Revenue Pack",
        "name_ar": "حزمة البيانات والإيرادات",
        "current_price_sar": 1_500,
        "floor_sar": 1_200,
        "ceiling_sar": 2_000,
        "upsell_trigger_score": 68,
        "upsell_target_en": "Growth Ops Monthly",
        "upsell_target_ar": "عمليات النمو الشهرية",
        "kind": "one_off",
    },
    {
        "tier_id": "growth_ops_2999",
        "name_en": "Growth Ops Monthly",
        "name_ar": "عمليات النمو الشهرية",
        "current_price_sar": 2_999,
        "floor_sar": 2_499,
        "ceiling_sar": 3_499,
        "upsell_trigger_score": 75,
        "upsell_target_en": "Support OS Add-on",
        "upsell_target_ar": "إضافة دعم العمليات",
        "kind": "subscription",
    },
    {
        "tier_id": "support_addon_1500",
        "name_en": "Support OS Add-on",
        "name_ar": "إضافة دعم العمليات",
        "current_price_sar": 1_500,
        "floor_sar": 1_200,
        "ceiling_sar": 1_800,
        "upsell_trigger_score": 80,
        "upsell_target_en": "Executive Command Center",
        "upsell_target_ar": "مركز القيادة التنفيذية",
        "kind": "subscription",
    },
    {
        "tier_id": "executive_7500",
        "name_en": "Executive Command Center",
        "name_ar": "مركز القيادة التنفيذية",
        "current_price_sar": 7_500,
        "floor_sar": 6_500,
        "ceiling_sar": 9_500,
        "upsell_trigger_score": 85,
        "upsell_target_en": "Custom Enterprise Agreement",
        "upsell_target_ar": "اتفاقية مؤسسية مخصصة",
        "kind": "subscription",
    },
]

# ---------------------------------------------------------------------------
# Win-rate data by deal-size bucket (historical approximation)
# ---------------------------------------------------------------------------

_WIN_RATE_BUCKETS: list[dict[str, Any]] = [
    {
        "bucket_label_en": "Entry (0–1,999 SAR)",
        "bucket_label_ar": "مدخل (0–1,999 ريال)",
        "min_sar": 0,
        "max_sar": 1_999,
        "win_rate": 0.52,
        "sample_size": 47,
    },
    {
        "bucket_label_en": "Core (2,000–3,999 SAR)",
        "bucket_label_ar": "أساسي (2,000–3,999 ريال)",
        "min_sar": 2_000,
        "max_sar": 3_999,
        "win_rate": 0.45,
        "sample_size": 83,
    },
    {
        "bucket_label_en": "Mid-market (4,000–6,999 SAR)",
        "bucket_label_ar": "متوسط (4,000–6,999 ريال)",
        "min_sar": 4_000,
        "max_sar": 6_999,
        "win_rate": 0.38,
        "sample_size": 54,
    },
    {
        "bucket_label_en": "Enterprise (7,000+ SAR)",
        "bucket_label_ar": "مؤسسي (7,000+ ريال)",
        "min_sar": 7_000,
        "max_sar": 999_999,
        "win_rate": 0.28,
        "sample_size": 19,
    },
]

# ---------------------------------------------------------------------------
# Competitor pricing landscape (fictional Saudi tech companies)
# ---------------------------------------------------------------------------

_COMPETITORS: list[dict[str, Any]] = [
    {
        "name": "AlphaRevenue",
        "positioning_en": "Revenue analytics for Saudi mid-market",
        "positioning_ar": "تحليلات الإيرادات للسوق السعودي المتوسط",
        "entry_price_sar": 1_800,
        "mid_price_sar": 3_500,
        "enterprise_price_sar": 8_000,
        "pricing_model": "tiered_subscription",
        "pricing_model_ar": "اشتراك متدرج",
        "strength_en": "Established brand in Riyadh fintech",
        "strength_ar": "علامة تجارية راسخة في تقنية مالية الرياض",
        "weakness_en": "No proof-pack delivery; report-only",
        "weakness_ar": "لا حزمة أدلة؛ تقارير فقط",
    },
    {
        "name": "NexusOps",
        "positioning_en": "Operations automation for logistics and manufacturing",
        "positioning_ar": "أتمتة العمليات للخدمات اللوجستية والتصنيع",
        "entry_price_sar": 2_200,
        "mid_price_sar": 4_800,
        "enterprise_price_sar": 10_000,
        "pricing_model": "annual_contract",
        "pricing_model_ar": "عقد سنوي",
        "strength_en": "Deep logistics integrations",
        "strength_ar": "تكاملات لوجستية عميقة",
        "weakness_en": "Long onboarding (8–12 weeks)",
        "weakness_ar": "إعداد طويل (8–12 أسبوع)",
    },
    {
        "name": "DataFlow KSA",
        "positioning_en": "Data pipeline and BI for Saudi SMEs",
        "positioning_ar": "خطوط بيانات وذكاء أعمال للشركات الصغيرة",
        "entry_price_sar": 1_200,
        "mid_price_sar": 2_800,
        "enterprise_price_sar": 6_500,
        "pricing_model": "seat_based",
        "pricing_model_ar": "حسب عدد المستخدمين",
        "strength_en": "Low entry price attracts early-stage companies",
        "strength_ar": "سعر منخفض يجذب الشركات الناشئة",
        "weakness_en": "No AI layer; manual configuration",
        "weakness_ar": "بدون طبقة ذكاء اصطناعي؛ إعداد يدوي",
    },
    {
        "name": "RiyadhTech",
        "positioning_en": "Full-suite ERP add-ons for Saudi corporates",
        "positioning_ar": "إضافات ERP متكاملة للشركات السعودية",
        "entry_price_sar": 3_000,
        "mid_price_sar": 6_000,
        "enterprise_price_sar": 15_000,
        "pricing_model": "module_based",
        "pricing_model_ar": "حسب الوحدات",
        "strength_en": "Deep SAP and Oracle integration",
        "strength_ar": "تكامل عميق مع SAP وOracle",
        "weakness_en": "High minimum contract (12 months); limited flexibility",
        "weakness_ar": "عقد أدنى 12 شهر؛ مرونة محدودة",
    },
    {
        "name": "Jadara Analytics",
        "positioning_en": "Marketing and sales analytics for retail and e-commerce",
        "positioning_ar": "تحليلات التسويق والمبيعات للتجزئة والتجارة الإلكترونية",
        "entry_price_sar": 900,
        "mid_price_sar": 2_200,
        "enterprise_price_sar": 5_000,
        "pricing_model": "usage_based",
        "pricing_model_ar": "حسب الاستخدام",
        "strength_en": "Affordable analytics dashboard",
        "strength_ar": "لوحة تحليلات بأسعار معقولة",
        "weakness_en": "B2B features limited; no governance layer",
        "weakness_ar": "ميزات B2B محدودة؛ بدون طبقة حوكمة",
    },
]

# ---------------------------------------------------------------------------
# Discount policy per tier
# ---------------------------------------------------------------------------

_DISCOUNT_POLICY: list[dict[str, Any]] = [
    {
        "tier_id": "sprint_499",
        "name_en": "Revenue Proof Sprint",
        "name_ar": "سبرنت إثبات الإيرادات",
        "max_discount_pct": 10,
        "requires_approval": True,
        "approval_level_en": "Founder sign-off required",
        "approval_level_ar": "يتطلب موافقة المؤسس",
        "conditions_en": "Only for warm-referral or multi-deal bundling",
        "conditions_ar": "فقط للإحالات الدافئة أو تجميع الصفقات",
    },
    {
        "tier_id": "data_pack_1500",
        "name_en": "Data-to-Revenue Pack",
        "name_ar": "حزمة البيانات والإيرادات",
        "max_discount_pct": 15,
        "requires_approval": True,
        "approval_level_en": "Founder sign-off required",
        "approval_level_ar": "يتطلب موافقة المؤسس",
        "conditions_en": "Only when bundled with sprint or retainer",
        "conditions_ar": "فقط عند الدمج مع السبرنت أو الاستبقاء",
    },
    {
        "tier_id": "growth_ops_2999",
        "name_en": "Growth Ops Monthly",
        "name_ar": "عمليات النمو الشهرية",
        "max_discount_pct": 10,
        "requires_approval": True,
        "approval_level_en": "Founder sign-off required",
        "approval_level_ar": "يتطلب موافقة المؤسس",
        "conditions_en": "Quarterly prepayment only; no rolling-month discount",
        "conditions_ar": "دفع ربع سنوي مسبق فقط؛ لا خصم شهري متكرر",
    },
    {
        "tier_id": "support_addon_1500",
        "name_en": "Support OS Add-on",
        "name_ar": "إضافة دعم العمليات",
        "max_discount_pct": 10,
        "requires_approval": True,
        "approval_level_en": "Founder sign-off required",
        "approval_level_ar": "يتطلب موافقة المؤسس",
        "conditions_en": "Only when bundled with Growth Ops tier",
        "conditions_ar": "فقط عند دمجه مع مستوى عمليات النمو",
    },
    {
        "tier_id": "executive_7500",
        "name_en": "Executive Command Center",
        "name_ar": "مركز القيادة التنفيذية",
        "max_discount_pct": 5,
        "requires_approval": True,
        "approval_level_en": "Founder sign-off required — no exceptions",
        "approval_level_ar": "موافقة المؤسس إلزامية — بدون استثناءات",
        "conditions_en": "Annual contract only; no monthly discount",
        "conditions_ar": "عقد سنوي فقط؛ لا خصم شهري",
    },
]

# ---------------------------------------------------------------------------
# Pure helper functions
# ---------------------------------------------------------------------------


def _predict_win_rate(
    proposed_price_sar: float,
    sector: str,
    company_size: str,
) -> dict[str, Any]:
    """Return predicted win rate and confidence based on deal size bucket.

    Sector and company_size modulate the base bucket win rate slightly.
    All outputs are estimates, not guarantees.
    """
    base_rate: float = 0.35
    confidence: float = 0.60

    for bucket in _WIN_RATE_BUCKETS:
        if bucket["min_sar"] <= proposed_price_sar <= bucket["max_sar"]:
            base_rate = bucket["win_rate"]
            confidence = min(0.90, bucket["sample_size"] / 100.0 + 0.40)
            break

    sector_key = sector.lower().replace(" ", "_")
    sector_avg = _SECTOR_DEAL_SIZES.get(sector_key, 3_500)

    if proposed_price_sar <= sector_avg * 0.8:
        base_rate = min(0.65, base_rate + 0.05)
    elif proposed_price_sar >= sector_avg * 1.3:
        base_rate = max(0.25, base_rate - 0.07)

    size_lower = company_size.lower()
    if size_lower in ("small", "sme", "startup"):
        base_rate = min(0.65, base_rate + 0.03)
    elif size_lower in ("enterprise", "large", "corporate"):
        base_rate = max(0.25, base_rate - 0.04)

    recommended_min = max(0, sector_avg * 0.75)
    recommended_max = sector_avg * 1.25

    return {
        "predicted_win_rate": round(base_rate, 3),
        "confidence": round(confidence, 2),
        "recommended_range_ar": f"النطاق المقترح: {recommended_min:,.0f}–{recommended_max:,.0f} ريال",
        "recommended_range_en": f"Recommended range: {recommended_min:,.0f}–{recommended_max:,.0f} SAR",
        "sector_avg_deal_sar": sector_avg,
        "note_ar": "التوقع تقديري بناءً على بيانات تاريخية — ليس ضماناً",
        "note_en": "Prediction is an estimate from historical data — not a guarantee",
    }


# ---------------------------------------------------------------------------
# Pydantic models
# ---------------------------------------------------------------------------


class WinRateSimulatorInput(BaseModel):
    proposed_price_sar: float = Field(..., ge=0, description="Proposed deal price in SAR")
    sector: str = Field(..., min_length=1, description="Target sector key")
    company_size: str = Field(
        default="sme",
        description="Target company size: startup/sme/enterprise",
    )


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------


@router.get("/market-rates")
async def get_market_rates() -> dict[str, Any]:
    """Return average B2B deal sizes by sector with a Dealix recommended price.

    Recommendation is set at 90% of the market average to maintain
    a value-positioned entry point.
    """
    sectors = []
    for sector_key, avg_sar in sorted(
        _SECTOR_DEAL_SIZES.items(), key=lambda x: x[1], reverse=True
    ):
        recommended_sar = round(avg_sar * 0.9, -1)
        sectors.append(
            {
                "sector": sector_key,
                "sector_ar": _SECTOR_LABELS_AR.get(sector_key, sector_key),
                "market_avg_sar": avg_sar,
                "dealix_recommended_sar": int(recommended_sar),
                "delta_to_market_pct": round(
                    (recommended_sar - avg_sar) / avg_sar * 100, 1
                ),
            }
        )

    return {
        "governance_decision": _GOV,
        "generated_at": _NOW.isoformat(),
        "note_ar": "الأسعار تقديرية بناءً على بيانات السوق السعودي — ليست ضماناً",
        "note_en": "Prices are estimates from Saudi market data — not a guarantee",
        "sectors": sectors,
        "currency": "SAR",
    }


@router.get("/competitor-landscape")
async def get_competitor_landscape() -> dict[str, Any]:
    """Return fictional competitor pricing overview.

    No real company names are used. All pricing is approximated from
    public market research, not scraping or proprietary data.
    """
    return {
        "governance_decision": _GOV,
        "generated_at": _NOW.isoformat(),
        "competitors": _COMPETITORS,
        "source_note_en": "Based on public market research — no proprietary data used",
        "source_note_ar": "مستند إلى أبحاث السوق العامة — لا تُستخدم بيانات خاصة",
        "disclaimer_en": "Competitor names are fictional; used for scenario planning only",
        "disclaimer_ar": "أسماء المنافسين خيالية؛ للتخطيط الاستراتيجي فقط",
        "currency": "SAR",
    }


@router.post("/win-rate-simulator")
async def win_rate_simulator(body: WinRateSimulatorInput) -> dict[str, Any]:
    """Predict win rate for a proposed deal price given sector and company size.

    Uses a bucket-based elasticity model derived from historical deal data.
    Output is a probability estimate, not a guaranteed outcome.
    """
    prediction = _predict_win_rate(
        proposed_price_sar=body.proposed_price_sar,
        sector=body.sector,
        company_size=body.company_size,
    )

    return {
        "governance_decision": _GOV,
        "generated_at": _NOW.isoformat(),
        "inputs": {
            "proposed_price_sar": body.proposed_price_sar,
            "sector": body.sector,
            "company_size": body.company_size,
        },
        **prediction,
        "currency": "SAR",
    }


@router.get("/tier-optimization")
async def get_tier_optimization() -> dict[str, Any]:
    """Return floor, ceiling, and upsell trigger score for each Dealix product tier.

    Floors and ceilings are based on market elasticity analysis.
    Upsell trigger score is the adoption score threshold above which
    a tier upgrade conversation should be initiated.
    """
    return {
        "governance_decision": _GOV,
        "generated_at": _NOW.isoformat(),
        "tiers": _TIERS,
        "methodology_en": (
            "Floor = minimum price that maintains perceived value. "
            "Ceiling = maximum price the market segment absorbs without friction. "
            "Upsell trigger = adoption score (0-100) above which upsell is appropriate."
        ),
        "methodology_ar": (
            "الحد الأدنى = أقل سعر يحافظ على القيمة المدركة. "
            "الحد الأقصى = أعلى سعر يستوعبه القطاع بلا احتكاك. "
            "مستوى البيع التصاعدي = درجة التبني (0-100) التي يُناسب فوقها التصعيد."
        ),
        "currency": "SAR",
    }


@router.get("/discount-policy")
async def get_discount_policy() -> dict[str, Any]:
    """Return maximum discount rules per tier.

    All discounts require founder sign-off before application.
    governance_decision is APPROVAL_FIRST because discount authorisation
    must be recorded before any quote is issued to a customer.
    """
    return {
        "governance_decision": _GOV_APPROVAL,
        "generated_at": _NOW.isoformat(),
        "policy_en": (
            "No discount may be applied without an explicit founder approval "
            "recorded in the approval center. Discounts beyond the stated ceiling "
            "are prohibited."
        ),
        "policy_ar": (
            "لا يجوز تطبيق أي خصم دون موافقة صريحة من المؤسس "
            "مسجلة في مركز الاعتماد. الخصومات التي تتجاوز السقف المحدد محظورة."
        ),
        "discount_policy": _DISCOUNT_POLICY,
        "currency": "SAR",
        "hard_gate_ar": "جميع الخصومات تتطلب اعتماد المؤسس — لا استثناءات",
        "hard_gate_en": "All discounts require founder approval — no exceptions",
    }
