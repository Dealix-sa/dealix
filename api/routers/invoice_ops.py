"""Invoice Operations API — ZATCA Phase 2 compliant invoice lifecycle management.

Endpoints:
  GET  /api/v1/invoices                   — all invoices with summary
  GET  /api/v1/invoices/overdue           — overdue invoices with days_overdue
  GET  /api/v1/invoices/zatca-compliance  — ZATCA compliance summary
  GET  /api/v1/invoices/{invoice_id}      — full invoice detail
  POST /api/v1/invoices                   — create new invoice draft
  POST /api/v1/invoices/{invoice_id}/issue      — move draft to issued
  POST /api/v1/invoices/{invoice_id}/mark-paid  — mark invoice as paid

All admin-gated.
Read endpoints: governance_decision = ALLOW_WITH_REVIEW
Mutating endpoints: governance_decision = APPROVAL_FIRST
"""

from __future__ import annotations

from datetime import UTC, date, datetime, timedelta
from typing import Any

from fastapi import APIRouter, Body, Depends, HTTPException
from pydantic import BaseModel, ConfigDict, Field

from api.security.api_key import require_admin_key
from core.logging import get_logger

_log = get_logger(__name__)

router = APIRouter(
    prefix="/api/v1/invoices",
    tags=["invoice-ops"],
    dependencies=[Depends(require_admin_key)],
)

_GOV_READ = "ALLOW_WITH_REVIEW"
_GOV_MUTATE = "APPROVAL_FIRST"

_VALID_STATES = {"draft", "issued", "paid", "overdue", "cancelled"}
_VALID_ZATCA_STATUSES = {"reported", "cleared", "pending", None}
_VALID_INVOICE_TYPES = {"standard", "simplified"}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _now_iso() -> str:
    """Return current UTC timestamp as ISO-8601 string."""
    return datetime.now(UTC).isoformat()


def _today_str() -> str:
    """Return today's date as YYYY-MM-DD string."""
    return date.today().isoformat()


def _days_overdue(due_date_str: str) -> int:
    """Return number of days past the due date (0 if not yet overdue)."""
    try:
        due = date.fromisoformat(due_date_str)
        delta = date.today() - due
        return max(0, delta.days)
    except ValueError:
        return 0


def _compute_vat(amount: float) -> float:
    """Return 15% VAT for the given amount, rounded to 2 decimal places."""
    return round(amount * 0.15, 2)


# ---------------------------------------------------------------------------
# Demo data — 10 invoices INV-001 through INV-010
# ---------------------------------------------------------------------------

