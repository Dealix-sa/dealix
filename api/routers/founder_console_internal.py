"""Dealix internal Founder Console API surface.

All endpoints under /api/v1/internal/* are intended for the Founder
Console UI only. They:

- read from the private ops runtime (CSVs) when available
- return deterministic, safe fallbacks when not
- never send anything externally
- never publish proof
- record audit intent for actions (approve/reject/escalate/disable/etc.)

Auth: requires `x-dealix-internal-token` when DEALIX_INTERNAL_TOKEN is
set. Otherwise responses carry `auth_mode: "dev_unprotected"`.
"""
from __future__ import annotations

import csv
import os
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from api.internal.auth import auth_mode, require_internal_token
from api.internal.policy_adapter import evaluate_action, list_rules
from api.internal.runtime_reader import _runtime_dir, read_csv

router = APIRouter(prefix="/api/v1/internal", tags=["founder-console-internal"])


# ── helpers ────────────────────────────────────────────────────


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _audit_event(actor: str, action: str, target: str, payload: dict[str, Any], risk: str = "low") -> dict[str, Any]:
    """Append an audit event to private ops if available; always return the row."""
    event = {
        "id": str(uuid.uuid4()),
        "ts": _now(),
        "actor": actor,
        "action": action,
        "target": target,
        "payload": payload,
        "risk": risk,
    }
    base = _runtime_dir()
    if base is not None:
        audit_dir = base / "trust"
        audit_dir.mkdir(parents=True, exist_ok=True)
        audit_file = audit_dir / "approval_decisions.csv"
        is_new = not audit_file.exists()
        with audit_file.open("a", encoding="utf-8", newline="") as fh:
            w = csv.writer(fh)
            if is_new:
                w.writerow(["id", "ts", "actor", "action", "target", "risk", "payload_json"])
            import json

            w.writerow([event["id"], event["ts"], actor, action, target, risk, json.dumps(payload, ensure_ascii=False)])
    return event


def _envelope(data: dict[str, Any] | list[Any], extra: dict[str, Any] | None = None) -> dict[str, Any]:
    out = {"data": data, "auth_mode": auth_mode(), "fetched_at": _now()}
    if extra:
        out.update(extra)
    return out


def _rows_or_empty(rel_path: str) -> tuple[list[dict[str, str]], str]:
    rr = read_csv(rel_path)
    return rr.rows, rr.source


# ── read endpoints ─────────────────────────────────────────────


@router.get("/ceo/summary")
async def ceo_summary(_mode: str = Depends(require_internal_token)) -> dict[str, Any]:
    rows, source = _rows_or_empty("finance/cash_collected.csv")
    cash_30d = 0.0
    for r in rows:
        try:
            cash_30d += float(r.get("amount_sar", "0") or 0)
        except ValueError:
            continue
    appr_rows, _ = _rows_or_empty("approvals/approval_queue.csv")
    flags, _ = _rows_or_empty("trust/trust_flags.csv")
    inc, _ = _rows_or_empty("trust/incidents.csv")
    return _envelope(
        {
            "pipeline_value_sar": 0,
            "pipeline_count": 0,
            "deals_won_this_quarter": 0,
            "cash_collected_30d_sar": cash_30d,
            "open_approvals": len([r for r in appr_rows if (r.get("status") or "open") == "open"]),
            "trust_flags": len(flags),
            "incidents_open": len([r for r in inc if (r.get("status") or "open") == "open"]),
            "runway_months": None,
            "data_source": source,
        }
    )


@router.get("/sales/funnel")
async def sales_funnel(_mode: str = Depends(require_internal_token)) -> dict[str, Any]:
    rows, source = _rows_or_empty("outreach/conversation_log.csv")
    stages = ["lead", "engaged", "qualified", "proposal_sent", "negotiation", "won"]
    counts = {s: 0 for s in stages}
    for r in rows:
        s = (r.get("stage") or "lead").strip().lower()
        if s in counts:
            counts[s] += 1
    return _envelope({"stages": [{"stage": s, "count": counts[s]} for s in stages], "data_source": source})


@router.get("/approvals")
async def approvals_list(_mode: str = Depends(require_internal_token)) -> dict[str, Any]:
    rows, source = _rows_or_empty("approvals/approval_queue.csv")
    items = [
        {
            "id": r.get("id") or f"apr_{i}",
            "type": r.get("type", "unspecified"),
            "risk": r.get("risk", "low"),
            "summary": r.get("summary", ""),
            "created_at": r.get("created_at", ""),
            "status": r.get("status", "open"),
        }
        for i, r in enumerate(rows)
    ]
    return _envelope({"items": items, "data_source": source})


