"""Health score explainer for customer health scoring methodology.

Explains the scoring dimensions, weights, and bands. Provides a breakdown
function that computes overall score, per-dimension status, and improvement
levers. All data is static; no LLM or external API calls are made.

Prefix: /api/v1/health-score-explainer
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel, Field

router = APIRouter(
    prefix="/api/v1/health-score-explainer",
    tags=["Analytics"],
)

# ---------------------------------------------------------------------------
# Governance constants
# ---------------------------------------------------------------------------

_GOV_REVIEW = "ALLOW_WITH_REVIEW"

# ---------------------------------------------------------------------------
# Static data: health dimensions
# ---------------------------------------------------------------------------

_HEALTH_DIMENSIONS: list[dict[str, Any]] = [
    {
        "order": 1,
        "dimension_id": "product_usage",
        "dimension_name_en": "Product Usage",
        "dimension_name_ar": "استخدام المنتج",
        "weight": 25,
        "description_en": "Measures active feature adoption and usage frequency relative to purchased capacity.",
        "green_threshold": 75,
        "amber_threshold": 50,
    },
    {
        "order": 2,
        "dimension_id": "nps",
        "dimension_name_en": "NPS Score",
        "dimension_name_ar": "نقاط صافي المروجين",
        "weight": 20,
        "description_en": "Net Promoter Score normalized to 0-100; reflects customer satisfaction and likelihood to recommend.",
        "green_threshold": 8,
        "amber_threshold": 6,
    },
    {
        "order": 3,
        "dimension_id": "support_health",
        "dimension_name_en": "Support Health",
        "dimension_name_ar": "صحة الدعم الفني",
        "weight": 15,
        "description_en": "Tracks open ticket volume, escalation rate, and time-to-resolution trends.",
        "green_threshold": 80,
        "amber_threshold": 60,
    },
    {
        "order": 4,
        "dimension_id": "engagement",
        "dimension_name_en": "Engagement",
        "dimension_name_ar": "مستوى التفاعل",
        "weight": 15,
        "description_en": "Captures stakeholder participation in QBRs, training sessions, and platform logins.",
        "green_threshold": 70,
        "amber_threshold": 40,
    },
    {
        "order": 5,
        "dimension_id": "expansion_signals",
        "dimension_name_en": "Expansion Signals",
        "dimension_name_ar": "إشارات التوسع",
        "weight": 15,
        "description_en": "Monitors upsell intent, seat growth requests, and cross-product exploration.",
        "green_threshold": 60,
        "amber_threshold": 30,
    },
    {
        "order": 6,
        "dimension_id": "billing_health",
        "dimension_name_en": "Billing Health",
        "dimension_name_ar": "صحة الفوترة",
        "weight": 10,
        "description_en": "Tracks on-time payment rate, failed payment attempts, and invoice dispute frequency.",
        "green_threshold": 95,
        "amber_threshold": 80,
    },
]

# ---------------------------------------------------------------------------
# Static data: health score bands
# ---------------------------------------------------------------------------

_HEALTH_SCORE_BANDS: dict[str, Any] = {
    "expansion_ready": {
        "band_name_en": "Expansion Ready",
        "band_name_ar": "جاهز للتوسع",
        "score_range_en": "90-100",
        "recommended_actions_en": [
            "Initiate upsell conversation with champion.",
            "Invite to reference customer or case study program.",
        ],
    },
    "healthy": {
        "band_name_en": "Healthy",
        "band_name_ar": "بصحة جيدة",
        "score_range_en": "75-89",
        "recommended_actions_en": [
            "Schedule quarterly business review to reinforce value.",
            "Present roadmap features aligned to client goals.",
        ],
    },
    "stable": {
        "band_name_en": "Stable",
        "band_name_ar": "مستقر",
        "score_range_en": "60-74",
        "recommended_actions_en": [
            "Run usage adoption session to activate underused features.",
            "Set 60-day improvement plan with clear success milestones.",
        ],
    },
    "at_risk": {
        "band_name_en": "At Risk",
        "band_name_ar": "في خطر",
        "score_range_en": "40-59",
        "recommended_actions_en": [
            "Escalate to customer success manager for immediate outreach.",
            "Conduct root cause analysis on weakest dimensions.",
        ],
    },
    "critical": {
        "band_name_en": "Critical",
        "band_name_ar": "حرج",
        "score_range_en": "20-39",
        "recommended_actions_en": [
            "Executive sponsor call within 48 hours.",
            "Deploy rapid recovery playbook with weekly check-ins.",
        ],
    },
    "blocked": {
        "band_name_en": "Blocked",
        "band_name_ar": "محظور",
        "score_range_en": "0-19",
        "recommended_actions_en": [
            "Initiate emergency intervention protocol immediately.",
            "Assess churn risk and escalate to leadership.",
        ],
    },
}

# ---------------------------------------------------------------------------
# Static data: improvement levers
# ---------------------------------------------------------------------------

_HEALTH_IMPROVEMENT_LEVERS: list[dict[str, Any]] = [
    {
        "lever_en": "Dedicated onboarding session for underused features",
        "lever_ar": "جلسة تأهيل مخصصة للميزات قليلة الاستخدام",
        "typical_score_improvement": 15,
        "time_to_impact_weeks": 4,
    },
    {
        "lever_en": "Executive business review with ROI presentation",
        "lever_ar": "مراجعة تجارية تنفيذية مع عرض عائد الاستثمار",
        "typical_score_improvement": 10,
        "time_to_impact_weeks": 6,
    },
    {
        "lever_en": "Proactive support health check and ticket closure sprint",
        "lever_ar": "فحص صحة الدعم الاستباقي وجلسة إغلاق التذاكر",
        "typical_score_improvement": 12,
        "time_to_impact_weeks": 2,
    },
    {
        "lever_en": "NPS recovery outreach and action plan",
        "lever_ar": "التواصل لتحسين نقاط صافي المروجين وخطة العمل",
        "typical_score_improvement": 8,
        "time_to_impact_weeks": 8,
    },
    {
        "lever_en": "Billing reconciliation and payment plan alignment",
        "lever_ar": "مطابقة الفوترة ومواءمة خطة السداد",
        "typical_score_improvement": 5,
        "time_to_impact_weeks": 1,
    },
]

# ---------------------------------------------------------------------------
# Dimension to input field mapping
# ---------------------------------------------------------------------------

_DIMENSION_INPUT_FIELDS: dict[str, str] = {
    "product_usage": "product_usage_score",
    "nps": "nps_score_normalized",
    "support_health": "support_health_score",
    "engagement": "engagement_score",
    "expansion_signals": "expansion_signals_score",
    "billing_health": "billing_health_score",
}

# ---------------------------------------------------------------------------
# Pydantic models
# ---------------------------------------------------------------------------


class HealthScoreBreakdownInput(BaseModel):
    client_name: str
    product_usage_score: float = Field(..., ge=0, le=100)
    nps_score_normalized: float = Field(..., ge=0, le=100)
    support_health_score: float = Field(..., ge=0, le=100)
    engagement_score: float = Field(..., ge=0, le=100)
    expansion_signals_score: float = Field(..., ge=0, le=100)
    billing_health_score: float = Field(..., ge=0, le=100)


# ---------------------------------------------------------------------------
# Pure-function core
# ---------------------------------------------------------------------------


def _explain_health_score(inp: HealthScoreBreakdownInput) -> dict[str, Any]:
    """Compute an overall health score and explain each dimension's contribution.

    Returns weighted score, band, per-dimension breakdown, weakest dimensions,
    and improvement levers. Governance decision: ALLOW_WITH_REVIEW.
    """
    score_values: dict[str, float] = {
        "product_usage": inp.product_usage_score,
        "nps": inp.nps_score_normalized,
        "support_health": inp.support_health_score,
        "engagement": inp.engagement_score,
        "expansion_signals": inp.expansion_signals_score,
        "billing_health": inp.billing_health_score,
    }

    overall_score: float = (
        inp.product_usage_score * 0.25
        + inp.nps_score_normalized * 0.20
        + inp.support_health_score * 0.15
        + inp.engagement_score * 0.15
        + inp.expansion_signals_score * 0.15
        + inp.billing_health_score * 0.10
    )

    if overall_score >= 90:
        score_band = "expansion_ready"
    elif overall_score >= 75:
        score_band = "healthy"
    elif overall_score >= 60:
        score_band = "stable"
    elif overall_score >= 40:
        score_band = "at_risk"
    elif overall_score >= 20:
        score_band = "critical"
    else:
        score_band = "blocked"

    band_data = _HEALTH_SCORE_BANDS[score_band]

    dimension_breakdown: list[dict[str, Any]] = []
    for dim in _HEALTH_DIMENSIONS:
        dim_id = dim["dimension_id"]
        score = score_values[dim_id]
        weight = dim["weight"]
        weighted_contribution = score * (weight / 100)
        green_threshold = dim["green_threshold"]
        amber_threshold = dim["amber_threshold"]
        if score >= green_threshold:
            status = "green"
        elif score >= amber_threshold:
            status = "amber"
        else:
            status = "red"
        dimension_breakdown.append(
            {
                "dimension_id": dim_id,
                "score": score,
                "weight": weight,
                "weighted_contribution": weighted_contribution,
                "status": status,
            }
        )

    red_dimensions = [d for d in dimension_breakdown if d["status"] == "red"]
    red_dimensions_sorted = sorted(red_dimensions, key=lambda d: d["weighted_contribution"])
    weakest_dimensions = [d["dimension_id"] for d in red_dimensions_sorted[:3]]

    return {
        "client_name": inp.client_name,
        "overall_score": overall_score,
        "score_band": score_band,
        "band_data": band_data,
        "dimension_breakdown": dimension_breakdown,
        "weakest_dimensions": weakest_dimensions,
        "improvement_levers": _HEALTH_IMPROVEMENT_LEVERS,
        "governance_decision": _GOV_REVIEW,
    }


# ---------------------------------------------------------------------------
# Router endpoints
# ---------------------------------------------------------------------------


@router.get("/dimensions", summary="All 6 health score dimensions")
def get_dimensions() -> dict[str, Any]:
    """Return all health scoring dimensions with weights and thresholds."""
    total_weight = sum(d["weight"] for d in _HEALTH_DIMENSIONS)
    return {
        "dimensions": _HEALTH_DIMENSIONS,
        "total_weight": total_weight,
        "governance_decision": _GOV_REVIEW,
    }


@router.get("/score-bands", summary="All 6 health score bands")
def get_score_bands() -> dict[str, Any]:
    """Return all health score bands with recommended actions."""
    return {
        "score_bands": _HEALTH_SCORE_BANDS,
        "governance_decision": _GOV_REVIEW,
    }


@router.get("/improvement-levers", summary="All 5 health improvement levers")
def get_improvement_levers() -> dict[str, Any]:
    """Return all health improvement levers with estimated impact and timeline."""
    return {
        "improvement_levers": _HEALTH_IMPROVEMENT_LEVERS,
        "governance_decision": _GOV_REVIEW,
    }


@router.post("/explain", summary="Explain health score breakdown for a client")
def explain_health_score(body: HealthScoreBreakdownInput) -> dict[str, Any]:
    """Accept per-dimension scores and return a full health score explanation.

    Governance decision: ALLOW_WITH_REVIEW.
    """
    return _explain_health_score(body)
