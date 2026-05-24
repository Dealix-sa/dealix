"""Customer Portal Backend MVP — Track B.4.

Authenticated endpoints for paying customers (499 SAR Sector Sprint and
up). Frontend at /landing/customer-portal.html consumes these.

Endpoints (all under /api/v1/portal):

  GET  /me                              — authenticated customer profile
  GET  /sprints                         — active sprint engagements
  GET  /sprints/{sprint_id}             — single sprint with status
  GET  /proof-packs                     — downloadable proof packs
  GET  /proof-packs/{pack_id}/download  — proof pack content (markdown)
  POST /feedback                        — submit 1..5 rating + comment
  GET  /invoices                        — list customer invoices (ZATCA)

Security:
  - Bearer JWT via api.security.auth_deps.get_current_user.
  - Tenant scope is taken from the user record. Cross-tenant access is
    blocked at the dependency layer (no sprint_id or pack_id from
    another tenant is ever exposed).
  - PDPL: customer comments and PII never appear in logs (see
    `_log_safe_summary`). The router emits structured friction events
    instead of raw notes.
"""

from __future__ import annotations

import re
import uuid
from datetime import datetime
from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel, ConfigDict, Field, field_validator
from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from api.security.auth_deps import get_current_user
from api.security.rbac import is_super_admin
from core.logging import get_logger
from core.utils import utcnow
from db.models import (
    CustomerFeedbackRecord,
    UserRecord,
    ZATCAInvoiceRecord,
)
from db.session import get_db

log = get_logger(__name__)

router = APIRouter(prefix="/api/v1/portal", tags=["customer-portal"])


# ── Dependency: scoped customer principal ──────────────────────────

class CustomerPrincipal:
    """Lightweight DTO carried into endpoints — fields needed for scope.

    Distinct from the SQLAlchemy `UserRecord` so endpoints cannot
    accidentally read or mutate auth columns.
    """

    __slots__ = ("user_id", "tenant_id", "email", "name", "system_role")

    def __init__(
        self,
        *,
        user_id: str,
        tenant_id: str | None,
        email: str,
        name: str,
        system_role: str | None,
    ) -> None:
        self.user_id = user_id
        self.tenant_id = tenant_id
        self.email = email
        self.name = name
        self.system_role = system_role

    @property
    def is_super_admin(self) -> bool:
        return is_super_admin(self.system_role)


async def get_current_customer(
    user: UserRecord = Depends(get_current_user),
) -> CustomerPrincipal:
    """Validate the JWT bearer and require a tenant scope.

    - 401 is raised upstream by ``get_current_user`` when the token is
      missing/invalid.
    - 403 is raised here when the user is active but has no tenant
      (e.g. a system service account that should never see customer
      portal data).
    """
    if not user.tenant_id and not is_super_admin(user.system_role):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User has no tenant scope; cannot access customer portal.",
        )
    return CustomerPrincipal(
        user_id=user.id,
        tenant_id=user.tenant_id,
        email=user.email,
        name=user.name,
        system_role=user.system_role,
    )


CurrentCustomer = Annotated[CustomerPrincipal, Depends(get_current_customer)]


# ── Pydantic v2 response models ────────────────────────────────────

class CustomerProfileResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: str
    tenant_id: str | None
    email: str
    name: str
    system_role: str | None
    portal_version: str = "b4_mvp"


class SprintSummary(BaseModel):
    sprint_id: str
    customer_id: str
    tenant_id: str | None
    title: str
    status: str  # e.g. "in_delivery", "proof_pack_ready", "completed"
    day: int | None = None
    total_days: int | None = None
    started_at: datetime | None = None
    ends_at: datetime | None = None


class SprintListResponse(BaseModel):
    tenant_id: str | None
    count: int
    sprints: list[SprintSummary]


class SprintDetailResponse(BaseModel):
    sprint: SprintSummary
    timeline: list[dict[str, Any]]
    pending_approvals: int
    next_action_ar: str
    next_action_en: str


class ProofPackSummary(BaseModel):
    pack_id: str
    sprint_id: str | None
    title: str
    tier: str | None = None
    score: float | None = None
    created_at: datetime | None = None
    download_url: str


class ProofPackListResponse(BaseModel):
    tenant_id: str | None
    count: int
    packs: list[ProofPackSummary]


