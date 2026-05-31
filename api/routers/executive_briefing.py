"""
Executive briefing builder for Saudi B2B AI deals.

Generates structured one-page executive summaries tailored to the
C-level persona (CFO, CEO, CTO, CIO, COO, CHRO) and their primary
concerns in the Saudi market. Pure Python, no LLM calls, bilingual.
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

router = APIRouter(prefix="/api/v1/executive-briefing", tags=["Sales"])

# ---------------------------------------------------------------------------
# Persona definitions
# ---------------------------------------------------------------------------

_PERSONAS: dict[str, dict[str, Any]] = {
    "cfo": {
        "title_ar": "المدير المالي",
        "title_en": "Chief Financial Officer (CFO)",
        "primary_concerns": [
            "Cost reduction and operational efficiency",
            "ZATCA compliance and e-invoicing automation",
            "Cash flow visibility and forecasting accuracy",
            "ROI and payback period clarity",
            "Audit trail and financial controls",
        ],
        "primary_concerns_ar": [
            "خفض التكاليف والكفاءة التشغيلية",
            "الامتثال لهيئة الزكاة والجمارك وأتمتة الفوترة الإلكترونية",
            "رؤية التدفق النقدي ودقة التنبؤ",
            "وضوح العائد على الاستثمار وفترة الاسترداد",
            "مسار التدقيق والضوابط المالية",
        ],
        "proof_points": [
            "% cost reduction in target process",
            "Months to full payback",
            "ZATCA Phase 2 compliance status",
            "Financial audit trail quality score",
        ],
        "headline_formula": "Reduce {process} cost by {pct}% within {months} months",
        "headline_formula_ar": "تخفيض تكلفة {process} بنسبة {pct}% خلال {months} شهراً",
        "objection_anticipation": [
            "Budget already allocated — this replaces a line item",
            "Needs CFO sign-off for >SAR 100K — position as opex",
            "Risk-averse — provide case study reference with similar size",
        ],
    },
    "ceo": {
        "title_ar": "الرئيس التنفيذي",
        "title_en": "Chief Executive Officer (CEO)",
        "primary_concerns": [
            "Revenue growth and market share in Vision 2030 sectors",
            "Competitive differentiation through AI",
            "Saudi talent retention and Saudization compliance",
            "Investor and board narrative",
            "Strategic alignment with national programs",
        ],
        "primary_concerns_ar": [
            "نمو الإيرادات وحصة السوق في قطاعات رؤية 2030",
            "التميز التنافسي من خلال الذكاء الاصطناعي",
            "الاحتفاظ بالمواهب السعودية والامتثال للتوطين",
            "رواية المستثمرين ومجلس الإدارة",
            "التوافق الاستراتيجي مع البرامج الوطنية",
        ],
        "proof_points": [
            "Market expansion opportunity in SAR",
            "Competitive win rate improvement",
            "Vision 2030 program alignment score",
            "Employee NPS and retention uplift",
        ],
        "headline_formula": "Capture SAR {size} in {sector} market by {date}",
        "headline_formula_ar": "اكتساب {size} ريال في سوق {sector} بحلول {date}",
        "objection_anticipation": [
            "Focus on strategic narrative not cost",
            "Board must approve — prepare board memo version",
            "Saudi timing: avoid pitching in Ramadan week 1 or pre-Eid",
        ],
    },
    "cto": {
        "title_ar": "الرئيس التقني",
        "title_en": "Chief Technology Officer (CTO)",
        "primary_concerns": [
            "Integration with existing ERP/CRM (SAP, Oracle, SFDC)",
            "Data security and PDPL compliance",
            "API reliability and SLA guarantees",
            "On-premises vs. cloud (Saudi data residency requirements)",
            "Team skill ramp and support model",
        ],
        "primary_concerns_ar": [
            "التكامل مع أنظمة ERP/CRM الحالية (SAP، Oracle، Salesforce)",
            "أمن البيانات والامتثال لنظام حماية البيانات الشخصية",
            "موثوقية API وضمانات مستوى الخدمة",
            "الخوادم الداخلية مقابل السحابة (متطلبات إقامة البيانات السعودية)",
            "تأهيل الفريق ونموذج الدعم",
        ],
        "proof_points": [
            "API uptime SLA (target 99.9%)",
            "Integration connectors available",
            "PDPL compliance certification",
            "Time-to-first-value (days)",
        ],
        "headline_formula": "Deploy in {days} days, integrate with {system} via REST API",
        "headline_formula_ar": "نشر خلال {days} يوماً، تكامل مع {system} عبر REST API",
        "objection_anticipation": [
            "Build vs. buy — position total cost of ownership",
            "Security concerns — provide architecture diagram upfront",
            "Saudi data residency — confirm AWS Riyadh / local hosting option",
        ],
    },
    "cio": {
        "title_ar": "مدير نظم المعلومات",
        "title_en": "Chief Information Officer (CIO)",
        "primary_concerns": [
            "IT portfolio rationalization and vendor consolidation",
            "PDPL and NCA (National Cybersecurity Authority) compliance",
            "Change management and user adoption",
            "IT governance and procurement process",
            "Long-term vendor stability and roadmap",
        ],
        "primary_concerns_ar": [
            "ترشيد محفظة تقنية المعلومات وتوحيد الموردين",
            "الامتثال لنظام حماية البيانات الشخصية والهيئة الوطنية للأمن السيبراني",
            "إدارة التغيير وتبني المستخدمين",
            "حوكمة تقنية المعلومات وعملية الشراء",
            "استقرار المورد على المدى البعيد وخارطة الطريق",
        ],
        "proof_points": [
            "NCA Essential Cybersecurity Controls compliance",
            "PDPL Article 5 data minimization compliance",
            "Uptime and incident response SLA",
            "References from Saudi government or large enterprise clients",
        ],
        "headline_formula": "NCA-compliant deployment, live in {days} days",
        "headline_formula_ar": "نشر متوافق مع الهيئة الوطنية للأمن السيبراني، نشط خلال {days} يوماً",
        "objection_anticipation": [
            "Procurement process 90+ days — offer POC to unlock fast-track",
            "Security review required — provide pre-filled VAPT summary",
            "IT budget frozen — position as cost avoidance, not new spend",
        ],
    },
    "coo": {
        "title_ar": "الرئيس التشغيلي",
        "title_en": "Chief Operating Officer (COO)",
        "primary_concerns": [
            "Process bottleneck elimination",
            "Headcount productivity without workforce reduction",
            "SLA performance and customer satisfaction",
            "Operational visibility and real-time reporting",
            "Compliance with Saudi labor regulations",
        ],
        "primary_concerns_ar": [
            "إزالة اختناقات العمليات",
            "إنتاجية الموظفين دون تخفيض القوى العاملة",
            "أداء مستوى الخدمة ورضا العملاء",
            "الرؤية التشغيلية والتقارير الفورية",
            "الامتثال للوائح العمل السعودية",
        ],
        "proof_points": [
            "% reduction in processing time",
            "% improvement in SLA adherence",
            "Headcount productivity multiplier",
            "Error rate reduction %",
        ],
        "headline_formula": "Cut {process} processing time by {pct}% in 90 days",
        "headline_formula_ar": "خفض وقت معالجة {process} بنسبة {pct}% في 90 يوماً",
        "objection_anticipation": [
            "Staff will resist — offer change management playbook",
            "Operations during Ramadan — plan deployment for post-Ramadan",
            "Process too complex — offer process audit as first step",
        ],
    },
    "chro": {
        "title_ar": "مدير الموارد البشرية",
        "title_en": "Chief Human Resources Officer (CHRO)",
        "primary_concerns": [
            "Saudization (Nitaqat) compliance and Saudi talent development",
            "Recruitment automation for high-volume hiring",
            "Employee engagement and retention",
            "Vision 2030 workforce localization programs",
            "HRSD regulatory compliance",
        ],
        "primary_concerns_ar": [
            "امتثال نطاقات وتطوير المواهب السعودية",
            "أتمتة التوظيف للاستقطاب الكثيف",
            "مشاركة الموظفين والاحتفاظ بهم",
            "برامج توطين القوى العاملة في رؤية 2030",
            "الامتثال للوائح وزارة الموارد البشرية",
        ],
        "proof_points": [
            "Time-to-hire reduction %",
            "Saudization rate improvement",
            "Employee NPS uplift",
            "HRSD compliance coverage %",
        ],
        "headline_formula": "Reduce time-to-hire by {pct}% while improving Nitaqat band",
        "headline_formula_ar": "تقليل وقت التوظيف بنسبة {pct}% مع تحسين فئة نطاقات",
        "objection_anticipation": [
            "Employees fear job loss — position as augmentation not replacement",
            "Saudization impact — highlight Saudi talent development features",
            "Ministry approval needed — provide HRSD-aligned data classification",
        ],
    },
}

# ---------------------------------------------------------------------------
# Briefing generation
# ---------------------------------------------------------------------------

class BriefingRequest(BaseModel):
    persona: str = Field(..., description="C-level persona ID: cfo|ceo|cto|cio|coo|chro")
    company_name: str = Field(..., max_length=100)
    sector: str = Field(..., max_length=80, description="Client's industry sector")
    primary_use_case: str = Field(..., max_length=200, description="What problem Dealix solves for them")
    estimated_roi_pct: float = Field(..., ge=0, description="Estimated ROI % (from calculator or estimate)")
    estimated_payback_months: float = Field(..., ge=1, description="Estimated payback period in months")
    dealix_tier: str = Field(
        "managed_ops",
        description="Product tier: sprint|data_pack|managed_ops|custom_ai",
    )


_TIER_DESCRIPTIONS = {
    "sprint": {"en": "7-Day Revenue Intelligence Sprint (SAR 499)", "ar": "سبرينت استخبارات الإيرادات 7 أيام (499 ريال)"},
    "data_pack": {"en": "Saudi Market Data Pack (SAR 1,500)", "ar": "باقة البيانات السعودية (1,500 ريال)"},
    "managed_ops": {"en": "Managed AI Operations (SAR 2,999–4,999/mo)", "ar": "عمليات الذكاء الاصطناعي المُدارة (2,999–4,999 ريال/شهر)"},
    "custom_ai": {"en": "Custom AI Build (SAR 5K–25K)", "ar": "بناء ذكاء اصطناعي مخصص (5,000–25,000 ريال)"},
}


def build_briefing(req: BriefingRequest) -> dict[str, Any]:
    persona = _PERSONAS[req.persona]
    tier = _TIER_DESCRIPTIONS.get(req.dealix_tier, _TIER_DESCRIPTIONS["managed_ops"])

    executive_summary_en = (
        f"Dealix proposes an AI-powered solution for {req.company_name} "
        f"to {req.primary_use_case}. "
        f"Based on {req.sector} sector benchmarks, the projected ROI is "
        f"{req.estimated_roi_pct:.0f}% with a {req.estimated_payback_months:.0f}-month payback period."
    )

    executive_summary_ar = (
        f"تقترح ديليكس حلاً مدعوماً بالذكاء الاصطناعي لـ{req.company_name} "
        f"لـ{req.primary_use_case}. "
        f"استناداً إلى معايير قطاع {req.sector}، العائد المتوقع على الاستثمار "
        f"{req.estimated_roi_pct:.0f}% مع فترة استرداد {req.estimated_payback_months:.0f} شهراً."
    )

    recommended_sections = [
        {
            "section": "Problem Statement",
            "section_ar": "بيان المشكلة",
            "content_en": f"Current state in {req.sector}: {req.primary_use_case}.",
            "content_ar": f"الوضع الحالي في قطاع {req.sector}: {req.primary_use_case}.",
        },
        {
            "section": "Proposed Solution",
            "section_ar": "الحل المقترح",
            "content_en": f"Dealix — {tier['en']} — delivers measurable results in 30–90 days.",
            "content_ar": f"ديليكس — {tier['ar']} — تحقق نتائج قابلة للقياس في 30–90 يوماً.",
        },
        {
            "section": "Financial Impact",
            "section_ar": "الأثر المالي",
            "content_en": (
                f"Projected ROI: {req.estimated_roi_pct:.0f}% | "
                f"Payback: {req.estimated_payback_months:.0f} months | "
                f"Vision 2030 alignment: High"
            ),
            "content_ar": (
                f"العائد المتوقع: {req.estimated_roi_pct:.0f}% | "
                f"فترة الاسترداد: {req.estimated_payback_months:.0f} شهراً | "
                f"توافق رؤية 2030: مرتفع"
            ),
        },
        {
            "section": "Proof Points",
            "section_ar": "نقاط الإثبات",
            "content_en": " | ".join(persona["proof_points"]),
            "content_ar": "نقاط القياس تُحدد عند بدء المشروع",
        },
        {
            "section": "Next Step",
            "section_ar": "الخطوة التالية",
            "content_en": "Free 30-minute diagnostic call → 7-day sprint POC → Full deployment.",
            "content_ar": "جلسة تشخيص مجانية 30 دقيقة ← سبرينت تجريبي 7 أيام ← نشر كامل.",
        },
    ]

    return {
        "persona": req.persona,
        "persona_title_ar": persona["title_ar"],
        "persona_title_en": persona["title_en"],
        "company_name": req.company_name,
        "executive_summary_en": executive_summary_en,
        "executive_summary_ar": executive_summary_ar,
        "primary_concerns_en": persona["primary_concerns"],
        "primary_concerns_ar": persona["primary_concerns_ar"],
        "briefing_sections": recommended_sections,
        "objection_anticipation": persona["objection_anticipation"],
        "recommended_dealix_tier": tier,
        "cultural_context_en": (
            "Saudi C-level meetings: open with relationship and vision alignment before numbers. "
            "Use Arabic for executive summary when presenting to Arabic-speaking executives. "
            "Avoid scheduling near prayer times and major holidays."
        ),
        "cultural_context_ar": (
            "اجتماعات كبار المسؤولين السعوديين: ابدأ بالعلاقة وتوافق الرؤية قبل الأرقام. "
            "استخدم العربية في الملخص التنفيذي عند التقديم لمسؤولين ناطقين بالعربية. "
            "تجنب الجدولة قرب أوقات الصلاة والأعياد الكبرى."
        ),
    }


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@router.get("/personas", summary="Available C-level personas with Saudi context")
async def list_personas() -> dict[str, Any]:
    return {
        "personas": [
            {
                "id": k,
                "title_ar": v["title_ar"],
                "title_en": v["title_en"],
                "top_concern_en": v["primary_concerns"][0],
                "top_concern_ar": v["primary_concerns_ar"][0],
            }
            for k, v in _PERSONAS.items()
        ],
        "governance_decision": "ALLOW_WITH_REVIEW",
    }


@router.get("/persona/{persona_id}", summary="Full persona profile with concerns and objections")
async def get_persona(persona_id: str) -> dict[str, Any]:
    persona = _PERSONAS.get(persona_id)
    if not persona:
        raise HTTPException(
            status_code=404,
            detail=f"Persona '{persona_id}' not found. Valid: {list(_PERSONAS.keys())}",
        )
    return {
        "id": persona_id,
        **persona,
        "governance_decision": "ALLOW_WITH_REVIEW",
    }


@router.post("/generate", summary="Generate a one-page executive briefing")
async def generate_briefing(body: BriefingRequest) -> dict[str, Any]:
    if body.persona not in _PERSONAS:
        raise HTTPException(
            status_code=422,
            detail=f"Persona '{body.persona}' not found. Valid: {list(_PERSONAS.keys())}",
        )
    if body.dealix_tier not in _TIER_DESCRIPTIONS:
        raise HTTPException(
            status_code=422,
            detail=f"Invalid tier '{body.dealix_tier}'. Valid: {list(_TIER_DESCRIPTIONS.keys())}",
        )

    result = build_briefing(body)
    return {
        **result,
        "disclaimer_en": (
            "This briefing template is a starting point. "
            "Customize with verified client data before presenting. "
            "ROI figures should reference completed assessments."
        ),
        "disclaimer_ar": (
            "هذا النموذج نقطة انطلاق. "
            "خصّصه ببيانات العميل الموثقة قبل التقديم. "
            "يجب أن تستند أرقام العائد على الاستثمار إلى تقييمات مكتملة."
        ),
        "governance_decision": "ALLOW_WITH_REVIEW",
    }
