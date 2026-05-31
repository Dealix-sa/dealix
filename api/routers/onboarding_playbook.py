"""Onboarding playbook phases, risks, and plan builder for Dealix Saudi B2B clients.

All data is static; no LLM or external API calls are made.
All generated plans carry a mandatory draft disclaimer and must be
reviewed and approved before sharing with any client.

Prefix: /api/v1/onboarding-playbook
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

router = APIRouter(
    prefix="/api/v1/onboarding-playbook",
    tags=["Sales"],
)

# ---------------------------------------------------------------------------
# Governance constants
# ---------------------------------------------------------------------------

_GOV_REVIEW = "ALLOW_WITH_REVIEW"
_GOV_APPROVAL = "APPROVAL_FIRST"

_DISCLAIMER_EN = (
    "This onboarding plan is a draft generated from inputs provided. "
    "All timelines, milestones, and recommendations are estimates and must be "
    "reviewed and confirmed by the delivery team before sharing with the client."
)
_DISCLAIMER_AR = (
    "خطة الإعداد هذه مسودة أُنشئت استناداً إلى المدخلات المقدمة. "
    "جميع الجداول الزمنية والمعالم والتوصيات تقديرية ويجب على فريق التسليم "
    "مراجعتها وتأكيدها قبل مشاركتها مع العميل."
)

# ---------------------------------------------------------------------------
# Static data: onboarding phases
# ---------------------------------------------------------------------------

_ONBOARDING_PHASES: list[dict[str, Any]] = [
    {
        "order": 1,
        "phase_name_en": "Kickoff",
        "phase_name_ar": "الانطلاق",
        "duration_days": 3,
        "key_milestones_en": [
            "Conduct project kickoff meeting with all stakeholders.",
            "Confirm project scope, timelines, and success criteria.",
            "Assign internal and client-side project leads.",
        ],
        "key_milestones_ar": [
            "عقد اجتماع انطلاق المشروع مع جميع أصحاب المصلحة.",
            "تأكيد نطاق المشروع والجداول الزمنية ومعايير النجاح.",
            "تعيين قادة المشروع على الجانبين الداخلي وجانب العميل.",
        ],
        "success_criteria_en": "All stakeholders aligned on scope, roles, and timeline.",
        "success_criteria_ar": "توافق جميع أصحاب المصلحة على النطاق والأدوار والجدول الزمني.",
    },
    {
        "order": 2,
        "phase_name_en": "Data Integration",
        "phase_name_ar": "تكامل البيانات",
        "duration_days": 7,
        "key_milestones_en": [
            "Map client data sources and confirm data access credentials.",
            "Complete initial data ingestion and validation run.",
            "Resolve data quality issues identified in validation.",
        ],
        "key_milestones_ar": [
            "رسم مصادر بيانات العميل وتأكيد بيانات الاعتماد للوصول.",
            "إكمال عملية استيعاب البيانات الأولية وتشغيل التحقق.",
            "حل مشكلات جودة البيانات المحددة في التحقق.",
        ],
        "success_criteria_en": "Data pipeline is live with validation passing at 95% or above.",
        "success_criteria_ar": "خط أنابيب البيانات شغّال مع اجتياز التحقق بنسبة 95% أو أكثر.",
    },
    {
        "order": 3,
        "phase_name_en": "Configuration",
        "phase_name_ar": "الإعداد والتهيئة",
        "duration_days": 5,
        "key_milestones_en": [
            "Configure platform settings to match client's business rules.",
            "Set up user roles, permissions, and access controls.",
            "Run end-to-end configuration validation with client team.",
        ],
        "key_milestones_ar": [
            "تهيئة إعدادات المنصة لتتوافق مع قواعد أعمال العميل.",
            "إعداد أدوار المستخدمين والأذونات وضوابط الوصول.",
            "تشغيل التحقق الشامل من الإعداد مع فريق العميل.",
        ],
        "success_criteria_en": "Platform configuration signed off by client operational lead.",
        "success_criteria_ar": "تمت الموافقة على تهيئة المنصة من قِبَل المسؤول التشغيلي للعميل.",
    },
    {
        "order": 4,
        "phase_name_en": "Training",
        "phase_name_ar": "التدريب",
        "duration_days": 3,
        "key_milestones_en": [
            "Deliver role-based training sessions for all user groups.",
            "Share bilingual user guides and quick-start materials.",
            "Conduct knowledge-check assessment to confirm competency.",
        ],
        "key_milestones_ar": [
            "تقديم جلسات تدريبية قائمة على الأدوار لجميع مجموعات المستخدمين.",
            "مشاركة أدلة المستخدم ثنائية اللغة ومواد البدء السريع.",
            "إجراء تقييم اختبار المعرفة للتحقق من الكفاءة.",
        ],
        "success_criteria_en": "All primary users have completed training with a passing score.",
        "success_criteria_ar": "أكمل جميع المستخدمون الرئيسيون التدريب بدرجة ناجحة.",
    },
    {
        "order": 5,
        "phase_name_en": "Go Live",
        "phase_name_ar": "الإطلاق الفعلي",
        "duration_days": 2,
        "key_milestones_en": [
            "Execute final pre-launch checklist with client and delivery team.",
            "Switch production environment to live and confirm system health.",
            "Brief client support contacts on escalation procedures.",
        ],
        "key_milestones_ar": [
            "تنفيذ قائمة التحقق النهائية قبل الإطلاق مع العميل وفريق التسليم.",
            "تحويل بيئة الإنتاج إلى الوضع المباشر والتأكد من سلامة النظام.",
            "إحاطة جهات الدعم لدى العميل بإجراءات التصعيد.",
        ],
        "success_criteria_en": "System is live, stable, and client team is operating independently.",
        "success_criteria_ar": "النظام يعمل بشكل مباشر ومستقر وفريق العميل يعمل باستقلالية.",
    },
]

# ---------------------------------------------------------------------------
# Static data: onboarding risks
# ---------------------------------------------------------------------------

_ONBOARDING_RISKS: list[dict[str, Any]] = [
    {
        "risk_en": "Delayed data access from client IT team",
        "risk_ar": "تأخر وصول البيانات من فريق تقنية المعلومات لدى العميل",
        "mitigation_en": "Agree on data access SLA in the kickoff meeting and escalate to sponsor if breached.",
        "mitigation_ar": "الاتفاق على اتفاقية مستوى خدمة الوصول إلى البيانات في اجتماع الانطلاق والتصعيد للراعي عند الخرق.",
        "probability": "high",
    },
    {
        "risk_en": "Low adoption due to insufficient end-user training",
        "risk_ar": "انخفاض التبني بسبب عدم كفاية تدريب المستخدم النهائي",
        "mitigation_en": "Schedule dedicated training sessions per role group and provide follow-up office hours.",
        "mitigation_ar": "جدولة جلسات تدريبية مخصصة لكل مجموعة أدوار وتوفير ساعات مكتبية للمتابعة.",
        "probability": "medium",
    },
    {
        "risk_en": "Scope creep extending the project timeline",
        "risk_ar": "زحف النطاق الذي يمدد الجدول الزمني للمشروع",
        "mitigation_en": "Maintain a formal change request process; any scope change requires written approval.",
        "mitigation_ar": "الحفاظ على عملية طلب تغيير رسمية؛ أي تغيير في النطاق يتطلب موافقة خطية.",
        "probability": "medium",
    },
    {
        "risk_en": "Champion changes role or leaves during onboarding",
        "risk_ar": "البطل يغير دوره أو يغادر خلال فترة الإعداد",
        "mitigation_en": "Identify a secondary internal champion early and keep executive sponsor briefed.",
        "mitigation_ar": "تحديد بطل داخلي ثانٍ مبكراً وإبقاء الراعي التنفيذي على اطلاع.",
        "probability": "low",
    },
    {
        "risk_en": "Integration failures with legacy internal systems",
        "risk_ar": "فشل التكاملات مع الأنظمة الداخلية القديمة",
        "mitigation_en": "Conduct a technical discovery session before kickoff to identify compatibility risks.",
        "mitigation_ar": "إجراء جلسة اكتشاف تقني قبل الانطلاق لتحديد مخاطر التوافق.",
        "probability": "medium",
    },
]

# ---------------------------------------------------------------------------
# Valid engagement types
# ---------------------------------------------------------------------------

_VALID_ENGAGEMENT_TYPES: set[str] = {"sprint", "data_pack", "managed_ops", "custom_ai"}

# ---------------------------------------------------------------------------
# Pydantic models
# ---------------------------------------------------------------------------


class OnboardingPlanInput(BaseModel):
    client_name: str
    engagement_type: str
    start_date: str = Field(..., min_length=1)
    primary_contact_name: str
    primary_contact_title: str
    data_systems: list[str] = Field(default_factory=list)
    arabic_primary: bool = False


# ---------------------------------------------------------------------------
# Pure-function core
# ---------------------------------------------------------------------------


def _build_onboarding_plan(inp: OnboardingPlanInput) -> dict[str, Any]:
    """Build a structured onboarding plan from validated input.

    Raises HTTPException 422 if engagement_type is not a valid value.
    Returns a structured dict with phases, risks, contact, and language preference.
    """
    if inp.engagement_type not in _VALID_ENGAGEMENT_TYPES:
        raise HTTPException(
            status_code=422,
            detail={
                "error": f"Invalid engagement_type '{inp.engagement_type}'.",
                "valid_values": sorted(_VALID_ENGAGEMENT_TYPES),
                "governance_decision": _GOV_REVIEW,
            },
        )

    total_duration_days = sum(p["duration_days"] for p in _ONBOARDING_PHASES)

    return {
        "client_name": inp.client_name,
        "engagement_type": inp.engagement_type,
        "phases": list(_ONBOARDING_PHASES),
        "total_duration_days": total_duration_days,
        "primary_contact": {
            "name": inp.primary_contact_name,
            "title": inp.primary_contact_title,
        },
        "data_systems_count": len(inp.data_systems),
        "language_primary": "ar" if inp.arabic_primary else "en",
        "risks": list(_ONBOARDING_RISKS),
        "disclaimer_en": _DISCLAIMER_EN,
        "disclaimer_ar": _DISCLAIMER_AR,
        "governance_decision": _GOV_APPROVAL,
    }


# ---------------------------------------------------------------------------
# Router endpoints
# ---------------------------------------------------------------------------


@router.get("/phases", summary="All 5 onboarding phases")
def get_phases() -> dict[str, Any]:
    """Return all onboarding phases with bilingual names, milestones, and success criteria."""
    return {
        "phases": _ONBOARDING_PHASES,
        "total_phases": len(_ONBOARDING_PHASES),
        "total_duration_days": sum(p["duration_days"] for p in _ONBOARDING_PHASES),
        "governance_decision": _GOV_REVIEW,
    }


@router.get("/risks", summary="All 5 onboarding risk items")
def get_risks() -> dict[str, Any]:
    """Return all onboarding risk items with bilingual descriptions and mitigation strategies."""
    return {
        "risks": _ONBOARDING_RISKS,
        "total_risks": len(_ONBOARDING_RISKS),
        "governance_decision": _GOV_REVIEW,
    }


@router.post("/build-plan", summary="Build a full bilingual onboarding plan")
def build_plan(body: OnboardingPlanInput) -> dict[str, Any]:
    """Accept onboarding input and return a structured draft onboarding plan.

    All output carries a mandatory draft disclaimer and requires delivery
    team review before sharing with the client.
    Governance decision: APPROVAL_FIRST.
    """
    return _build_onboarding_plan(body)
