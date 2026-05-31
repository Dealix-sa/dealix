"""Sales cadence templates and communication planning for Dealix Saudi B2B.

Provides cadence templates, Saudi-specific communication rules, and a
plan-builder that combines them into an actionable outreach sequence.
All data is static; no LLM or external API calls are made.

Prefix: /api/v1/sales-cadence
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

router = APIRouter(
    prefix="/api/v1/sales-cadence",
    tags=["Sales"],
)

# ---------------------------------------------------------------------------
# Governance constants
# ---------------------------------------------------------------------------

_GOV_REVIEW = "ALLOW_WITH_REVIEW"
_GOV_APPROVAL = "APPROVAL_FIRST"

# ---------------------------------------------------------------------------
# Static data: cadence templates
# ---------------------------------------------------------------------------

_CADENCE_TEMPLATES: dict[str, Any] = {
    "cold_outreach": {
        "name_en": "Cold Outreach",
        "name_ar": "التواصل البارد",
        "total_touches": 5,
        "duration_days": 14,
        "touch_sequence": [
            {
                "day": 1,
                "channel": "email",
                "message_hook_en": "Introduction to Dealix and how we help Saudi SMEs grow.",
                "message_hook_ar": "مقدمة عن ديليكس وكيف نساعد المنشآت الصغيرة والمتوسطة في المملكة.",
            },
            {
                "day": 3,
                "channel": "whatsapp",
                "message_hook_en": "Brief follow-up sharing one relevant client result.",
                "message_hook_ar": "متابعة سريعة تتضمن نتيجة عميل ذات صلة.",
            },
            {
                "day": 6,
                "channel": "call",
                "message_hook_en": "Discovery call to understand current growth challenges.",
                "message_hook_ar": "مكالمة استكشافية لفهم تحديات النمو الحالية.",
            },
            {
                "day": 10,
                "channel": "email",
                "message_hook_en": "Case study aligned to their sector.",
                "message_hook_ar": "دراسة حالة موجهة لقطاعهم.",
            },
            {
                "day": 14,
                "channel": "whatsapp",
                "message_hook_en": "Final check-in with a soft call to action.",
                "message_hook_ar": "متابعة أخيرة مع دعوة لطيفة للتصرف.",
            },
        ],
    },
    "warm_intro": {
        "name_en": "Warm Introduction",
        "name_ar": "التعريف الدافئ",
        "total_touches": 4,
        "duration_days": 7,
        "touch_sequence": [
            {
                "day": 1,
                "channel": "whatsapp",
                "message_hook_en": "Warm greeting referencing the mutual connection.",
                "message_hook_ar": "تحية دافئة مع الإشارة إلى الاتصال المشترك.",
            },
            {
                "day": 2,
                "channel": "call",
                "message_hook_en": "Introduction call to explore fit and shared priorities.",
                "message_hook_ar": "مكالمة تعريفية لاستكشاف التوافق والأولويات المشتركة.",
            },
            {
                "day": 4,
                "channel": "email",
                "message_hook_en": "Tailored one-pager based on call discussion.",
                "message_hook_ar": "ملخص مخصص بناءً على ما تم نقاشه في المكالمة.",
            },
            {
                "day": 7,
                "channel": "whatsapp",
                "message_hook_en": "Proposal or next-step confirmation.",
                "message_hook_ar": "تأكيد العرض أو الخطوة التالية.",
            },
        ],
    },
    "post_demo": {
        "name_en": "Post-Demo Follow-Up",
        "name_ar": "متابعة ما بعد العرض التوضيحي",
        "total_touches": 6,
        "duration_days": 21,
        "touch_sequence": [
            {
                "day": 1,
                "channel": "email",
                "message_hook_en": "Thank you and demo summary with key takeaways.",
                "message_hook_ar": "شكر وملخص العرض مع النقاط الرئيسية.",
            },
            {
                "day": 2,
                "channel": "whatsapp",
                "message_hook_en": "Quick check-in on any immediate questions.",
                "message_hook_ar": "متابعة سريعة للإجابة على أي أسئلة فورية.",
            },
            {
                "day": 5,
                "channel": "call",
                "message_hook_en": "Objection-handling call to address concerns.",
                "message_hook_ar": "مكالمة للتعامل مع الاعتراضات وتوضيح المخاوف.",
            },
            {
                "day": 9,
                "channel": "email",
                "message_hook_en": "Custom pricing proposal based on their requirements.",
                "message_hook_ar": "عرض أسعار مخصص بناءً على متطلباتهم.",
            },
            {
                "day": 14,
                "channel": "call",
                "message_hook_en": "Decision-timeline call to understand approval process.",
                "message_hook_ar": "مكالمة لفهم الجدول الزمني لاتخاذ القرار.",
            },
            {
                "day": 21,
                "channel": "whatsapp",
                "message_hook_en": "Final nudge with limited-time onboarding incentive.",
                "message_hook_ar": "تذكير أخير مع حافز تأهيل محدود الوقت.",
            },
        ],
    },
    "renewal_touch": {
        "name_en": "Renewal Touch",
        "name_ar": "متابعة التجديد",
        "total_touches": 5,
        "duration_days": 30,
        "touch_sequence": [
            {
                "day": 1,
                "channel": "email",
                "message_hook_en": "Annual review invitation highlighting value delivered.",
                "message_hook_ar": "دعوة للمراجعة السنوية مع إبراز القيمة المحققة.",
            },
            {
                "day": 5,
                "channel": "call",
                "message_hook_en": "Value-review call showcasing ROI and outcomes.",
                "message_hook_ar": "مكالمة مراجعة القيمة لعرض العائد على الاستثمار والنتائج.",
            },
            {
                "day": 10,
                "channel": "whatsapp",
                "message_hook_en": "Renewal options summary with upgrade benefits.",
                "message_hook_ar": "ملخص خيارات التجديد مع فوائد الترقية.",
            },
            {
                "day": 20,
                "channel": "email",
                "message_hook_en": "Renewal proposal with next-year service plan.",
                "message_hook_ar": "عرض التجديد مع خطة الخدمة للعام القادم.",
            },
            {
                "day": 30,
                "channel": "call",
                "message_hook_en": "Commitment call to close renewal before expiry.",
                "message_hook_ar": "مكالمة الالتزام لإتمام التجديد قبل انتهاء الصلاحية.",
            },
        ],
    },
}

# ---------------------------------------------------------------------------
# Static data: Saudi communication rules
# ---------------------------------------------------------------------------

_SAUDI_COMMUNICATION_RULES: list[dict[str, Any]] = [
    {
        "rule_en": "Avoid contact during the five daily prayer times.",
        "rule_ar": "تجنب التواصل خلال أوقات الصلوات الخمس.",
    },
    {
        "rule_en": "Reduce outreach frequency during Ramadan; respect the slower business pace.",
        "rule_ar": "تقليل وتيرة التواصل خلال شهر رمضان واحترام إيقاع الأعمال الأبطأ.",
    },
    {
        "rule_en": "WhatsApp is the preferred channel over email for most Saudi business contacts.",
        "rule_ar": "واتساب هو القناة المفضلة على البريد الإلكتروني لمعظم جهات الأعمال السعودية.",
    },
    {
        "rule_en": "Use Arabic as the primary language for non-corporate contacts.",
        "rule_ar": "استخدم العربية كلغة أساسية للتواصل مع جهات الاتصال غير المؤسسية.",
    },
    {
        "rule_en": "Decision-makers prefer direct phone calls over text messages.",
        "rule_ar": "يفضل صانعو القرار المكالمات الهاتفية المباشرة على الرسائل النصية.",
    },
    {
        "rule_en": "Follow up within 48 hours of any meeting or call to maintain momentum.",
        "rule_ar": "تابع خلال 48 ساعة من أي اجتماع أو مكالمة للحفاظ على الزخم.",
    },
]

# ---------------------------------------------------------------------------
# Valid cadence types
# ---------------------------------------------------------------------------

_VALID_CADENCE_TYPES: set[str] = {
    "cold_outreach",
    "warm_intro",
    "post_demo",
    "renewal_touch",
}

# ---------------------------------------------------------------------------
# Pydantic models
# ---------------------------------------------------------------------------


class CadencePlanInput(BaseModel):
    cadence_type: str
    prospect_name: str
    prospect_company: str
    preferred_channel: str = Field(default="whatsapp")
    arabic_primary: bool = False


# ---------------------------------------------------------------------------
# Pure-function core
# ---------------------------------------------------------------------------


def _build_cadence_plan(inp: CadencePlanInput) -> dict[str, Any]:
    """Build a personalised cadence plan for a prospect.

    Returns a structured dict with the full touch sequence, Saudi communication
    rules to observe, and a governance decision of APPROVAL_FIRST.
    """
    if inp.cadence_type not in _VALID_CADENCE_TYPES:
        raise HTTPException(
            status_code=422,
            detail=(
                f"Invalid cadence_type '{inp.cadence_type}'. "
                f"Valid values: {sorted(_VALID_CADENCE_TYPES)}"
            ),
        )

    template = _CADENCE_TEMPLATES[inp.cadence_type]

    return {
        "cadence_type": inp.cadence_type,
        "prospect_name": inp.prospect_name,
        "prospect_company": inp.prospect_company,
        "template_name_en": template["name_en"],
        "template_name_ar": template["name_ar"],
        "total_touches": template["total_touches"],
        "duration_days": template["duration_days"],
        "touch_sequence": list(template["touch_sequence"]),
        "language_preference": "ar" if inp.arabic_primary else "en",
        "saudi_rules_to_observe": list(_SAUDI_COMMUNICATION_RULES),
        "governance_decision": _GOV_APPROVAL,
    }


# ---------------------------------------------------------------------------
# Router endpoints
# ---------------------------------------------------------------------------


@router.get("/templates", summary="All 4 cadence templates with metadata")
def get_templates() -> dict[str, Any]:
    """Return metadata for all cadence templates (no touch_sequence detail)."""
    templates_meta = [
        {
            "cadence_type": key,
            "name_en": val["name_en"],
            "name_ar": val["name_ar"],
            "total_touches": val["total_touches"],
            "duration_days": val["duration_days"],
        }
        for key, val in _CADENCE_TEMPLATES.items()
    ]
    return {
        "templates": templates_meta,
        "total_templates": len(templates_meta),
        "governance_decision": _GOV_REVIEW,
    }


@router.get("/communication-rules", summary="All 6 Saudi communication rules")
def get_communication_rules() -> dict[str, Any]:
    """Return all Saudi-specific communication rules with bilingual labels."""
    return {
        "communication_rules": _SAUDI_COMMUNICATION_RULES,
        "total_rules": len(_SAUDI_COMMUNICATION_RULES),
        "governance_decision": _GOV_REVIEW,
    }


@router.post("/build-plan", summary="Build a personalised cadence plan for a prospect")
def build_plan(body: CadencePlanInput) -> dict[str, Any]:
    """Accept cadence input and return a full outreach plan.

    Governance decision: APPROVAL_FIRST.
    """
    return _build_cadence_plan(body)