_INVOICES: dict[str, dict[str, Any]] = {
    "INV-001": {
        "invoice_id": "INV-001",
        "client_id": "CLT-001",
        "company_ar": "شركة الرياض للتقنية",
        "company_en": "Riyadh Tech Co",
        "invoice_number": "INV-2026-001",
        "issue_date": "2026-03-01",
        "due_date": "2026-03-31",
        "amount_sar": 10000.00,
        "vat_15_sar": 1500.00,
        "total_with_vat_sar": 11500.00,
        "state": "paid",
        "payment_method": "bank_transfer",
        "paid_at": "2026-03-25T10:00:00+00:00",
        "zatca_status": "cleared",
        "invoice_type": "standard",
        "line_items": [
            {
                "description_ar": "خدمات استشارية — الربع الأول",
                "description_en": "Consulting Services — Q1",
                "quantity": 1,
                "unit_price_sar": 10000.00,
                "line_total_sar": 10000.00,
            }
        ],
        "uuid": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    },
    "INV-002": {
        "invoice_id": "INV-002",
        "client_id": "CLT-002",
        "company_ar": "مجموعة الخليج للخدمات المالية",
        "company_en": "Gulf Financial Services Group",
        "invoice_number": "INV-2026-002",
        "issue_date": "2026-03-15",
        "due_date": "2026-04-14",
        "amount_sar": 4999.00,
        "vat_15_sar": 749.85,
        "total_with_vat_sar": 5748.85,
        "state": "paid",
        "payment_method": "moyasar_card",
        "paid_at": "2026-04-10T14:30:00+00:00",
        "zatca_status": "reported",
        "invoice_type": "simplified",
        "line_items": [
            {
                "description_ar": "اشتراك شهري — المؤسسي",
                "description_en": "Monthly Subscription — Enterprise",
                "quantity": 1,
                "unit_price_sar": 4999.00,
                "line_total_sar": 4999.00,
            }
        ],
        "uuid": "b2c3d4e5-f6a7-8901-bcde-f12345678901",
    },
    "INV-003": {
        "invoice_id": "INV-003",
        "client_id": "CLT-003",
        "company_ar": "شركة سفا للخدمات اللوجستية",
        "company_en": "Safa Logistics Co",
        "invoice_number": "INV-2026-003",
        "issue_date": "2026-04-01",
        "due_date": "2026-05-01",
        "amount_sar": 2999.00,
        "vat_15_sar": 449.85,
        "total_with_vat_sar": 3448.85,
        "state": "overdue",
        "payment_method": None,
        "paid_at": None,
        "zatca_status": "pending",
        "invoice_type": "standard",
        "line_items": [
            {
                "description_ar": "اشتراك شهري — الأساسي",
                "description_en": "Monthly Subscription — Essential",
                "quantity": 1,
                "unit_price_sar": 2999.00,
                "line_total_sar": 2999.00,
            }
        ],
        "uuid": "c3d4e5f6-a7b8-9012-cdef-123456789012",
    },
    "INV-004": {
        "invoice_id": "INV-004",
        "client_id": "CLT-004",
        "company_ar": "تمكين الصحية",
        "company_en": "Tamkeen Health Tech",
        "invoice_number": "INV-2026-004",
        "issue_date": "2026-04-15",
        "due_date": "2026-05-15",
        "amount_sar": 3999.00,
        "vat_15_sar": 599.85,
        "total_with_vat_sar": 4598.85,
        "state": "issued",
        "payment_method": None,
        "paid_at": None,
        "zatca_status": "cleared",
        "invoice_type": "standard",
        "line_items": [
            {
                "description_ar": "اشتراك شهري — الاحترافي",
                "description_en": "Monthly Subscription — Professional",
                "quantity": 1,
                "unit_price_sar": 3999.00,
                "line_total_sar": 3999.00,
            }
        ],
        "uuid": "d4e5f6a7-b8c9-0123-defa-234567890123",
    },
    "INV-005": {
        "invoice_id": "INV-005",
        "client_id": "CLT-005",
        "company_ar": "شركة جازان للتصنيع",
        "company_en": "Jazan Manufacturing Co",
        "invoice_number": "INV-2026-005",
        "issue_date": "2026-04-20",
        "due_date": "2026-05-20",
        "amount_sar": 15000.00,
        "vat_15_sar": 2250.00,
        "total_with_vat_sar": 17250.00,
        "state": "overdue",
        "payment_method": None,
        "paid_at": None,
        "zatca_status": "reported",
        "invoice_type": "simplified",
        "line_items": [
            {
                "description_ar": "تطوير منصة الذكاء الاصطناعي المخصص",
                "description_en": "Custom AI Platform Development",
                "quantity": 1,
                "unit_price_sar": 15000.00,
                "line_total_sar": 15000.00,
            }
        ],
        "uuid": "e5f6a7b8-c9d0-1234-efab-345678901234",
    },
    "INV-006": {
        "invoice_id": "INV-006",
        "client_id": "CLT-006",
        "company_ar": "الوافي للتمويل",
        "company_en": "Al-Wafi Finance",
        "invoice_number": "INV-2026-006",
        "issue_date": "2026-05-01",
        "due_date": "2026-05-31",
        "amount_sar": 1500.00,
        "vat_15_sar": 225.00,
        "total_with_vat_sar": 1725.00,
        "state": "issued",
        "payment_method": None,
        "paid_at": None,
        "zatca_status": None,
        "invoice_type": "simplified",
        "line_items": [
            {
                "description_ar": "حزمة البيانات الشهرية",
                "description_en": "Monthly Data Pack",
                "quantity": 1,
                "unit_price_sar": 1500.00,
                "line_total_sar": 1500.00,
            }
        ],
        "uuid": None,
    },
    "INV-007": {
        "invoice_id": "INV-007",
        "client_id": "CLT-007",
        "company_ar": "شركة الأفق للتقنية",
        "company_en": "Horizon Technology Co",
        "invoice_number": "INV-2026-007",
        "issue_date": "2026-05-10",
        "due_date": "2026-06-09",
        "amount_sar": 3999.00,
        "vat_15_sar": 599.85,
        "total_with_vat_sar": 4598.85,
        "state": "draft",
        "payment_method": None,
        "paid_at": None,
        "zatca_status": None,
        "invoice_type": "standard",
        "line_items": [
            {
                "description_ar": "اشتراك شهري — الاحترافي",
                "description_en": "Monthly Subscription — Professional",
                "quantity": 1,
                "unit_price_sar": 3999.00,
                "line_total_sar": 3999.00,
            }
        ],
        "uuid": None,
    },
    "INV-008": {
        "invoice_id": "INV-008",
        "client_id": "CLT-008",
        "company_ar": "مجموعة الريادة للاستشارات",
        "company_en": "Riyadah Consulting Group",
        "invoice_number": "INV-2026-008",
        "issue_date": "2026-05-15",
        "due_date": "2026-06-14",
        "amount_sar": 8500.00,
        "vat_15_sar": 1275.00,
        "total_with_vat_sar": 9775.00,
        "state": "draft",
        "payment_method": None,
        "paid_at": None,
        "zatca_status": None,
        "invoice_type": "standard",
        "line_items": [
            {
                "description_ar": "تحليل السوق وخدمات الاستشارة الاستراتيجية",
                "description_en": "Market Analysis and Strategic Consulting",
                "quantity": 2,
                "unit_price_sar": 4250.00,
                "line_total_sar": 8500.00,
            }
        ],
        "uuid": None,
    },
    "INV-009": {
        "invoice_id": "INV-009",
        "client_id": "CLT-009",
        "company_ar": "شركة النخبة الطبية",
        "company_en": "Elite Medical Co",
        "invoice_number": "INV-2026-009",
        "issue_date": "2026-02-01",
        "due_date": "2026-03-01",
        "amount_sar": 4999.00,
        "vat_15_sar": 749.85,
        "total_with_vat_sar": 5748.85,
        "state": "cancelled",
        "payment_method": None,
        "paid_at": None,
        "zatca_status": None,
        "invoice_type": "simplified",
        "line_items": [
            {
                "description_ar": "اشتراك شهري — المؤسسي",
                "description_en": "Monthly Subscription — Enterprise",
                "quantity": 1,
                "unit_price_sar": 4999.00,
                "line_total_sar": 4999.00,
            }
        ],
        "uuid": None,
    },
    "INV-010": {
        "invoice_id": "INV-010",
        "client_id": "CLT-010",
        "company_ar": "التوسع العقاري السعودي",
        "company_en": "Saudi Real Estate Expansion",
        "invoice_number": "INV-2026-010",
        "issue_date": "2026-05-20",
        "due_date": "2026-06-19",
        "amount_sar": 3999.00,
        "vat_15_sar": 599.85,
        "total_with_vat_sar": 4598.85,
        "state": "issued",
        "payment_method": None,
        "paid_at": None,
        "zatca_status": "cleared",
        "invoice_type": "standard",
        "line_items": [
            {
                "description_ar": "اشتراك شهري — الاحترافي",
                "description_en": "Monthly Subscription — Professional",
                "quantity": 1,
                "unit_price_sar": 3999.00,
                "line_total_sar": 3999.00,
            }
        ],
        "uuid": "f6a7b8c9-d0e1-2345-fabc-456789012345",
    },
}