class ApprovalNote(BaseModel):
    note: str | None = None


class EditRequest(BaseModel):
    instructions: str = Field(min_length=1, max_length=5000)


class EscalateRequest(BaseModel):
    escalate_to: str
    reason: str = Field(min_length=1, max_length=5000)


@router.post("/approvals/{approval_id}/approve")
async def approve(approval_id: str, body: ApprovalNote, _mode: str = Depends(require_internal_token)) -> dict[str, Any]:
    decision = evaluate_action("approval_approve", {"approval_id": approval_id})
    if not decision.allowed:
        raise HTTPException(status_code=409, detail={"rule": decision.rule, "reason": decision.reason})
    ev = _audit_event("founder", "approval_approve", approval_id, {"note": body.note}, risk="medium")
    return _envelope({"ok": True, "approval_id": approval_id}, {"audit_id": ev["id"], "message": "approval_recorded"})


@router.post("/approvals/{approval_id}/reject")
async def reject(approval_id: str, body: ApprovalNote, _mode: str = Depends(require_internal_token)) -> dict[str, Any]:
    ev = _audit_event("founder", "approval_reject", approval_id, {"note": body.note}, risk="low")
    return _envelope({"ok": True, "approval_id": approval_id}, {"audit_id": ev["id"], "message": "rejection_recorded"})


@router.post("/approvals/{approval_id}/request-edit")
async def request_edit(
    approval_id: str, body: EditRequest, _mode: str = Depends(require_internal_token)
) -> dict[str, Any]:
    ev = _audit_event(
        "founder", "approval_request_edit", approval_id, {"instructions": body.instructions}, risk="low"
    )
    return _envelope({"ok": True, "approval_id": approval_id}, {"audit_id": ev["id"], "message": "edit_requested"})


@router.post("/approvals/{approval_id}/escalate")
async def escalate(
    approval_id: str, body: EscalateRequest, _mode: str = Depends(require_internal_token)
) -> dict[str, Any]:
    ev = _audit_event(
        "founder",
        "approval_escalate",
        approval_id,
        {"escalate_to": body.escalate_to, "reason": body.reason},
        risk="high",
    )
    return _envelope(
        {"ok": True, "approval_id": approval_id}, {"audit_id": ev["id"], "message": "escalation_recorded"}
    )


@router.get("/workers/health")
async def workers_health(_mode: str = Depends(require_internal_token)) -> dict[str, Any]:
    rows, source = _rows_or_empty("runtime/worker_state.csv")
    workers = [
        {
            "id": r.get("id", ""),
            "name": r.get("name", r.get("id", "")),
            "status": r.get("status", "unknown"),
            "last_run": r.get("last_run") or None,
            "failure_count": int(r.get("failure_count", "0") or 0),
        }
        for r in rows
    ]
    return _envelope({"workers": workers, "data_source": source})


@router.post("/workers/{worker_id}/retry")
async def workers_retry(worker_id: str, _mode: str = Depends(require_internal_token)) -> dict[str, Any]:
    ev = _audit_event("founder", "worker_retry", worker_id, {}, risk="low")
    return _envelope({"ok": True, "worker_id": worker_id}, {"audit_id": ev["id"], "message": "retry_requested"})


@router.get("/trust/flags")
async def trust_flags(_mode: str = Depends(require_internal_token)) -> dict[str, Any]:
    rows, source = _rows_or_empty("trust/trust_flags.csv")
    flags = [
        {
            "id": r.get("id", ""),
            "severity": r.get("severity", "info"),
            "description": r.get("description", ""),
            "created_at": r.get("created_at", ""),
        }
        for r in rows
    ]
    return _envelope({"flags": flags, "data_source": source})


@router.get("/finance/summary")
async def finance_summary(_mode: str = Depends(require_internal_token)) -> dict[str, Any]:
    rows, source = _rows_or_empty("finance/cash_collected.csv")
    ue_rows, _ = _rows_or_empty("finance/ai_unit_economics.csv")
    cash_30d = 0.0
    for r in rows:
        try:
            cash_30d += float(r.get("amount_sar", "0") or 0)
        except ValueError:
            continue
    ai_cost = 0.0
    for r in ue_rows:
        try:
            ai_cost += float(r.get("ai_cost_usd", "0") or 0)
        except ValueError:
            continue
    return _envelope(
        {
            "cash_collected_30d_sar": cash_30d,
            "pipeline_value_sar": 0,
            "arr_estimate_sar": 0,
            "invoices_outstanding": 0,
            "ai_cost_30d_usd": ai_cost,
            "margin_health": "unknown",
            "data_source": source,
        }
    )


