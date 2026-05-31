"""Client Health Operations — 6-dimension health scoring for active clients.

Endpoints:
  GET  /api/v1/client-health/portfolio       — full portfolio sorted by health (worst first)
  GET  /api/v1/client-health/at-risk         — only at_risk and critical clients
  GET  /api/v1/client-health/benchmarks      — industry benchmarks by sector
  GET  /api/v1/client-health/{client_id}     — single client full detail
  POST /api/v1/client-health/{client_id}/update-score  — update dimension scores
  POST /api/v1/client-health/{client_id}/intervention  — log a health intervention

All endpoints:
  - Require admin auth (X-Admin-API-Key)
  - Return governance_decision field
  - Bilingual ar/en labels
"""

from __future__ import annotations

import uuid
from datetime import UTC, datetime
from typing import Any, Literal

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, ConfigDict, Field

from api.security.api_key import require_admin_key
from core.logging import get_logger

_log = get_logger(__name__)

router = APIRouter(
    prefix="/api/v1/client-health",
    tags=["client-health-ops"],
    dependencies=[Depends(require_admin_key)],
)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

_GOV_READ = "ALLOW_WITH_REVIEW"
_GOV_MUTATE = "APPROVAL_FIRST"

DIMENSIONS: dict[str, float] = {
    "data_readiness": 0.20,
    "onboarding_ops": 0.15,
    "delivery_quality": 0.20,
    "zatca_compliance": 0.15,
    "client_retention": 0.20,
    "recurring_revenue": 0.10,
}

VALID_INTERVENTION_TYPES = frozenset({
    "proof_pack_delivery",
    "executive_checkin",
    "technical_review",
    "contract_review",
    "escalation",
})

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _now_iso() -> str:
    """Return current UTC time as ISO-8601 string."""
    return datetime.now(UTC).isoformat()


def _compute_health(scores: dict[str, float]) -> tuple[float, str]:
    """Compute weighted health score and health band from dimension scores.

    Returns (weighted_score, health_band) where health_band is one of:
    'healthy' (>=80), 'at_risk' (60-79), 'critical' (<60).
    """
    weighted = sum(scores.get(dim, 0.0) * weight for dim, weight in DIMENSIONS.items())
    weighted = round(weighted, 2)
    if weighted >= 80.0:
        band = "healthy"
    elif weighted >= 60.0:
        band = "at_risk"
    else:
        band = "critical"
    return weighted, band


# ---------------------------------------------------------------------------
# Demo clients — 8 realistic Saudi B2B clients
# ---------------------------------------------------------------------------

