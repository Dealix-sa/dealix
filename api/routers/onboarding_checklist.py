"""
Client onboarding checklist engine for Dealix Saudi B2B engagements.

Provides structured onboarding checklists for each Dealix tier,
tracks completion, flags Saudi-specific compliance requirements (PDPL,
ZATCA data integration), and generates 30-day success plans.
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field, model_validator

router = APIRouter(prefix="/api/v1/onboarding-checklist", tags=["Analytics"])

# ---------------------------------------------------------------------------
# Checklist templates by tier
# ---------------------------------------------------------------------------

_TIER_CHECKLISTS: dict[str, Any] = {
    "sprint": {
        "tier_en": "Revenue Intelligence Sprint (SAR 499)",
        "tier_ar": "سبرنت ذكاء الإيرادات (499 ريال)",
        "duration_days": 7,
        "phases": [
            {
                "phase": 1,
                "phase_name_en": "Kickoff & Data Access",
                "phase_name_ar": "انطلاق المشروع والوصول إلى البيانات",
                "days": "Day 1",
                "tasks_en": [
                    "Send welcome email + sprint agenda",
                    "Collect CRM export (CSV/Excel) or API credentials",
                    "Sign PDPL data processing consent form",
                    "Confirm champion contact and availability",
                    "Set Slack/WhatsApp communication channel",
                ],
                "tasks_ar": [
                    "أرسل بريد الترحيب + جدول السبرنت",
                    "اجمع تصدير CRM (CSV/Excel) أو بيانات API",
                    "وقّع نموذج موافقة معالجة البيانات (PDPL)",
                    "تأكيد جهة الاتصال للبطل ومدى توافره",
                    "ضبط قناة تواصل Slack/WhatsApp",
                ],
                "pdpl_required": True,
                "blocking": True,
            },
            {
                "phase": 2,
                "phase_name_en": "Data Analysis",
                "phase_name_ar": "تحليل البيانات",
                "days": "Days 2–4",
                "tasks_en": [
                    "Run revenue intelligence audit on pipeline data",
                    "Score accounts by likelihood to close / expand",
                    "Identify top 3 revenue leaks",
                    "Benchmark against Saudi sector averages",
                ],
                "tasks_ar": [
                    "تشغيل تدقيق ذكاء الإيرادات على بيانات المسار",
                    "تصنيف الحسابات حسب احتمالية الإغلاق / التوسع",
                    "تحديد أبرز 3 تسربات إيرادات",
                    "قياس الأداء مقارنةً بمتوسطات القطاع السعودي",
                ],
                "pdpl_required": False,
                "blocking": False,
            },
            {
                "phase": 3,
                "phase_name_en": "Insight Delivery",
                "phase_name_ar": "تسليم الرؤى",
                "days": "Days 5–7",
                "tasks_en": [
                    "Prepare bilingual insight deck (AR + EN)",
                    "Present findings to champion + economic buyer",
                    "Deliver prioritized action list",
                    "Propose next tier (Data Pack or Managed Ops)",
                ],
                "tasks_ar": [
                    "إعداد عرض الرؤى ثنائي اللغة (عربي + إنجليزي)",
                    "تقديم النتائج للبطل + صاحب القرار الاقتصادي",
                    "تسليم قائمة الإجراءات ذات الأولوية",
                    "اقتراح المستوى التالي (حزمة البيانات أو العمليات المُدارة)",
                ],
                "pdpl_required": False,
                "blocking": False,
            },
        ],
        "success_criteria_en": [
            "Client rates insight session ≥8/10",
            "At least 1 revenue leak identified and quantified",
            "Next step agreed within 48 hours of delivery",
        ],
        "churn_risk_signals_en": [
            "Champion cancels/reschedules delivery call",
            "No data provided by Day 2",
            "Economic buyer not present at delivery",
        ],
    },
    "data_pack": {
        "tier_en": "Data Intelligence Pack (SAR 1,500)",
        "tier_ar": "حزمة ذكاء البيانات (1,500 ريال)",
        "duration_days": 14,
        "phases": [
            {
                "phase": 1,
                "phase_name_en": "Data Architecture Review",
                "phase_name_ar": "مراجعة هندسة البيانات",
                "days": "Days 1–3",
                "tasks_en": [
                    "Map all data sources (CRM, ERP, ZATCA, spreadsheets)",
                    "Sign PDPL data processing agreement",
                    "Assess data quality score (completeness, accuracy, freshness)",
                    "Identify integration points",
                ],
                "tasks_ar": [
                    "رسم خريطة جميع مصادر البيانات (CRM، ERP، هيئة الزكاة، جداول البيانات)",
                    "توقيع اتفاقية معالجة بيانات PDPL",
                    "تقييم درجة جودة البيانات (الاكتمال، الدقة، الحداثة)",
                    "تحديد نقاط التكامل",
                ],
                "pdpl_required": True,
                "blocking": True,
            },
            {
                "phase": 2,
                "phase_name_en": "Pipeline & Revenue Analysis",
                "phase_name_ar": "تحليل المسار والإيرادات",
                "days": "Days 4–10",
                "tasks_en": [
                    "Build revenue analytics dashboard",
                    "Score full account portfolio",
                    "Identify expansion opportunities (upsell/cross-sell)",
                    "Run ZATCA compliance revenue check if applicable",
                    "Segment pipeline by probability and deal size",
                ],
                "tasks_ar": [
                    "بناء لوحة تحليلات الإيرادات",
                    "تصنيف محفظة الحسابات الكاملة",
                    "تحديد فرص التوسع (زيادة البيع / البيع المتقاطع)",
                    "تشغيل فحص إيرادات الامتثال لهيئة الزكاة إن اقتضى الأمر",
                    "تقسيم المسار حسب الاحتمالية وحجم الصفقة",
                ],
                "pdpl_required": False,
                "blocking": False,
            },
            {
                "phase": 3,
                "phase_name_en": "Recommendations & Roadmap",
                "phase_name_ar": "التوصيات وخارطة الطريق",
                "days": "Days 11–14",
                "tasks_en": [
                    "Deliver full data intelligence report (AR + EN)",
                    "Present 90-day revenue roadmap",
                    "Recommend Managed Ops engagement",
                    "Obtain client sign-off on findings",
                ],
                "tasks_ar": [
                    "تسليم تقرير ذكاء البيانات الكامل (عربي + إنجليزي)",
                    "تقديم خارطة الطريق الإيرادية لـ 90 يوماً",
                    "التوصية بتعاقد العمليات المُدارة",
                    "الحصول على موافقة العميل على النتائج",
                ],
                "pdpl_required": False,
                "blocking": False,
            },
        ],
        "success_criteria_en": [
            "Data quality score ≥70% at handoff",
            "3+ actionable revenue opportunities identified",
            "Client agrees to 90-day roadmap",
        ],
        "churn_risk_signals_en": [
            "Data access blocked by IT for >3 days",
            "No executive sponsor engaged",
            "Findings presented to wrong stakeholder level",
        ],
    },
    "managed_ops": {
        "tier_en": "Managed Revenue Operations (SAR 2,999–4,999/mo)",
        "tier_ar": "عمليات الإيرادات المُدارة (2,999–4,999 ريال/شهر)",
        "duration_days": 30,
        "phases": [
            {
                "phase": 1,
                "phase_name_en": "Foundation Setup (Week 1)",
                "phase_name_ar": "إعداد الأساس (الأسبوع الأول)",
                "days": "Days 1–7",
                "tasks_en": [
                    "Execute PDPL Data Processing Agreement (DPA)",
                    "Complete security questionnaire (NCA/SAMA if applicable)",
                    "Integrate CRM, ERP, ZATCA data feeds",
                    "Configure Saudi market benchmarks and KPIs",
                    "Set up bilingual reporting dashboard",
                    "Establish weekly cadence and review schedule",
                ],
                "tasks_ar": [
                    "تنفيذ اتفاقية معالجة البيانات (DPA) وفق PDPL",
                    "إتمام استبيان الأمان (NCA/SAMA إن اقتضى الأمر)",
                    "دمج تغذيات بيانات CRM وERP وهيئة الزكاة",
                    "تهيئة معايير السوق السعودي ومؤشرات الأداء الرئيسية",
                    "إعداد لوحة التقارير ثنائية اللغة",
                    "تأسيس الإيقاع الأسبوعي وجدول المراجعة",
                ],
                "pdpl_required": True,
                "blocking": True,
            },
            {
                "phase": 2,
                "phase_name_en": "Activation (Weeks 2–3)",
                "phase_name_ar": "التفعيل (الأسبوعان الثاني والثالث)",
                "days": "Days 8–21",
                "tasks_en": [
                    "Launch account scoring model",
                    "Run first pipeline review with sales team",
                    "Deliver first weekly revenue brief",
                    "Train champion on self-serve dashboard",
                    "Identify top 5 accounts for focus this month",
                ],
                "tasks_ar": [
                    "إطلاق نموذج تصنيف الحسابات",
                    "إجراء أول مراجعة للمسار مع فريق المبيعات",
                    "تسليم أول ملخص إيرادات أسبوعي",
                    "تدريب البطل على لوحة الخدمة الذاتية",
                    "تحديد أفضل 5 حسابات للتركيز عليها هذا الشهر",
                ],
                "pdpl_required": False,
                "blocking": False,
            },
            {
                "phase": 3,
                "phase_name_en": "Value Demonstration (Week 4)",
                "phase_name_ar": "إثبات القيمة (الأسبوع الرابع)",
                "days": "Days 22–30",
                "tasks_en": [
                    "Deliver Month 1 ROI report",
                    "Conduct executive sponsor review",
                    "Agree KPIs for Month 2–3",
                    "Evaluate custom AI upgrade fit",
                ],
                "tasks_ar": [
                    "تسليم تقرير عائد الاستثمار للشهر الأول",
                    "إجراء مراجعة الراعي التنفيذي",
                    "الاتفاق على مؤشرات الأداء الرئيسية للشهرين 2-3",
                    "تقييم مناسبة ترقية الذكاء الاصطناعي المخصص",
                ],
                "pdpl_required": False,
                "blocking": False,
            },
        ],
        "success_criteria_en": [
            "All data integrations live by Day 7",
            "Dashboard adopted by ≥3 team members",
            "Month 1 ROI documented and signed off",
            "NPS ≥8 at 30-day check-in",
        ],
        "churn_risk_signals_en": [
            "Integration stalls at IT security review",
            "Champion changed mid-engagement",
            "Executive sponsor disengaged after kickoff",
            "No pipeline data for 7+ days",
        ],
    },
}

# ---------------------------------------------------------------------------
# Saudi-specific compliance notes
# ---------------------------------------------------------------------------

_COMPLIANCE_REQUIREMENTS: list[dict[str, Any]] = [
    {
        "requirement": "PDPL Data Processing Agreement",
        "requirement_ar": "اتفاقية معالجة البيانات وفق نظام حماية البيانات الشخصية",
        "applies_to_tiers": ["sprint", "data_pack", "managed_ops", "custom_ai"],
        "blocking": True,
        "description_en": (
            "Saudi Personal Data Protection Law (PDPL) requires explicit consent "
            "and a signed DPA before processing any personal data. "
            "Must be signed before data collection begins."
        ),
        "description_ar": (
            "يستوجب نظام حماية البيانات الشخصية السعودي الحصول على موافقة صريحة "
            "وتوقيع اتفاقية معالجة البيانات قبل معالجة أي بيانات شخصية. "
            "يجب التوقيع قبل البدء في جمع البيانات."
        ),
        "template_available": True,
    },
    {
        "requirement": "ZATCA Data Integration Authorization",
        "requirement_ar": "تفويض تكامل بيانات هيئة الزكاة والضريبة والجمارك",
        "applies_to_tiers": ["data_pack", "managed_ops", "custom_ai"],
        "blocking": False,
        "description_en": (
            "If pulling ZATCA e-invoice data, client must authorize API access "
            "and confirm Phase 2 compliance status."
        ),
        "description_ar": (
            "عند سحب بيانات الفوترة الإلكترونية من هيئة الزكاة، يجب على العميل تفويض وصول API "
            "والتأكد من حالة الامتثال للمرحلة الثانية."
        ),
        "template_available": False,
    },
    {
        "requirement": "NCA Cybersecurity Compliance (CSCC)",
        "requirement_ar": "امتثال الأمن السيبراني (NCA) للمنشآت الكبرى",
        "applies_to_tiers": ["managed_ops", "custom_ai"],
        "blocking": False,
        "description_en": (
            "Saudi National Cybersecurity Authority (NCA) Essential Controls "
            "apply to critical infrastructure operators. Large clients may require "
            "vendor security questionnaire completion."
        ),
        "description_ar": (
            "تنطبق الضوابط الأساسية للهيئة الوطنية للأمن السيبراني على مشغلي البنية التحتية الحيوية. "
            "قد يستلزم العملاء الكبار إتمام استبيان أمان الموردين."
        ),
        "template_available": True,
    },
    {
        "requirement": "Data Residency Declaration",
        "requirement_ar": "إعلان إقامة البيانات",
        "applies_to_tiers": ["managed_ops", "custom_ai"],
        "blocking": False,
        "description_en": (
            "Confirm data is stored in Saudi Arabia (PDPL Article 29). "
            "Provide cloud region certificate (AWS Bahrain, Azure KSA, etc.)."
        ),
        "description_ar": (
            "تأكيد تخزين البيانات في المملكة العربية السعودية (نظام حماية البيانات الشخصية، المادة 29). "
            "تقديم شهادة منطقة السحابة (AWS البحرين، Azure السعودية، إلخ)."
        ),
        "template_available": True,
    },
]


class OnboardingProgressInput(BaseModel):
    client_name: str = Field(..., min_length=2)
    tier: str = Field(..., description="sprint | data_pack | managed_ops | custom_ai")
    day_number: int = Field(..., ge=1, description="Current day of engagement")
    completed_tasks: list[str] = Field(default_factory=list)
    pdpl_signed: bool = False
    champion_active: bool = True
    data_received: bool = False

    @model_validator(mode="after")
    def validate_tier(self) -> "OnboardingProgressInput":
        valid = set(_TIER_CHECKLISTS.keys()) | {"custom_ai"}
        if self.tier not in valid:
            raise ValueError(f"tier must be one of {sorted(valid)}")
        return self


def _assess_onboarding(inp: OnboardingProgressInput) -> dict[str, Any]:
    checklist = _TIER_CHECKLISTS.get(inp.tier)
    duration = checklist["duration_days"] if checklist else 30
    progress_pct = min(100.0, round(inp.day_number / duration * 100, 1))

    risks: list[str] = []
    if not inp.pdpl_signed:
        risks.append("CRITICAL: PDPL DPA not signed — stop data processing immediately")
    if not inp.champion_active:
        risks.append("Champion inactive — escalate to economic buyer within 24 hours")
    if not inp.data_received and inp.day_number > 2:
        risks.append(f"No data received by Day {inp.day_number} — engagement at risk")

    health = "On Track"
    if len(risks) >= 2:
        health = "At Risk"
    elif not inp.pdpl_signed:
        health = "Blocked"

    next_actions: list[str] = []
    if not inp.pdpl_signed:
        next_actions.append("Obtain PDPL DPA signature immediately before proceeding")
    if not inp.data_received:
        next_actions.append("Follow up on data access — send step-by-step guide if needed")
    if not next_actions:
        next_actions.append("Continue per checklist — next milestone review in 2 days")
        next_actions.append("Document completed tasks in client ledger")

    return {
        "client_name": inp.client_name,
        "tier": inp.tier,
        "day_number": inp.day_number,
        "progress_pct": progress_pct,
        "engagement_health": health,
        "risks": risks,
        "next_actions_en": next_actions,
        "governance_decision": "ALLOW_WITH_REVIEW",
    }


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@router.get("/tiers", summary="Onboarding checklists by tier")
async def get_tier_checklists(
    tier: str | None = Query(None, description="Filter by tier slug"),
) -> dict[str, Any]:
    if tier is not None:
        t = _TIER_CHECKLISTS.get(tier)
        if t is None:
            raise HTTPException(status_code=404, detail=f"Tier '{tier}' not found.")
        return {tier: t, "governance_decision": "ALLOW_WITH_REVIEW"}
    return {
        "checklists": _TIER_CHECKLISTS,
        "total_tiers": len(_TIER_CHECKLISTS),
        "governance_decision": "ALLOW_WITH_REVIEW",
    }


@router.get("/compliance-requirements", summary="Saudi compliance requirements for onboarding")
async def get_compliance_requirements(
    tier: str | None = Query(None, description="Filter by tier"),
) -> dict[str, Any]:
    reqs = _COMPLIANCE_REQUIREMENTS
    if tier is not None:
        reqs = [r for r in _COMPLIANCE_REQUIREMENTS if tier in r["applies_to_tiers"]]
    return {
        "requirements": reqs,
        "total": len(reqs),
        "note_en": "PDPL DPA is blocking — do not process data without it.",
        "note_ar": "اتفاقية معالجة البيانات وفق PDPL إلزامية — لا تعالج البيانات بدونها.",
        "governance_decision": "ALLOW_WITH_REVIEW",
    }


@router.post("/assess-progress", summary="Assess onboarding health")
async def assess_progress(inp: OnboardingProgressInput) -> dict[str, Any]:
    return _assess_onboarding(inp)


@router.get("/success-criteria", summary="Success criteria by tier")
async def get_success_criteria() -> dict[str, Any]:
    return {
        "criteria": {
            tid: {
                "tier_en": t["tier_en"],
                "duration_days": t["duration_days"],
                "success_criteria_en": t["success_criteria_en"],
                "churn_risk_signals_en": t["churn_risk_signals_en"],
            }
            for tid, t in _TIER_CHECKLISTS.items()
        },
        "governance_decision": "ALLOW_WITH_REVIEW",
    }