@router.get("/distribution/summary")
async def distribution_summary(_mode: str = Depends(require_internal_token)) -> dict[str, Any]:
    ch, src_ch = _rows_or_empty("distribution/channel_scorecard.csv")
    se, _ = _rows_or_empty("distribution/sector_scorecard.csv")
    ex, _ = _rows_or_empty("distribution/experiment_log.csv")
    return _envelope(
        {
            "channels": ch,
            "sectors": se,
            "experiments_open": len([r for r in ex if (r.get("status") or "open") == "open"]),
            "data_source": src_ch,
        }
    )


@router.get("/delivery/queue")
async def delivery_queue(_mode: str = Depends(require_internal_token)) -> dict[str, Any]:
    rows, source = _rows_or_empty("sales/proposal_queue.csv")
    items = [
        {
            "id": r.get("id", ""),
            "client": r.get("client", ""),
            "sprint": r.get("sprint", r.get("offer", "")),
            "status": r.get("status", "pending"),
        }
        for r in rows
    ]
    return _envelope({"items": items, "data_source": source})


@router.get("/retention/queue")
async def retention_queue(_mode: str = Depends(require_internal_token)) -> dict[str, Any]:
    rows, source = _rows_or_empty("customer_success/client_health.csv")
    items = [
        {
            "client": r.get("client", ""),
            "health": r.get("health", "unknown"),
            "next_action": r.get("next_action", ""),
            "due": r.get("due", ""),
        }
        for r in rows
    ]
    return _envelope({"items": items, "data_source": source})


@router.get("/proof/library")
async def proof_library(_mode: str = Depends(require_internal_token)) -> dict[str, Any]:
    rows, source = _rows_or_empty("proof/proof_library.csv")
    items = [
        {
            "id": r.get("id", ""),
            "sector": r.get("sector", ""),
            "title": r.get("title", ""),
            "approval_state": r.get("approval_state", "draft"),
        }
        for r in rows
    ]
    return _envelope({"items": items, "data_source": source})


@router.get("/audit/events")
async def audit_events(_mode: str = Depends(require_internal_token)) -> dict[str, Any]:
    rows, source = _rows_or_empty("trust/approval_decisions.csv")
    items = [
        {
            "id": r.get("id", ""),
            "actor": r.get("actor", ""),
            "action": r.get("action", ""),
            "ts": r.get("ts", ""),
            "risk": r.get("risk", ""),
        }
        for r in rows
    ]
    return _envelope({"items": items, "data_source": source})


@router.get("/control/summary")
async def control_summary(_mode: str = Depends(require_internal_token)) -> dict[str, Any]:
    return _envelope(
        {
            "agents_total": 0,
            "agents_enabled": 0,
            "policies_active": len(list_rules()),
            "kill_switches_open": 0,
            "last_eval_gate": None,
        }
    )


@router.get("/control/policies")
async def control_policies(_mode: str = Depends(require_internal_token)) -> dict[str, Any]:
    rules = [
        {"id": r.get("id", ""), "rule": r.get("description", r.get("id", "")), "severity": r.get("severity", "info")}
        for r in list_rules()
    ]
    return _envelope({"policies": rules})


@router.get("/control/agents")
async def control_agents(_mode: str = Depends(require_internal_token)) -> dict[str, Any]:
    reg_path = Path(os.getenv("DEALIX_AGENT_REGISTRY", "registries/agent_registry.yaml"))
    agents: list[dict[str, Any]] = []
    if reg_path.exists():
        try:
            import yaml  # type: ignore

            with reg_path.open("r", encoding="utf-8") as fh:
                data = yaml.safe_load(fh) or {}
            for a in data.get("agents", []) or []:
                agents.append(
                    {
                        "id": a.get("id", ""),
                        "name": a.get("name", a.get("id", "")),
                        "approval_class_max": a.get("approval_class_max", "A2"),
                        "enabled": bool(a.get("enabled", True)),
                    }
                )
        except Exception:
            pass
    return _envelope({"agents": agents})


class AgentToggle(BaseModel):
    reason: str = Field(min_length=1, max_length=500)


@router.post("/control/agents/{agent_id}/disable")
async def agent_disable(
    agent_id: str, body: AgentToggle, _mode: str = Depends(require_internal_token)
) -> dict[str, Any]:
    ev = _audit_event("founder", "agent_disable", agent_id, {"reason": body.reason}, risk="high")
    return _envelope({"ok": True, "agent_id": agent_id}, {"audit_id": ev["id"], "message": "agent_disable_recorded"})