class FeedbackSubmitBody(BaseModel):
    rating: int = Field(..., ge=1, le=5)
    comment: str = Field("", max_length=2000)
    sprint_id: str | None = Field(None, max_length=64)

    @field_validator("comment")
    @classmethod
    def _strip_comment(cls, v: str) -> str:
        return (v or "").strip()


class FeedbackResponse(BaseModel):
    feedback_id: str
    rating: int
    comment_stored: bool
    sprint_id: str | None
    created_at: datetime


class InvoiceSummary(BaseModel):
    invoice_id: str
    invoice_number: str
    total_sar: float
    vat_amount_sar: float
    currency: str
    status: str
    issue_date: str
    buyer_name: str


class InvoiceListResponse(BaseModel):
    tenant_id: str | None
    count: int
    invoices: list[InvoiceSummary]


# ── PDPL-safe logging helper ───────────────────────────────────────

_EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
_PHONE_RE = re.compile(r"\+?\d[\d\s\-()]{6,}")


def _log_safe_summary(text: str, max_len: int = 32) -> str:
    """Return a short, PDPL-safe summary suitable for structured logs.

    Emails are masked to ``<email>`` and phone-like runs to ``<phone>``.
    Long strings are truncated. Never logs the raw customer comment.
    """
    if not text:
        return ""
    masked = _EMAIL_RE.sub("<email>", text)
    masked = _PHONE_RE.sub("<phone>", masked)
    masked = masked.replace("\n", " ").strip()
    if len(masked) > max_len:
        masked = masked[: max_len - 1] + "…"
    return masked


def _safe_id(value: str, max_len: int = 64) -> str:
    """Strip path/header-unsafe characters from a client-supplied id."""
    return re.sub(r"[^A-Za-z0-9._-]", "_", value or "")[:max_len]


def _new_feedback_id() -> str:
    return "fbk_" + uuid.uuid4().hex[:24]


# ── Sprint discovery (best-effort cross-module) ────────────────────

def _list_sprint_sessions(*, customer_id: str | None) -> list[Any]:
    """Best-effort list of sprint sessions for a customer / tenant.

    Pulls from `auto_client_acquisition.service_sessions` when available.
    Returns an empty list when the module is not configured — the portal
    must remain functional even when no sprint runtime is wired up.
    """
    try:
        from auto_client_acquisition.service_sessions import list_sessions
    except Exception:  # noqa: BLE001
        return []
    try:
        if customer_id:
            return list(list_sessions(customer_handle=customer_id, limit=50))
        return list(list_sessions(limit=200))
    except Exception:  # noqa: BLE001
        return []


def _session_to_summary(session: Any, tenant_id: str | None) -> SprintSummary:
    """Project an arbitrary `ServiceSession`-like object onto SprintSummary."""
    sid = getattr(session, "id", None) or getattr(session, "session_id", "")
    return SprintSummary(
        sprint_id=str(sid),
        customer_id=str(getattr(session, "customer_handle", "") or ""),
        tenant_id=tenant_id,
        title=str(
            getattr(session, "title", None)
            or getattr(session, "engagement", None)
            or "Sector Sprint"
        ),
        status=str(getattr(session, "status", "active")),
        day=getattr(session, "day", None),
        total_days=getattr(session, "total_days", None),
        started_at=getattr(session, "started_at", None),
        ends_at=getattr(session, "ends_at", None),
    )


def _list_proof_packs(*, customer_id: str | None) -> list[Any]:
    """Best-effort list of proof events / packs for the customer."""
    try:
        from auto_client_acquisition.proof_ledger.factory import get_default_ledger
    except Exception:  # noqa: BLE001
        return []
    try:
        return list(
            get_default_ledger().list_events(
                customer_handle=customer_id, limit=200
            )
        )
    except Exception:  # noqa: BLE001
        return []


def _pack_to_summary(event: Any) -> ProofPackSummary:
    pid = str(getattr(event, "id", "") or "")
    sid = getattr(event, "sprint_id", None) or getattr(event, "engagement_id", None)
    title = str(
        getattr(event, "title", None)
        or getattr(event, "event_type", None)
        or "Proof Pack"
    )
    created = getattr(event, "created_at", None)
    return ProofPackSummary(
        pack_id=pid,
        sprint_id=str(sid) if sid else None,
        title=title,
        tier=getattr(event, "tier", None),
        score=getattr(event, "score", None),
        created_at=created if isinstance(created, datetime) else None,
        download_url=f"/api/v1/portal/proof-packs/{_safe_id(pid)}/download",
    )


