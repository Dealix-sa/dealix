"""Customer journey mapping and analytics for Dealix Saudi B2B.

Provides journey stage definitions, touchpoint library, health indicators,
and a journey-mapping function that assesses stage health and suggests
priority touchpoints. All data is static; no LLM or external API calls.

Prefix: /api/v1/customer-journey
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

router = APIRouter(
    prefix="/api/v1/customer-journey",
    tags=["Analytics"],
)

# ---------------------------------------------------------------------------
# Governance constants
# ---------------------------------------------------------------------------

_GOV_REVIEW = "ALLOW_WITH_REVIEW"

# ---------------------------------------------------------------------------
# Impact ordering for sorting touchpoints
# ---------------------------------------------------------------------------

_IMPACT_ORDER: dict[str, int] = {"high": 0, "medium": 1, "low": 2}

# ---------------------------------------------------------------------------
# Static data: journey stages
# ---------------------------------------------------------------------------

_JOURNEY_STAGES: list[dict[str, Any]] = [
    {
        "order": 1,
        "stage_id": "awareness",
        "stage_name_en": "Awareness",
        "stage_name_ar": "الوعي",
        "avg_duration_days": 30,
        "key_experience_en": "Prospect discovers Dealix through referral, content, or outreach.",
        "key_experience_ar": "يكتشف العميل المحتمل ديليكس عبر الإحالة أو المحتوى أو التواصل.",
        "success_metrics_en": [
            "Prospect has engaged with at least one Dealix touchpoint.",
            "Prospect has expressed interest or requested more information.",
        ],
        "dropout_risks_en": [
            "No follow-up within 48 hours of initial contact.",
            "Irrelevant outreach that does not address the prospect's sector.",
        ],
    },
    {
        "order": 2,
        "stage_id": "consideration",
        "stage_name_en": "Consideration",
        "stage_name_ar": "التفكير والمقارنة",
        "avg_duration_days": 14,
        "key_experience_en": "Prospect evaluates Dealix against alternatives and internal priorities.",
        "key_experience_ar": "يقيّم العميل المحتمل ديليكس مقارنةً بالبدائل والأولويات الداخلية.",
        "success_metrics_en": [
            "Prospect has attended a demo or product walkthrough.",
            "Prospect has shared internal evaluation criteria.",
        ],
        "dropout_risks_en": [
            "Failure to address key objections within two follow-ups.",
            "Competitor offers a significantly lower price without value context.",
        ],
    },
    {
        "order": 3,
        "stage_id": "purchase",
        "stage_name_en": "Purchase",
        "stage_name_ar": "الشراء",
        "avg_duration_days": 7,
        "key_experience_en": "Prospect signs the contract and completes the first payment.",
        "key_experience_ar": "يوقّع العميل العقد ويُتم الدفع الأول.",
        "success_metrics_en": [
            "Contract signed and received.",
            "First payment confirmed.",
        ],
        "dropout_risks_en": [
            "Procurement delays or contract review bottlenecks.",
            "Last-minute negotiation stalls without escalation path.",
        ],
    },
    {
        "order": 4,
        "stage_id": "onboarding",
        "stage_name_en": "Onboarding",
        "stage_name_ar": "الإعداد والتأهيل",
        "avg_duration_days": 20,
        "key_experience_en": "New client is set up, trained, and activated on the platform.",
        "key_experience_ar": "يتم إعداد العميل الجديد وتدريبه وتفعيله على المنصة.",
        "success_metrics_en": [
            "Client has completed onboarding checklist.",
            "First active use of core platform features recorded.",
        ],
        "dropout_risks_en": [
            "Onboarding call not scheduled within three business days of contract signing.",
            "Key stakeholders not included in the onboarding session.",
        ],
    },
    {
        "order": 5,
        "stage_id": "value_realization",
        "stage_name_en": "Value Realization",
        "stage_name_ar": "تحقيق القيمة",
        "avg_duration_days": 60,
        "key_experience_en": "Client experiences measurable outcomes and ROI from the platform.",
        "key_experience_ar": "يُجرّب العميل نتائج قابلة للقياس وعائداً على الاستثمار من المنصة.",
        "success_metrics_en": [
            "Client can cite at least one quantified business outcome.",
            "NPS score of 7 or above recorded.",
        ],
        "dropout_risks_en": [
            "No success metric agreed within 30 days of onboarding.",
            "Low platform engagement in the first 90 days.",
        ],
    },
    {
        "order": 6,
        "stage_id": "expansion",
        "stage_name_en": "Expansion",
        "stage_name_ar": "التوسع",
        "avg_duration_days": 0,
        "key_experience_en": "Client expands usage, upgrades tier, or refers new customers.",
        "key_experience_ar": "يوسّع العميل استخدامه أو يُرقّي خطته أو يُحيل عملاء جدداً.",
        "success_metrics_en": [
            "Upsell or cross-sell opportunity identified and actioned.",
            "At least one referral or case study agreed.",
        ],
        "dropout_risks_en": [
            "No expansion conversation initiated before 12-month renewal.",
            "Unresolved support tickets dampening expansion intent.",
        ],
    },
]

# ---------------------------------------------------------------------------
# Static data: touchpoint library
# ---------------------------------------------------------------------------

_TOUCHPOINT_LIBRARY: list[dict[str, Any]] = [
    {
        "touchpoint_en": "Cold outreach email introducing Dealix",
        "touchpoint_ar": "بريد تواصل بارد يُعرّف بديليكس",
        "stage_id": "awareness",
        "channel": "email",
        "impact": "high",
    },
    {
        "touchpoint_en": "Sector-specific case study shared on WhatsApp",
        "touchpoint_ar": "دراسة حالة قطاعية مشتركة عبر واتساب",
        "stage_id": "awareness",
        "channel": "whatsapp",
        "impact": "medium",
    },
    {
        "touchpoint_en": "Live product demonstration tailored to prospect's use case",
        "touchpoint_ar": "عرض توضيحي حي مخصص لحالة استخدام العميل",
        "stage_id": "consideration",
        "channel": "call",
        "impact": "high",
    },
    {
        "touchpoint_en": "Competitive comparison document delivered via email",
        "touchpoint_ar": "وثيقة مقارنة تنافسية مُسلَّمة عبر البريد الإلكتروني",
        "stage_id": "consideration",
        "channel": "email",
        "impact": "medium",
    },
    {
        "touchpoint_en": "Contract walkthrough call with legal and commercial teams",
        "touchpoint_ar": "مكالمة مراجعة العقد مع الفرق القانونية والتجارية",
        "stage_id": "purchase",
        "channel": "call",
        "impact": "high",
    },
    {
        "touchpoint_en": "Onboarding kick-off session with dedicated success manager",
        "touchpoint_ar": "جلسة انطلاق التأهيل مع مدير النجاح المخصص",
        "stage_id": "onboarding",
        "channel": "call",
        "impact": "high",
    },
    {
        "touchpoint_en": "30-day value check-in to review early outcomes",
        "touchpoint_ar": "متابعة القيمة بعد 30 يوماً لمراجعة النتائج الأولية",
        "stage_id": "value_realization",
        "channel": "call",
        "impact": "high",
    },
    {
        "touchpoint_en": "Expansion proposal highlighting upgrade benefits",
        "touchpoint_ar": "عرض توسعة يُبرز فوائد الترقية",
        "stage_id": "expansion",
        "channel": "email",
        "impact": "high",
    },
]

# ---------------------------------------------------------------------------
# Static data: journey health indicators
# ---------------------------------------------------------------------------

_JOURNEY_HEALTH_INDICATORS: list[dict[str, Any]] = [
    {
        "indicator_en": "Platform Engagement Rate",
        "indicator_ar": "معدل التفاعل مع المنصة",
        "measurement_en": "Percentage of weekly active users relative to licensed seats.",
    },
    {
        "indicator_en": "Time to First Value",
        "indicator_ar": "الوقت حتى تحقيق القيمة الأولى",
        "measurement_en": "Days from contract signing to client's first confirmed outcome.",
    },
    {
        "indicator_en": "NPS Score Trend",
        "indicator_ar": "اتجاه درجة صافي الترويج",
        "measurement_en": "Rolling 90-day average NPS score across active accounts.",
    },
    {
        "indicator_en": "Support Ticket Resolution Time",
        "indicator_ar": "وقت حل تذاكر الدعم",
        "measurement_en": "Average hours to resolve P1 and P2 support tickets.",
    },
    {
        "indicator_en": "Renewal Likelihood Score",
        "indicator_ar": "درجة احتمالية التجديد",
        "measurement_en": "Composite score based on engagement, NPS, and account growth signals.",
    },
]

# ---------------------------------------------------------------------------
# Valid journey stage IDs
# ---------------------------------------------------------------------------

_VALID_JOURNEY_STAGES: set[str] = {s["stage_id"] for s in _JOURNEY_STAGES}

# ---------------------------------------------------------------------------
# Pydantic models
# ---------------------------------------------------------------------------


class JourneyMappingInput(BaseModel):
    client_name: str
    current_stage: str
    days_in_current_stage: int = Field(..., ge=0)
    has_completed_onboarding: bool = False
    first_value_delivered: bool = False
    nps_score: float = Field(default=7.0, ge=0, le=10)


# ---------------------------------------------------------------------------
# Pure-function core
# ---------------------------------------------------------------------------


def _map_customer_journey(inp: JourneyMappingInput) -> dict[str, Any]:
    """Map a client's current position in the customer journey.

    Returns stage health, next stage, journey completion percentage, priority
    touchpoints, and a governance decision of ALLOW_WITH_REVIEW.
    """
    if inp.current_stage not in _VALID_JOURNEY_STAGES:
        raise HTTPException(
            status_code=422,
            detail=(
                f"Invalid current_stage '{inp.current_stage}'. "
                f"Valid values: {sorted(_VALID_JOURNEY_STAGES)}"
            ),
        )

    current_stage_data = next(s for s in _JOURNEY_STAGES if s["stage_id"] == inp.current_stage)
    avg_days = current_stage_data["avg_duration_days"]

    if avg_days == 0:
        stage_health = "on_track"
    elif inp.days_in_current_stage > avg_days * 2:
        stage_health = "at_risk"
    elif inp.days_in_current_stage > avg_days:
        stage_health = "slow"
    else:
        stage_health = "on_track"

    current_order = current_stage_data["order"]
    next_stage_data = next(
        (s for s in _JOURNEY_STAGES if s["order"] == current_order + 1), None
    )
    next_stage = next_stage_data["stage_id"] if next_stage_data else None

    journey_completion_pct = (current_order - 1) / 5 * 100

    stage_touchpoints = [
        t for t in _TOUCHPOINT_LIBRARY if t["stage_id"] == inp.current_stage
    ]
    stage_touchpoints_sorted = sorted(
        stage_touchpoints, key=lambda t: _IMPACT_ORDER.get(t["impact"], 99)
    )
    priority_touchpoints = stage_touchpoints_sorted[:3]

    return {
        "client_name": inp.client_name,
        "current_stage": inp.current_stage,
        "stage_health": stage_health,
        "next_stage": next_stage,
        "journey_completion_pct": journey_completion_pct,
        "priority_touchpoints": priority_touchpoints,
        "governance_decision": _GOV_REVIEW,
    }


# ---------------------------------------------------------------------------
# Router endpoints
# ---------------------------------------------------------------------------


@router.get("/stages", summary="All 6 customer journey stages")
def get_stages() -> dict[str, Any]:
    """Return all journey stages with bilingual labels, metrics, and risk info."""
    return {
        "stages": _JOURNEY_STAGES,
        "total_stages": len(_JOURNEY_STAGES),
        "governance_decision": _GOV_REVIEW,
    }


@router.get("/touchpoints", summary="All 8 journey touchpoints")
def get_touchpoints() -> dict[str, Any]:
    """Return all touchpoints with stage, channel, and impact level."""
    return {
        "touchpoints": _TOUCHPOINT_LIBRARY,
        "total_touchpoints": len(_TOUCHPOINT_LIBRARY),
        "governance_decision": _GOV_REVIEW,
    }


@router.post("/map", summary="Map a client's current position in the customer journey")
def map_journey(body: JourneyMappingInput) -> dict[str, Any]:
    """Accept journey input and return a full journey mapping assessment.

    Governance decision: ALLOW_WITH_REVIEW.
    """
    return _map_customer_journey(body)
