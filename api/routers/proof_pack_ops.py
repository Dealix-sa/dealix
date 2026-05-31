"""Proof Pack Operations — verifiable, auditable client result packs.

Endpoints:
  GET  /api/v1/proof-packs/                  — all proof packs with summary
  GET  /api/v1/proof-packs/pending-delivery  — approved packs not yet delivered
  GET  /api/v1/proof-packs/metrics-library   — unique metrics used across packs
  GET  /api/v1/proof-packs/{pack_id}         — single pack full detail
  POST /api/v1/proof-packs/generate          — generate new draft pack
  POST /api/v1/proof-packs/{pack_id}/submit-for-review  — move draft to review
  POST /api/v1/proof-packs/{pack_id}/approve            — approve pack under review
  POST /api/v1/proof-packs/{pack_id}/deliver            — mark pack as delivered

All endpoints:
  - Require admin auth (X-Admin-API-Key)
  - Return governance_decision field
  - WhatsApp delivery requires consent note (doctrine compliance)
  - Mutating actions use APPROVAL_FIRST
  - Read-only actions use ALLOW_WITH_REVIEW
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from fastapi import APIRouter, Body, Depends, HTTPException, Query
from pydantic import BaseModel, Field

from api.security.api_key import require_admin_key
from core.logging import get_logger

_log = get_logger(__name__)

router = APIRouter(
    prefix="/api/v1/proof-packs",
    tags=["proof-pack-ops"],
    dependencies=[Depends(require_admin_key)],
)

_GOV_READ = "ALLOW_WITH_REVIEW"
_GOV_MUTATE = "APPROVAL_FIRST"

_VALID_PACK_TYPES = frozenset({"sprint_result", "monthly_ops", "annual_review", "zatca_compliance"})
_VALID_STATUSES = frozenset({"draft", "review", "approved", "delivered", "archived"})
_VALID_CHANNELS = frozenset({"email", "whatsapp", "in_person"})

_PACK_COUNTER = {"value": 8}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _now_iso() -> str:
    """Return current UTC time as ISO-8601 string."""
    return datetime.now(UTC).isoformat()


def _days_since(date_str: str) -> int:
    """Return days elapsed since the given ISO-8601 date string."""
    try:
        past = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        delta = datetime.now(UTC) - past
        return max(0, delta.days)
    except Exception:
        return 0


def _compute_proof_score(metrics: list[dict[str, Any]]) -> int:
    """Compute proof score from a list of metric dicts.

    Score = percentage of verified metrics * average improvement_pct,
    capped at 0-100. Returns 0 if no metrics provided.
    """
    if not metrics:
        return 0
    verified = [m for m in metrics if m.get("verified", False)]
    verified_ratio = len(verified) / len(metrics)
    improvements = [abs(m.get("improvement_pct", 0.0)) for m in metrics]
    avg_improvement = sum(improvements) / len(improvements) if improvements else 0.0
    raw = verified_ratio * min(avg_improvement, 100.0)
    return max(0, min(100, round(raw)))


# ---------------------------------------------------------------------------
# Demo proof packs
# ---------------------------------------------------------------------------

_PACKS: list[dict[str, Any]] = [
    # --- 3 delivered packs ---
    {
        "pack_id": "PP-001",
        "client_id": "CLT-001",
        "company_ar": "شركة التقنية المتقدمة",
        "company_en": "Advanced Technology Co.",
        "sprint_id": "SPR-001",
        "status": "delivered",
        "pack_type": "sprint_result",
        "generated_at": "2026-03-15T10:00:00+00:00",
        "delivered_at": "2026-03-18T14:30:00+00:00",
        "metrics": [
            {
                "metric_name_ar": "درجة جودة البيانات",
                "metric_name_en": "Data Quality Score",
                "baseline_value": 48.0,
                "current_value": 89.0,
                "unit": "score",
                "improvement_pct": 85.42,
                "verified": True,
            },
            {
                "metric_name_ar": "معدل التسليم في الوقت المحدد",
                "metric_name_en": "On-Time Delivery Rate",
                "baseline_value": 62.0,
                "current_value": 91.0,
                "unit": "%",
                "improvement_pct": 46.77,
                "verified": True,
            },
            {
                "metric_name_ar": "وقت معالجة الفاتورة",
                "metric_name_en": "Invoice Processing Time",
                "baseline_value": 5.0,
                "current_value": 1.5,
                "unit": "days",
                "improvement_pct": 70.0,
                "verified": True,
            },
        ],
        "proof_score": 82,
        "reviewer_notes": "Excellent results across all KPIs. Ready for annual review expansion.",
        "approved_by": "Bassam Al-Assiri",
        "delivery_channel": "email",
    },
    {
        "pack_id": "PP-002",
        "client_id": "CLT-002",
        "company_ar": "مجموعة الخدمات المالية الخليجية",
        "company_en": "Gulf Financial Services Group",
        "sprint_id": "SPR-002",
        "status": "delivered",
        "pack_type": "zatca_compliance",
        "generated_at": "2026-04-01T09:00:00+00:00",
        "delivered_at": "2026-04-04T11:00:00+00:00",
        "metrics": [
            {
                "metric_name_ar": "معدل الامتثال لهيئة الزكاة والضريبة",
                "metric_name_en": "ZATCA Compliance Rate",
                "baseline_value": 0.0,
                "current_value": 100.0,
                "unit": "%",
                "improvement_pct": 100.0,
                "verified": True,
            },
            {
                "metric_name_ar": "نسبة الفواتير الإلكترونية المُرسلة",
                "metric_name_en": "E-Invoice Submission Rate",
                "baseline_value": 10.0,
                "current_value": 98.0,
                "unit": "%",
                "improvement_pct": 880.0,
                "verified": True,
            },
            {
                "metric_name_ar": "وقت التحقق من الامتثال",
                "metric_name_en": "Compliance Verification Time",
                "baseline_value": 14.0,
                "current_value": 2.0,
                "unit": "days",
                "improvement_pct": 85.71,
                "verified": True,
            },
        ],
        "proof_score": 94,
        "reviewer_notes": "Full ZATCA Phase 2 compliance achieved. Delivered in-person at client HQ.",
        "approved_by": "Bassam Al-Assiri",
        "delivery_channel": "in_person",
    },
    {
        "pack_id": "PP-003",
        "client_id": "CLT-003",
        "company_ar": "شركة العقارات السعودية الكبرى",
        "company_en": "Major Saudi Real Estate Co.",
        "sprint_id": None,
        "status": "delivered",
        "pack_type": "monthly_ops",
        "generated_at": "2026-04-30T08:00:00+00:00",
        "delivered_at": "2026-05-02T10:00:00+00:00",
        "metrics": [
            {
                "metric_name_ar": "تخفيض تسرب الإيرادات",
                "metric_name_en": "Revenue Leakage Reduction",
                "baseline_value": 85000.0,
                "current_value": 12000.0,
                "unit": "SAR",
                "improvement_pct": 85.88,
                "verified": True,
            },
            {
                "metric_name_ar": "درجة رضا العملاء",
                "metric_name_en": "Client Satisfaction Score",
                "baseline_value": 3.1,
                "current_value": 4.4,
                "unit": "score/5",
                "improvement_pct": 41.94,
                "verified": False,
            },
            {
                "metric_name_ar": "معدل التسليم في الوقت المحدد",
                "metric_name_en": "On-Time Delivery Rate",
                "baseline_value": 71.0,
                "current_value": 88.0,
                "unit": "%",
                "improvement_pct": 23.94,
                "verified": True,
            },
        ],
        "proof_score": 58,
        "reviewer_notes": "Good revenue leakage reduction. Client satisfaction metric awaiting verification.",
        "approved_by": "Bassam Al-Assiri",
        "delivery_channel": "email",
    },
    # --- 2 approved packs (ready to deliver) ---
    {
        "pack_id": "PP-004",
        "client_id": "CLT-004",
        "company_ar": "شركة التجزئة الذكية",
        "company_en": "Smart Retail Solutions",
        "sprint_id": "SPR-004",
        "status": "approved",
        "pack_type": "sprint_result",
        "generated_at": "2026-05-20T09:00:00+00:00",
        "delivered_at": None,
        "metrics": [
            {
                "metric_name_ar": "درجة جودة البيانات",
                "metric_name_en": "Data Quality Score",
                "baseline_value": 52.0,
                "current_value": 78.0,
                "unit": "score",
                "improvement_pct": 50.0,
                "verified": True,
            },
            {
                "metric_name_ar": "تخفيض وقت معالجة الطلبات",
                "metric_name_en": "Order Processing Time Reduction",
                "baseline_value": 4.0,
                "current_value": 1.2,
                "unit": "hours",
                "improvement_pct": 70.0,
                "verified": True,
            },
        ],
        "proof_score": 60,
        "reviewer_notes": "Solid improvement in data quality and processing. Approved for delivery.",
        "approved_by": "Bassam Al-Assiri",
        "delivery_channel": None,
    },
    {
        "pack_id": "PP-005",
        "client_id": "CLT-005",
        "company_ar": "مستشفى الصحة المتكاملة",
        "company_en": "Integrated Health Hospital",
        "sprint_id": None,
        "status": "approved",
        "pack_type": "monthly_ops",
        "generated_at": "2026-05-22T11:00:00+00:00",
        "delivered_at": None,
        "metrics": [
            {
                "metric_name_ar": "معدل الامتثال لهيئة الزكاة والضريبة",
                "metric_name_en": "ZATCA Compliance Rate",
                "baseline_value": 45.0,
                "current_value": 92.0,
                "unit": "%",
                "improvement_pct": 104.44,
                "verified": True,
            },
            {
                "metric_name_ar": "تخفيض تسرب الإيرادات",
                "metric_name_en": "Revenue Leakage Reduction",
                "baseline_value": 120000.0,
                "current_value": 30000.0,
                "unit": "SAR",
                "improvement_pct": 75.0,
                "verified": True,
            },
            {
                "metric_name_ar": "وقت معالجة الفاتورة",
                "metric_name_en": "Invoice Processing Time",
                "baseline_value": 8.0,
                "current_value": 2.0,
                "unit": "days",
                "improvement_pct": 75.0,
                "verified": False,
            },
        ],
        "proof_score": 72,
        "reviewer_notes": "Strong compliance and revenue recovery. Invoice time pending audit verification.",
        "approved_by": "Bassam Al-Assiri",
        "delivery_channel": None,
    },
    # --- 2 draft packs ---
    {
        "pack_id": "PP-006",
        "client_id": "CLT-006",
        "company_ar": "شركة الخدمات اللوجستية المتطورة",
        "company_en": "Advanced Logistics Services Co.",
        "sprint_id": "SPR-006",
        "status": "draft",
        "pack_type": "sprint_result",
        "generated_at": "2026-05-28T13:00:00+00:00",
        "delivered_at": None,
        "metrics": [
            {
                "metric_name_ar": "درجة جودة البيانات",
                "metric_name_en": "Data Quality Score",
                "baseline_value": 30.0,
                "current_value": 55.0,
                "unit": "score",
                "improvement_pct": 83.33,
                "verified": False,
            },
            {
                "metric_name_ar": "معدل التسليم في الوقت المحدد",
                "metric_name_en": "On-Time Delivery Rate",
                "baseline_value": 55.0,
                "current_value": 72.0,
                "unit": "%",
                "improvement_pct": 30.91,
                "verified": False,
            },
        ],
        "proof_score": 0,
        "reviewer_notes": None,
        "approved_by": None,
        "delivery_channel": None,
    },
    {
        "pack_id": "PP-007",
        "client_id": "CLT-007",
        "company_ar": "أكاديمية التعليم الرقمي",
        "company_en": "Digital Education Academy",
        "sprint_id": None,
        "status": "draft",
        "pack_type": "annual_review",
        "generated_at": "2026-05-29T09:00:00+00:00",
        "delivered_at": None,
        "metrics": [
            {
                "metric_name_ar": "نسبة الفواتير الإلكترونية المُرسلة",
                "metric_name_en": "E-Invoice Submission Rate",
                "baseline_value": 0.0,
                "current_value": 60.0,
                "unit": "%",
                "improvement_pct": 100.0,
                "verified": False,
            },
        ],
        "proof_score": 0,
        "reviewer_notes": None,
        "approved_by": None,
        "delivery_channel": None,
    },
    # --- 1 review pack ---
    {
        "pack_id": "PP-008",
        "client_id": "CLT-008",
        "company_ar": "شركة التصنيع الصناعي الخليجي",
        "company_en": "Gulf Industrial Manufacturing Co.",
        "sprint_id": "SPR-008",
        "status": "review",
        "pack_type": "zatca_compliance",
        "generated_at": "2026-05-25T10:00:00+00:00",
        "delivered_at": None,
        "metrics": [
            {
                "metric_name_ar": "معدل الامتثال لهيئة الزكاة والضريبة",
                "metric_name_en": "ZATCA Compliance Rate",
                "baseline_value": 20.0,
                "current_value": 95.0,
                "unit": "%",
                "improvement_pct": 375.0,
                "verified": True,
            },
            {
                "metric_name_ar": "تخفيض تسرب الإيرادات",
                "metric_name_en": "Revenue Leakage Reduction",
                "baseline_value": 200000.0,
                "current_value": 18000.0,
                "unit": "SAR",
                "improvement_pct": 91.0,
                "verified": True,
            },
            {
                "metric_name_ar": "درجة رضا العملاء",
                "metric_name_en": "Client Satisfaction Score",
                "baseline_value": 2.8,
                "current_value": 4.6,
                "unit": "score/5",
                "improvement_pct": 64.29,
                "verified": False,
            },
        ],
        "proof_score": 67,
        "reviewer_notes": "Pending founder sign-off. ZATCA gains are verified; satisfaction score still being audited.",
        "approved_by": None,
        "delivery_channel": None,
    },
]

# ---------------------------------------------------------------------------
# In-memory index helpers
# ---------------------------------------------------------------------------


def _get_pack(pack_id: str) -> dict[str, Any] | None:
    return next((p for p in _PACKS if p["pack_id"] == pack_id), None)


def _pack_or_404(pack_id: str) -> dict[str, Any]:
    p = _get_pack(pack_id)
    if p is None:
        raise HTTPException(
            status_code=404,
            detail={
                "ar": f"الحزمة '{pack_id}' غير موجودة",
                "en": f"Proof pack '{pack_id}' not found",
            },
        )
    return p


def _next_pack_id() -> str:
    _PACK_COUNTER["value"] += 1
    return f"PP-{_PACK_COUNTER['value']:03d}"


# ---------------------------------------------------------------------------
# Request models
# ---------------------------------------------------------------------------


class GeneratePackBody(BaseModel):
    client_id: str = Field(min_length=1)
    company_ar: str = Field(min_length=1)
    company_en: str = Field(min_length=1)
    pack_type: str
    sprint_id: str | None = None
    initial_metrics: list[dict[str, Any]] = Field(default_factory=list)


class SubmitReviewBody(BaseModel):
    notes: str = Field(min_length=5)


class ApproveBody(BaseModel):
    approved_by: str = Field(min_length=3)
    notes: str | None = None


class DeliverBody(BaseModel):
    delivery_channel: str
    delivery_notes: str | None = None


# ---------------------------------------------------------------------------
# Endpoints — fixed paths first, then parameterised
# ---------------------------------------------------------------------------


@router.get("/")
async def list_proof_packs(
    status: str | None = Query(default=None),
) -> dict[str, Any]:
    """All proof packs with portfolio summary. Filter by ?status= query param.

    Sorted by generated_at descending (most recent first).
    """
    packs = list(_PACKS)
    if status:
        packs = [p for p in packs if p["status"] == status]

    packs.sort(key=lambda p: p["generated_at"], reverse=True)

    total = len(_PACKS)
    delivered_count = sum(1 for p in _PACKS if p["status"] == "delivered")
    pending_delivery_count = sum(
        1 for p in _PACKS if p["status"] == "approved" and p["delivered_at"] is None
    )
    scores = [p["proof_score"] for p in _PACKS]
    avg_proof_score = round(sum(scores) / len(scores), 1) if scores else 0.0
    total_clients_with_packs = len({p["client_id"] for p in _PACKS})

    _log.info("proof_packs_listed", count=len(packs), status_filter=status)

    return {
        "governance_decision": _GOV_READ,
        "generated_at": _now_iso(),
        "summary": {
            "total_packs": total,
            "delivered_count": delivered_count,
            "pending_delivery_count": pending_delivery_count,
            "avg_proof_score": avg_proof_score,
            "total_clients_with_packs": total_clients_with_packs,
        },
        "packs": packs,
    }


@router.get("/pending-delivery")
async def get_pending_delivery() -> dict[str, Any]:
    """Approved packs not yet delivered, enriched with days_since_approval."""
    pending = [
        p for p in _PACKS
        if p["status"] == "approved" and p["delivered_at"] is None
    ]

    enriched = [
        {
            **p,
            "days_since_approval": _days_since(p["generated_at"]),
        }
        for p in pending
    ]

    _log.info("pending_delivery_queried", count=len(enriched))

    return {
        "governance_decision": _GOV_READ,
        "generated_at": _now_iso(),
        "pending_count": len(enriched),
        "action_ar": "راجع كل Pack وأرسله بعد موافقة المؤسس",
        "action_en": "Review each pack and deliver after founder approval",
        "packs": enriched,
    }


@router.get("/metrics-library")
async def get_metrics_library() -> dict[str, Any]:
    """All unique metric names used across all packs with usage count."""
    counts: dict[str, int] = {}
    for pack in _PACKS:
        for metric in pack.get("metrics", []):
            name_en = metric.get("metric_name_en", "")
            if name_en:
                counts[name_en] = counts.get(name_en, 0) + 1

    _log.info("metrics_library_queried", unique_metrics=len(counts))

    return {
        "governance_decision": _GOV_READ,
        "generated_at": _now_iso(),
        "total_unique_metrics": len(counts),
        "metrics": counts,
    }


@router.get("/{pack_id}")
async def get_proof_pack(pack_id: str) -> dict[str, Any]:
    """Full proof pack detail. Returns 404 if not found."""
    pack = _pack_or_404(pack_id)

    _log.info("proof_pack_fetched", pack_id=pack_id, status=pack["status"])

    return {
        "governance_decision": _GOV_READ,
        "generated_at": _now_iso(),
        **pack,
    }


@router.post("/generate")
async def generate_proof_pack(body: GeneratePackBody = Body(...)) -> dict[str, Any]:
    """Generate a new draft proof pack with auto-computed metrics and proof score.

    pack_type must be one of: sprint_result, monthly_ops, annual_review, zatca_compliance.
    improvement_pct is computed per metric. proof_score is computed from verified ratios.
    """
    if body.pack_type not in _VALID_PACK_TYPES:
        raise HTTPException(
            status_code=422,
            detail={
                "ar": f"نوع الحزمة '{body.pack_type}' غير صالح",
                "en": f"Invalid pack_type '{body.pack_type}'. Must be one of: {sorted(_VALID_PACK_TYPES)}",
            },
        )

    processed_metrics: list[dict[str, Any]] = []
    for m in body.initial_metrics:
        baseline = float(m.get("baseline_value", 0))
        current = float(m.get("current_value", 0))
        if baseline != 0:
            improvement_pct = round(((current - baseline) / abs(baseline)) * 100.0, 2)
        else:
            improvement_pct = 0.0 if current == 0 else 100.0

        processed_metrics.append({
            "metric_name_ar": m.get("metric_name_ar", ""),
            "metric_name_en": m.get("metric_name_en", ""),
            "baseline_value": baseline,
            "current_value": current,
            "unit": m.get("unit", ""),
            "improvement_pct": improvement_pct,
            "verified": bool(m.get("verified", False)),
        })

    proof_score = _compute_proof_score(processed_metrics)
    pack_id = _next_pack_id()
    now = _now_iso()

    new_pack: dict[str, Any] = {
        "pack_id": pack_id,
        "client_id": body.client_id,
        "company_ar": body.company_ar,
        "company_en": body.company_en,
        "sprint_id": body.sprint_id,
        "status": "draft",
        "pack_type": body.pack_type,
        "generated_at": now,
        "delivered_at": None,
        "metrics": processed_metrics,
        "proof_score": proof_score,
        "reviewer_notes": None,
        "approved_by": None,
        "delivery_channel": None,
    }
    _PACKS.append(new_pack)

    _log.info(
        "proof_pack_generated",
        pack_id=pack_id,
        client_id=body.client_id,
        pack_type=body.pack_type,
        proof_score=proof_score,
    )

    return {
        "governance_decision": _GOV_MUTATE,
        "generated_at": now,
        "status": "draft_created",
        "pack": new_pack,
        "message_ar": "تم إنشاء Proof Pack كمسودة — يتطلب مراجعة وموافقة المؤسس قبل التسليم",
        "message_en": "Proof Pack created as draft — requires review and founder approval before delivery",
    }


@router.post("/{pack_id}/submit-for-review")
async def submit_for_review(
    pack_id: str,
    body: SubmitReviewBody = Body(...),
) -> dict[str, Any]:
    """Move a draft proof pack to review status.

    Returns 400 if the pack is not in draft status.
    """
    pack = _pack_or_404(pack_id)

    if pack["status"] != "draft":
        raise HTTPException(
            status_code=400,
            detail={
                "ar": f"لا يمكن تقديم الحزمة '{pack_id}' للمراجعة — الحالة الحالية: {pack['status']}",
                "en": f"Cannot submit pack '{pack_id}' for review — current status: {pack['status']}",
            },
        )

    pack["status"] = "review"
    pack["reviewer_notes"] = body.notes
    now = _now_iso()

    _log.info("proof_pack_submitted_for_review", pack_id=pack_id)

    return {
        "governance_decision": _GOV_MUTATE,
        "generated_at": now,
        "status": "submitted_for_review",
        "pack_id": pack_id,
        "reviewer_notes": body.notes,
        "message_ar": "تم تقديم الحزمة للمراجعة — في انتظار موافقة المؤسس",
        "message_en": "Pack submitted for review — awaiting founder sign-off",
    }


@router.post("/{pack_id}/approve")
async def approve_proof_pack(
    pack_id: str,
    body: ApproveBody = Body(...),
) -> dict[str, Any]:
    """Approve a proof pack that is under review.

    Returns 400 if the pack is not in review status.
    """
    pack = _pack_or_404(pack_id)

    if pack["status"] != "review":
        raise HTTPException(
            status_code=400,
            detail={
                "ar": f"لا يمكن الموافقة على الحزمة '{pack_id}' — الحالة الحالية: {pack['status']}",
                "en": f"Cannot approve pack '{pack_id}' — current status: {pack['status']}",
            },
        )

    pack["status"] = "approved"
    pack["approved_by"] = body.approved_by
    if body.notes:
        pack["reviewer_notes"] = body.notes
    now = _now_iso()

    _log.info("proof_pack_approved", pack_id=pack_id, approved_by=body.approved_by)

    return {
        "governance_decision": _GOV_MUTATE,
        "generated_at": now,
        "status": "approved",
        "pack_id": pack_id,
        "approved_by": body.approved_by,
        "message_ar": f"تمت الموافقة على Proof Pack بواسطة {body.approved_by} — جاهز للتسليم",
        "message_en": f"Proof Pack approved by {body.approved_by} — ready for delivery",
    }


@router.post("/{pack_id}/deliver")
async def deliver_proof_pack(
    pack_id: str,
    body: DeliverBody = Body(...),
) -> dict[str, Any]:
    """Mark a proof pack as delivered via the specified channel.

    Returns 400 if the pack is not in approved status.
    WhatsApp delivery includes a mandatory client consent note (doctrine compliance).
    """
    pack = _pack_or_404(pack_id)

    if body.delivery_channel not in _VALID_CHANNELS:
        raise HTTPException(
            status_code=422,
            detail={
                "ar": f"قناة التسليم '{body.delivery_channel}' غير صالحة",
                "en": f"Invalid delivery_channel '{body.delivery_channel}'. Must be one of: email, whatsapp, in_person",
            },
        )

    if pack["status"] != "approved":
        raise HTTPException(
            status_code=400,
            detail={
                "ar": f"لا يمكن تسليم الحزمة '{pack_id}' — الحالة الحالية: {pack['status']}",
                "en": f"Cannot deliver pack '{pack_id}' — current status: {pack['status']}",
            },
        )

    now = _now_iso()
    pack["status"] = "delivered"
    pack["delivered_at"] = now
    pack["delivery_channel"] = body.delivery_channel

    _log.info(
        "proof_pack_delivered",
        pack_id=pack_id,
        channel=body.delivery_channel,
    )

    response: dict[str, Any] = {
        "governance_decision": _GOV_MUTATE,
        "generated_at": now,
        "status": "delivered",
        "pack_id": pack_id,
        "delivery_channel": body.delivery_channel,
        "delivered_at": now,
        "delivery_notes": body.delivery_notes,
        "message_ar": "تم تسليم Proof Pack بنجاح — سجَّل ردّ فعل العميل في جلسة المتابعة",
        "message_en": "Proof Pack delivered successfully — record client reaction in the follow-up session",
    }

    if body.delivery_channel == "whatsapp":
        response["whatsapp_note_ar"] = "يتطلب موافقة العميل المسبقة على التواصل عبر واتساب"
        response["whatsapp_note_en"] = "Requires prior client consent for WhatsApp contact"

    return response