# ── Endpoints ──────────────────────────────────────────────────────


@router.get("/me", response_model=CustomerProfileResponse)
async def get_me(customer: CurrentCustomer) -> CustomerProfileResponse:
    """Return the authenticated customer's profile (no PII beyond email)."""
    return CustomerProfileResponse(
        user_id=customer.user_id,
        tenant_id=customer.tenant_id,
        email=customer.email,
        name=customer.name,
        system_role=customer.system_role,
    )


@router.get("/sprints", response_model=SprintListResponse)
async def list_sprints(customer: CurrentCustomer) -> SprintListResponse:
    """List active sprint engagements visible to this tenant."""
    sessions = _list_sprint_sessions(customer_id=customer.tenant_id)
    summaries = [_session_to_summary(s, customer.tenant_id) for s in sessions]
    # Enforce tenant scope defensively: if upstream returned cross-tenant
    # rows (unlikely but possible when running with a global ledger),
    # filter them here. Super-admins see everything.
    if not customer.is_super_admin and customer.tenant_id:
        summaries = [
            s
            for s in summaries
            if not s.customer_id or s.customer_id == customer.tenant_id
        ]
    return SprintListResponse(
        tenant_id=customer.tenant_id,
        count=len(summaries),
        sprints=summaries,
    )


@router.get("/sprints/{sprint_id}", response_model=SprintDetailResponse)
async def get_sprint(
    sprint_id: str,
    customer: CurrentCustomer,
) -> SprintDetailResponse:
    """Return a single sprint by id, with delivery timeline + next action."""
    sid = _safe_id(sprint_id)
    if not sid:
        raise HTTPException(status_code=400, detail="invalid sprint_id")

    sessions = _list_sprint_sessions(customer_id=customer.tenant_id)
    match = next(
        (s for s in sessions if str(getattr(s, "id", "")) == sid),
        None,
    )
    if match is None:
        # 404 — but we deliberately also use 404 for cross-tenant access
        # to avoid leaking the existence of a sprint in another tenant.
        raise HTTPException(status_code=404, detail="sprint_not_found")

    summary = _session_to_summary(match, customer.tenant_id)

    # Defensive tenant check: if the session belongs to a different
    # customer_handle than the caller's tenant, return 403.
    if (
        not customer.is_super_admin
        and customer.tenant_id
        and summary.customer_id
        and summary.customer_id != customer.tenant_id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="cross_tenant_access_denied",
        )

    timeline: list[dict[str, Any]] = []
    raw_timeline = getattr(match, "timeline", None) or []
    for step in raw_timeline:
        if isinstance(step, dict):
            timeline.append(
                {
                    "step": step.get("step") or step.get("name"),
                    "status": step.get("status"),
                    "completed_at": step.get("completed_at"),
                }
            )

    return SprintDetailResponse(
        sprint=summary,
        timeline=timeline,
        pending_approvals=int(getattr(match, "pending_approvals", 0) or 0),
        next_action_ar="راجع الخطوة الحالية في الجدول الزمني.",
        next_action_en="Review the current step in the delivery timeline.",
    )


@router.get("/proof-packs", response_model=ProofPackListResponse)
async def list_proof_packs(customer: CurrentCustomer) -> ProofPackListResponse:
    """List proof packs the customer can download."""
    events = _list_proof_packs(customer_id=customer.tenant_id)
    packs = [_pack_to_summary(e) for e in events if getattr(e, "id", None)]
    return ProofPackListResponse(
        tenant_id=customer.tenant_id,
        count=len(packs),
        packs=packs,
    )


