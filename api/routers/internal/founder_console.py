"""
Internal Dealix Founder Console router.

Mounts at /api/v1/internal. Every endpoint depends on the internal-token
auth dependency. GET endpoints return `{auth_mode, source, data}`. POST
endpoints queue an action into the private ops CSV root and NEVER trigger
an external side effect.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Request, status
from pydantic import BaseModel, Field

from api.internal.auth import InternalAuthContext, require_internal_token
from api.internal.policy_adapter import load_policies
from api.internal.runtime_reader import append_csv_row, read_csv_rows

router = APIRouter(prefix="/api/v1/internal", tags=["internal"])


# ── Helpers ────────────────────────────────────────────────────────
def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _wrap(auth: InternalAuthContext, source: str, data: Any) -> dict[str, Any]:
    return {"auth_mode": auth.auth_mode, "source": source, "data": data}


def _rows(auth: InternalAuthContext, csv_path: str) -> dict[str, Any]:
    payload = read_csv_rows(csv_path)
    return _wrap(auth, payload.get("source", "fallback"), {"rows": payload.get("rows", [])})


def _summary_from_csv(
    auth: InternalAuthContext,
    csv_path: str,
    metric_keys: list[tuple[str, str]],
) -> dict[str, Any]:
    """Render a SummaryPayload by taking the first row and pulling named keys."""
    payload = read_csv_rows(csv_path)
    rows = payload.get("rows", []) or []
    first = rows[0] if rows else {}
    metrics = [
        {"label": label, "value": first.get(key, "—")}
        for key, label in metric_keys
    ]
    highlights = []
    if "highlights" in first and first["highlights"]:
        highlights = [h.strip() for h in str(first["highlights"]).split("|") if h.strip()]
    return _wrap(
        auth,
        payload.get("source", "fallback"),
        {"metrics": metrics, "highlights": highlights},
    )


# ── Action payload models ──────────────────────────────────────────
class ReasonBody(BaseModel):
    reason: str = Field(default="", max_length=2000)


class NoteBody(BaseModel):
    note: str = Field(default="", max_length=2000)


# ── CEO ────────────────────────────────────────────────────────────
@router.get("/ceo/summary")
async def ceo_summary(auth: InternalAuthContext = Depends(require_internal_token)) -> dict[str, Any]:
    return _summary_from_csv(
        auth,
        "ceo/summary.csv",
        [
            ("active_deals", "Active Deals"),
            ("pipeline_value", "Pipeline (SAR)"),
            ("approvals_pending", "Approvals Pending"),
            ("trust_risk", "Trust Risk"),
        ],
    )


# ── Sales ──────────────────────────────────────────────────────────
@router.get("/sales/funnel")
async def sales_funnel(auth: InternalAuthContext = Depends(require_internal_token)) -> dict[str, Any]:
    return _rows(auth, "sales/funnel.csv")


# ── Approvals ──────────────────────────────────────────────────────
@router.get("/approvals")
async def approvals(auth: InternalAuthContext = Depends(require_internal_token)) -> dict[str, Any]:
    return _rows(auth, "approvals/approval_queue.csv")


def _record_approval_decision(approval_id: str, decision: str, note: str) -> dict[str, Any]:
    return append_csv_row(
        "trust/approval_decisions.csv",
        {
            "decided_at": _now_iso(),
            "approval_id": approval_id,
            "decision": decision,
            "note": note,
        },
    )


@router.post("/approvals/{approval_id}/approve")
async def approve_approval(
    approval_id: str,
    request: Request,
    auth: InternalAuthContext = Depends(require_internal_token),
) -> dict[str, Any]:
    body: dict[str, Any] = {}
    try:
        body = await request.json()
    except Exception:
        body = {}
    res = _record_approval_decision(approval_id, "approve", str(body.get("note", "")))
    if not res.get("ok"):
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=res.get("error", "write_failed"))
    return _wrap(auth, "csv", {"queued": True, "decision": "approve", "approval_id": approval_id})


@router.post("/approvals/{approval_id}/reject")
async def reject_approval(
    approval_id: str,
    body: ReasonBody,
    auth: InternalAuthContext = Depends(require_internal_token),
) -> dict[str, Any]:
    res = _record_approval_decision(approval_id, "reject", body.reason)
    if not res.get("ok"):
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=res.get("error", "write_failed"))
    return _wrap(auth, "csv", {"queued": True, "decision": "reject", "approval_id": approval_id})


@router.post("/approvals/{approval_id}/request-edit")
async def request_edit_approval(
    approval_id: str,
    body: NoteBody,
    auth: InternalAuthContext = Depends(require_internal_token),
) -> dict[str, Any]:
    res = _record_approval_decision(approval_id, "request_edit", body.note)
    if not res.get("ok"):
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=res.get("error", "write_failed"))
    return _wrap(auth, "csv", {"queued": True, "decision": "request_edit", "approval_id": approval_id})


@router.post("/approvals/{approval_id}/escalate")
async def escalate_approval(
    approval_id: str,
    body: ReasonBody,
    auth: InternalAuthContext = Depends(require_internal_token),
) -> dict[str, Any]:
    res = _record_approval_decision(approval_id, "escalate", body.reason)
    if not res.get("ok"):
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=res.get("error", "write_failed"))
    return _wrap(auth, "csv", {"queued": True, "decision": "escalate", "approval_id": approval_id})


# ── Workers ────────────────────────────────────────────────────────
@router.get("/workers/health")
async def worker_health(auth: InternalAuthContext = Depends(require_internal_token)) -> dict[str, Any]:
    return _rows(auth, "workers/health.csv")


@router.post("/workers/{worker_id}/retry")
async def retry_worker(
    worker_id: str,
    auth: InternalAuthContext = Depends(require_internal_token),
) -> dict[str, Any]:
    res = append_csv_row(
        "approvals/approval_queue.csv",
        {
            "queued_at": _now_iso(),
            "kind": "worker_retry",
            "target_id": worker_id,
            "status": "pending",
            "note": "founder-console retry request",
        },
    )
    if not res.get("ok"):
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=res.get("error", "write_failed"))
    return _wrap(auth, "csv", {"queued": True, "worker_id": worker_id})


# ── Trust ──────────────────────────────────────────────────────────
@router.get("/trust/flags")
async def trust_flags(auth: InternalAuthContext = Depends(require_internal_token)) -> dict[str, Any]:
    return _rows(auth, "trust/flags.csv")


# ── Finance & Distribution ─────────────────────────────────────────
@router.get("/finance/summary")
async def finance_summary(auth: InternalAuthContext = Depends(require_internal_token)) -> dict[str, Any]:
    return _summary_from_csv(
        auth,
        "finance/summary.csv",
        [
            ("mrr", "MRR (SAR)"),
            ("collections", "Collections (SAR)"),
            ("ar_aging", "AR > 30d"),
            ("runway_days", "Runway (days)"),
        ],
    )


@router.get("/distribution/summary")
async def distribution_summary(auth: InternalAuthContext = Depends(require_internal_token)) -> dict[str, Any]:
    return _summary_from_csv(
        auth,
        "distribution/summary.csv",
        [
            ("channels_active", "Active Channels"),
            ("sends_today", "Sends Today"),
            ("opt_outs", "Opt-Outs"),
            ("compliance_rate", "Compliance Rate"),
        ],
    )


# ── Delivery & Retention ───────────────────────────────────────────
@router.get("/delivery/queue")
async def delivery_queue(auth: InternalAuthContext = Depends(require_internal_token)) -> dict[str, Any]:
    return _rows(auth, "delivery/queue.csv")


@router.get("/retention/queue")
async def retention_queue(auth: InternalAuthContext = Depends(require_internal_token)) -> dict[str, Any]:
    return _rows(auth, "retention/queue.csv")


# ── Proof & Audit ──────────────────────────────────────────────────
@router.get("/proof/library")
async def proof_library(auth: InternalAuthContext = Depends(require_internal_token)) -> dict[str, Any]:
    return _rows(auth, "proof/library.csv")


@router.get("/audit/events")
async def audit_events(auth: InternalAuthContext = Depends(require_internal_token)) -> dict[str, Any]:
    return _rows(auth, "audit/events.csv")


# ── Control plane ──────────────────────────────────────────────────
@router.get("/control/summary")
async def control_summary(auth: InternalAuthContext = Depends(require_internal_token)) -> dict[str, Any]:
    return _summary_from_csv(
        auth,
        "control/summary.csv",
        [
            ("runs_live", "Live Runs"),
            ("approvals_pending", "Approvals Pending"),
            ("violations_today", "Violations Today"),
            ("uptime", "Uptime"),
        ],
    )


@router.get("/control/policies")
async def control_policies(auth: InternalAuthContext = Depends(require_internal_token)) -> dict[str, Any]:
    policies = load_policies()
    return _wrap(auth, policies.get("source", "fallback"), {"rows": policies.get("rules", [])})


@router.get("/control/agents")
async def control_agents(auth: InternalAuthContext = Depends(require_internal_token)) -> dict[str, Any]:
    return _rows(auth, "control/agents.csv")


@router.post("/control/agents/{agent_id}/disable")
async def disable_agent(
    agent_id: str,
    auth: InternalAuthContext = Depends(require_internal_token),
) -> dict[str, Any]:
    res = append_csv_row(
        "approvals/approval_queue.csv",
        {
            "queued_at": _now_iso(),
            "kind": "agent_disable",
            "target_id": agent_id,
            "status": "pending",
            "note": "founder-console disable request",
        },
    )
    if not res.get("ok"):
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=res.get("error", "write_failed"))
    return _wrap(auth, "csv", {"queued": True, "agent_id": agent_id, "action": "disable"})


@router.post("/control/agents/{agent_id}/enable")
async def enable_agent(
    agent_id: str,
    auth: InternalAuthContext = Depends(require_internal_token),
) -> dict[str, Any]:
    res = append_csv_row(
        "approvals/approval_queue.csv",
        {
            "queued_at": _now_iso(),
            "kind": "agent_enable",
            "target_id": agent_id,
            "status": "pending",
            "note": "founder-console enable request",
        },
    )
    if not res.get("ok"):
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=res.get("error", "write_failed"))
    return _wrap(auth, "csv", {"queued": True, "agent_id": agent_id, "action": "enable"})


@router.get("/control/scorecard")
async def control_scorecard(auth: InternalAuthContext = Depends(require_internal_token)) -> dict[str, Any]:
    return _summary_from_csv(
        auth,
        "control/scorecard.csv",
        [
            ("overall_score", "Overall Score"),
            ("trust_score", "Trust"),
            ("delivery_score", "Delivery"),
            ("finance_score", "Finance"),
        ],
    )


@router.post("/control/scorecard/generate")
async def generate_scorecard(
    auth: InternalAuthContext = Depends(require_internal_token),
) -> dict[str, Any]:
    res = append_csv_row(
        "approvals/approval_queue.csv",
        {
            "queued_at": _now_iso(),
            "kind": "scorecard_generate",
            "target_id": "operating",
            "status": "pending",
            "note": "founder-console scorecard request",
        },
    )
    if not res.get("ok"):
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=res.get("error", "write_failed"))
    return _wrap(auth, "csv", {"queued": True, "kind": "scorecard"})


@router.get("/control/risks")
async def control_risks(auth: InternalAuthContext = Depends(require_internal_token)) -> dict[str, Any]:
    return _rows(auth, "control/risks.csv")


@router.post("/control/risks/{risk_id}/accept")
async def accept_risk(
    risk_id: str,
    body: NoteBody,
    auth: InternalAuthContext = Depends(require_internal_token),
) -> dict[str, Any]:
    res = _record_approval_decision(f"risk:{risk_id}", "risk_accepted", body.note)
    if not res.get("ok"):
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=res.get("error", "write_failed"))
    return _wrap(auth, "csv", {"queued": True, "risk_id": risk_id})


# ── Evals / Product / Security ─────────────────────────────────────
@router.get("/evals/status")
async def evals_status(auth: InternalAuthContext = Depends(require_internal_token)) -> dict[str, Any]:
    return _summary_from_csv(
        auth,
        "evals/status.csv",
        [
            ("suites_passing", "Suites Passing"),
            ("suites_failing", "Suites Failing"),
            ("last_run", "Last Run"),
            ("coverage", "Coverage"),
        ],
    )


@router.get("/product/productization")
async def product_productization(
    auth: InternalAuthContext = Depends(require_internal_token),
) -> dict[str, Any]:
    return _summary_from_csv(
        auth,
        "product/productization.csv",
        [
            ("services_live", "Services Live"),
            ("services_beta", "Services in Beta"),
            ("sla_compliance", "SLA Compliance"),
            ("backlog_count", "Backlog"),
        ],
    )


@router.get("/security/status")
async def security_status(
    auth: InternalAuthContext = Depends(require_internal_token),
) -> dict[str, Any]:
    return _summary_from_csv(
        auth,
        "security/status.csv",
        [
            ("posture", "Posture"),
            ("open_incidents", "Open Incidents"),
            ("pdpl_status", "PDPL"),
            ("last_audit", "Last Audit"),
        ],
    )


# ── Sovereign / Brand / Growth ─────────────────────────────────────
@router.get("/sovereign/readiness")
async def sovereign_readiness(
    auth: InternalAuthContext = Depends(require_internal_token),
) -> dict[str, Any]:
    return _summary_from_csv(
        auth,
        "sovereign/readiness.csv",
        [
            ("score", "Sovereign Score"),
            ("data_residency", "Data Residency"),
            ("local_partners", "Local Partners"),
            ("nca_align", "NCA Alignment"),
        ],
    )


@router.post("/sovereign/readiness/generate")
async def generate_sovereign_readiness(
    auth: InternalAuthContext = Depends(require_internal_token),
) -> dict[str, Any]:
    res = append_csv_row(
        "approvals/approval_queue.csv",
        {
            "queued_at": _now_iso(),
            "kind": "sovereign_readiness_generate",
            "target_id": "sovereign",
            "status": "pending",
            "note": "founder-console sovereign readiness request",
        },
    )
    if not res.get("ok"):
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=res.get("error", "write_failed"))
    return _wrap(auth, "csv", {"queued": True, "kind": "sovereign_readiness"})


@router.get("/brand/summary")
async def brand_summary(auth: InternalAuthContext = Depends(require_internal_token)) -> dict[str, Any]:
    return _summary_from_csv(
        auth,
        "brand/summary.csv",
        [
            ("pillars_aligned", "Pillars Aligned"),
            ("public_mentions", "Mentions (30d)"),
            ("sentiment", "Sentiment"),
            ("share_of_voice", "Share of Voice"),
        ],
    )


@router.get("/growth/targeting")
async def growth_targeting(auth: InternalAuthContext = Depends(require_internal_token)) -> dict[str, Any]:
    return _rows(auth, "growth/targeting.csv")


@router.get("/marketing/summary")
async def marketing_summary(auth: InternalAuthContext = Depends(require_internal_token)) -> dict[str, Any]:
    return _summary_from_csv(
        auth,
        "marketing/summary.csv",
        [
            ("content_published", "Content Published"),
            ("inbound_leads", "Inbound Leads"),
            ("cost_per_lead", "CPL (SAR)"),
            ("conversion", "Conversion %"),
        ],
    )


@router.get("/product/distribution")
async def product_distribution(
    auth: InternalAuthContext = Depends(require_internal_token),
) -> dict[str, Any]:
    return _summary_from_csv(
        auth,
        "product/distribution.csv",
        [
            ("active_partners", "Active Partners"),
            ("partner_pipeline", "Partner Pipeline"),
            ("partner_revenue", "Partner Revenue"),
            ("activation_rate", "Activation"),
        ],
    )


@router.get("/customer-success/summary")
async def customer_success_summary(
    auth: InternalAuthContext = Depends(require_internal_token),
) -> dict[str, Any]:
    return _summary_from_csv(
        auth,
        "customer_success/summary.csv",
        [
            ("nrr", "NRR"),
            ("active_customers", "Active Customers"),
            ("nps", "NPS"),
            ("at_risk", "At Risk"),
        ],
    )


@router.get("/finance-ops/summary")
async def finance_ops_summary(
    auth: InternalAuthContext = Depends(require_internal_token),
) -> dict[str, Any]:
    return _summary_from_csv(
        auth,
        "finance_ops/summary.csv",
        [
            ("invoices_pending", "Invoices Pending"),
            ("zatca_status", "ZATCA"),
            ("refunds_pending", "Refunds Pending"),
            ("payouts_due", "Payouts Due"),
        ],
    )