# Counter for generating new invoice IDs — starts after INV-010
_INVOICE_COUNTER: list[int] = [10]


# ---------------------------------------------------------------------------
# Internal lookup helpers
# ---------------------------------------------------------------------------


def _get_invoice(invoice_id: str) -> dict[str, Any]:
    """Return invoice dict or raise HTTP 404."""
    inv = _INVOICES.get(invoice_id.upper())
    if inv is None:
        raise HTTPException(
            status_code=404,
            detail={
                "ar": f"الفاتورة '{invoice_id}' غير موجودة",
                "en": f"Invoice '{invoice_id}' not found",
            },
        )
    return inv


def _build_vat_breakdown(inv: dict[str, Any]) -> dict[str, Any]:
    """Return a structured VAT breakdown for a single invoice."""
    return {
        "subtotal_sar": inv["amount_sar"],
        "vat_rate_pct": 15.0,
        "vat_amount_sar": inv["vat_15_sar"],
        "total_with_vat_sar": inv["total_with_vat_sar"],
        "label_ar": "ضريبة القيمة المضافة 15%",
        "label_en": "VAT 15%",
    }


def _enrich_invoice(inv: dict[str, Any]) -> dict[str, Any]:
    """Return invoice with optional days_overdue added."""
    enriched = dict(inv)
    if inv["state"] == "overdue":
        enriched["days_overdue"] = _days_overdue(inv["due_date"])
    return enriched