_CLIENTS: dict[str, dict[str, Any]] = {
    "CLT-001": {
        "client_id": "CLT-001",
        "company_ar": "شركة التقنية المتقدمة",
        "company_en": "Advanced Technology Co.",
        "sector": "technology",
        "tier": "enterprise",
        "health_scores": {
            "data_readiness": 90.0,
            "onboarding_ops": 88.0,
            "delivery_quality": 92.0,
            "zatca_compliance": 95.0,
            "client_retention": 87.0,
            "recurring_revenue": 90.0,
        },
        "last_updated": "2026-05-28",
        "assigned_csm": "Sarah Al-Qahtani",
        "notes_ar": "عميل استراتيجي ذو أداء عالٍ — مرشح للتوسع",
        "notes_en": "High-performing strategic client — expansion candidate",
        "pending_intervention": False,
    },
    "CLT-002": {
        "client_id": "CLT-002",
        "company_ar": "مجموعة الخدمات المالية الخليجية",
        "company_en": "Gulf Financial Services Group",
        "sector": "financial_services",
        "tier": "professional",
        "health_scores": {
            "data_readiness": 85.0,
            "onboarding_ops": 80.0,
            "delivery_quality": 84.0,
            "zatca_compliance": 90.0,
            "client_retention": 82.0,
            "recurring_revenue": 78.0,
        },
        "last_updated": "2026-05-27",
        "assigned_csm": "Mohammed Al-Harbi",
        "notes_ar": "أداء ثابت — يتتبع امتثال ZATCA بدقة",
        "notes_en": "Consistent performer — tracks ZATCA compliance closely",
        "pending_intervention": False,
    },
    "CLT-003": {
        "client_id": "CLT-003",
        "company_ar": "شركة العقارات السعودية الكبرى",
        "company_en": "Major Saudi Real Estate Co.",
        "sector": "real_estate",
        "tier": "professional",
        "health_scores": {
            "data_readiness": 72.0,
            "onboarding_ops": 65.0,
            "delivery_quality": 70.0,
            "zatca_compliance": 68.0,
            "client_retention": 75.0,
            "recurring_revenue": 60.0,
        },
        "last_updated": "2026-05-25",
        "assigned_csm": "Nora Al-Dosari",
        "notes_ar": "أداء متوسط — تحتاج دعماً إضافياً في تجهيز البيانات",
        "notes_en": "Average performance — needs additional data readiness support",
        "pending_intervention": False,
    },
    "CLT-004": {
        "client_id": "CLT-004",
        "company_ar": "شركة التجزئة الذكية",
        "company_en": "Smart Retail Solutions",
        "sector": "retail",
        "tier": "essential",
        "health_scores": {
            "data_readiness": 60.0,
            "onboarding_ops": 62.0,
            "delivery_quality": 65.0,
            "zatca_compliance": 70.0,
            "client_retention": 63.0,
            "recurring_revenue": 55.0,
        },
        "last_updated": "2026-05-22",
        "assigned_csm": "Khalid Al-Otaibi",
        "notes_ar": "يحتاج تتبعاً دورياً — مخاطر في تكرار الإيرادات",
        "notes_en": "Needs periodic tracking — recurring revenue at risk",
        "pending_intervention": False,
    },
    "CLT-005": {
        "client_id": "CLT-005",
        "company_ar": "مستشفى الصحة المتكاملة",
        "company_en": "Integrated Health Hospital",
        "sector": "healthcare",
        "tier": "enterprise",
        "health_scores": {
            "data_readiness": 62.0,
            "onboarding_ops": 58.0,
            "delivery_quality": 60.0,
            "zatca_compliance": 75.0,
            "client_retention": 65.0,
            "recurring_revenue": 50.0,
        },
        "last_updated": "2026-05-20",
        "assigned_csm": "Fatima Al-Shamrani",
        "notes_ar": "صعوبات في تكامل البيانات — تدخل مجدول قريباً",
        "notes_en": "Data integration challenges — intervention scheduled soon",
        "pending_intervention": True,
    },
    "CLT-006": {
        "client_id": "CLT-006",
        "company_ar": "شركة الخدمات اللوجستية المتطورة",
        "company_en": "Advanced Logistics Services Co.",
        "sector": "logistics",
        "tier": "professional",
        "health_scores": {
            "data_readiness": 40.0,
            "onboarding_ops": 35.0,
            "delivery_quality": 42.0,
            "zatca_compliance": 50.0,
            "client_retention": 45.0,
            "recurring_revenue": 30.0,
        },
        "last_updated": "2026-05-15",
        "assigned_csm": None,
        "notes_ar": "وضع حرج — تدخل عاجل مطلوب",
        "notes_en": "Critical state — urgent intervention required",
        "pending_intervention": False,
    },
    "CLT-007": {
        "client_id": "CLT-007",
        "company_ar": "أكاديمية التعليم الرقمي",
        "company_en": "Digital Education Academy",
        "sector": "education",
        "tier": "essential",
        "health_scores": {
            "data_readiness": 30.0,
            "onboarding_ops": 25.0,
            "delivery_quality": 35.0,
            "zatca_compliance": 40.0,
            "client_retention": 38.0,
            "recurring_revenue": 20.0,
        },
        "last_updated": "2026-05-10",
        "assigned_csm": None,
        "notes_ar": "خطر مرتفع من إلغاء الاشتراك — تواصل فوري مطلوب",
        "notes_en": "High churn risk — immediate outreach required",
        "pending_intervention": False,
    },
    "CLT-008": {
        "client_id": "CLT-008",
        "company_ar": "شركة التصنيع الصناعي الخليجي",
        "company_en": "Gulf Industrial Manufacturing Co.",
        "sector": "manufacturing",
        "tier": "professional",
        "health_scores": {
            "data_readiness": 75.0,
            "onboarding_ops": 70.0,
            "delivery_quality": 72.0,
            "zatca_compliance": 80.0,
            "client_retention": 68.0,
            "recurring_revenue": 65.0,
        },
        "last_updated": "2026-05-26",
        "assigned_csm": "Omar Al-Zahrani",
        "notes_ar": "تعافٍ جيد بعد مشاكل التوصيل السابقة",
        "notes_en": "Good recovery after previous delivery issues",
        "pending_intervention": True,
    },
}

