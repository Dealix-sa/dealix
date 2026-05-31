"""
Saudi B2B proposal structure builder.

Generates structured, bilingual proposal outlines tailored to the
Dealix service tier, client sector, and identified pain. Pure Python —
no LLM calls. Returns a structured JSON proposal that the founder
reviews and refines before sending.

All proposals include Saudi-market-specific sections (Vision 2030
alignment, ZATCA/PDPL, Saudization impact, Islamic finance payment
options). No cold outreach — founder must initiate manually.
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

router = APIRouter(prefix="/api/v1/proposal-builder", tags=["Sales"])

# ---------------------------------------------------------------------------
# Tier templates
# ---------------------------------------------------------------------------

_TIERS: dict[str, dict[str, Any]] = {
    "free_diagnostic": {
        "id": "free_diagnostic",
        "name_ar": "تشخيص مجاني",
        "name_en": "Free Diagnostic",
        "price_sar": 0,
        "duration": "30 minutes",
        "deliverables_en": [
            "Diagnostic report: top 3 revenue/efficiency gaps identified",
            "Prioritized action list (5 quick wins)",
            "Go/No-Go recommendation for paid engagement",
        ],
        "deliverables_ar": [
            "تقرير تشخيصي: أفضل 3 ثغرات في الإيرادات/الكفاءة",
            "قائمة أولويات العمل (5 مكاسب سريعة)",
            "توصية المضي/عدم المضي للمشاركة المدفوعة",
        ],
        "suitable_for": ["SME first meeting", "Qualifying new prospect"],
        "decision_maker": "Any level",
    },
    "sprint": {
        "id": "sprint",
        "name_ar": "سبرينت استخبارات الإيرادات",
        "name_en": "7-Day Revenue Intelligence Sprint",
        "price_sar": 499,
        "duration": "7 business days",
        "deliverables_en": [
            "Data quality score for prospect's top data sources",
            "3 prioritized revenue intelligence insights",
            "Quick-win automation recommendation (1 process)",
            "Implementation roadmap (30/60/90 day plan)",
        ],
        "deliverables_ar": [
            "درجة جودة البيانات لأهم مصادر البيانات",
            "3 رؤى ذكاء إيرادات مُرتَّبة بالأولوية",
            "توصية أتمتة المكسب السريع (عملية واحدة)",
            "خارطة طريق التنفيذ (خطة 30/60/90 يوم)",
        ],
        "suitable_for": ["SME first paid engagement", "Proof of concept"],
        "decision_maker": "Manager / Director",
    },
    "data_pack": {
        "id": "data_pack",
        "name_ar": "باقة البيانات السعودية",
        "name_en": "Saudi Market Data Pack",
        "price_sar": 1_500,
        "duration": "5 business days",
        "deliverables_en": [
            "Saudi sector benchmarking report (vs. 3 competitors)",
            "ICP (Ideal Customer Profile) analysis for target segment",
            "Prospect enrichment: 50 target accounts with intent signals",
            "Bilingual AR/EN executive summary",
        ],
        "deliverables_ar": [
            "تقرير معايير القطاع السعودي (مقارنة 3 منافسين)",
            "تحليل الملف المثالي للعميل للشريحة المستهدفة",
            "إثراء المحتملين: 50 حساب مستهدف مع إشارات النية",
            "ملخص تنفيذي ثنائي اللغة عربي/إنجليزي",
        ],
        "suitable_for": ["Companies starting B2B sales", "Market entry"],
        "decision_maker": "VP Sales / CMO",
    },
    "managed_ops": {
        "id": "managed_ops",
        "name_ar": "عمليات الذكاء الاصطناعي المُدارة",
        "name_en": "Managed AI Operations",
        "price_sar": None,  # variable 2999–4999
        "price_range_sar": {"min": 2_999, "max": 4_999},
        "duration": "Ongoing monthly",
        "deliverables_en": [
            "Dedicated AI operator (10h/month)",
            "Monthly revenue intelligence dashboard",
            "Automated reporting and alerts",
            "Quarterly business review (QBR) with ROI report",
            "ZATCA compliance monitoring",
            "Priority support (4h SLA)",
        ],
        "deliverables_ar": [
            "مشغّل ذكاء اصطناعي مخصص (10 ساعات/شهر)",
            "لوحة تحكم ذكاء الإيرادات الشهرية",
            "تقارير وتنبيهات آلية",
            "مراجعة أعمال ربع سنوية مع تقرير العائد على الاستثمار",
            "مراقبة الامتثال لهيئة الزكاة",
            "دعم أولوية (SLA 4 ساعات)",
        ],
        "suitable_for": ["Series A+", "100+ employees", "SAR 5M+ annual revenue"],
        "decision_maker": "C-level or VP",
    },
    "custom_ai": {
        "id": "custom_ai",
        "name_ar": "بناء ذكاء اصطناعي مخصص",
        "name_en": "Custom AI Build",
        "price_sar": None,
        "price_range_sar": {"min": 5_000, "max": 25_000},
        "duration": "4–12 weeks",
        "deliverables_en": [
            "Custom AI model / workflow tailored to client's process",
            "Full documentation and handover",
            "3-month post-launch support",
            "PDPL data handling documentation",
            "ZATCA integration (if applicable)",
            "Arabic language fine-tuning",
        ],
        "deliverables_ar": [
            "نموذج ذكاء اصطناعي مخصص / سير عمل مُصمَّم لعملية العميل",
            "توثيق كامل وتسليم",
            "دعم لمدة 3 أشهر بعد الإطلاق",
            "توثيق معالجة البيانات وفق PDPL",
            "تكامل هيئة الزكاة (إن انطبق)",
            "ضبط دقيق للغة العربية",
        ],
        "suitable_for": ["Enterprise", "Complex integration needs"],
        "decision_maker": "C-level + Board",
    },
}

# ---------------------------------------------------------------------------
# Proposal sections
# ---------------------------------------------------------------------------

_STANDARD_SECTIONS = [
    {
        "order": 1,
        "title_en": "Executive Summary",
        "title_ar": "الملخص التنفيذي",
        "guidance_en": "2–3 sentences: problem, solution, expected impact. Emphasize ROI and payback.",
        "guidance_ar": "2–3 جمل: المشكلة، الحل، الأثر المتوقع. أبرز العائد على الاستثمار وفترة الاسترداد.",
    },
    {
        "order": 2,
        "title_en": "Understanding of Your Situation",
        "title_ar": "فهمنا لوضعكم",
        "guidance_en": "Restate the pain points discovered in discovery. Use their exact language.",
        "guidance_ar": "أعد صياغة نقاط الألم المكتشفة. استخدم لغتهم الدقيقة.",
    },
    {
        "order": 3,
        "title_en": "Proposed Solution",
        "title_ar": "الحل المقترح",
        "guidance_en": "Describe the deliverables, timeline, and methodology. Be specific.",
        "guidance_ar": "صف التسليمات والجدول الزمني والمنهجية. كن محدداً.",
    },
    {
        "order": 4,
        "title_en": "Investment & ROI",
        "title_ar": "الاستثمار والعائد",
        "guidance_en": "Price in SAR with payment terms. ROI model with conservative assumptions.",
        "guidance_ar": "السعر بالريال السعودي مع شروط الدفع. نموذج عائد بافتراضات محافظة.",
    },
    {
        "order": 5,
        "title_en": "Vision 2030 Alignment",
        "title_ar": "التوافق مع رؤية 2030",
        "guidance_en": "Explain how this engagement contributes to the client's Vision 2030 goals.",
        "guidance_ar": "اشرح كيف تُسهم هذه المشاركة في أهداف رؤية 2030 للعميل.",
    },
    {
        "order": 6,
        "title_en": "Implementation Timeline",
        "title_ar": "الجدول الزمني للتنفيذ",
        "guidance_en": "Week-by-week milestones. Note any prayer time / Ramadan / holiday impacts.",
        "guidance_ar": "معالم أسبوعية. أشر إلى أي تأثيرات لأوقات الصلاة / رمضان / الأعياد.",
    },
    {
        "order": 7,
        "title_en": "Why Dealix",
        "title_ar": "لماذا ديليكس",
        "guidance_en": "3 differentiators: Saudi-native AI, bilingual AR/EN, ZATCA/PDPL built-in.",
        "guidance_ar": "3 مميزات: ذكاء اصطناعي سعودي أصلي، ثنائية عربية/إنجليزية، زكاة/PDPL مدمجة.",
    },
    {
        "order": 8,
        "title_en": "Next Steps & Acceptance",
        "title_ar": "الخطوات التالية والقبول",
        "guidance_en": "Clear CTA: review deadline, acceptance instructions, and kickoff date.",
        "guidance_ar": "دعوة عمل واضحة: موعد المراجعة، تعليمات القبول، وتاريخ الانطلاق.",
    },
]

# ---------------------------------------------------------------------------
# Pydantic model
# ---------------------------------------------------------------------------

class ProposalRequest(BaseModel):
    tier: str = Field(..., description="Tier ID from GET /api/v1/proposal-builder/tiers")
    client_name: str = Field(..., max_length=100)
    client_sector: str = Field(..., max_length=80)
    identified_pains: list[str] = Field(
        ..., min_length=1, max_length=5,
        description="1–5 pain points identified in discovery",
    )
    estimated_roi_pct: float = Field(..., ge=0)
    custom_price_sar: float | None = Field(
        None, gt=0,
        description="Override price for managed_ops or custom_ai tiers",
    )
    payment_terms: str = Field(
        "50% upfront, 50% on delivery",
        max_length=100,
    )


def _build_proposal(req: ProposalRequest) -> dict[str, Any]:
    tier = _TIERS[req.tier]

    price_display = (
        f"SAR {req.custom_price_sar:,.0f}"
        if req.custom_price_sar
        else (
            f"SAR {tier['price_sar']:,.0f}"
            if tier.get("price_sar") is not None and tier["price_sar"] > 0
            else (
                f"SAR {tier['price_range_sar']['min']:,}–{tier['price_range_sar']['max']:,}/month"
                if tier.get("price_range_sar") and req.tier == "managed_ops"
                else f"SAR {tier['price_range_sar']['min']:,}–{tier['price_range_sar']['max']:,}"
            )
            if tier.get("price_range_sar")
            else "Free"
        )
    )

    sections_with_content = []
    for section in _STANDARD_SECTIONS:
        pain_text = "; ".join(req.identified_pains)
        content_en = section["guidance_en"]
        content_ar = section["guidance_ar"]

        if section["order"] == 1:
            content_en = (
                f"Dealix proposes to help {req.client_name} in the {req.client_sector} sector "
                f"address: {pain_text}. "
                f"Expected ROI: {req.estimated_roi_pct:.0f}%."
            )
            content_ar = (
                f"تقترح ديليكس مساعدة {req.client_name} في قطاع {req.client_sector} "
                f"لمعالجة: {pain_text}. "
                f"العائد المتوقع: {req.estimated_roi_pct:.0f}%."
            )
        elif section["order"] == 4:
            content_en = (
                f"Investment: {price_display}. "
                f"Payment: {req.payment_terms}. "
                f"Estimated ROI: {req.estimated_roi_pct:.0f}% (conservative assumptions)."
            )
            content_ar = (
                f"الاستثمار: {price_display}. "
                f"الدفع: {req.payment_terms}. "
                f"العائد المقدر: {req.estimated_roi_pct:.0f}% (افتراضات محافظة)."
            )

        sections_with_content.append({
            **section,
            "draft_content_en": content_en,
            "draft_content_ar": content_ar,
            "status": "draft",
        })

    return {
        "client_name": req.client_name,
        "client_sector": req.client_sector,
        "tier_id": tier["id"],
        "tier_name_en": tier["name_en"],
        "tier_name_ar": tier["name_ar"],
        "price_display": price_display,
        "payment_terms": req.payment_terms,
        "identified_pains": req.identified_pains,
        "deliverables_en": tier["deliverables_en"],
        "deliverables_ar": tier["deliverables_ar"],
        "proposal_sections": sections_with_content,
        "suitable_for": tier["suitable_for"],
        "recommended_decision_maker": tier["decision_maker"],
    }


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@router.get("/tiers", summary="Dealix service tiers for proposals")
async def list_tiers() -> dict[str, Any]:
    return {
        "tiers": list(_TIERS.values()),
        "governance_decision": "ALLOW_WITH_REVIEW",
    }


@router.get("/tiers/{tier_id}", summary="Detail for a specific service tier")
async def get_tier(tier_id: str) -> dict[str, Any]:
    tier = _TIERS.get(tier_id)
    if not tier:
        raise HTTPException(
            status_code=404,
            detail=f"Tier '{tier_id}' not found. Valid: {list(_TIERS.keys())}",
        )
    return {
        "tier": tier,
        "governance_decision": "ALLOW_WITH_REVIEW",
    }


@router.get("/sections", summary="Standard proposal sections with guidance")
async def get_sections() -> dict[str, Any]:
    return {
        "sections": _STANDARD_SECTIONS,
        "total": len(_STANDARD_SECTIONS),
        "note_en": "Customize each section with verified client data before sending.",
        "note_ar": "خصّص كل قسم ببيانات موثّقة للعميل قبل الإرسال.",
        "governance_decision": "ALLOW_WITH_REVIEW",
    }


# ---------------------------------------------------------------------------
# New static data: simplified proposal sections (ordered 1-6)
# ---------------------------------------------------------------------------

_PROPOSAL_SECTIONS: list[dict[str, Any]] = [
    {
        "order": 1,
        "section_name_en": "Executive Summary",
        "section_name_ar": "الملخص التنفيذي",
        "purpose_en": "Capture the decision-maker's attention with a concise summary of the value proposition.",
        "purpose_ar": "استقطاب انتباه صاحب القرار بملخص موجز لعرض القيمة.",
        "word_count_guideline": 150,
        "required": True,
    },
    {
        "order": 2,
        "section_name_en": "Problem Statement",
        "section_name_ar": "بيان المشكلة",
        "purpose_en": "Articulate the client's current pain points and the cost of inaction.",
        "purpose_ar": "توضيح نقاط الألم الحالية لدى العميل وتكلفة عدم التحرك.",
        "word_count_guideline": 200,
        "required": True,
    },
    {
        "order": 3,
        "section_name_en": "Solution Overview",
        "section_name_ar": "نظرة عامة على الحل",
        "purpose_en": "Describe the proposed solution and how it directly addresses the stated problem.",
        "purpose_ar": "وصف الحل المقترح وكيفية معالجته المباشرة للمشكلة المطروحة.",
        "word_count_guideline": 200,
        "required": True,
    },
    {
        "order": 4,
        "section_name_en": "ROI Case",
        "section_name_ar": "حجة العائد على الاستثمار",
        "purpose_en": "Present quantified expected returns and the financial justification for the investment.",
        "purpose_ar": "عرض العوائد المتوقعة المقدَّرة والمبرر المالي للاستثمار.",
        "word_count_guideline": 250,
        "required": True,
    },
    {
        "order": 5,
        "section_name_en": "Implementation Timeline",
        "section_name_ar": "الجدول الزمني للتنفيذ",
        "purpose_en": "Outline the key milestones, phases, and expected time to value.",
        "purpose_ar": "توضيح المعالم الرئيسية والمراحل والوقت المتوقع لتحقيق القيمة.",
        "word_count_guideline": 150,
        "required": True,
    },
    {
        "order": 6,
        "section_name_en": "Pricing and Next Steps",
        "section_name_ar": "التسعير والخطوات التالية",
        "purpose_en": "Present the pricing structure and a clear call to action for moving forward.",
        "purpose_ar": "عرض هيكل التسعير ودعوة واضحة للتحرك للمضي قدمًا.",
        "word_count_guideline": 100,
        "required": True,
    },
]

# ---------------------------------------------------------------------------
# New static data: proposal types with price display and page count
# ---------------------------------------------------------------------------

_PROPOSAL_TYPES: dict[str, dict[str, Any]] = {
    "sprint": {
        "name_en": "Diagnostic Sprint",
        "name_ar": "سبرينت التشخيص",
        "price_sar_display": "SAR 499",
        "page_count": 3,
    },
    "data_pack": {
        "name_en": "Data Intelligence Pack",
        "name_ar": "حزمة استخبارات البيانات",
        "price_sar_display": "SAR 1,500",
        "page_count": 4,
    },
    "managed_ops": {
        "name_en": "Managed Operations",
        "name_ar": "العمليات المُدارة",
        "price_sar_display": "SAR 2,999–4,999/mo",
        "page_count": 6,
    },
    "custom_ai": {
        "name_en": "Custom AI Solution",
        "name_ar": "حل الذكاء الاصطناعي المخصص",
        "price_sar_display": "SAR 5,000–25,000",
        "page_count": 10,
    },
}

_VALID_PROPOSAL_TYPES: set[str] = {"sprint", "data_pack", "managed_ops", "custom_ai"}

_DRAFT_DISCLAIMER_EN = "This outline requires founder review before being sent to any prospect."
_DRAFT_DISCLAIMER_AR = "تتطلب هذه المخطوطة مراجعة المؤسس قبل إرسالها إلى أي عميل محتمل."

# ---------------------------------------------------------------------------
# New Pydantic model for draft outline
# ---------------------------------------------------------------------------


class ProposalDraftInput(BaseModel):
    proposal_type: str
    client_name: str
    client_sector: str
    champion_name: str
    champion_title: str
    key_pain_en: str
    key_pain_ar: str
    proposed_start_date: str
    arabic_primary: bool = False


# ---------------------------------------------------------------------------
# New pure-function core: draft outline
# ---------------------------------------------------------------------------


def _draft_proposal_outline(inp: ProposalDraftInput) -> dict[str, Any]:
    """Generate a structured proposal outline from validated input.

    Returns a structured dict with proposal metadata, enriched sections,
    language preference, and disclaimers.
    """
    if inp.proposal_type not in _VALID_PROPOSAL_TYPES:
        raise HTTPException(
            status_code=422,
            detail=(
                f"Invalid proposal_type '{inp.proposal_type}'. "
                f"Must be one of: {sorted(_VALID_PROPOSAL_TYPES)}"
            ),
        )

    proposal_meta = dict(_PROPOSAL_TYPES[inp.proposal_type])

    enriched_sections = []
    for section in _PROPOSAL_SECTIONS:
        enriched = dict(section)
        enriched["draft_hook_en"] = (
            f"For {inp.client_name}: address '{inp.key_pain_en}' in this section."
        )
        enriched["draft_hook_ar"] = (
            f"لـ{inp.client_name}: تناول '{inp.key_pain_ar}' في هذا القسم."
        )
        enriched_sections.append(enriched)

    return {
        "client_name": inp.client_name,
        "proposal_type": inp.proposal_type,
        "proposal_meta": proposal_meta,
        "sections": enriched_sections,
        "total_sections": len(enriched_sections),
        "language_primary": "ar" if inp.arabic_primary else "en",
        "governance_decision": "APPROVAL_FIRST",
        "disclaimer_en": _DRAFT_DISCLAIMER_EN,
        "disclaimer_ar": _DRAFT_DISCLAIMER_AR,
    }


# ---------------------------------------------------------------------------
# New endpoints for draft outline
# ---------------------------------------------------------------------------


@router.get("/outline-sections", summary="All 6 simplified proposal sections")
def get_outline_sections() -> dict[str, Any]:
    """Return all simplified proposal sections with bilingual labels and guidelines."""
    return {
        "sections": _PROPOSAL_SECTIONS,
        "total_sections": len(_PROPOSAL_SECTIONS),
        "governance_decision": "ALLOW_WITH_REVIEW",
    }


@router.get("/draft-types", summary="All 4 draft proposal types")
def get_draft_types() -> dict[str, Any]:
    """Return all proposal types with bilingual names, pricing, and page counts."""
    return {
        "proposal_types": _PROPOSAL_TYPES,
        "governance_decision": "ALLOW_WITH_REVIEW",
    }


@router.post("/draft", summary="Generate a proposal outline draft")
def draft_proposal(body: ProposalDraftInput) -> dict[str, Any]:
    """Accept proposal parameters and return a structured outline draft.

    Governance decision: APPROVAL_FIRST.
    """
    return _draft_proposal_outline(body)


@router.post("/generate", summary="Generate a structured proposal outline")
async def generate_proposal(body: ProposalRequest) -> dict[str, Any]:
    if body.tier not in _TIERS:
        raise HTTPException(
            status_code=422,
            detail=f"Tier '{body.tier}' not found. Valid: {list(_TIERS.keys())}",
        )

    result = _build_proposal(body)
    return {
        **result,
        "disclaimer_en": (
            "This is a draft outline. Do NOT send without founder review and "
            "customization with verified client data. "
            "All ROI figures must be supported by a completed assessment."
        ),
        "disclaimer_ar": (
            "هذا مخطط مسودة. لا ترسله دون مراجعة المؤسس وتخصيصه "
            "ببيانات موثّقة للعميل. "
            "يجب دعم جميع أرقام العائد على الاستثمار بتقييم مكتمل."
        ),
        "governance_decision": "APPROVAL_FIRST",
    }