def _next_invoice_id() -> str:
    """Generate the next sequential invoice ID."""
    _INVOICE_COUNTER[0] += 1
    return f"INV-{_INVOICE_COUNTER[0]:03d}"


# ---------------------------------------------------------------------------
# Pydantic request models
# ---------------------------------------------------------------------------


class LineItemBody(BaseModel):
    model_config = ConfigDict(extra="forbid")

    description_ar: str = Field(min_length=1)
    description_en: str = Field(min_length=1)
    quantity: int = Field(ge=1)
    unit_price_sar: float = Field(gt=0)


class CreateInvoiceBody(BaseModel):
    model_config = ConfigDict(extra="forbid")

    client_id: str = Field(min_length=1)
    company_ar: str = Field(min_length=1)
    company_en: str = Field(min_length=1)
    line_items: list[LineItemBody] = Field(min_length=1)
    invoice_type: str = Field(default="standard")
    due_days: int = Field(default=30, ge=1, le=180)


class IssueBody(BaseModel):
    model_config = ConfigDict(extra="forbid")

    reason: str = Field(min_length=5)


class MarkPaidBody(BaseModel):
    model_config = ConfigDict(extra="forbid")

    payment_method: str = Field(min_length=1)
    payment_date: str = Field(min_length=10)
    notes: str | None = None


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------


@router.get("/overdue")
async def list_overdue_invoices() -> dict[str, Any]:
    """All overdue invoices enriched with days_overdue and bilingual action text."""
    overdue = [
        inv for inv in _INVOICES.values()
        if inv["state"] == "overdue"
    ]
    enriched = []
    for inv in sorted(overdue, key=lambda x: x["issue_date"], reverse=True):
        item = dict(inv)
        item["days_overdue"] = _days_overdue(inv["due_date"])
        enriched.append(item)

    oldest_days = max((e["days_overdue"] for e in enriched), default=0)
    total_overdue_sar = sum(inv["total_with_vat_sar"] for inv in overdue)

    return {
        "governance_decision": _GOV_READ,
        "generated_at": _now_iso(),
        "overdue_count": len(enriched),
        "total_overdue_sar": round(total_overdue_sar, 2),
        "oldest_overdue_days": oldest_days,
        "action_ar": "تواصل مع العملاء فوراً وأرسل إشعار السداد",
        "action_en": "Contact clients immediately and send payment reminder",
        "invoices": enriched,
    }