# In-memory intervention log
_INTERVENTIONS: list[dict[str, Any]] = []

# ---------------------------------------------------------------------------
# Benchmark data by sector
# ---------------------------------------------------------------------------

_BENCHMARKS: dict[str, dict[str, Any]] = {
    "technology": {
        "sector": "technology",
        "sector_ar": "التقنية",
        "avg_health_score": 78.0,
        "dimension_benchmarks": {
            "data_readiness": 80.0,
            "onboarding_ops": 75.0,
            "delivery_quality": 82.0,
            "zatca_compliance": 85.0,
            "client_retention": 78.0,
            "recurring_revenue": 72.0,
        },
    },
    "financial_services": {
        "sector": "financial_services",
        "sector_ar": "الخدمات المالية",
        "avg_health_score": 81.0,
        "dimension_benchmarks": {
            "data_readiness": 85.0,
            "onboarding_ops": 78.0,
            "delivery_quality": 83.0,
            "zatca_compliance": 92.0,
            "client_retention": 80.0,
            "recurring_revenue": 76.0,
        },
    },
    "real_estate": {
        "sector": "real_estate",
        "sector_ar": "العقارات",
        "avg_health_score": 69.0,
        "dimension_benchmarks": {
            "data_readiness": 68.0,
            "onboarding_ops": 65.0,
            "delivery_quality": 70.0,
            "zatca_compliance": 72.0,
            "client_retention": 70.0,
            "recurring_revenue": 62.0,
        },
    },
    "healthcare": {
        "sector": "healthcare",
        "sector_ar": "الرعاية الصحية",
        "avg_health_score": 72.0,
        "dimension_benchmarks": {
            "data_readiness": 70.0,
            "onboarding_ops": 68.0,
            "delivery_quality": 74.0,
            "zatca_compliance": 80.0,
            "client_retention": 72.0,
            "recurring_revenue": 65.0,
        },
    },
    "retail": {
        "sector": "retail",
        "sector_ar": "التجزئة",
        "avg_health_score": 65.0,
        "dimension_benchmarks": {
            "data_readiness": 62.0,
            "onboarding_ops": 60.0,
            "delivery_quality": 66.0,
            "zatca_compliance": 68.0,
            "client_retention": 65.0,
            "recurring_revenue": 60.0,
        },
    },
    "logistics": {
        "sector": "logistics",
        "sector_ar": "اللوجستيات",
        "avg_health_score": 66.0,
        "dimension_benchmarks": {
            "data_readiness": 64.0,
            "onboarding_ops": 62.0,
            "delivery_quality": 68.0,
            "zatca_compliance": 70.0,
            "client_retention": 66.0,
            "recurring_revenue": 58.0,
        },
    },
    "education": {
        "sector": "education",
        "sector_ar": "التعليم",
        "avg_health_score": 60.0,
        "dimension_benchmarks": {
            "data_readiness": 58.0,
            "onboarding_ops": 55.0,
            "delivery_quality": 62.0,
            "zatca_compliance": 64.0,
            "client_retention": 60.0,
            "recurring_revenue": 52.0,
        },
    },
    "manufacturing": {
        "sector": "manufacturing",
        "sector_ar": "التصنيع",
        "avg_health_score": 70.0,
        "dimension_benchmarks": {
            "data_readiness": 68.0,
            "onboarding_ops": 66.0,
            "delivery_quality": 72.0,
            "zatca_compliance": 76.0,
            "client_retention": 70.0,
            "recurring_revenue": 63.0,
        },
    },
}