@router.post("/control/agents/{agent_id}/enable")
async def agent_enable(
    agent_id: str, body: AgentToggle, _mode: str = Depends(require_internal_token)
) -> dict[str, Any]:
    ev = _audit_event("founder", "agent_enable", agent_id, {"reason": body.reason}, risk="medium")
    return _envelope({"ok": True, "agent_id": agent_id}, {"audit_id": ev["id"], "message": "agent_enable_recorded"})


@router.get("/control/scorecard")
async def control_scorecard(_mode: str = Depends(require_internal_token)) -> dict[str, Any]:
    return _envelope(
        {
            "revenue_pillar": {"score": None, "status": "unknown"},
            "trust_pillar": {"score": None, "status": "unknown"},
            "delivery_pillar": {"score": None, "status": "unknown"},
            "growth_pillar": {"score": None, "status": "unknown"},
            "last_refresh": None,
        }
    )


@router.post("/control/scorecard/refresh")
async def control_scorecard_refresh(_mode: str = Depends(require_internal_token)) -> dict[str, Any]:
    ev = _audit_event("founder", "scorecard_refresh", "control_plane", {}, risk="low")
    return _envelope({"ok": True}, {"audit_id": ev["id"], "message": "scorecard_refresh_recorded"})


class RiskAccept(BaseModel):
    justification: str = Field(min_length=10, max_length=5000)


@router.post("/control/risks/{risk_id}/accept")
async def control_risk_accept(
    risk_id: str, body: RiskAccept, _mode: str = Depends(require_internal_token)
) -> dict[str, Any]:
    ev = _audit_event("founder", "risk_accept", risk_id, {"justification": body.justification}, risk="high")
    return _envelope({"ok": True, "risk_id": risk_id}, {"audit_id": ev["id"], "message": "risk_acceptance_recorded"})


@router.get("/evals/status")
async def evals_status(_mode: str = Depends(require_internal_token)) -> dict[str, Any]:
    rows, source = _rows_or_empty("evals/eval_status.csv")
    return _envelope(
        {
            "last_run": rows[-1].get("ts") if rows else None,
            "suites": rows,
            "pass_rate": None,
            "blocking_failures": 0,
            "data_source": source,
        }
    )


@router.get("/product/productization")
async def product_productization(_mode: str = Depends(require_internal_token)) -> dict[str, Any]:
    cand, source = _rows_or_empty("product/productization_candidates.csv")
    ladder, _ = _rows_or_empty("product/offer_ladder.csv")
    return _envelope(
        {
            "candidates": cand,
            "ladder": ladder,
            "data_source": source,
        }
    )


@router.get("/security/status")
async def security_status(_mode: str = Depends(require_internal_token)) -> dict[str, Any]:
    rows, source = _rows_or_empty("security/security_status.csv")
    latest = rows[-1] if rows else {}
    return _envelope(
        {
            "secrets_scan": latest.get("secrets_scan", "unknown"),
            "dependency_scan": latest.get("dependency_scan", "unknown"),
            "pdpl_review": latest.get("pdpl_review", "unknown"),
            "incident_open": int(latest.get("incident_open", "0") or 0),
            "data_source": source,
        }
    )


@router.get("/sovereign/readiness")
async def sovereign_readiness(_mode: str = Depends(require_internal_token)) -> dict[str, Any]:
    return _envelope(
        {
            "saudi_data_residency": "unknown",
            "pdpl_alignment": "unknown",
            "nca_alignment": "unknown",
            "arabic_quality": "unknown",
            "last_review": None,
        }
    )


@router.post("/sovereign/readiness/refresh")
async def sovereign_readiness_refresh(_mode: str = Depends(require_internal_token)) -> dict[str, Any]:
    ev = _audit_event("founder", "sovereign_readiness_refresh", "sovereign", {}, risk="low")
    return _envelope({"ok": True}, {"audit_id": ev["id"], "message": "refresh_recorded"})


@router.get("/brand/summary")
async def brand_summary(_mode: str = Depends(require_internal_token)) -> dict[str, Any]:
    rows, source = _rows_or_empty("brand/brand_assets_registry.csv")
    return _envelope(
        {
            "wordmark": "DEALIX",
            "tagline": "INTELLIGENT DEALS. REAL GROWTH.",
            "assets_registered": len(rows),
            "last_audit": rows[-1].get("ts") if rows else None,
            "data_source": source,
        }
    )