@router.get("/zatca-compliance")
async def zatca_compliance_summary() -> dict[str, Any]:
    """ZATCA Phase 2 compliance summary across all invoices."""
    all_invoices = list(_INVOICES.values())
    total = len(all_invoices)
    compliant_statuses = {"reported", "cleared"}

    compliant = [inv for inv in all_invoices if inv["zatca_status"] in compliant_statuses]
    non_compliant = total - len(compliant)
    compliance_rate = round(len(compliant) / total * 100, 1) if total > 0 else 0.0

    by_status: dict[str, int] = {}
    for inv in all_invoices:
        status_key = inv["zatca_status"] if inv["zatca_status"] else "none"
        by_status[status_key] = by_status.get(status_key, 0) + 1

    return {
        "governance_decision": _GOV_READ,
        "generated_at": _now_iso(),
        "total_invoices": total,
        "compliant_count": len(compliant),
        "non_compliant": non_compliant,
        "compliance_rate_pct": compliance_rate,
        "by_status": by_status,
        "action_ar": "راجع الفواتير غير المتوافقة وأرسلها لـ ZATCA",
        "action_en": "Review non-compliant invoices and submit to ZATCA",
    }


@router.get("/{invoice_id}")
async def get_invoice(invoice_id: str) -> dict[str, Any]:
    """Full invoice detail including vat_breakdown. Returns 404 if not found."""
    inv = _get_invoice(invoice_id)
    enriched = _enrich_invoice(inv)
    return {
        "governance_decision": _GOV_READ,
        "generated_at": _now_iso(),
        **enriched,
        "vat_breakdown": _build_vat_breakdown(inv),
    }


@router.get("/")
async def list_invoices() -> dict[str, Any]:
    """All invoices sorted by issue_date descending with portfolio summary."""
    all_invoices = list(_INVOICES.values())
    sorted_invoices = sorted(all_invoices, key=lambda x: x["issue_date"], reverse=True)
    enriched = [_enrich_invoice(inv) for inv in sorted_invoices]

    total_outstanding = sum(
        inv["total_with_vat_sar"]
        for inv in all_invoices
        if inv["state"] in {"issued", "overdue"}
    )
    total_paid = sum(
        inv["total_with_vat_sar"]
        for inv in all_invoices
        if inv["state"] == "paid"
    )
    overdue_count = sum(1 for inv in all_invoices if inv["state"] == "overdue")
    compliant_count = sum(
        1 for inv in all_invoices
        if inv["zatca_status"] in {"reported", "cleared"}
    )
    zatca_compliance_rate = round(compliant_count / len(all_invoices) * 100, 1) if all_invoices else 0.0

    return {
        "governance_decision": _GOV_READ,
        "generated_at": _now_iso(),
        "summary": {
            "total_invoices": len(all_invoices),
            "total_outstanding_sar": round(total_outstanding, 2),
            "total_paid_sar": round(total_paid, 2),
            "overdue_count": overdue_count,
            "zatca_compliance_rate": zatca_compliance_rate,
        },
        "invoices": enriched,
    }


