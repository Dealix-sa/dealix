"""PDPL Readiness Assessment API — Saudi Personal Data Protection Law compliance scoring.

Endpoints:
  POST /api/v1/pdpl-readiness/assess      — score PDPL readiness (0-100)
  GET  /api/v1/pdpl-readiness/checklist   — full PDPL compliance checklist
  GET  /api/v1/pdpl-readiness/penalties   — PDPL penalty structure
  POST /api/v1/pdpl-readiness/data-map    — analyze a company's data categories

All endpoints:
  - Open (no admin auth — lead generation tool)
  - governance_decision: ALLOW_WITH_REVIEW
  - Bilingual ar/en
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any, Literal

from fastapi import APIRouter, Body
from pydantic import BaseModel, ConfigDict, Field

_NOW = datetime.now(UTC)

router = APIRouter(
    prefix="/api/v1/pdpl-readiness",
    tags=["pdpl-readiness"],
)

_GOV = "ALLOW_WITH_REVIEW"

_DISCLAIMER_AR = (
    "التقييم أداة توجيهية فقط — احصل على مراجعة رسمية من مستشار قانوني أو خبير حماية بيانات معتمد."
)
_DISCLAIMER_EN = (
    "Assessment is a guidance tool only — obtain formal review from a certified legal advisor or data protection expert."
)

# ---------------------------------------------------------------------------
# Checklist items — weights must sum to 100
# ---------------------------------------------------------------------------

CHECKLIST: list[dict[str, Any]] = [
    {
        "id": "CK-PDPL-001",
        "field": "has_privacy_policy",
        "category": "documentation",
        "title_ar": "سياسة الخصوصية منشورة ومحدّثة",
        "title_en": "Privacy policy published and up-to-date",
        "weight": 15,
        "critical": False,
    },
    {
        "id": "CK-PDPL-002",
        "field": "has_consent_mechanism",
        "category": "consent",
        "title_ar": "آلية موافقة صريحة للمستخدمين (PDPL المادة 5)",
        "title_en": "Explicit consent mechanism for users (PDPL Art. 5)",
        "weight": 20,
        "critical": True,
    },
    {
        "id": "CK-PDPL-003",
        "field": "has_data_retention_policy",
        "category": "documentation",
        "title_ar": "سياسة الاحتفاظ بالبيانات محددة",
        "title_en": "Data retention policy defined",
        "weight": 10,
        "critical": False,
    },
    {
        "id": "CK-PDPL-004",
        "field": "has_dsar_process",
        "category": "rights",
        "title_ar": "إجراء طلبات الوصول لموضوع البيانات (DSAR)",
        "title_en": "Data Subject Access Request (DSAR) process in place",
        "weight": 15,
        "critical": True,
    },
    {
        "id": "CK-PDPL-005",
        "field": "stores_data_saudi_servers",
        "category": "localization",
        "title_ar": "تخزين البيانات على خوادم داخل المملكة العربية السعودية",
        "title_en": "Data stored on servers within Saudi Arabia",
        "weight": 10,
        "critical": False,
    },
    {
        "id": "CK-PDPL-006",
        "field": "has_breach_response_plan",
        "category": "incident",
        "title_ar": "خطة الاستجابة لخروقات البيانات (PDPL المادة 21)",
        "title_en": "Data breach response plan (PDPL Art. 21)",
        "weight": 10,
        "critical": False,
    },
    {
        "id": "CK-PDPL-007",
        "field": "has_dpo_appointed",
        "category": "governance",
        "title_ar": "مسؤول حماية البيانات (DPO) معيّن",
        "title_en": "Data Protection Officer (DPO) appointed",
        "weight": 5,
        "critical": False,
    },
    {
        "id": "CK-PDPL-008",
        "field": "has_staff_training",
        "category": "governance",
        "title_ar": "الموظفون مدرّبون على متطلبات PDPL",
        "title_en": "Staff trained on PDPL requirements",
        "weight": 5,
        "critical": False,
    },
    {
        "id": "CK-PDPL-009",
        "field": "has_vendor_agreements",
        "category": "third_party",
        "title_ar": "اتفاقيات معالجة البيانات مع موردي الطرف الثالث",
        "title_en": "Data processing agreements with third-party vendors",
        "weight": 10,
        "critical": False,
    },
]

# Note: processes_sensitive_data has weight 0 — it is a risk flag only,
# not included in score calculation. It is appended below for reference but
# excluded from the weight-bearing checklist items above.

_SENSITIVE_DATA_ITEM: dict[str, Any] = {
    "id": "CK-PDPL-010",
    "field": "processes_sensitive_data",
    "category": "risk_flag",
    "title_ar": "معالجة بيانات حساسة (صحية، دينية، مالية، إلخ)",
    "title_en": "Processing sensitive data (health, religion, financial, etc.)",
    "weight": 0,
    "critical": False,
    "risk_flag": True,
    "note_ar": "يرفع مستوى المخاطر — لا يؤثر على النقاط",
    "note_en": "Raises risk level — does not affect score",
}

# ---------------------------------------------------------------------------
# Penalty structure (Saudi PDPL 2021)
# ---------------------------------------------------------------------------

PENALTIES: list[dict[str, Any]] = [
    {
        "id": "PEN-PDPL-001",
        "violation_ar": "معالجة بيانات شخصية بدون موافقة",
        "violation_en": "Processing personal data without consent",
        "penalty_sar": 1_000_000,
        "max_sar": 1_000_000,
        "criminal": False,
        "pdpl_article": "Art. 5",
    },
    {
        "id": "PEN-PDPL-002",
        "violation_ar": "انتهاكات سياسة الخصوصية",
        "violation_en": "Privacy policy violations",
        "penalty_sar": 1_000_000,
        "max_sar": 1_000_000,
        "criminal": False,
        "pdpl_article": "Art. 6",
    },
    {
        "id": "PEN-PDPL-003",
        "violation_ar": "بيع البيانات الشخصية",
        "violation_en": "Selling personal data",
        "penalty_sar": 3_000_000,
        "max_sar": 3_000_000,
        "criminal": True,
        "pdpl_article": "Art. 32",
    },
    {
        "id": "PEN-PDPL-004",
        "violation_ar": "نقل عابر للحدود بدون موافقة SDAIA",
        "violation_en": "Cross-border transfer without SDAIA approval",
        "penalty_sar": 5_000_000,
        "max_sar": 5_000_000,
        "criminal": False,
        "pdpl_article": "Art. 29",
    },
    {
        "id": "PEN-PDPL-005",
        "violation_ar": "انتهاكات البيانات الحساسة",
        "violation_en": "Sensitive data violations",
        "penalty_sar": 5_000_000,
        "max_sar": 5_000_000,
        "criminal": True,
        "pdpl_article": "Art. 23",
    },
]

# ---------------------------------------------------------------------------
# Data category classification
# ---------------------------------------------------------------------------

_DATA_CATEGORY_MAP: dict[str, dict[str, Any]] = {
    "email": {
        "pdpl_class": "personal",
        "pdpl_class_ar": "بيانات شخصية",
        "risk_level": "medium",
        "required_controls": [
            "consent_mechanism",
            "privacy_policy",
            "data_retention_policy",
            "dsar_process",
        ],
        "relevant_article": "Art. 5",
    },
    "phone": {
        "pdpl_class": "personal",
        "pdpl_class_ar": "بيانات شخصية",
        "risk_level": "medium",
        "required_controls": [
            "consent_mechanism",
            "privacy_policy",
            "data_retention_policy",
        ],
        "relevant_article": "Art. 5",
    },
    "name": {
        "pdpl_class": "personal",
        "pdpl_class_ar": "بيانات شخصية",
        "risk_level": "low",
        "required_controls": [
            "consent_mechanism",
            "privacy_policy",
        ],
        "relevant_article": "Art. 5",
    },
    "location": {
        "pdpl_class": "personal",
        "pdpl_class_ar": "بيانات شخصية",
        "risk_level": "high",
        "required_controls": [
            "consent_mechanism",
            "privacy_policy",
            "data_retention_policy",
            "dsar_process",
            "breach_response_plan",
        ],
        "relevant_article": "Art. 5",
    },
    "financial": {
        "pdpl_class": "sensitive",
        "pdpl_class_ar": "بيانات حساسة",
        "risk_level": "critical",
        "required_controls": [
            "consent_mechanism",
            "privacy_policy",
            "data_retention_policy",
            "dsar_process",
            "breach_response_plan",
            "vendor_agreements",
            "dpo_appointed",
        ],
        "relevant_article": "Art. 23",
    },
    "health": {
        "pdpl_class": "sensitive",
        "pdpl_class_ar": "بيانات صحية حساسة",
        "risk_level": "critical",
        "required_controls": [
            "consent_mechanism",
            "privacy_policy",
            "data_retention_policy",
            "dsar_process",
            "breach_response_plan",
            "vendor_agreements",
            "dpo_appointed",
            "staff_training",
        ],
        "relevant_article": "Art. 23",
    },
    "national_id": {
        "pdpl_class": "sensitive",
        "pdpl_class_ar": "بيانات هوية وطنية حساسة",
        "risk_level": "critical",
        "required_controls": [
            "consent_mechanism",
            "privacy_policy",
            "data_retention_policy",
            "dsar_process",
            "breach_response_plan",
            "stores_data_saudi_servers",
        ],
        "relevant_article": "Art. 23",
    },
    "religion": {
        "pdpl_class": "sensitive",
        "pdpl_class_ar": "بيانات دينية حساسة",
        "risk_level": "critical",
        "required_controls": [
            "consent_mechanism",
            "privacy_policy",
            "dpo_appointed",
        ],
        "relevant_article": "Art. 23",
    },
    "biometric": {
        "pdpl_class": "sensitive",
        "pdpl_class_ar": "بيانات قياسية حيوية حساسة",
        "risk_level": "critical",
        "required_controls": [
            "consent_mechanism",
            "privacy_policy",
            "data_retention_policy",
            "dsar_process",
            "breach_response_plan",
            "dpo_appointed",
            "stores_data_saudi_servers",
        ],
        "relevant_article": "Art. 23",
    },
    "behavioral": {
        "pdpl_class": "personal",
        "pdpl_class_ar": "بيانات سلوكية شخصية",
        "risk_level": "medium",
        "required_controls": [
            "consent_mechanism",
            "privacy_policy",
            "data_retention_policy",
        ],
        "relevant_article": "Art. 5",
    },
    "ip_address": {
        "pdpl_class": "personal",
        "pdpl_class_ar": "بيانات شخصية تقنية",
        "risk_level": "low",
        "required_controls": [
            "privacy_policy",
            "data_retention_policy",
        ],
        "relevant_article": "Art. 5",
    },
}

_UNKNOWN_CATEGORY: dict[str, Any] = {
    "pdpl_class": "unknown",
    "pdpl_class_ar": "غير محدد",
    "risk_level": "review_required",
    "required_controls": ["privacy_policy", "consent_mechanism"],
    "relevant_article": "Art. 5",
}

# ---------------------------------------------------------------------------
# Request/Response models
# ---------------------------------------------------------------------------


class PDPLAssessBody(BaseModel):
    model_config = ConfigDict(extra="forbid")

    company_name: str | None = Field(default=None, max_length=200)
    has_privacy_policy: bool = False
    has_consent_mechanism: bool = False
    has_data_retention_policy: bool = False
    has_dsar_process: bool = False
    stores_data_saudi_servers: bool = False
    has_breach_response_plan: bool = False
    processes_sensitive_data: bool = False
    has_dpo_appointed: bool = False
    has_staff_training: bool = False
    has_vendor_agreements: bool = False


class DataMapBody(BaseModel):
    model_config = ConfigDict(extra="forbid")

    company_name: str | None = Field(default=None, max_length=200)
    data_categories: list[str] = Field(
        default_factory=list,
        description="List of data category identifiers, e.g. email, phone, health, financial",
        max_length=50,
    )


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _score_assessment(body: PDPLAssessBody) -> dict[str, Any]:
    """Compute a 0-100 PDPL readiness score from assessment body answers."""
    field_values: dict[str, bool] = {
        "has_privacy_policy": body.has_privacy_policy,
        "has_consent_mechanism": body.has_consent_mechanism,
        "has_data_retention_policy": body.has_data_retention_policy,
        "has_dsar_process": body.has_dsar_process,
        "stores_data_saudi_servers": body.stores_data_saudi_servers,
        "has_breach_response_plan": body.has_breach_response_plan,
        "has_dpo_appointed": body.has_dpo_appointed,
        "has_staff_training": body.has_staff_training,
        "has_vendor_agreements": body.has_vendor_agreements,
    }

    total_weight = sum(item["weight"] for item in CHECKLIST)
    earned = sum(
        item["weight"]
        for item in CHECKLIST
        if field_values.get(item["field"], False)
    )
    score = round(earned / total_weight * 100) if total_weight > 0 else 0

    gaps = [
        {
            "id": item["id"],
            "field": item["field"],
            "title_ar": item["title_ar"],
            "title_en": item["title_en"],
            "critical": item["critical"],
            "weight": item["weight"],
        }
        for item in CHECKLIST
        if not field_values.get(item["field"], False)
    ]
    critical_gaps = [g for g in gaps if g["critical"]]

    sensitive_data_flag = body.processes_sensitive_data

    if score >= 80:
        tier: str = "compliant"
        tier_ar: str = "ممتثل"
        risk_level: str = "low"
    elif score >= 60:
        tier = "partial"
        tier_ar = "ممتثل جزئياً"
        risk_level = "medium"
    elif score >= 40:
        tier = "at_risk"
        tier_ar = "في خطر"
        risk_level = "high"
    else:
        tier = "critical"
        tier_ar = "حرج"
        risk_level = "critical"

    # Sensitive data flag elevates risk level by one step
    if sensitive_data_flag and risk_level == "low":
        risk_level = "medium"
    elif sensitive_data_flag and risk_level == "medium":
        risk_level = "high"

    return {
        "score": score,
        "tier": tier,
        "tier_ar": tier_ar,
        "risk_level": risk_level,
        "gaps": gaps,
        "critical_gaps": critical_gaps,
        "critical_gap_count": len(critical_gaps),
        "sensitive_data_flag": sensitive_data_flag,
        "earned_weight": earned,
        "total_weight": total_weight,
    }


def _classify_data_category(category: str) -> dict[str, Any]:
    """Return PDPL classification, risk level and required controls for a data category."""
    normalized = category.strip().lower().replace(" ", "_").replace("-", "_")
    info = _DATA_CATEGORY_MAP.get(normalized, _UNKNOWN_CATEGORY)
    return {
        "category": category,
        "pdpl_class": info["pdpl_class"],
        "pdpl_class_ar": info["pdpl_class_ar"],
        "risk_level": info["risk_level"],
        "required_controls": info["required_controls"],
        "relevant_article": info["relevant_article"],
    }


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------


@router.post("/assess")
async def assess_pdpl_readiness(body: PDPLAssessBody = Body(...)) -> dict[str, Any]:
    """Score a company's PDPL readiness (0-100)."""
    result = _score_assessment(body)

    if result["tier"] == "compliant":
        recommendation_ar = "الشركة ممتثلة بشكل جيد — استمر في المراجعة الدورية."
        recommendation_en = "Company is well-compliant — continue periodic review."
    elif result["critical_gap_count"] > 0:
        recommendation_ar = (
            f"تم تحديد {result['critical_gap_count']} ثغرات حرجة — "
            "يُعالجها Sprint Dealix خلال 7 أيام."
        )
        recommendation_en = (
            f"{result['critical_gap_count']} critical gaps identified — "
            "Dealix Sprint resolves them in 7 days."
        )
    else:
        recommendation_ar = "ثغرات غير حرجة — يمكن معالجتها خلال 30 يوماً."
        recommendation_en = "Non-critical gaps — can be addressed within 30 days."

    return {
        "governance_decision": _GOV,
        "generated_at": _NOW.isoformat(),
        "company": body.company_name,
        "readiness_score": result["score"],
        "readiness_tier": {"id": result["tier"], "ar": result["tier_ar"]},
        "risk_level": result["risk_level"],
        "sensitive_data_flag": result["sensitive_data_flag"],
        "critical_gaps": result["critical_gaps"],
        "all_gaps": result["gaps"],
        "recommendation": {"ar": recommendation_ar, "en": recommendation_en},
        "next_step": {
            "offer_ar": "Sprint الامتثال PDPL — 499 SAR / 7 أيام",
            "offer_en": "PDPL Compliance Sprint — 499 SAR / 7 days",
            "cta": "/dealix-diagnostic",
        },
        "disclaimer_ar": _DISCLAIMER_AR,
        "disclaimer_en": _DISCLAIMER_EN,
    }


