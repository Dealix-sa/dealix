"""Data quality operations framework for Dealix Saudi B2B.

Defines data quality dimensions, ZATCA compliance requirements, remediation
playbooks, and an assessment calculator. All data is static; no LLM or
external API calls are made.

Prefix: /api/v1/data-quality-ops
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel, Field

router = APIRouter(
    prefix="/api/v1/data-quality-ops",
    tags=["Analytics"],
)

# ---------------------------------------------------------------------------
# Governance constants
# ---------------------------------------------------------------------------

_GOV_REVIEW = "ALLOW_WITH_REVIEW"

# ---------------------------------------------------------------------------
# Static data: DQ dimensions
# ---------------------------------------------------------------------------

_DQ_DIMENSIONS: list[dict[str, Any]] = [
    {
        "dimension_id": "completeness",
        "dimension_name_en": "Completeness",
        "dimension_name_ar": "الاكتمال",
        "description_en": "The degree to which all required data fields are populated.",
        "weight": 25,
        "measurement_method_en": "Percentage of non-null values across mandatory fields.",
    },
    {
        "dimension_id": "accuracy",
        "dimension_name_en": "Accuracy",
        "dimension_name_ar": "الدقة",
        "description_en": "The degree to which data correctly reflects real-world values.",
        "weight": 25,
        "measurement_method_en": "Comparison of data values against verified reference sources.",
    },
    {
        "dimension_id": "timeliness",
        "dimension_name_en": "Timeliness",
        "dimension_name_ar": "الحداثة",
        "description_en": "The degree to which data is available when needed and up to date.",
        "weight": 20,
        "measurement_method_en": "Percentage of records updated within the required time window.",
    },
    {
        "dimension_id": "consistency",
        "dimension_name_en": "Consistency",
        "dimension_name_ar": "الاتساق",
        "description_en": "The degree to which data values are coherent across systems.",
        "weight": 20,
        "measurement_method_en": "Cross-system reconciliation rate for shared data entities.",
    },
    {
        "dimension_id": "uniqueness",
        "dimension_name_en": "Uniqueness",
        "dimension_name_ar": "التفرد",
        "description_en": "The degree to which records are free of unintended duplicates.",
        "weight": 10,
        "measurement_method_en": "Percentage of records with no duplicate keys or identifiers.",
    },
]

# ---------------------------------------------------------------------------
# Static data: DQ remediation playbooks
# ---------------------------------------------------------------------------

_DQ_REMEDIATION_PLAYBOOKS: dict[str, dict[str, Any]] = {
    "critical": {
        "label_en": "Critical",
        "label_ar": "حرج",
        "priority_actions_en": [
            "Halt automated reporting until data quality issues are resolved.",
            "Initiate a full data audit with designated data stewards.",
            "Establish a corrective action plan with a 14-day resolution target.",
        ],
        "priority_actions_ar": [
            "إيقاف التقارير الآلية حتى تُحل مشكلات جودة البيانات.",
            "بدء تدقيق كامل للبيانات بمشاركة أمناء البيانات المعيّنين.",
            "وضع خطة إجراءات تصحيحية بهدف حل المشكلة خلال 14 يوماً.",
        ],
    },
    "needs_work": {
        "label_en": "Needs Work",
        "label_ar": "يحتاج تحسيناً",
        "priority_actions_en": [
            "Identify the top three fields contributing to score degradation.",
            "Assign data quality owners for each underperforming dimension.",
            "Implement automated validation rules at the point of data entry.",
        ],
        "priority_actions_ar": [
            "تحديد الحقول الثلاثة الأكثر تأثيراً في تراجع الدرجة.",
            "تعيين مسؤولين عن جودة البيانات لكل بُعد ضعيف الأداء.",
            "تطبيق قواعد التحقق الآلي عند إدخال البيانات.",
        ],
    },
    "healthy": {
        "label_en": "Healthy",
        "label_ar": "بصحة جيدة",
        "priority_actions_en": [
            "Maintain current data governance practices and review quarterly.",
            "Document data lineage and ownership for audit readiness.",
            "Explore advanced analytics use cases enabled by high data quality.",
        ],
        "priority_actions_ar": [
            "الحفاظ على ممارسات حوكمة البيانات الحالية ومراجعتها فصلياً.",
            "توثيق سلسلة البيانات والملكية لضمان الجاهزية للتدقيق.",
            "استكشاف حالات استخدام التحليلات المتقدمة التي تتيحها جودة البيانات المرتفعة.",
        ],
    },
}

# ---------------------------------------------------------------------------
# Static data: ZATCA DQ requirements
# ---------------------------------------------------------------------------

_ZATCA_DQ_REQUIREMENTS: list[dict[str, Any]] = [
    {
        "requirement_en": "Invoice data completeness must meet or exceed the ZATCA Phase 2 minimum threshold.",
        "requirement_ar": "يجب أن يستوفي اكتمال بيانات الفاتورة الحد الأدنى المطلوب من المرحلة الثانية لهيئة الزكاة والجمارك أو يتجاوزه.",
        "minimum_score": 95,
    },
    {
        "requirement_en": "Tax calculation accuracy must reach the required level to prevent assessment errors.",
        "requirement_ar": "يجب أن تبلغ دقة احتساب الضريبة المستوى المطلوب لتجنب أخطاء التقييم.",
        "minimum_score": 99,
    },
    {
        "requirement_en": "Invoice timestamp timeliness is mandatory to satisfy real-time reporting obligations.",
        "requirement_ar": "تُعدّ حداثة طوابع وقت الفاتورة إلزامية للوفاء بالتزامات الإبلاغ الفوري.",
        "minimum_score": 90,
    },
    {
        "requirement_en": "Invoice record uniqueness must be absolute to prevent duplicate submission penalties.",
        "requirement_ar": "يجب أن يكون تفرد سجلات الفاتورة مطلقاً لتجنب غرامات التقديم المكرر.",
        "minimum_score": 100,
    },
]

# ---------------------------------------------------------------------------
# Pydantic models
# ---------------------------------------------------------------------------


class DQAssessmentInput(BaseModel):
    client_name: str
    completeness_score: float = Field(..., ge=0, le=100)
    accuracy_score: float = Field(..., ge=0, le=100)
    timeliness_score: float = Field(..., ge=0, le=100)
    consistency_score: float = Field(..., ge=0, le=100)
    uniqueness_score: float = Field(..., ge=0, le=100)


# ---------------------------------------------------------------------------
# Pure-function core
# ---------------------------------------------------------------------------


def _assess_data_quality(inp: DQAssessmentInput) -> dict[str, Any]:
    """Compute a weighted data quality assessment.

    Returns overall score, health label, remediation playbook, per-dimension
    scores, ZATCA compliance flag, and weakest dimension.
    """
    score_map: dict[str, float] = {
        "completeness": inp.completeness_score,
        "accuracy": inp.accuracy_score,
        "timeliness": inp.timeliness_score,
        "consistency": inp.consistency_score,
        "uniqueness": inp.uniqueness_score,
    }

    dimension_scores: list[dict[str, Any]] = []
    overall_score: float = 0.0
    for dim in _DQ_DIMENSIONS:
        dim_id = dim["dimension_id"]
        score = score_map[dim_id]
        weight = dim["weight"]
        weighted_contribution = score * weight / 100
        overall_score += weighted_contribution
        dimension_scores.append(
            {
                "dimension_id": dim_id,
                "score": score,
                "weight": weight,
                "weighted_contribution": weighted_contribution,
            }
        )

    if overall_score < 60:
        dq_label = "critical"
    elif overall_score < 80:
        dq_label = "needs_work"
    else:
        dq_label = "healthy"

    playbook = _DQ_REMEDIATION_PLAYBOOKS[dq_label]

    zatca_compliant: bool = (
        inp.completeness_score >= 95
        and inp.accuracy_score >= 99
        and inp.timeliness_score >= 90
        and inp.uniqueness_score >= 100
    )

    weakest_dimension: str = min(score_map, key=lambda k: score_map[k])

    return {
        "client_name": inp.client_name,
        "overall_score": overall_score,
        "dq_label": dq_label,
        "playbook": playbook,
        "dimension_scores": dimension_scores,
        "zatca_compliant": zatca_compliant,
        "weakest_dimension": weakest_dimension,
        "governance_decision": _GOV_REVIEW,
    }


# ---------------------------------------------------------------------------
# Router endpoints
# ---------------------------------------------------------------------------


@router.get("/dimensions", summary="All 5 data quality dimensions")
def get_dimensions() -> dict[str, Any]:
    """Return all DQ dimensions with weights and measurement methods."""
    total_weight = sum(d["weight"] for d in _DQ_DIMENSIONS)
    return {
        "dimensions": _DQ_DIMENSIONS,
        "total_weight": total_weight,
        "governance_decision": _GOV_REVIEW,
    }


@router.get("/zatca-requirements", summary="ZATCA Phase 2 data quality requirements")
def get_zatca_requirements() -> dict[str, Any]:
    """Return ZATCA Phase 2 minimum data quality thresholds."""
    return {
        "zatca_requirements": _ZATCA_DQ_REQUIREMENTS,
        "total_requirements": len(_ZATCA_DQ_REQUIREMENTS),
        "governance_decision": _GOV_REVIEW,
    }


@router.post("/assess", summary="Assess data quality across all five dimensions")
def assess_data_quality(body: DQAssessmentInput) -> dict[str, Any]:
    """Accept dimension scores and return a full DQ assessment.

    Governance decision: ALLOW_WITH_REVIEW.
    """
    return _assess_data_quality(body)
