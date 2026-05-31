"""Customer Lifecycle Management API.

Endpoints:
  GET  /api/v1/lifecycle/stages              — list all lifecycle stages with counts
  GET  /api/v1/lifecycle/at-risk             — clients at churn risk (health < 60)
  GET  /api/v1/lifecycle/cohort/{month}      — cohort analysis for YYYY-MM
  GET  /api/v1/lifecycle/{client_id}         — full lifecycle state for one client
  POST /api/v1/lifecycle/{client_id}/advance — advance client to next stage
  POST /api/v1/lifecycle/{client_id}/intervention — log a retention intervention

All endpoints:
  - Require admin auth (X-Admin-API-Key)
  - Return bilingual ar/en labels
  - governance_decision: ALLOW_WITH_REVIEW on all responses
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from fastapi import APIRouter, Body, Depends, HTTPException
from pydantic import BaseModel, ConfigDict, Field

from api.security.api_key import require_admin_key
from core.logging import get_logger

_log = get_logger(__name__)

router = APIRouter(
    prefix="/api/v1/lifecycle",
    tags=["customer-lifecycle"],
    dependencies=[Depends(require_admin_key)],
)

_GOV = "ALLOW_WITH_REVIEW"
_NOW = datetime.now(UTC)

# ---------------------------------------------------------------------------
# Lifecycle stage catalogue — ordered forward stages + terminal
# ---------------------------------------------------------------------------

STAGE_ORDER: list[str] = [
    "diagnostic",
    "sprint_active",
    "sprint_complete",
    "data_pack",
    "managed_ops",
    "custom_ai",
]

STAGE_META: dict[str, dict[str, Any]] = {
    "diagnostic": {
        "id": "diagnostic",
        "label_ar": "التشخيص المجاني",
        "label_en": "Free Diagnostic",
        "description_ar": "اكتمال التشخيص المجاني",
        "description_en": "Free diagnostic completed",
        "price_sar": 0,
        "position": 1,
    },
    "sprint_active": {
        "id": "sprint_active",
        "label_ar": "سبرينت نشط",
        "label_en": "499 SAR Sprint Active",
        "description_ar": "سبرينت 499 ريال جاري",
        "description_en": "499 SAR Sprint in progress",
        "price_sar": 499,
        "position": 2,
    },
    "sprint_complete": {
        "id": "sprint_complete",
        "label_ar": "سبرينت مكتمل",
        "label_en": "Sprint Complete",
        "description_ar": "تم تسليم السبرينت وحزمة الإثبات جاهزة",
        "description_en": "Sprint delivered, proof pack ready",
        "price_sar": 499,
        "position": 3,
    },
    "data_pack": {
        "id": "data_pack",
        "label_ar": "حزمة البيانات",
        "label_en": "1,500 SAR Data Pack",
        "description_ar": "حزمة البيانات 1500 ريال مفعّلة",
        "description_en": "1,500 SAR Data Pack engaged",
        "price_sar": 1500,
        "position": 4,
    },
    "managed_ops": {
        "id": "managed_ops",
        "label_ar": "العمليات المدارة",
        "label_en": "Managed Ops Active",
        "description_ar": "عمليات مدارة 2999-4999 ريال/شهر نشطة",
        "description_en": "2,999-4,999 SAR/mo Managed Ops active",
        "price_sar": 2999,
        "position": 5,
    },
    "custom_ai": {
        "id": "custom_ai",
        "label_ar": "ذكاء اصطناعي مخصص",
        "label_en": "Custom AI",
        "description_ar": "مشاركة ذكاء اصطناعي مخصص 5000-25000 ريال",
        "description_en": "5,000-25,000 SAR Custom AI engaged",
        "price_sar": 5000,
        "position": 6,
    },
    "churned": {
        "id": "churned",
        "label_ar": "مغادر",
        "label_en": "Churned",
        "description_ar": "العميل غادر",
        "description_en": "Client churned",
        "price_sar": 0,
        "position": 7,
    },
}

# ---------------------------------------------------------------------------
# Demo client store — 8 representative accounts
# ---------------------------------------------------------------------------

_CLIENTS: dict[str, dict[str, Any]] = {
    "CLT-001": {
        "client_id": "CLT-001",
        "name_ar": "شركة الأنظمة التقنية",
        "name_en": "TechSystems Co.",
        "stage": "managed_ops",
        "health_score": 82,
        "arr_sar": 47_988,
        "days_in_stage": 47,
        "sector": "technology",
        "city": "Riyadh",
        "interventions": [],
    },
    "CLT-002": {
        "client_id": "CLT-002",
        "name_ar": "مجموعة الخدمات الصحية",
        "name_en": "HealthCare Group",
        "stage": "sprint_active",
        "health_score": 55,
        "arr_sar": 5_988,
        "days_in_stage": 12,
        "sector": "healthcare",
        "city": "Jeddah",
        "interventions": [],
    },
    "CLT-003": {
        "client_id": "CLT-003",
        "name_ar": "شركة التطوير العقاري",
        "name_en": "Realty Dev Ltd",
        "stage": "data_pack",
        "health_score": 71,
        "arr_sar": 18_000,
        "days_in_stage": 23,
        "sector": "real_estate",
        "city": "Riyadh",
        "interventions": [],
    },
    "CLT-004": {
        "client_id": "CLT-004",
        "name_ar": "مؤسسة التعليم الرقمي",
        "name_en": "Digital Education Co.",
        "stage": "sprint_complete",
        "health_score": 68,
        "arr_sar": 5_988,
        "days_in_stage": 7,
        "sector": "education",
        "city": "Riyadh",
        "interventions": [],
    },
    "CLT-005": {
        "client_id": "CLT-005",
        "name_ar": "شركة الخدمات اللوجستية",
        "name_en": "LogiServices Inc.",
        "stage": "diagnostic",
        "health_score": 45,
        "arr_sar": 0,
        "days_in_stage": 3,
        "sector": "logistics",
        "city": "Dammam",
        "interventions": [],
    },
    "CLT-006": {
        "client_id": "CLT-006",
        "name_ar": "مجموعة التجزئة الرقمية",
        "name_en": "Digital Retail Group",
        "stage": "custom_ai",
        "health_score": 91,
        "arr_sar": 120_000,
        "days_in_stage": 91,
        "sector": "retail",
        "city": "Riyadh",
        "interventions": [],
    },
    "CLT-007": {
        "client_id": "CLT-007",
        "name_ar": "شركة الخدمات المالية",
        "name_en": "FinServ Arabia",
        "stage": "managed_ops",
        "health_score": 38,
        "arr_sar": 35_988,
        "days_in_stage": 180,
        "sector": "financial_services",
        "city": "Riyadh",
        "interventions": [],
    },
    "CLT-008": {
        "client_id": "CLT-008",
        "name_ar": "مكتب الاستشارات الإدارية",
        "name_en": "Management Consulting Office",
        "stage": "churned",
        "health_score": 22,
        "arr_sar": 0,
        "days_in_stage": 30,
        "sector": "professional_services",
        "city": "Jeddah",
        "interventions": [],
    },
}

# ---------------------------------------------------------------------------
# Pydantic models
# ---------------------------------------------------------------------------


class AdvanceStageBody(BaseModel):
    model_config = ConfigDict(extra="forbid")

    reason: str = Field(default="", max_length=500)
    override_stage: str | None = Field(
        default=None,
        description="Force a specific stage instead of advancing to the next one.",
    )


class InterventionBody(BaseModel):
    model_config = ConfigDict(extra="forbid")

    intervention_type: str = Field(
        min_length=1,
        max_length=100,
        description="Type: call / email / discount / sprint_review / executive_review",
    )
    notes: str = Field(default="", max_length=1000)
    owner: str = Field(default="founder", max_length=100)


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _client_or_404(client_id: str) -> dict[str, Any]:
    client = _CLIENTS.get(client_id.upper())
    if client is None:
        raise HTTPException(
            status_code=404,
            detail={
                "ar": f"العميل '{client_id}' غير موجود",
                "en": f"Client '{client_id}' not found",
                "valid_ids": list(_CLIENTS.keys()),
            },
        )
    return client


def _health_tier(score: int) -> dict[str, str]:
    if score >= 80:
        return {"tier": "champion", "ar": "بطل", "en": "Champion"}
    if score >= 60:
        return {"tier": "healthy", "ar": "بصحة جيدة", "en": "Healthy"}
    if score >= 40:
        return {"tier": "at_risk", "ar": "في خطر", "en": "At Risk"}
    return {"tier": "critical", "ar": "حرج", "en": "Critical"}


def _next_stage(current: str) -> str | None:
    """Return the next forward stage, or None if at terminal."""
    if current == "churned":
        return None
    try:
        idx = STAGE_ORDER.index(current)
    except ValueError:
        return None
    if idx + 1 >= len(STAGE_ORDER):
        return None
    return STAGE_ORDER[idx + 1]


def _stage_label(stage_id: str) -> dict[str, str]:
    meta = STAGE_META.get(stage_id, {})
    return {
        "ar": meta.get("label_ar", stage_id),
        "en": meta.get("label_en", stage_id),
    }


def _build_client_summary(c: dict[str, Any]) -> dict[str, Any]:
    return {
        "client_id": c["client_id"],
        "name": {"ar": c["name_ar"], "en": c["name_en"]},
        "stage": c["stage"],
        "stage_label": _stage_label(c["stage"]),
        "health_score": c["health_score"],
        "health_tier": _health_tier(c["health_score"]),
        "arr_sar": c["arr_sar"],
        "days_in_stage": c["days_in_stage"],
        "sector": c["sector"],
        "city": c["city"],
    }


# ---------------------------------------------------------------------------
# Endpoints — fixed paths first (before path params)
# ---------------------------------------------------------------------------


@router.get("/stages")
async def list_stages() -> dict[str, Any]:
    """List all lifecycle stages with client counts and aggregate metrics."""
    stage_counts: dict[str, int] = {s: 0 for s in STAGE_META}
    stage_arr: dict[str, float] = {s: 0.0 for s in STAGE_META}
    stage_health: dict[str, list[int]] = {s: [] for s in STAGE_META}

    for c in _CLIENTS.values():
        s = c["stage"]
        stage_counts[s] = stage_counts.get(s, 0) + 1
        stage_arr[s] = stage_arr.get(s, 0.0) + c["arr_sar"]
        stage_health.setdefault(s, []).append(c["health_score"])

    stages_out: list[dict[str, Any]] = []
    for stage_id, meta in STAGE_META.items():
        scores = stage_health.get(stage_id, [])
        avg_health = round(sum(scores) / len(scores), 1) if scores else None
        stages_out.append(
            {
                "id": stage_id,
                "label": {"ar": meta["label_ar"], "en": meta["label_en"]},
                "description": {
                    "ar": meta["description_ar"],
                    "en": meta["description_en"],
                },
                "position": meta["position"],
                "price_sar": meta["price_sar"],
                "client_count": stage_counts.get(stage_id, 0),
                "total_arr_sar": stage_arr.get(stage_id, 0.0),
                "avg_health_score": avg_health,
                "is_terminal": stage_id == "churned",
            }
        )

    total_arr = sum(c["arr_sar"] for c in _CLIENTS.values())
    return {
        "governance_decision": _GOV,
        "generated_at": _NOW.isoformat(),
        "total_clients": len(_CLIENTS),
        "total_arr_sar": total_arr,
        "stages": stages_out,
    }


@router.get("/at-risk")
async def list_at_risk_clients() -> dict[str, Any]:
    """Return clients with health score below 60 (churn risk)."""
    at_risk = [
        _build_client_summary(c)
        for c in _CLIENTS.values()
        if c["health_score"] < 60 and c["stage"] != "churned"
    ]
    at_risk.sort(key=lambda x: x["health_score"])

    return {
        "governance_decision": _GOV,
        "generated_at": _NOW.isoformat(),
        "at_risk_count": len(at_risk),
        "threshold_note": {
            "ar": "العملاء الذين تقل درجة صحتهم عن 60",
            "en": "Clients with health score below 60",
        },
        "clients": at_risk,
    }


@router.get("/cohort/{month}")
async def cohort_analysis(month: str) -> dict[str, Any]:
    """Cohort analysis for a given YYYY-MM month.

    Uses demo data bucketed into the requested month.
    """
    # Validate YYYY-MM format
    try:
        datetime.strptime(month, "%Y-%m")
    except ValueError:
        raise HTTPException(
            status_code=422,
            detail={
                "ar": "تنسيق الشهر غير صحيح — استخدم YYYY-MM",
                "en": "Invalid month format — use YYYY-MM",
            },
        )

    # Demo cohort: distribute clients deterministically across months
    # In production this would query a real cohort table.
    cohort_clients = [
        c for c in _CLIENTS.values() if c["stage"] != "churned"
    ]
    churned_clients = [c for c in _CLIENTS.values() if c["stage"] == "churned"]

    total = len(cohort_clients)
    active_arr = sum(c["arr_sar"] for c in cohort_clients)
    avg_health = (
        round(sum(c["health_score"] for c in cohort_clients) / total, 1)
        if total
        else 0
    )

    stage_distribution: dict[str, int] = {}
    for c in cohort_clients:
        stage_distribution[c["stage"]] = stage_distribution.get(c["stage"], 0) + 1

    return {
        "governance_decision": _GOV,
        "generated_at": _NOW.isoformat(),
        "cohort_month": month,
        "cohort_summary": {
            "active_clients": total,
            "churned_clients": len(churned_clients),
            "retention_rate_pct": round(total / (total + len(churned_clients)) * 100, 1)
            if (total + len(churned_clients)) > 0
            else 0,
            "active_arr_sar": active_arr,
            "avg_health_score": avg_health,
        },
        "stage_distribution": stage_distribution,
        "note": {
            "ar": "بيانات توضيحية — ستُستبدل بقراءات الكوهورت الفعلية من قاعدة البيانات",
            "en": "Demo data — will be replaced by real cohort reads from DB",
        },
    }


# ---------------------------------------------------------------------------
# Endpoints — path-param routes (must come after fixed-path routes)
# ---------------------------------------------------------------------------


@router.get("/{client_id}")
async def get_client_lifecycle(client_id: str) -> dict[str, Any]:
    """Full lifecycle state for a single client."""
    c = _client_or_404(client_id)
    next_s = _next_stage(c["stage"])
    return {
        "governance_decision": _GOV,
        "generated_at": _NOW.isoformat(),
        "client": _build_client_summary(c),
        "stage_detail": STAGE_META.get(c["stage"], {}),
        "next_stage": {
            "id": next_s,
            "label": _stage_label(next_s) if next_s else None,
            "meta": STAGE_META.get(next_s) if next_s else None,
        },
        "interventions": c.get("interventions", []),
    }


@router.post("/{client_id}/advance")
async def advance_client_stage(
    client_id: str,
    body: AdvanceStageBody = Body(...),
) -> dict[str, Any]:
    """Advance a client to the next lifecycle stage (or to a specified override stage)."""
    c = _client_or_404(client_id)
    current_stage = c["stage"]

    if body.override_stage:
        if body.override_stage not in STAGE_META:
            raise HTTPException(
                status_code=422,
                detail={
                    "ar": f"المرحلة '{body.override_stage}' غير موجودة",
                    "en": f"Stage '{body.override_stage}' is not a valid stage",
                    "valid_stages": list(STAGE_META.keys()),
                },
            )
        new_stage = body.override_stage
    else:
        new_stage = _next_stage(current_stage)
        if new_stage is None:
            raise HTTPException(
                status_code=409,
                detail={
                    "ar": "لا توجد مرحلة تالية — العميل في المرحلة النهائية أو مغادر",
                    "en": "No next stage — client is at the final stage or churned",
                    "current_stage": current_stage,
                },
            )

    _log.info(
        "client_stage_advanced",
        client_id=client_id,
        from_stage=current_stage,
        to_stage=new_stage,
        reason=body.reason,
    )

    # Mutate in-memory store (demo behaviour)
    c["stage"] = new_stage
    c["days_in_stage"] = 0

    return {
        "governance_decision": _GOV,
        "advanced_at": _NOW.isoformat(),
        "client_id": client_id,
        "from_stage": current_stage,
        "from_stage_label": _stage_label(current_stage),
        "to_stage": new_stage,
        "to_stage_label": _stage_label(new_stage),
        "reason": body.reason,
        "next_recommended_action": {
            "ar": STAGE_META.get(new_stage, {}).get("description_ar", ""),
            "en": STAGE_META.get(new_stage, {}).get("description_en", ""),
        },
    }


@router.post("/{client_id}/intervention")
async def log_intervention(
    client_id: str,
    body: InterventionBody = Body(...),
) -> dict[str, Any]:
    """Log a retention intervention for an at-risk client."""
    c = _client_or_404(client_id)

    entry: dict[str, Any] = {
        "logged_at": _NOW.isoformat(),
        "intervention_type": body.intervention_type,
        "notes": body.notes,
        "owner": body.owner,
        "health_score_at_log": c["health_score"],
    }
    c.setdefault("interventions", []).append(entry)

    _log.info(
        "intervention_logged",
        client_id=client_id,
        intervention_type=body.intervention_type,
        health_score=c["health_score"],
    )

    return {
        "governance_decision": _GOV,
        "logged_at": _NOW.isoformat(),
        "client_id": client_id,
        "client_name": {"ar": c["name_ar"], "en": c["name_en"]},
        "intervention": entry,
        "total_interventions": len(c["interventions"]),
        "note": {
            "ar": "تم تسجيل التدخل — راجع نقاط الصحة خلال 7 أيام لقياس الأثر",
            "en": "Intervention logged — review health score in 7 days to measure impact",
        },
    }
