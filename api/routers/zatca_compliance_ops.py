"""ZATCA Compliance Operations — Phase 2 e-invoicing compliance management.

Endpoints:
  GET  /api/v1/zatca-ops/invoices                   — list ZATCA invoices with optional filters
  GET  /api/v1/zatca-ops/invoices/pending           — invoices requiring action (draft/signed/rejected)
  GET  /api/v1/zatca-ops/invoices/{invoice_id}      — single invoice detail
  POST /api/v1/zatca-ops/invoices/{invoice_id}/submit     — submit draft to ZATCA (APPROVAL_FIRST)
  POST /api/v1/zatca-ops/invoices/{invoice_id}/resubmit   — resubmit rejected invoice (APPROVAL_FIRST)
  GET  /api/v1/zatca-ops/compliance-dashboard       — overall compliance metrics
  GET  /api/v1/zatca-ops/vat-summary                — VAT breakdown for current period

All endpoints:
  - Require admin auth (X-Admin-API-Key)
  - Return governance_decision field
  - PDPL-compliant: no individual PII in aggregate views
  - No guaranteed-outcome language
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from fastapi import APIRouter, Body, Depends, HTTPException, Query
from pydantic import BaseModel, ConfigDict, Field

from api.security.api_key import require_admin_key
from core.logging import get_logger

_log = get_logger(__name__)

router = APIRouter(
    prefix="/api/v1/zatca-ops",
    tags=["ZATCA Compliance"],
    dependencies=[Depends(require_admin_key)],
)

# ---------------------------------------------------------------------------
# Governance constants
# ---------------------------------------------------------------------------

_GOV_READ = "ALLOW_WITH_REVIEW"
_GOV_MUTATE = "APPROVAL_FIRST"

# ---------------------------------------------------------------------------
# Valid ZATCA statuses and invoice types
# ---------------------------------------------------------------------------

_PENDING_STATUSES: frozenset[str] = frozenset({"draft", "signed", "rejected"})
_ACTIVE_STATUSES: frozenset[str] = frozenset({"reported", "cleared"})
_ALL_STATUSES: frozenset[str] = frozenset(
    {"draft", "signed", "reported", "cleared", "rejected"}
)
_ALL_INVOICE_TYPES: frozenset[str] = frozenset(
    {"standard", "simplified", "credit_note", "debit_note"}
)

# ---------------------------------------------------------------------------
# Demo data — 8 ZATCA invoices ZTV-001 through ZTV-008
# ---------------------------------------------------------------------------

ZATCA_INVOICES: dict[str, dict[str, Any]] = {
    "ZTV-001": {
        "id": "ZTV-001",
        "invoice_number": "INV-2026-001",
        "seller_vat": "300012345600003",
        "buyer_vat": "300098765400001",
        "buyer_name": "شركة الرياض للتقنية",
        "invoice_date": "2026-05-01",
        "supply_date": "2026-05-01",
        "subtotal_sar": 10000.00,
        "vat_rate": 0.15,
        "vat_amount_sar": 1500.00,
        "total_sar": 11500.00,
        "invoice_type": "standard",
        "zatca_status": "reported",
        "clearance_id": "ZATCA-CL-001-2026",
        "qr_code_b64": "base64_encoded_qr_placeholder",
        "xml_hash": "sha256_placeholder_001",
        "submitted_at": "2026-05-01T12:00:00Z",
        "cleared_at": "2026-05-01T12:05:00Z",
        "compliance_score": 100,
    },
    "ZTV-002": {
        "id": "ZTV-002",
        "invoice_number": "INV-2026-002",
        "seller_vat": "300012345600003",
        "buyer_vat": "300087654300002",
        "buyer_name": "مجموعة الصحة الوطنية",
        "invoice_date": "2026-05-05",
        "supply_date": "2026-05-05",
        "subtotal_sar": 24999.00,
        "vat_rate": 0.15,
        "vat_amount_sar": 3749.85,
        "total_sar": 28748.85,
        "invoice_type": "standard",
        "zatca_status": "cleared",
        "clearance_id": "ZATCA-CL-002-2026",
        "qr_code_b64": "base64_placeholder",
        "xml_hash": "sha256_placeholder_002",
        "submitted_at": "2026-05-05T14:00:00Z",
        "cleared_at": "2026-05-05T14:03:00Z",
        "compliance_score": 100,
    },
    "ZTV-003": {
        "id": "ZTV-003",
        "invoice_number": "INV-2026-003",
        "seller_vat": "300012345600003",
        "buyer_vat": None,
        "buyer_name": "عميل نقدي",
        "invoice_date": "2026-05-10",
        "supply_date": "2026-05-10",
        "subtotal_sar": 499.00,
        "vat_rate": 0.15,
        "vat_amount_sar": 74.85,
        "total_sar": 573.85,
        "invoice_type": "simplified",
        "zatca_status": "reported",
        "clearance_id": None,
        "qr_code_b64": "base64_placeholder",
        "xml_hash": "sha256_placeholder_003",
        "submitted_at": "2026-05-10T09:00:00Z",
        "cleared_at": None,
        "compliance_score": 98,
    },
    "ZTV-004": {
        "id": "ZTV-004",
        "invoice_number": "INV-2026-004",
        "seller_vat": "300012345600003",
        "buyer_vat": "300011122300003",
        "buyer_name": "شركة التجزئة الذكية",
        "invoice_date": "2026-05-15",
        "supply_date": "2026-05-15",
        "subtotal_sar": 4999.00,
        "vat_rate": 0.15,
        "vat_amount_sar": 749.85,
        "total_sar": 5748.85,
        "invoice_type": "standard",
        "zatca_status": "draft",
        "clearance_id": None,
        "qr_code_b64": None,
        "xml_hash": None,
        "submitted_at": None,
        "cleared_at": None,
        "compliance_score": 72,
    },
    "ZTV-005": {
        "id": "ZTV-005",
        "invoice_number": "CN-2026-001",
        "seller_vat": "300012345600003",
        "buyer_vat": "300012345600003",
        "buyer_name": "عميل مرتجع",
        "invoice_date": "2026-05-20",
        "supply_date": "2026-05-20",
        "subtotal_sar": -1500.00,
        "vat_rate": 0.15,
        "vat_amount_sar": -225.00,
        "total_sar": -1725.00,
        "invoice_type": "credit_note",
        "zatca_status": "cleared",
        "clearance_id": "ZATCA-CN-001-2026",
        "qr_code_b64": "base64_placeholder",
        "xml_hash": "sha256_placeholder_005",
        "submitted_at": "2026-05-20T11:00:00Z",
        "cleared_at": "2026-05-20T11:02:00Z",
        "compliance_score": 100,
    },
    "ZTV-006": {
        "id": "ZTV-006",
        "invoice_number": "INV-2026-005",
        "seller_vat": "300012345600003",
        "buyer_vat": "300034567800004",
        "buyer_name": "مؤسسة الأعمال المتميزة",
        "invoice_date": "2026-05-22",
        "supply_date": "2026-05-22",
        "subtotal_sar": 12500.00,
        "vat_rate": 0.15,
        "vat_amount_sar": 1875.00,
        "total_sar": 14375.00,
        "invoice_type": "standard",
        "zatca_status": "rejected",
        "clearance_id": None,
        "qr_code_b64": "base64_placeholder",
        "xml_hash": "sha256_placeholder_006",
        "submitted_at": "2026-05-22T16:00:00Z",
        "cleared_at": None,
        "compliance_score": 65,
        "rejection_reason": "Missing mandatory field: supply_date_format",
    },
    "ZTV-007": {
        "id": "ZTV-007",
        "invoice_number": "INV-2026-006",
        "seller_vat": "300012345600003",
        "buyer_vat": "300045678900005",
        "buyer_name": "شركة الاستشارات الرقمية",
        "invoice_date": "2026-05-28",
        "supply_date": "2026-05-28",
        "subtotal_sar": 8500.00,
        "vat_rate": 0.15,
        "vat_amount_sar": 1275.00,
        "total_sar": 9775.00,
        "invoice_type": "standard",
        "zatca_status": "signed",
        "clearance_id": None,
        "qr_code_b64": "base64_placeholder",
        "xml_hash": "sha256_placeholder_007",
        "submitted_at": None,
        "cleared_at": None,
        "compliance_score": 95,
    },
    "ZTV-008": {
        "id": "ZTV-008",
        "invoice_number": "INV-2026-007",
        "seller_vat": "300012345600003",
        "buyer_vat": "300056789000006",
        "buyer_name": "مركز التدريب التقني",
        "invoice_date": "2026-05-30",
        "supply_date": "2026-05-30",
        "subtotal_sar": 3000.00,
        "vat_rate": 0.15,
        "vat_amount_sar": 450.00,
        "total_sar": 3450.00,
        "invoice_type": "standard",
        "zatca_status": "draft",
        "clearance_id": None,
        "qr_code_b64": None,
        "xml_hash": None,
        "submitted_at": None,
        "cleared_at": None,
        "compliance_score": 78,
    },
}

# ---------------------------------------------------------------------------
# Pydantic request models
# ---------------------------------------------------------------------------


class SubmitBody(BaseModel):
    model_config = ConfigDict(extra="forbid")

    reason: str = Field(min_length=5)


class ResubmitBody(BaseModel):
    model_config = ConfigDict(extra="forbid")

    reason: str = Field(min_length=5)
    corrections: list[str] = Field(default_factory=list)


# ---------------------------------------------------------------------------
# Pure helper functions
# ---------------------------------------------------------------------------


def _now_iso() -> str:
    """Return current UTC timestamp as ISO-8601 string."""
    return datetime.now(UTC).isoformat()


def _get_invoice(invoice_id: str) -> dict[str, Any]:
    """Return ZATCA invoice dict or raise HTTP 404."""
    inv = ZATCA_INVOICES.get(invoice_id.upper())
    if inv is None:
        raise HTTPException(
            status_code=404,
            detail={
                "ar": f"الفاتورة '{invoice_id}' غير موجودة",
                "en": f"Invoice '{invoice_id}' not found",
            },
        )
    return inv


def _status_counts(invoices: list[dict[str, Any]]) -> dict[str, int]:
    """Return a dict mapping each zatca_status value to its count."""
    counts: dict[str, int] = {}
    for inv in invoices:
        status = inv.get("zatca_status", "unknown") or "unknown"
        counts[status] = counts.get(status, 0) + 1
    return counts


def _compute_compliance_rate(invoices: list[dict[str, Any]]) -> float:
    """Return fraction of invoices in reported or cleared status.

    Credit notes and debit notes are excluded from the denominator
    because they are corrective documents, not revenue-generating transactions.
    """
    taxable = [
        inv for inv in invoices
        if inv.get("invoice_type") not in {"credit_note", "debit_note"}
    ]
    if not taxable:
        return 0.0
    active = sum(
        1 for inv in taxable
        if inv.get("zatca_status") in _ACTIVE_STATUSES
    )
    return round(active / len(taxable), 3)


def _compute_avg_score(invoices: list[dict[str, Any]]) -> float:
    """Return mean compliance_score across all invoices."""
    if not invoices:
        return 0.0
    total = sum(float(inv.get("compliance_score", 0)) for inv in invoices)
    return round(total / len(invoices), 2)


def _sum_positive_vat(invoices: list[dict[str, Any]]) -> float:
    """Return total VAT for active invoices with positive vat_amount_sar."""
    return round(
        sum(
            float(inv.get("vat_amount_sar", 0))
            for inv in invoices
            if inv.get("zatca_status") in _ACTIVE_STATUSES
            and float(inv.get("vat_amount_sar", 0)) > 0
        ),
        2,
    )


def _sum_positive_revenue(invoices: list[dict[str, Any]]) -> float:
    """Return total revenue for active invoices with positive total_sar."""
    return round(
        sum(
            float(inv.get("total_sar", 0))
            for inv in invoices
            if inv.get("zatca_status") in _ACTIVE_STATUSES
            and float(inv.get("total_sar", 0)) > 0
        ),
        2,
    )


def _build_vat_type_counts(invoices: list[dict[str, Any]]) -> dict[str, int]:
    """Return count of each invoice_type across all invoices."""
    counts: dict[str, int] = {t: 0 for t in _ALL_INVOICE_TYPES}
    for inv in invoices:
        itype = inv.get("invoice_type", "")
        if itype in counts:
            counts[itype] += 1
    return counts


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------


@router.get("/invoices")
async def list_zatca_invoices(
    status: str | None = Query(None, description="Filter by zatca_status"),
    invoice_type: str | None = Query(None, description="Filter by invoice_type"),
) -> dict[str, Any]:
    """List all ZATCA Phase 2 invoices with optional status and type filters."""
    invoices = list(ZATCA_INVOICES.values())

    if status is not None:
        if status not in _ALL_STATUSES:
            raise HTTPException(
                status_code=422,
                detail=(
                    f"Invalid status '{status}'. "
                    f"Allowed values: {sorted(_ALL_STATUSES)}"
                ),
            )
        invoices = [inv for inv in invoices if inv.get("zatca_status") == status]

    if invoice_type is not None:
        if invoice_type not in _ALL_INVOICE_TYPES:
            raise HTTPException(
                status_code=422,
                detail=(
                    f"Invalid invoice_type '{invoice_type}'. "
                    f"Allowed values: {sorted(_ALL_INVOICE_TYPES)}"
                ),
            )
        invoices = [inv for inv in invoices if inv.get("invoice_type") == invoice_type]

    sorted_invoices = sorted(invoices, key=lambda x: x.get("invoice_date", ""), reverse=True)

    return {
        "governance_decision": _GOV_READ,
        "generated_at": _now_iso(),
        "total": len(sorted_invoices),
        "filters_applied": {
            "status": status,
            "invoice_type": invoice_type,
        },
        "invoices": sorted_invoices,
    }


@router.get("/invoices/pending")
async def list_pending_zatca_invoices() -> dict[str, Any]:
    """List invoices requiring action: draft, signed, or rejected."""
    pending = [
        inv for inv in ZATCA_INVOICES.values()
        if inv.get("zatca_status") in _PENDING_STATUSES
    ]
    sorted_pending = sorted(
        pending,
        key=lambda x: x.get("invoice_date", ""),
        reverse=True,
    )

    by_status = _status_counts(sorted_pending)

    return {
        "governance_decision": _GOV_READ,
        "generated_at": _now_iso(),
        "total": len(sorted_pending),
        "by_status": by_status,
        "action_ar": "راجع الفواتير المعلقة وأرسلها إلى ZATCA في أقرب وقت",
        "action_en": "Review pending invoices and submit to ZATCA promptly",
        "invoices": sorted_pending,
    }


@router.get("/invoices/{invoice_id}")
async def get_zatca_invoice(invoice_id: str) -> dict[str, Any]:
    """Get full detail for a single ZATCA invoice. Returns 404 if not found."""
    inv = _get_invoice(invoice_id)
    return {
        "governance_decision": _GOV_READ,
        "generated_at": _now_iso(),
        **inv,
    }


@router.post("/invoices/{invoice_id}/submit")
async def submit_zatca_invoice(
    invoice_id: str,
    body: SubmitBody = Body(...),
) -> dict[str, Any]:
    """Submit a draft invoice to ZATCA for signing and clearance.

    Only invoices in 'draft' status may be submitted. Transitions the invoice
    to 'signed' status. Requires APPROVAL_FIRST governance.
    """
    inv = _get_invoice(invoice_id)

    if inv.get("zatca_status") != "draft":
        raise HTTPException(
            status_code=409,
            detail={
                "ar": (
                    f"لا يمكن إرسال الفاتورة — الحالة الحالية: "
                    f"'{inv.get('zatca_status')}'. "
                    "يمكن إرسال المسودات فقط."
                ),
                "en": (
                    f"Cannot submit invoice — current status: "
                    f"'{inv.get('zatca_status')}'. "
                    "Only draft invoices may be submitted."
                ),
            },
        )

    inv["zatca_status"] = "signed"
    inv["xml_hash"] = f"sha256_signed_{invoice_id.lower()}"
    inv["qr_code_b64"] = f"base64_qr_{invoice_id.lower()}"

    _log.info(
        "zatca_invoice_submitted",
        invoice_id=invoice_id,
        reason=body.reason,
    )

    return {
        "governance_decision": _GOV_MUTATE,
        "generated_at": _now_iso(),
        "invoice_id": invoice_id,
        "invoice_number": inv.get("invoice_number"),
        "previous_status": "draft",
        "new_status": "signed",
        "reason": body.reason,
        "message_ar": "تم إرسال الفاتورة للتوقيع — تنتظر التخليص من ZATCA",
        "message_en": "Invoice submitted for signing — awaiting ZATCA clearance",
    }


@router.post("/invoices/{invoice_id}/resubmit")
async def resubmit_zatca_invoice(
    invoice_id: str,
    body: ResubmitBody = Body(...),
) -> dict[str, Any]:
    """Resubmit a rejected invoice to ZATCA after corrections.

    Only invoices in 'rejected' status may be resubmitted. Transitions the
    invoice to 'signed' status. Requires APPROVAL_FIRST governance.
    """
    inv = _get_invoice(invoice_id)

    if inv.get("zatca_status") != "rejected":
        raise HTTPException(
            status_code=409,
            detail={
                "ar": (
                    f"لا يمكن إعادة إرسال الفاتورة — الحالة الحالية: "
                    f"'{inv.get('zatca_status')}'. "
                    "يمكن إعادة إرسال الفواتير المرفوضة فقط."
                ),
                "en": (
                    f"Cannot resubmit invoice — current status: "
                    f"'{inv.get('zatca_status')}'. "
                    "Only rejected invoices may be resubmitted."
                ),
            },
        )

    inv["zatca_status"] = "signed"
    inv["xml_hash"] = f"sha256_resubmitted_{invoice_id.lower()}"
    inv["qr_code_b64"] = f"base64_qr_resubmitted_{invoice_id.lower()}"
    inv.pop("rejection_reason", None)

    _log.info(
        "zatca_invoice_resubmitted",
        invoice_id=invoice_id,
        corrections_count=len(body.corrections),
        reason=body.reason,
    )

    return {
        "governance_decision": _GOV_MUTATE,
        "generated_at": _now_iso(),
        "invoice_id": invoice_id,
        "invoice_number": inv.get("invoice_number"),
        "previous_status": "rejected",
        "new_status": "signed",
        "reason": body.reason,
        "corrections_applied": body.corrections,
        "message_ar": "تمت إعادة إرسال الفاتورة بعد التصحيحات — تنتظر مراجعة ZATCA",
        "message_en": "Invoice resubmitted after corrections — awaiting ZATCA review",
    }


@router.get("/compliance-dashboard")
async def get_compliance_dashboard() -> dict[str, Any]:
    """Overall ZATCA Phase 2 compliance metrics for the current period."""
    all_invoices = list(ZATCA_INVOICES.values())
    by_status = _status_counts(all_invoices)
    compliance_rate = _compute_compliance_rate(all_invoices)
    avg_score = _compute_avg_score(all_invoices)
    total_vat = _sum_positive_vat(all_invoices)
    total_revenue = _sum_positive_revenue(all_invoices)

    pending_clearance_count = sum(
        1 for inv in all_invoices if inv.get("zatca_status") == "signed"
    )
    rejected_count = by_status.get("rejected", 0)

    seller_vat = all_invoices[0].get("seller_vat", "") if all_invoices else ""
    report_month = datetime.now(UTC).strftime("%Y-%m")

    return {
        "governance_decision": _GOV_READ,
        "generated_at": _now_iso(),
        "total_invoices": len(all_invoices),
        "by_status": by_status,
        "compliance_rate": compliance_rate,
        "avg_compliance_score": avg_score,
        "total_vat_collected_sar": total_vat,
        "total_revenue_sar": total_revenue,
        "pending_clearance_count": pending_clearance_count,
        "rejected_count": rejected_count,
        "phase2_active": True,
        "seller_vat": seller_vat,
        "report_month": report_month,
    }


@router.get("/vat-summary")
async def get_vat_summary() -> dict[str, Any]:
    """VAT breakdown for current reporting period.

    Input VAT is a placeholder — full computation requires AP integration.
    All figures should be cross-checked against the official ZATCA portal.
    """
    all_invoices = list(ZATCA_INVOICES.values())
    period = datetime.now(UTC).strftime("%Y-%m")

    type_counts = _build_vat_type_counts(all_invoices)

    # Output VAT: sum positive vat_amount_sar for standard and simplified invoices
    output_vat = round(
        sum(
            float(inv.get("vat_amount_sar", 0))
            for inv in all_invoices
            if inv.get("invoice_type") in {"standard", "simplified"}
            and float(inv.get("vat_amount_sar", 0)) > 0
        ),
        2,
    )

    input_vat = 0.0  # requires AP (accounts payable) integration

    return {
        "governance_decision": _GOV_READ,
        "generated_at": _now_iso(),
        "period": period,
        "output_vat_sar": output_vat,
        "input_vat_sar": input_vat,
        "net_vat_payable_sar": round(output_vat - input_vat, 2),
        "standard_invoices": type_counts["standard"],
        "simplified_invoices": type_counts["simplified"],
        "credit_notes": type_counts["credit_note"],
        "debit_notes": type_counts["debit_note"],
        "vat_rate": 0.15,
        "note": "VAT figures are estimates. Official figures from ZATCA portal.",
    }