@router.get("/checklist")
async def get_pdpl_checklist() -> dict[str, Any]:
    """Full PDPL compliance checklist with weights."""
    by_category: dict[str, list[dict[str, Any]]] = {}
    for item in CHECKLIST:
        cat = item["category"]
        if cat not in by_category:
            by_category[cat] = []
        by_category[cat].append(item)

    checklist_all = CHECKLIST + [_SENSITIVE_DATA_ITEM]

    return {
        "governance_decision": _GOV,
        "generated_at": _NOW.isoformat(),
        "total_items": len(checklist_all),
        "scored_items": len(CHECKLIST),
        "risk_flag_items": 1,
        "critical_items": sum(1 for i in CHECKLIST if i["critical"]),
        "total_weight": sum(i["weight"] for i in CHECKLIST),
        "checklist_by_category": by_category,
        "sensitive_data_item": _SENSITIVE_DATA_ITEM,
        "note_ar": "هذه القائمة تعكس متطلبات نظام حماية البيانات الشخصية السعودي (PDPL 2021).",
        "note_en": "This checklist reflects Saudi Personal Data Protection Law (PDPL 2021) requirements.",
        "disclaimer_ar": _DISCLAIMER_AR,
        "disclaimer_en": _DISCLAIMER_EN,
    }