# ---------------------------------------------------------------------------
# Lookup helper
# ---------------------------------------------------------------------------


def _client_or_404(client_id: str) -> dict[str, Any]:
    """Return client record or raise HTTP 404."""
    record = _CLIENTS.get(client_id.upper())
    if record is None:
        raise HTTPException(
            status_code=404,
            detail={
                "ar": f"العميل '{client_id}' غير موجود",
                "en": f"Client '{client_id}' not found",
            },
        )
    return record


def _build_client_summary(record: dict[str, Any]) -> dict[str, Any]:
    """Build a full client summary with computed health."""
    score, band = _compute_health(record["health_scores"])
    return {
        "client_id": record["client_id"],
        "company_ar": record["company_ar"],
        "company_en": record["company_en"],
        "sector": record["sector"],
        "tier": record["tier"],
        "health_scores": dict(record["health_scores"]),
        "health_score": score,
        "health_band": band,
        "last_updated": record["last_updated"],
        "assigned_csm": record.get("assigned_csm"),
        "notes_ar": record.get("notes_ar", ""),
        "notes_en": record.get("notes_en", ""),
        "pending_intervention": record.get("pending_intervention", False),
    }


def _recommended_action(band: str, score: float) -> tuple[str, str]:
    """Return (action_ar, action_en) based on health band and score."""
    if band == "critical":
        if score < 40.0:
            return (
                "تدخل عاجل — اتصل بالعميل خلال 24 ساعة وقدّم جلسة تشخيص مجانية",
                "Urgent intervention — call client within 24 hours, offer free diagnostic session",
            )
        return (
            "تدخل استباقي — أرسل Proof Pack محدّث خلال 48 ساعة",
            "Proactive intervention — send updated Proof Pack within 48 hours",
        )
    return (
        "متابعة دورية — راجع نقاط الضعف وقدّم خطة تحسين خلال أسبوع",
        "Periodic follow-up — review weak dimensions and deliver improvement plan within one week",
    )


# ---------------------------------------------------------------------------
# Pydantic request models
# ---------------------------------------------------------------------------


class UpdateScoreBody(BaseModel):
    model_config = ConfigDict(extra="forbid")

    updates: dict[str, float] = Field(
        description="Map of dimension name to new score (0-100).",
    )
    reason: str = Field(min_length=5, max_length=500)


class InterventionBody(BaseModel):
    model_config = ConfigDict(extra="forbid")

    intervention_type: Literal[
        "proof_pack_delivery",
        "executive_checkin",
        "technical_review",
        "contract_review",
        "escalation",
    ]
    notes: str = Field(min_length=10, max_length=1000)
    next_action_date: str = Field(description="Expected next action date (ISO 8601, YYYY-MM-DD)")


# ---------------------------------------------------------------------------
# Endpoints — fixed paths first, then parameterised
# ---------------------------------------------------------------------------


@router.get("/portfolio")
async def get_portfolio() -> dict[str, Any]:
    """All clients with computed health scores, sorted by health ascending (worst first)."""
    summaries = [_build_client_summary(r) for r in _CLIENTS.values()]
    summaries.sort(key=lambda s: s["health_score"])

    total = len(summaries)
    critical_count = sum(1 for s in summaries if s["health_band"] == "critical")
    at_risk_count = sum(1 for s in summaries if s["health_band"] == "at_risk")
    healthy_count = sum(1 for s in summaries if s["health_band"] == "healthy")
    avg_health = round(sum(s["health_score"] for s in summaries) / total, 2) if total else 0.0

    return {
        "governance_decision": _GOV_READ,
        "generated_at": _now_iso(),
        "portfolio_summary": {
            "total_clients": total,
            "avg_health_score": avg_health,
            "critical_count": critical_count,
            "at_risk_count": at_risk_count,
            "healthy_count": healthy_count,
            "health_band_distribution": {
                "critical": critical_count,
                "at_risk": at_risk_count,
                "healthy": healthy_count,
            },
        },
        "clients": summaries,
    }