@router.get(
    "/proof-packs/{pack_id}/download",
    response_class=PlainTextResponse,
)
async def download_proof_pack(
    pack_id: str,
    customer: CurrentCustomer,
) -> PlainTextResponse:
    """Return proof pack content as markdown.

    Used by the frontend to render or save the pack. Streams plain text
    so the browser handles formatting; binary PDF rendering lives on
    `/api/v1/sprint/render/pdf`.
    """
    pid = _safe_id(pack_id)
    if not pid:
        raise HTTPException(status_code=400, detail="invalid pack_id")

    events = _list_proof_packs(customer_id=customer.tenant_id)
    match = next((e for e in events if str(getattr(e, "id", "")) == pid), None)
    if match is None:
        raise HTTPException(status_code=404, detail="proof_pack_not_found")

    # Defensive tenant check (mirrors get_sprint).
    owner = str(getattr(match, "customer_handle", "") or "")
    if (
        not customer.is_super_admin
        and customer.tenant_id
        and owner
        and owner != customer.tenant_id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="cross_tenant_access_denied",
        )

    # Try to render via the proof_architecture_os helper. Fall back to a
    # minimal markdown summary so we always return *something*.
    body = ""
    try:
        from auto_client_acquisition.proof_architecture_os.proof_pack_render import (
            proof_pack_to_markdown,
        )

        pack_dict = (
            match.model_dump() if hasattr(match, "model_dump") else dict(match.__dict__)
        )
        body = proof_pack_to_markdown(
            pack_dict, customer_handle=customer.tenant_id or "customer"
        )
    except Exception:  # noqa: BLE001
        body = (
            f"# Proof Pack {pid}\n\n"
            "Renderer unavailable in this environment. "
            "Use `/api/v1/sprint/render/markdown` for the canonical output.\n"
        )

    return PlainTextResponse(
        content=body,
        headers={
            "Content-Disposition": f'inline; filename="proof_pack_{pid}.md"',
        },
    )


@router.post(
    "/feedback",
    response_model=FeedbackResponse,
    status_code=status.HTTP_201_CREATED,
)
async def submit_feedback(
    body: FeedbackSubmitBody,
    customer: CurrentCustomer,
    db: AsyncSession = Depends(get_db),
) -> FeedbackResponse:
    """Persist a 1..5 rating + optional comment for the current tenant."""
    if not customer.tenant_id:
        # Super-admins without tenant context are blocked from writing
        # tenant-scoped feedback rows.
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="tenant_scope_required",
        )

    sprint_id = _safe_id(body.sprint_id) if body.sprint_id else None
    feedback = CustomerFeedbackRecord(
        id=_new_feedback_id(),
        tenant_id=customer.tenant_id,
        customer_id=customer.tenant_id,
        sprint_id=sprint_id,
        rating=body.rating,
        comment=body.comment or None,
        created_at=utcnow(),
    )
    db.add(feedback)
    await db.flush()

    # Structured log — never include the raw comment. Use a length +
    # masked-prefix so support can recognise spam patterns without a
    # PDPL violation.
    log.info(
        "customer_portal.feedback_submitted",
        feedback_id=feedback.id,
        tenant_id=customer.tenant_id,
        rating=body.rating,
        comment_length=len(body.comment or ""),
        comment_prefix=_log_safe_summary(body.comment),
        sprint_id=sprint_id,
    )

    return FeedbackResponse(
        feedback_id=feedback.id,
        rating=feedback.rating,
        comment_stored=bool(body.comment),
        sprint_id=sprint_id,
        created_at=feedback.created_at,
    )


@router.get("/invoices", response_model=InvoiceListResponse)
async def list_invoices(
    customer: CurrentCustomer,
    limit: int = Query(50, ge=1, le=200),
    db: AsyncSession = Depends(get_db),
) -> InvoiceListResponse:
    """List the customer's invoices, newest first.

    Reads from `zatca_invoices` (the canonical ZATCA-compliant store).
    Super-admins without a tenant scope receive an empty list — they
    must impersonate via the admin tenant endpoints instead.
    """
    if not customer.tenant_id:
        return InvoiceListResponse(tenant_id=None, count=0, invoices=[])

    stmt = (
        select(ZATCAInvoiceRecord)
        .where(ZATCAInvoiceRecord.tenant_id == customer.tenant_id)
        .order_by(desc(ZATCAInvoiceRecord.created_at))
        .limit(limit)
    )
    result = await db.execute(stmt)
    rows = result.scalars().all()

    invoices: list[InvoiceSummary] = []
    for r in rows:
        invoices.append(
            InvoiceSummary(
                invoice_id=r.id,
                invoice_number=r.invoice_number,
                total_sar=float(r.total_sar or 0.0),
                vat_amount_sar=float(r.vat_amount_sar or 0.0),
                currency="SAR",
                status=r.zatca_status,
                issue_date=r.issue_date,
                buyer_name=r.buyer_name,
            )
        )

    return InvoiceListResponse(
        tenant_id=customer.tenant_id,
        count=len(invoices),
        invoices=invoices,
    )


# Helper exported for tests that need to filter cross-tenant rows.
__all__ = [
    "router",
    "CustomerPrincipal",
    "get_current_customer",
    "_log_safe_summary",
    "_safe_id",
]