@router.get("/penalties")
async def get_pdpl_penalties() -> dict[str, Any]:
    """PDPL penalty structure for non-compliance (Saudi PDPL 2021)."""
    max_single_penalty = max(p["max_sar"] for p in PENALTIES)
    return {
        "governance_decision": _GOV,
        "generated_at": _NOW.isoformat(),
        "total_penalty_items": len(PENALTIES),
        "max_single_penalty_sar": max_single_penalty,
        "penalties": PENALTIES,
        "note_ar": "الغرامات وفق نظام حماية البيانات الشخصية السعودي 2021. قابلة للتغيير.",
        "note_en": "Penalties per Saudi PDPL 2021. Subject to change.",
        "regulator_ar": "الهيئة السعودية للبيانات والذكاء الاصطناعي (SDAIA)",
        "regulator_en": "Saudi Data and AI Authority (SDAIA)",
        "disclaimer_ar": _DISCLAIMER_AR,
        "disclaimer_en": _DISCLAIMER_EN,
    }


@router.post("/data-map")
async def analyze_data_map(body: DataMapBody = Body(...)) -> dict[str, Any]:
    """Analyze a company's data categories for PDPL classification, risk level, and required controls."""
    classifications = [_classify_data_category(cat) for cat in body.data_categories]

    sensitive_count = sum(1 for c in classifications if c["pdpl_class"] == "sensitive")
    personal_count = sum(1 for c in classifications if c["pdpl_class"] == "personal")
    critical_count = sum(1 for c in classifications if c["risk_level"] == "critical")

    # Aggregate all unique required controls across categories
    all_controls: set[str] = set()
    for c in classifications:
        all_controls.update(c["required_controls"])

    overall_risk: str
    if critical_count > 0:
        overall_risk = "critical"
    elif sensitive_count > 0:
        overall_risk = "high"
    elif personal_count > 0:
        overall_risk = "medium"
    else:
        overall_risk = "low"

    return {
        "governance_decision": _GOV,
        "generated_at": _NOW.isoformat(),
        "company": body.company_name,
        "categories_analyzed": len(classifications),
        "sensitive_count": sensitive_count,
        "personal_count": personal_count,
        "unknown_count": sum(1 for c in classifications if c["pdpl_class"] == "unknown"),
        "critical_risk_count": critical_count,
        "overall_risk_level": overall_risk,
        "classifications": classifications,
        "aggregated_required_controls": sorted(all_controls),
        "disclaimer_ar": _DISCLAIMER_AR,
        "disclaimer_en": _DISCLAIMER_EN,
    }