@router.post("/")
async def create_invoice(body: CreateInvoiceBody = Body(...)) -> dict[str, Any]:
    """Create a new invoice draft. Auto-computes amounts from line_items."""
    if body.invoice_type not in _VALID_INVOICE_TYPES:
        raise HTTPException(
            status_code=422,
            detail=f"invoice_type must be one of: {sorted(_VALID_INVOICE_TYPES)}",
        )

    # Compute totals from line items
    computed_items: list[dict[str, Any]] = []
    amount_sar = 0.0
    for item in body.line_items:
        line_total = round(item.quantity * item.unit_price_sar, 2)
        amount_sar += line_total
        computed_items.append({
            "description_ar": item.description_ar,
            "description_en": item.description_en,
            "quantity": item.quantity,
            "unit_price_sar": item.unit_price_sar,
            "line_total_sar": line_total,
        })

    amount_sar = round(amount_sar, 2)
    vat_15_sar = _compute_vat(amount_sar)
    total_with_vat_sar = round(amount_sar + vat_15_sar, 2)

    today = _today_str()
    issue_dt = date.fromisoformat(today)
    due_date_str = (issue_dt + timedelta(days=body.due_days)).isoformat()

    new_id = _next_invoice_id()
    invoice_number = f"INV-{_today_str().replace('-', '')}-{_INVOICE_COUNTER[0]:03d}"

    new_invoice: dict[str, Any] = {
        "invoice_id": new_id,
        "client_id": body.client_id,
        "company_ar": body.company_ar,
        "company_en": body.company_en,
        "invoice_number": invoice_number,
        "issue_date": today,
        "due_date": due_date_str,
        "amount_sar": amount_sar,
        "vat_15_sar": vat_15_sar,
        "total_with_vat_sar": total_with_vat_sar,
        "state": "draft",
        "payment_method": None,
        "paid_at": None,
        "zatca_status": None,
        "invoice_type": body.invoice_type,
        "line_items": computed_items,
        "uuid": None,
    }

    _INVOICES[new_id] = new_invoice

    _log.info(
        "invoice_created",
        invoice_id=new_id,
        client_id=body.client_id,
        amount_sar=amount_sar,
    )

    return {
        "governance_decision": _GOV_MUTATE,
        "generated_at": _now_iso(),
        "invoice": new_invoice,
        "vat_breakdown": _build_vat_breakdown(new_invoice),
        "message_ar": "تم إنشاء مسودة الفاتورة — تحتاج موافقة المؤسس قبل الإصدار",
        "message_en": "Invoice draft created — requires founder approval before issuing",
    }


@router.post("/{invoice_id}/issue")
async def issue_invoice(invoice_id: str, body: IssueBody = Body(...)) -> dict[str, Any]:
    """Move an invoice from draft to issued state."""
    inv = _get_invoice(invoice_id)

    if inv["state"] != "draft":
        raise HTTPException(
            status_code=400,
            detail={
                "ar": f"لا يمكن إصدار الفاتورة — الحالة الحالية: {inv['state']}",
                "en": f"Cannot issue invoice — current state: {inv['state']}",
            },
        )

    inv["state"] = "issued"

    _log.info("invoice_issued", invoice_id=invoice_id, reason=body.reason)

    return {
        "governance_decision": _GOV_MUTATE,
        "generated_at": _now_iso(),
        "invoice_id": invoice_id,
        "new_state": "issued",
        "reason": body.reason,
        "invoice": inv,
        "message_ar": "تم إصدار الفاتورة — تحتاج موافقة المؤسس قبل الإرسال للعميل",
        "message_en": "Invoice issued — requires founder approval before sending to client",
    }


@router.post("/{invoice_id}/mark-paid")
async def mark_invoice_paid(invoice_id: str, body: MarkPaidBody = Body(...)) -> dict[str, Any]:
    """Mark an invoice as paid with payment details."""
    inv = _get_invoice(invoice_id)

    if inv["state"] in {"paid", "cancelled"}:
        raise HTTPException(
            status_code=400,
            detail={
                "ar": f"لا يمكن تسجيل الدفع — الحالة الحالية: {inv['state']}",
                "en": f"Cannot mark as paid — current state: {inv['state']}",
            },
        )

    inv["state"] = "paid"
    inv["payment_method"] = body.payment_method
    inv["paid_at"] = body.payment_date

    _log.info(
        "invoice_marked_paid",
        invoice_id=invoice_id,
        payment_method=body.payment_method,
    )

    return {
        "governance_decision": _GOV_MUTATE,
        "generated_at": _now_iso(),
        "invoice_id": invoice_id,
        "new_state": "paid",
        "payment_method": body.payment_method,
        "payment_date": body.payment_date,
        "notes": body.notes,
        "invoice": inv,
        "message_ar": "تم تسجيل السداد — تحتاج موافقة المؤسس للتأكيد النهائي",
        "message_en": "Payment recorded — requires founder approval for final confirmation",
    }
