"""Retainer Operations API — lifecycle management for monthly recurring clients.

Endpoints:
  GET  /api/v1/retainer/active           — all active retainers with health + MRR
  GET  /api/v1/retainer/{client_id}      — full retainer state for one client
  POST /api/v1/retainer/{client_id}/renew — process monthly renewal event
  POST /api/v1/retainer/{client_id}/upgrade — upgrade tier (2999→3999→4999 SAR)
  POST /api/v1/retainer/{client_id}/pause — pause retainer (30-day grace)
  GET  /api/v1/retainer/renewal-calendar  — upcoming renewals in the next 30 days
  GET  /api/v1/retainer/at-risk           — retainers at churn risk
  POST /api/v1/retainer/{client_id}/proof-update — queue new proof pack update
  GET  /api/v1/retainer/mrr-breakdown    — MRR by tier and cohort

All endpoints:
  - Require admin auth (X-Admin-API-Key)
  - governance_decision: ALLOW_WITH_REVIEW
  - Bilingual ar/en labels
"""

from __future__ import annotations

from datetime import UTC, date, datetime, timedelta
from typing import Any, Literal

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, ConfigDict, Field

from api.security.api_key import require_admin_key
from core.logging import get_logger

_log = get_logger(__name__)

router = APIRouter(
    prefix="/api/v1/retainer",
    tags=["retainer-ops"],
    dependencies=[Depends(require_admin_key)],
)

_GOV = "ALLOW_WITH_REVIEW"
_NOW = datetime.now(UTC)
_TODAY = _NOW.date()

# ---------------------------------------------------------------------------
# Type aliases
# ---------------------------------------------------------------------------

RetainerTier = Literal["essential", "professional", "enterprise"]
RetainerStatus = Literal["active", "paused", "at_risk", "churned", "pending"]

TIER_PRICE: dict[RetainerTier, int] = {
    "essential": 2_999,
    "professional": 3_999,
    "enterprise": 4_999,
}

TIER_LABELS: dict[RetainerTier, dict[str, str]] = {
    "essential": {"ar": "الأساسي", "en": "Essential"},
    "professional": {"ar": "الاحترافي", "en": "Professional"},
    "enterprise": {"ar": "المؤسسي", "en": "Enterprise"},
}

# ---------------------------------------------------------------------------
# Demo data — 8 realistic Saudi B2B retainer clients
# ---------------------------------------------------------------------------