@router.get("/growth/targeting")
async def growth_targeting(_mode: str = Depends(require_internal_token)) -> dict[str, Any]:
    rows, source = _rows_or_empty("growth/sector_targets.csv")
    segments = [
        {
            "sector": r.get("sector", ""),
            "priority": r.get("priority", "P3"),
            "accounts": int(r.get("accounts", "0") or 0),
            "score": float(r.get("score", "0") or 0),
        }
        for r in rows
    ]
    return _envelope({"segments": segments, "data_source": source})


@router.get("/marketing/summary")
async def marketing_summary(_mode: str = Depends(require_internal_token)) -> dict[str, Any]:
    cal, source = _rows_or_empty("marketing/content_calendar.csv")
    camp, _ = _rows_or_empty("marketing/campaigns.csv")
    return _envelope(
        {
            "campaigns": len(camp),
            "content_in_pipeline": len(cal),
            "calendar_next_7_days": [
                {"day": r.get("day", ""), "topic": r.get("topic", "")} for r in cal[:7]
            ],
            "data_source": source,
        }
    )


class CampaignDraft(BaseModel):
    name: str
    sector: str
    owner: str


@router.post("/marketing/campaigns/draft")
async def marketing_campaign_draft(
    body: CampaignDraft, _mode: str = Depends(require_internal_token)
) -> dict[str, Any]:
    ev = _audit_event("founder", "campaign_draft", body.name, body.model_dump(), risk="low")
    return _envelope({"ok": True}, {"audit_id": ev["id"], "message": "campaign_draft_recorded"})


@router.get("/product/distribution")
async def product_distribution(_mode: str = Depends(require_internal_token)) -> dict[str, Any]:
    rows, source = _rows_or_empty("product/product_distribution.csv")
    return _envelope(
        {
            "offers": [
                {
                    "rung": r.get("rung", ""),
                    "offer": r.get("offer", ""),
                    "channel": r.get("channel", ""),
                    "status": r.get("status", ""),
                }
                for r in rows
            ],
            "data_source": source,
        }
    )


@router.get("/customer-success/summary")
async def customer_success_summary(_mode: str = Depends(require_internal_token)) -> dict[str, Any]:
    rows, source = _rows_or_empty("customer_success/client_health.csv")
    ref, _ = _rows_or_empty("customer_success/referral_queue.csv")
    at_risk = sum(1 for r in rows if (r.get("health") or "").lower() in {"red", "at_risk"})
    return _envelope(
        {
            "clients_active": len(rows),
            "clients_at_risk": at_risk,
            "referrals_open": len(ref),
            "nps": None,
            "data_source": source,
        }
    )


@router.get("/finance-ops/summary")
async def finance_ops_summary(_mode: str = Depends(require_internal_token)) -> dict[str, Any]:
    inv, source = _rows_or_empty("finance/payment_capture_queue.csv")
    ue, _ = _rows_or_empty("finance/ai_unit_economics.csv")
    overdue = sum(1 for r in inv if (r.get("status") or "").lower() == "overdue")
    return _envelope(
        {
            "invoices_open": len(inv),
            "invoices_overdue": overdue,
            "cash_in_30d_sar": 0,
            "ai_unit_cost_per_deal_usd": ue[-1].get("ai_cost_usd") if ue else None,
            "data_source": source,
        }
    )


@router.get("/data/summary")
async def data_summary(_mode: str = Depends(require_internal_token)) -> dict[str, Any]:
    return _envelope(
        {
            "primary_store": os.getenv("DEALIX_PRIMARY_STORE", "postgres"),
            "dq_score": None,
            "pipelines_failed_24h": 0,
            "last_dq_run": None,
        }
    )


@router.get("/experiments/backlog")
async def experiments_backlog(_mode: str = Depends(require_internal_token)) -> dict[str, Any]:
    rows, source = _rows_or_empty("distribution/experiment_log.csv")
    items = [
        {
            "id": r.get("id", ""),
            "hypothesis": r.get("hypothesis", ""),
            "status": r.get("status", "draft"),
            "owner": r.get("owner", ""),
        }
        for r in rows
    ]
    return _envelope({"items": items, "data_source": source})


class ExperimentDraft(BaseModel):
    hypothesis: str
    owner: str


@router.post("/experiments/backlog/draft")
async def experiments_draft(body: ExperimentDraft, _mode: str = Depends(require_internal_token)) -> dict[str, Any]:
    ev = _audit_event("founder", "experiment_draft", body.hypothesis[:80], body.model_dump(), risk="low")
    return _envelope({"ok": True}, {"audit_id": ev["id"], "message": "experiment_draft_recorded"})
