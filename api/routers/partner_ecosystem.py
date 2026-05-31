"""
Saudi B2B partner ecosystem directory for Dealix.

Maps integration partners, referral partners, and technology alliances
relevant to the Saudi market — ZATCA ISVs, SAMA-regulated FinTechs,
Vision 2030 accelerators, ERP vendors, and cloud providers.
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

router = APIRouter(prefix="/api/v1/partner-ecosystem", tags=["Sales"])

# ---------------------------------------------------------------------------
# Partner directory
# ---------------------------------------------------------------------------

_PARTNERS: dict[str, Any] = {
    "zatca_isv": {
        "category_en": "ZATCA-Certified ISVs",
        "category_ar": "موردو البرمجيات المعتمدون من هيئة الزكاة",
        "relevance_en": (
            "Dealix complements ZATCA-certified ERP/invoicing ISVs by adding "
            "revenue intelligence and sales pipeline analytics on top of compliance data."
        ),
        "relevance_ar": (
            "تكمل ديليكس موردي البرمجيات المعتمدين من هيئة الزكاة بإضافة "
            "ذكاء الإيرادات وتحليلات مسار المبيعات فوق بيانات الامتثال."
        ),
        "partner_types": [
            "SAP (ZATCA-certified)",
            "Oracle NetSuite",
            "Odoo Saudi Edition",
            "Wafeq",
            "Qoyod",
            "Zatca.sa certified local ISVs",
        ],
        "integration_value_en": (
            "Pull invoice data → compute payment velocity → flag at-risk receivables. "
            "ZATCA e-invoicing data becomes revenue intelligence."
        ),
        "integration_value_ar": (
            "سحب بيانات الفواتير ← حساب سرعة الدفع ← تحديد المستحقات المعرضة للخطر. "
            "بيانات الفوترة الإلكترونية لهيئة الزكاة تصبح ذكاء إيرادات."
        ),
        "dealix_pitch_en": "Ask: 'You're ZATCA-compliant — are you turning that data into revenue insights?'",
        "referral_opportunity": True,
    },
    "cloud_providers": {
        "category_en": "Cloud Infrastructure Partners",
        "category_ar": "شركاء البنية التحتية السحابية",
        "relevance_en": (
            "Saudi Arabia's National Cloud Strategy (NCS) mandates Saudi data residency. "
            "Dealix deploys on Saudi-region cloud to satisfy PDPL and NCA requirements."
        ),
        "relevance_ar": (
            "تشترط استراتيجية السحابة الوطنية السعودية الإقامة الداخلية للبيانات. "
            "تنتشر ديليكس على السحابة في المنطقة السعودية لتلبية متطلبات نظام PDPL والهيئة الوطنية للأمن السيبراني."
        ),
        "partner_types": [
            "AWS (Bahrain + Saudi edge)",
            "Microsoft Azure (UAE North, Saudi West)",
            "Google Cloud (KSA region)",
            "STC Cloud (Hyperscale Saudi)",
            "Alibaba Cloud (Middle East)",
        ],
        "integration_value_en": "Data never leaves Saudi borders — key for PDPL Article 29 (cross-border transfer restrictions).",
        "integration_value_ar": "البيانات لا تغادر الحدود السعودية — أمر محوري لنظام حماية البيانات الشخصية.",
        "dealix_pitch_en": "Dealix is cloud-agnostic, deployed in Saudi region on your preferred provider.",
        "referral_opportunity": False,
    },
    "sama_fintechs": {
        "category_en": "SAMA-Regulated FinTechs",
        "category_ar": "شركات التقنية المالية المرخصة من ساما",
        "relevance_en": (
            "SAMA's FinTech sandbox has 80+ licensed players. "
            "Islamic BNPL, open banking, and lending platforms need B2B revenue analytics."
        ),
        "relevance_ar": (
            "بيئة ساندبوكس التقنية المالية لساما تضم أكثر من 80 مرخصاً. "
            "منصات BNPL الإسلامية والبنوك المفتوحة ومنصات الإقراض تحتاج إلى تحليلات إيرادات B2B."
        ),
        "partner_types": [
            "Tamara (BNPL)",
            "Tabby (BNPL)",
            "Lean Technologies (open banking)",
            "Geidea (payments)",
            "STC Pay / STC Bank",
        ],
        "integration_value_en": (
            "FinTechs serving Saudi B2B merchants can offer Dealix as a revenue intelligence add-on. "
            "White-label or referral model."
        ),
        "integration_value_ar": (
            "يمكن لشركات التقنية المالية التي تخدم التجار السعوديين B2B تقديم ديليكس كميزة إضافية لذكاء الإيرادات. "
            "نموذج علامة بيضاء أو إحالة."
        ),
        "dealix_pitch_en": "FinTech partnership deck available — ask for co-selling program.",
        "referral_opportunity": True,
    },
    "vision2030_accelerators": {
        "category_en": "Vision 2030 Accelerators & Incubators",
        "category_ar": "مسرّعات ومحاضن رؤية 2030",
        "relevance_en": (
            "Monsha'at, Badir, Misk, KACST, NEOM Innovation Hub, and LEAP partner programs "
            "provide access to Saudi SME cohorts — Dealix's primary market."
        ),
        "relevance_ar": (
            "تتيح برامج منشآت وبادر ومسك وكاكست ومركز إبداع نيوم وشركاء ليب "
            "الوصول إلى مجموعات المنشآت الصغيرة السعودية — السوق الأساسي لديليكس."
        ),
        "partner_types": [
            "Monsha'at (SME Authority)",
            "Badir Technology Incubator",
            "Misk Innovation",
            "KACST Technology Innovation Center",
            "NEOM Innovation Hub",
            "SVC (Saudi Venture Capital)",
        ],
        "integration_value_en": (
            "Become preferred revenue intelligence partner for accelerator cohorts. "
            "Offer discounted sprint (SAR 249) to cohort companies."
        ),
        "integration_value_ar": (
            "أصبح شريكاً مفضلاً لذكاء الإيرادات لمجموعات المسرّعات. "
            "قدّم سبرنت مخفضاً (249 ريال) لشركات المجموعة."
        ),
        "dealix_pitch_en": "Partnership MOU available for accelerators. Ask for the Monsha'at partnership brief.",
        "referral_opportunity": True,
    },
    "system_integrators": {
        "category_en": "Saudi System Integrators",
        "category_ar": "شركات تكامل الأنظمة السعودية",
        "relevance_en": (
            "Large Saudi SIs (STC Solutions, Elm, Almajal, GBM, Accenture KSA) "
            "handle enterprise digital transformation but lack AI revenue intelligence tooling."
        ),
        "relevance_ar": (
            "تتولى شركات تكامل الأنظمة الكبرى السعودية (حلول STC، إلم، المجال، GBM، أكسنتشر السعودية) "
            "التحول الرقمي للمؤسسات لكنها تفتقر إلى أدوات ذكاء الإيرادات بالذكاء الاصطناعي."
        ),
        "partner_types": [
            "STC Solutions",
            "Elm (إلم)",
            "GBM (Gulf Business Machines)",
            "Accenture KSA",
            "Almajal G4S Technology",
        ],
        "integration_value_en": (
            "Reseller or subcontract model: SI wins enterprise deal, Dealix provides "
            "revenue intelligence module. Revenue share 20–30%."
        ),
        "integration_value_ar": (
            "نموذج إعادة البيع أو المقاولة من الباطن: يفوز SI بعقد المؤسسة، توفر ديليكس "
            "وحدة ذكاء الإيرادات. حصة الإيرادات 20-30٪."
        ),
        "dealix_pitch_en": "White-label API available for enterprise SI deals. Ask for the partnership API spec.",
        "referral_opportunity": True,
    },
}

_PARTNERSHIP_TIERS: list[dict[str, Any]] = [
    {
        "tier": "referral",
        "tier_ar": "إحالة",
        "description_en": "Refer clients, earn 15% of first-year contract value.",
        "description_ar": "أحِل العملاء، واربح 15٪ من قيمة عقد السنة الأولى.",
        "requirements_en": "Signed referral agreement, 2+ qualified leads/quarter.",
        "commission_pct": 15,
        "support_level_en": "Self-serve partner portal, co-branded collateral.",
    },
    {
        "tier": "reseller",
        "tier_ar": "إعادة بيع",
        "description_en": "Resell Dealix to your clients at your own margin (min 20% discount).",
        "description_ar": "أعد بيع ديليكس لعملائك بهامش ربح خاص بك (خصم أدنى 20٪).",
        "requirements_en": "SAR 100K+ annual commitment, 1 dedicated sales rep trained.",
        "commission_pct": 20,
        "support_level_en": "Dedicated partner manager, joint go-to-market plan.",
    },
    {
        "tier": "strategic",
        "tier_ar": "استراتيجي",
        "description_en": "OEM or white-label integration. Dealix engine embedded in your platform.",
        "description_ar": "تكامل OEM أو علامة بيضاء. محرك ديليكس مدمج في منصتك.",
        "requirements_en": "SAR 500K+ annual deal, technical integration, NDA + IP agreement.",
        "commission_pct": None,
        "support_level_en": "Joint product roadmap, shared engineering, co-investment in features.",
    },
]


class PartnershipEnquiryRequest(BaseModel):
    company_name: str = Field(..., min_length=2)
    partner_category: str = Field(..., description="One of the partner category keys")
    preferred_tier: str = Field(..., description="referral | reseller | strategic")
    annual_client_base_size: int = Field(..., ge=1, description="Number of B2B clients you serve")
    notes: str = ""


def _build_partnership_brief(req: PartnershipEnquiryRequest) -> dict[str, Any]:
    category = _PARTNERS.get(req.partner_category)
    tier = next((t for t in _PARTNERSHIP_TIERS if t["tier"] == req.preferred_tier), None)

    if category is None:
        valid = list(_PARTNERS.keys())
        category_summary = f"Category '{req.partner_category}' not found. Valid: {valid}"
        category_name = req.partner_category
    else:
        category_summary = category["relevance_en"]
        category_name = category["category_en"]

    if tier is None:
        tier_name = req.preferred_tier
        commission = None
        support = "Contact partnerships@dealix.sa for custom terms."
    else:
        tier_name = tier["tier"]
        commission = tier.get("commission_pct")
        support = tier["support_level_en"]

    potential_revenue_sar = req.annual_client_base_size * 3_500 * 0.15

    return {
        "company_name": req.company_name,
        "category_en": category_name,
        "preferred_tier": tier_name,
        "partnership_value_en": category_summary,
        "estimated_annual_referral_revenue_sar": round(potential_revenue_sar, 0),
        "commission_pct": commission,
        "support_level_en": support,
        "next_steps_en": [
            f"Send partnership deck to {req.company_name}",
            "Schedule 30-min intro call with Dealix partnerships team",
            "Sign NDA and referral/reseller agreement",
            "Attend joint training: Dealix product + Saudi market positioning",
        ],
        "governance_decision": "APPROVAL_FIRST",
    }


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@router.get("/categories", summary="Saudi partner ecosystem categories")
async def get_categories() -> dict[str, Any]:
    return {
        "categories": {k: {
            "category_en": v["category_en"],
            "category_ar": v["category_ar"],
            "relevance_en": v["relevance_en"],
            "referral_opportunity": v.get("referral_opportunity", False),
        } for k, v in _PARTNERS.items()},
        "total": len(_PARTNERS),
        "governance_decision": "ALLOW_WITH_REVIEW",
    }


@router.get("/categories/{category_id}", summary="Detail for one partner category")
async def get_category(category_id: str) -> dict[str, Any]:
    cat = _PARTNERS.get(category_id)
    if cat is None:
        raise HTTPException(status_code=404, detail=f"Category '{category_id}' not found.")
    return {**cat, "governance_decision": "ALLOW_WITH_REVIEW"}


@router.get("/tiers", summary="Partnership tier definitions")
async def get_tiers() -> dict[str, Any]:
    return {
        "tiers": _PARTNERSHIP_TIERS,
        "governance_decision": "ALLOW_WITH_REVIEW",
    }


@router.post("/enquiry", summary="Generate partnership brief — requires founder review")
async def partnership_enquiry(req: PartnershipEnquiryRequest) -> dict[str, Any]:
    return _build_partnership_brief(req)