_RETAINERS: dict[str, dict[str, Any]] = {
    "RTN-001": {
        "client_id": "RTN-001",
        "company_name_ar": "شركة الأفق للتقنية",
        "company_name_en": "Horizon Technology Co.",
        "sector": "technology",
        "city": "Riyadh",
        "tier": "professional",
        "status": "active",
        "health_score": 78,
        "sprint_completed": True,
        "retainer_start": "2026-02-01",
        "next_renewal": "2026-06-01",
        "months_active": 4,
        "open_alerts": 1,
        "last_proof_update": "2026-05-15",
        "arr_sar": 3_999 * 12,
        "notes_ar": "عميل منتظم، يطلب تحديث Proof Pack شهرياً",
        "notes_en": "Regular client, requests monthly Proof Pack updates",
    },
    "RTN-002": {
        "client_id": "RTN-002",
        "company_name_ar": "مجموعة الريادة للاستشارات",
        "company_name_en": "Riyadah Consulting Group",
        "sector": "professional_services",
        "city": "Jeddah",
        "tier": "essential",
        "status": "active",
        "health_score": 65,
        "sprint_completed": True,
        "retainer_start": "2026-03-15",
        "next_renewal": "2026-06-15",
        "months_active": 2,
        "open_alerts": 0,
        "last_proof_update": "2026-05-10",
        "arr_sar": 2_999 * 12,
        "notes_ar": "أحضر 2 عملاء جدد من خلال الإحالة",
        "notes_en": "Referred 2 new clients",
    },
    "RTN-003": {
        "client_id": "RTN-003",
        "company_name_ar": "شركة النخبة الطبية",
        "company_name_en": "Elite Medical Co.",
        "sector": "healthcare",
        "city": "Riyadh",
        "tier": "enterprise",
        "status": "at_risk",
        "health_score": 42,
        "sprint_completed": True,
        "retainer_start": "2026-01-01",
        "next_renewal": "2026-06-01",
        "months_active": 5,
        "open_alerts": 3,
        "last_proof_update": "2026-04-30",
        "arr_sar": 4_999 * 12,
        "notes_ar": "صعوبات في تسليم البيانات — تحتاج تدخل فوري",
        "notes_en": "Data delivery challenges — needs immediate intervention",
    },
    "RTN-004": {
        "client_id": "RTN-004",
        "company_name_ar": "التوسع العقاري السعودي",
        "company_name_en": "Saudi Real Estate Expansion",
        "sector": "real_estate",
        "city": "Dammam",
        "tier": "professional",
        "status": "active",
        "health_score": 82,
        "sprint_completed": True,
        "retainer_start": "2026-02-15",
        "next_renewal": "2026-06-15",
        "months_active": 3,
        "open_alerts": 0,
        "last_proof_update": "2026-05-20",
        "arr_sar": 3_999 * 12,
        "notes_ar": "عميل راضٍ، مرشح للترقية لـ Custom AI",
        "notes_en": "Satisfied client, candidate for Custom AI upgrade",
    },
    "RTN-005": {
        "client_id": "RTN-005",
        "company_name_ar": "أكاديمية المستقبل للتعليم",
        "company_name_en": "Future Academy",
        "sector": "education",
        "city": "Riyadh",
        "tier": "essential",
        "status": "paused",
        "health_score": 55,
        "sprint_completed": True,
        "retainer_start": "2026-01-15",
        "next_renewal": "2026-06-15",
        "months_active": 4,
        "open_alerts": 1,
        "last_proof_update": "2026-04-15",
        "arr_sar": 2_999 * 12,
        "notes_ar": "طلب توقف مؤقت لشهر رمضان — سيعود يونيو",
        "notes_en": "Requested pause for Ramadan month — returning June",
    },
    "RTN-006": {
        "client_id": "RTN-006",
        "company_name_ar": "سلسلة المتاجر الذكية",
        "company_name_en": "Smart Retail Chain",
        "sector": "retail",
        "city": "Jeddah",
        "tier": "professional",
        "status": "active",
        "health_score": 71,
        "sprint_completed": True,
        "retainer_start": "2026-03-01",
        "next_renewal": "2026-06-01",
        "months_active": 3,
        "open_alerts": 0,
        "last_proof_update": "2026-05-01",
        "arr_sar": 3_999 * 12,
        "notes_ar": "يعتزم توسيع النطاق إلى 3 فروع إضافية",
        "notes_en": "Plans to expand to 3 additional branches",
    },
    "RTN-007": {
        "client_id": "RTN-007",
        "company_name_ar": "خدمات اللوجستيات المتقدمة",
        "company_name_en": "Advanced Logistics Services",
        "sector": "logistics",
        "city": "Riyadh",
        "tier": "essential",
        "status": "active",
        "health_score": 68,
        "sprint_completed": True,
        "retainer_start": "2026-04-01",
        "next_renewal": "2026-07-01",
        "months_active": 2,
        "open_alerts": 1,
        "last_proof_update": "2026-05-15",
        "arr_sar": 2_999 * 12,
        "notes_ar": "ZATCA امتثال كامل محقق — يبحث عن تحسين إيرادات",
        "notes_en": "Full ZATCA compliance achieved — seeking revenue improvement",
    },
    "RTN-008": {
        "client_id": "RTN-008",
        "company_name_ar": "مصنع الجودة العالية",
        "company_name_en": "High Quality Manufacturing",
        "sector": "manufacturing",
        "city": "Dammam",
        "tier": "enterprise",
        "status": "active",
        "health_score": 88,
        "sprint_completed": True,
        "retainer_start": "2026-01-01",
        "next_renewal": "2026-07-01",
        "months_active": 5,
        "open_alerts": 0,
        "last_proof_update": "2026-05-25",
        "arr_sar": 4_999 * 12,
        "notes_ar": "مرشح مثالي لـ Custom AI — إيرادات متكررة قوية",
        "notes_en": "Ideal Custom AI candidate — strong recurring revenue",
    },
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _retainer_or_404(client_id: str) -> dict[str, Any]:
    r = _RETAINERS.get(client_id.upper())
    if r is None:
        raise HTTPException(
            status_code=404,
            detail={
                "ar": f"العميل '{client_id}' غير موجود",
                "en": f"Client '{client_id}' not found",
            },
        )
    return r


def _status_label(status: str) -> dict[str, str]:
    labels = {
        "active": {"ar": "نشط", "en": "Active"},
        "paused": {"ar": "موقوف مؤقتاً", "en": "Paused"},
        "at_risk": {"ar": "في خطر", "en": "At Risk"},
        "churned": {"ar": "ألغى الاشتراك", "en": "Churned"},
        "pending": {"ar": "معلق", "en": "Pending"},
    }
    return labels.get(status, {"ar": status, "en": status})


def _health_tier(score: int) -> dict[str, str]:
    if score >= 75:
        return {"tier": "healthy", "ar": "بصحة جيدة", "en": "Healthy", "color": "green"}
    if score >= 55:
        return {"tier": "moderate", "ar": "معتدل", "en": "Moderate", "color": "amber"}
    if score >= 35:
        return {"tier": "at_risk", "ar": "في خطر", "en": "At Risk", "color": "orange"}
    return {"tier": "critical", "ar": "حرج", "en": "Critical", "color": "red"}


def _days_until(date_str: str) -> int:
    try:
        target = date.fromisoformat(date_str)
        return (target - _TODAY).days
    except ValueError:
        return 0


def _upgrade_path(tier: RetainerTier) -> dict[str, Any] | None:
    paths: dict[str, Any] = {
        "essential": {
            "next_tier": "professional",
            "current_sar": 2_999,
            "next_sar": 3_999,
            "delta_sar": 1_000,
            "added_value_ar": "تقارير أسبوعية + تحليل قطاعي + أولوية الدعم",
            "added_value_en": "Weekly reports + sector analysis + priority support",
        },
        "professional": {
            "next_tier": "enterprise",
            "current_sar": 3_999,
            "next_sar": 4_999,
            "delta_sar": 1_000,
            "added_value_ar": "مدير نجاح مخصص + Custom AI sprint + تقارير مجلس الإدارة",
            "added_value_en": "Dedicated success manager + Custom AI sprint + board reports",
        },
        "enterprise": None,
    }
    return paths.get(tier)


# ---------------------------------------------------------------------------
# Pydantic request models
# ---------------------------------------------------------------------------

class RenewBody(BaseModel):
    model_config = ConfigDict(extra="forbid")
    payment_confirmed: bool = Field(default=False, description="Set true after Moyasar payment confirmed")
    notes: str | None = Field(default=None, max_length=500)


class UpgradeBody(BaseModel):
    model_config = ConfigDict(extra="forbid")
    target_tier: RetainerTier
    reason: str | None = Field(default=None, max_length=500)


class PauseBody(BaseModel):
    model_config = ConfigDict(extra="forbid")
    reason: str = Field(min_length=5, max_length=500)
    resume_date: str | None = Field(default=None, description="Expected resume date YYYY-MM-DD")


class ProofUpdateBody(BaseModel):
    model_config = ConfigDict(extra="forbid")
    sections: list[str] = Field(default_factory=list, description="Proof pack sections to update")
    notes: str | None = Field(default=None, max_length=500)


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@router.get("/active")
async def list_active_retainers() -> dict[str, Any]:
    """All active retainers with health scores and next renewal dates."""
    active = [r for r in _RETAINERS.values() if r["status"] != "churned"]
    total_mrr = sum(TIER_PRICE[r["tier"]] for r in active if r["status"] == "active")
    at_risk_count = sum(1 for r in active if r["health_score"] < 55)

    summary = []
    for r in sorted(active, key=lambda x: x["health_score"]):
        tier: RetainerTier = r["tier"]
        summary.append({
            "client_id": r["client_id"],
            "company": {"ar": r["company_name_ar"], "en": r["company_name_en"]},
            "sector": r["sector"],
            "city": r["city"],
            "tier": {"id": tier, **TIER_LABELS[tier]},
            "price_sar": TIER_PRICE[tier],
            "status": {**_status_label(r["status"]), "id": r["status"]},
            "health": {**_health_tier(r["health_score"]), "score": r["health_score"]},
            "months_active": r["months_active"],
            "next_renewal": r["next_renewal"],
            "days_until_renewal": _days_until(r["next_renewal"]),
            "open_alerts": r["open_alerts"],
        })

    return {
        "governance_decision": _GOV,
        "generated_at": _NOW.isoformat(),
        "summary": {
            "total_active": sum(1 for r in active if r["status"] == "active"),
            "total_paused": sum(1 for r in active if r["status"] == "paused"),
            "at_risk_count": at_risk_count,
            "monthly_mrr_sar": total_mrr,
            "annual_arr_sar": total_mrr * 12,
        },
        "retainers": summary,
    }


@router.get("/at-risk")
async def at_risk_retainers() -> dict[str, Any]:
    """Retainers with health score < 60 — prioritized intervention list."""
    at_risk = [r for r in _RETAINERS.values() if r["health_score"] < 60 and r["status"] != "churned"]
    at_risk.sort(key=lambda x: x["health_score"])

    interventions = []
    for r in at_risk:
        tier: RetainerTier = r["tier"]
        days_renewal = _days_until(r["next_renewal"])
        urgency = "critical" if r["health_score"] < 40 else ("high" if days_renewal <= 14 else "medium")
        interventions.append({
            "client_id": r["client_id"],
            "company": {"ar": r["company_name_ar"], "en": r["company_name_en"]},
            "health_score": r["health_score"],
            "health_tier": _health_tier(r["health_score"]),
            "tier": {"id": tier, **TIER_LABELS[tier]},
            "status": r["status"],
            "days_until_renewal": days_renewal,
            "open_alerts": r["open_alerts"],
            "urgency": urgency,
            "recommended_action_ar": (
                "اتصل بالعميل خلال 24 ساعة — عرض جلسة تشخيص مجانية"
                if urgency == "critical"
                else "أرسل تحديث Proof Pack مع نتائج ملموسة خلال 3 أيام"
            ),
            "recommended_action_en": (
                "Call client within 24 hours — offer free diagnostic session"
                if urgency == "critical"
                else "Send Proof Pack update with concrete findings within 3 days"
            ),
            "revenue_at_risk_sar": TIER_PRICE[tier] * 12,
        })

    return {
        "governance_decision": _GOV,
        "generated_at": _NOW.isoformat(),
        "at_risk_count": len(interventions),
        "revenue_at_risk_sar": sum(TIER_PRICE[r["tier"]] * 12 for r in at_risk),
        "interventions": interventions,
    }


@router.get("/renewal-calendar")
async def renewal_calendar(days_ahead: int = 30) -> dict[str, Any]:
    """Upcoming retainer renewals in the next N days."""
    upcoming = []
    for r in _RETAINERS.values():
        days = _days_until(r["next_renewal"])
        if 0 <= days <= days_ahead and r["status"] != "churned":
            tier: RetainerTier = r["tier"]
            upcoming.append({
                "client_id": r["client_id"],
                "company": {"ar": r["company_name_ar"], "en": r["company_name_en"]},
                "renewal_date": r["next_renewal"],
                "days_until": days,
                "tier": {"id": tier, **TIER_LABELS[tier]},
                "price_sar": TIER_PRICE[tier],
                "health_score": r["health_score"],
                "renewal_risk": "high" if r["health_score"] < 60 else ("medium" if r["health_score"] < 75 else "low"),
                "recommended_prep_ar": (
                    "أرسل Proof Pack محدّث 5 أيام قبل التجديد"
                    if days > 5
                    else "اتصل الآن — موعد التجديد قريب جداً"
                ),
                "recommended_prep_en": (
                    "Send updated Proof Pack 5 days before renewal"
                    if days > 5
                    else "Call now — renewal date is very close"
                ),
            })

    upcoming.sort(key=lambda x: x["days_until"])

    return {
        "governance_decision": _GOV,
        "generated_at": _NOW.isoformat(),
        "days_ahead": days_ahead,
        "renewal_count": len(upcoming),
        "total_renewal_mrr_sar": sum(r["price_sar"] for r in upcoming),
        "renewals": upcoming,
    }


@router.get("/mrr-breakdown")
async def mrr_breakdown() -> dict[str, Any]:
    """MRR breakdown by tier, sector, and cohort month."""
    active_retainers = [r for r in _RETAINERS.values() if r["status"] == "active"]

    by_tier: dict[str, dict[str, Any]] = {}
    for r in active_retainers:
        tier = r["tier"]
        if tier not in by_tier:
            by_tier[tier] = {"count": 0, "mrr_sar": 0, "label": TIER_LABELS[tier]}
        by_tier[tier]["count"] += 1
        by_tier[tier]["mrr_sar"] += TIER_PRICE[tier]

    by_sector: dict[str, dict[str, Any]] = {}
    for r in active_retainers:
        sector = r["sector"]
        if sector not in by_sector:
            by_sector[sector] = {"count": 0, "mrr_sar": 0}
        by_sector[sector]["count"] += 1
        by_sector[sector]["mrr_sar"] += TIER_PRICE[r["tier"]]

    total_mrr = sum(TIER_PRICE[r["tier"]] for r in active_retainers)

    return {
        "governance_decision": _GOV,
        "generated_at": _NOW.isoformat(),
        "total_active_retainers": len(active_retainers),
        "total_mrr_sar": total_mrr,
        "total_arr_sar": total_mrr * 12,
        "avg_mrr_per_client_sar": round(total_mrr / max(len(active_retainers), 1)),
        "by_tier": by_tier,
        "by_sector": dict(sorted(by_sector.items(), key=lambda x: x[1]["mrr_sar"], reverse=True)),
        "target_mrr_sar": 50_000,
        "target_progress_pct": round(total_mrr / 50_000 * 100, 1),
    }


@router.get("/{client_id}")
async def get_retainer(client_id: str) -> dict[str, Any]:
    """Full retainer state for one client — health, history, upgrade path."""
    r = _retainer_or_404(client_id)
    tier: RetainerTier = r["tier"]
    return {
        "governance_decision": _GOV,
        "generated_at": _NOW.isoformat(),
        "client_id": r["client_id"],
        "company": {"ar": r["company_name_ar"], "en": r["company_name_en"]},
        "sector": r["sector"],
        "city": r["city"],
        "tier": {"id": tier, "price_sar": TIER_PRICE[tier], **TIER_LABELS[tier]},
        "status": {**_status_label(r["status"]), "id": r["status"]},
        "health": {**_health_tier(r["health_score"]), "score": r["health_score"]},
        "retainer_start": r["retainer_start"],
        "months_active": r["months_active"],
        "next_renewal": r["next_renewal"],
        "days_until_renewal": _days_until(r["next_renewal"]),
        "arr_sar": TIER_PRICE[tier] * 12,
        "open_alerts": r["open_alerts"],
        "last_proof_update": r["last_proof_update"],
        "notes": {"ar": r.get("notes_ar", ""), "en": r.get("notes_en", "")},
        "upgrade_available": _upgrade_path(tier),
        "expansion_signals": _compute_expansion_signals(r),
    }


@router.post("/{client_id}/renew")
async def process_renewal(client_id: str, body: RenewBody) -> dict[str, Any]:
    """Process a retainer renewal — updates next_renewal date."""
    r = _retainer_or_404(client_id)
    if not body.payment_confirmed:
        return {
            "governance_decision": _GOV,
            "status": "pending_payment",
            "message_ar": "التجديد معلق — أكّد الدفع عبر Moyasar",
            "message_en": "Renewal pending — confirm payment via Moyasar",
            "client_id": client_id,
            "amount_sar": TIER_PRICE[r["tier"]],
        }

    new_renewal = (date.fromisoformat(r["next_renewal"]) + timedelta(days=30)).isoformat()
    r["next_renewal"] = new_renewal
    r["months_active"] = r["months_active"] + 1

    _log.info(
        "retainer_renewed client_id=%s tier=%s months_active=%d",
        client_id,
        r["tier"].replace("\n", "").replace("\r", ""),
        r["months_active"],
    )

    return {
        "governance_decision": _GOV,
        "status": "renewed",
        "client_id": client_id,
        "message_ar": f"تم التجديد بنجاح — التجديد القادم {new_renewal}",
        "message_en": f"Renewal successful — next renewal {new_renewal}",
        "new_renewal_date": new_renewal,
        "months_active": r["months_active"],
        "amount_charged_sar": TIER_PRICE[r["tier"]],
    }


@router.post("/{client_id}/upgrade")
async def upgrade_tier(client_id: str, body: UpgradeBody) -> dict[str, Any]:
    """Upgrade a retainer to a higher tier. Requires APPROVAL_FIRST."""
    r = _retainer_or_404(client_id)
    current_tier: RetainerTier = r["tier"]
    target_tier = body.target_tier

    tier_order = {"essential": 1, "professional": 2, "enterprise": 3}
    if tier_order.get(target_tier, 0) <= tier_order.get(current_tier, 0):
        raise HTTPException(
            status_code=400,
            detail={
                "ar": f"لا يمكن الترقية من {current_tier} إلى {target_tier}",
                "en": f"Cannot upgrade from {current_tier} to {target_tier}",
            },
        )

    delta = TIER_PRICE[target_tier] - TIER_PRICE[current_tier]
    r["tier"] = target_tier

    return {
        "governance_decision": "APPROVAL_FIRST",
        "status": "upgrade_queued_for_approval",
        "message_ar": "الترقية مُصفّفة — تحتاج موافقة المؤسس قبل التطبيق",
        "message_en": "Upgrade queued — requires founder approval before application",
        "client_id": client_id,
        "from_tier": current_tier,
        "to_tier": target_tier,
        "delta_sar": delta,
        "new_monthly_sar": TIER_PRICE[target_tier],
        "reason": body.reason,
    }


@router.post("/{client_id}/pause")
async def pause_retainer(client_id: str, body: PauseBody) -> dict[str, Any]:
    """Pause a retainer for up to 30 days. Status → paused."""
    r = _retainer_or_404(client_id)
    if r["status"] == "churned":
        raise HTTPException(
            status_code=400,
            detail={"ar": "لا يمكن إيقاف عميل ألغى الاشتراك", "en": "Cannot pause a churned client"},
        )

    r["status"] = "paused"
    resume = body.resume_date or (_TODAY + timedelta(days=30)).isoformat()

    return {
        "governance_decision": _GOV,
        "status": "paused",
        "client_id": client_id,
        "pause_reason": body.reason,
        "expected_resume": resume,
        "message_ar": f"الاشتراك موقوف مؤقتاً حتى {resume}",
        "message_en": f"Retainer paused until {resume}",
        "retention_tip_ar": "تابع مع العميل أسبوع قبل موعد الاستئناف المتوقع",
        "retention_tip_en": "Follow up with client one week before expected resume date",
    }


@router.post("/{client_id}/proof-update")
async def queue_proof_update(client_id: str, body: ProofUpdateBody) -> dict[str, Any]:
    """Queue a Proof Pack update for the client. Requires founder approval."""
    r = _retainer_or_404(client_id)
    default_sections = ["data_audit", "revenue_analysis", "action_plan", "roi_projection"]
    sections = body.sections or default_sections

    return {
        "governance_decision": "APPROVAL_FIRST",
        "status": "proof_update_queued",
        "client_id": client_id,
        "sections_to_update": sections,
        "message_ar": "تحديث Proof Pack مُصفّف — يحتاج موافقة المؤسس",
        "message_en": "Proof Pack update queued — requires founder approval",
        "estimated_hours": len(sections) * 1.5,
        "notes": body.notes,
    }


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _compute_expansion_signals(r: dict[str, Any]) -> list[dict[str, str]]:
    signals: list[dict[str, str]] = []
    if r["health_score"] >= 75:
        signals.append({
            "signal_ar": "درجة صحة عالية — مؤهل للترقية",
            "signal_en": "High health score — upgrade candidate",
        })
    if r["months_active"] >= 4:
        signals.append({
            "signal_ar": f"{r['months_active']} أشهر نشطة — إخلاص مثبت",
            "signal_en": f"{r['months_active']} active months — proven loyalty",
        })
    if r.get("open_alerts", 0) == 0:
        signals.append({
            "signal_ar": "لا تنبيهات مفتوحة — عمليات سلسة",
            "signal_en": "Zero open alerts — smooth operations",
        })
    if r["sector"] in ("technology", "financial_services", "healthcare"):
        signals.append({
            "signal_ar": "قطاع ذو قيمة عالية — مرشح لـ Custom AI",
            "signal_en": "High-value sector — Custom AI candidate",
        })
    return signals