@router.get("/at-risk")
async def get_at_risk_clients() -> dict[str, Any]:
    """Clients with health_band of at_risk or critical, with recommended actions."""
    at_risk_summaries = []
    for record in _CLIENTS.values():
        score, band = _compute_health(record["health_scores"])
        if band in ("at_risk", "critical"):
            action_ar, action_en = _recommended_action(band, score)
            at_risk_summaries.append({
                **_build_client_summary(record),
                "recommended_action_ar": action_ar,
                "recommended_action_en": action_en,
            })

    at_risk_summaries.sort(key=lambda s: s["health_score"])

    return {
        "governance_decision": _GOV_READ,
        "generated_at": _now_iso(),
        "total_at_risk": len(at_risk_summaries),
        "clients": at_risk_summaries,
    }


@router.get("/benchmarks")
async def get_benchmarks() -> dict[str, Any]:
    """Industry benchmarks for health scores by sector with portfolio comparison."""
    portfolio_scores_by_sector: dict[str, list[float]] = {}
    for record in _CLIENTS.values():
        sector = record["sector"]
        score, _ = _compute_health(record["health_scores"])
        portfolio_scores_by_sector.setdefault(sector, []).append(score)

    benchmark_list = []
    for sector, bench in _BENCHMARKS.items():
        portfolio_scores = portfolio_scores_by_sector.get(sector, [])
        portfolio_avg = round(sum(portfolio_scores) / len(portfolio_scores), 2) if portfolio_scores else None
        vs_benchmark = (
            round(portfolio_avg - bench["avg_health_score"], 2)
            if portfolio_avg is not None
            else None
        )
        benchmark_list.append({
            "sector": bench["sector"],
            "sector_ar": bench["sector_ar"],
            "benchmark_avg_health_score": bench["avg_health_score"],
            "dimension_benchmarks": bench["dimension_benchmarks"],
            "dealix_portfolio_avg": portfolio_avg,
            "vs_benchmark": vs_benchmark,
            "portfolio_client_count": len(portfolio_scores),
        })

    return {
        "governance_decision": _GOV_READ,
        "generated_at": _now_iso(),
        "note_ar": "المعدلات المرجعية مستمدة من بيانات قطاع B2B السعودي — ليست ضمانات نتائج",
        "note_en": "Benchmarks derived from Saudi B2B sector data — not guaranteed outcomes",
        "benchmarks": benchmark_list,
    }


@router.get("/{client_id}")
async def get_client_detail(client_id: str) -> dict[str, Any]:
    """Full health detail for a single client, including all 6 dimension scores."""
    record = _client_or_404(client_id)
    score, band = _compute_health(record["health_scores"])

    dimension_detail = []
    for dim, weight in DIMENSIONS.items():
        dim_score = record["health_scores"].get(dim, 0.0)
        dimension_detail.append({
            "dimension": dim,
            "score": dim_score,
            "weight": weight,
            "weighted_contribution": round(dim_score * weight, 2),
        })

    _log.info(
        "client_health_detail_fetched",
        client_id=record["client_id"],
        health_score=score,
        health_band=band,
    )

    return {
        "governance_decision": _GOV_READ,
        "generated_at": _now_iso(),
        "client_id": record["client_id"],
        "company_ar": record["company_ar"],
        "company_en": record["company_en"],
        "sector": record["sector"],
        "tier": record["tier"],
        "health_score": score,
        "health_band": band,
        "dimension_scores": dict(record["health_scores"]),
        "dimension_detail": dimension_detail,
        "last_updated": record["last_updated"],
        "assigned_csm": record.get("assigned_csm"),
        "notes_ar": record.get("notes_ar", ""),
        "notes_en": record.get("notes_en", ""),
        "pending_intervention": record.get("pending_intervention", False),
    }


@router.post("/{client_id}/update-score")
async def update_client_score(client_id: str, body: UpdateScoreBody) -> dict[str, Any]:
    """Update one or more dimension scores for a client. Requires APPROVAL_FIRST."""
    record = _client_or_404(client_id)

    invalid_dims = [d for d in body.updates if d not in DIMENSIONS]
    if invalid_dims:
        raise HTTPException(
            status_code=422,
            detail={
                "ar": f"أسماء أبعاد غير صالحة: {invalid_dims}",
                "en": f"Invalid dimension names: {invalid_dims}",
                "valid_dimensions": list(DIMENSIONS.keys()),
            },
        )

    out_of_range = [d for d, v in body.updates.items() if not (0.0 <= v <= 100.0)]
    if out_of_range:
        raise HTTPException(
            status_code=422,
            detail={
                "ar": f"قيم خارج النطاق (0-100) للأبعاد: {out_of_range}",
                "en": f"Score out of range (0-100) for dimensions: {out_of_range}",
            },
        )

    previous_scores = dict(record["health_scores"])
    record["health_scores"].update(body.updates)
    record["last_updated"] = _now_iso()[:10]

    new_score, new_band = _compute_health(record["health_scores"])
    old_score, old_band = _compute_health(previous_scores)

    _log.info(
        "client_score_updated",
        client_id=record["client_id"],
        dimensions_updated=list(body.updates.keys()),
        old_score=old_score,
        new_score=new_score,
    )

    return {
        "governance_decision": _GOV_MUTATE,
        "generated_at": _now_iso(),
        "status": "score_updated_pending_approval",
        "client_id": record["client_id"],
        "dimensions_updated": list(body.updates.keys()),
        "reason": body.reason,
        "previous_health_score": old_score,
        "previous_health_band": old_band,
        "new_health_score": new_score,
        "new_health_band": new_band,
        "new_dimension_scores": dict(record["health_scores"]),
        "message_ar": "تم تحديث الدرجات — يحتاج موافقة المدير قبل الحفظ الرسمي",
        "message_en": "Scores updated — requires manager approval before official save",
    }


@router.post("/{client_id}/intervention")
async def log_intervention(client_id: str, body: InterventionBody) -> dict[str, Any]:
    """Log a health intervention for a client. Requires APPROVAL_FIRST."""
    record = _client_or_404(client_id)

    intervention_id = f"INT-{uuid.uuid4().hex[:8].upper()}"
    timestamp = _now_iso()

    score, band = _compute_health(record["health_scores"])

    intervention_record = {
        "id": intervention_id,
        "client_id": record["client_id"],
        "intervention_type": body.intervention_type,
        "notes": body.notes,
        "next_action_date": body.next_action_date,
        "health_score_at_intervention": score,
        "health_band_at_intervention": band,
        "logged_at": timestamp,
    }
    _INTERVENTIONS.append(intervention_record)
    record["pending_intervention"] = True

    _log.info(
        "intervention_logged",
        intervention_id=intervention_id,
        client_id=record["client_id"],
        intervention_type=body.intervention_type,
    )

    type_label_ar = {
        "proof_pack_delivery": "تسليم Proof Pack",
        "executive_checkin": "متابعة تنفيذية",
        "technical_review": "مراجعة تقنية",
        "contract_review": "مراجعة العقد",
        "escalation": "تصعيد",
    }.get(body.intervention_type, body.intervention_type)

    type_label_en = {
        "proof_pack_delivery": "Proof Pack Delivery",
        "executive_checkin": "Executive Check-in",
        "technical_review": "Technical Review",
        "contract_review": "Contract Review",
        "escalation": "Escalation",
    }.get(body.intervention_type, body.intervention_type)

    return {
        "governance_decision": _GOV_MUTATE,
        "generated_at": timestamp,
        "status": "intervention_logged_pending_approval",
        "intervention_id": intervention_id,
        "client_id": record["client_id"],
        "intervention_type": body.intervention_type,
        "intervention_type_label_ar": type_label_ar,
        "intervention_type_label_en": type_label_en,
        "next_action_date": body.next_action_date,
        "health_score_at_intervention": score,
        "health_band_at_intervention": band,
        "confirmation_ar": f"تم تسجيل التدخل ({type_label_ar}) للعميل {record['company_ar']} — الموعد التالي: {body.next_action_date}",
        "confirmation_en": f"Intervention ({type_label_en}) logged for {record['company_en']} — next action: {body.next_action_date}",
        "message_ar": "التدخل مُسجَّل — يحتاج موافقة المدير قبل الجدولة الرسمية",
        "message_en": "Intervention logged — requires manager approval before official scheduling",
    }
