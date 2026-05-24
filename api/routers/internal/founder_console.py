"""Founder Console internal router.

Exposes read-only snapshots and an approval-queue write endpoint.
All routes require the internal key.
"""
from __future__ import annotations

import csv
import datetime
import uuid
from pathlib import Path
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field

from api.internal.auth import require_internal_key
from api.internal.policy_adapter import audit_record, contains_forbidden_claim
from api.internal.runtime_reader import read_csv, read_markdown, workspace_root

router = APIRouter(prefix="/internal/founder-console", tags=["founder-console-internal"])


# Page slug → snapshot recipe. Each slug bundles small CSV/MD reads.
PAGE_SOURCES: dict[str, list[tuple[str, str]]] = {
    "ceo": [
        ("csv", "founder/decision_log.csv"),
        ("csv", "trust/trust_flags.csv"),
        ("csv", "runtime/worker_state.csv"),
    ],
    "ceo-os": [("md", "founder/ceo_daily_brief.md"), ("md", "founder/ceo_weekly_review.md")],
    "founder-leverage": [
        ("csv", "founder/founder_time_audit.csv"),
        ("csv", "founder/delegation_queue.csv"),
    ],
    "strategy": [
        ("csv", "founder/strategic_assumptions.csv"),
        ("csv", "founder/decision_log.csv"),
    ],
    "capital-allocation": [
        ("csv", "finance/capital_allocation.csv"),
        ("csv", "finance/roi_priority_matrix.csv"),
    ],
    "sales-cockpit": [
        ("csv", "graph/accounts.csv"),
        ("csv", "outreach/outreach_queue.csv"),
    ],
    "deal-desk": [
        ("csv", "sales/proposal_queue.csv"),
        ("csv", "sales/sample_queue.csv"),
    ],
    "workers": [("csv", "runtime/worker_state.csv")],
    "trust": [
        ("csv", "trust/trust_flags.csv"),
        ("csv", "trust/incidents.csv"),
    ],
    "ai-governance": [("csv", "evals/eval_status.csv")],
    "finance": [("csv", "finance/cash_collected.csv")],
    "finance-ops": [("csv", "finance/payment_capture_queue.csv")],
    "distribution": [("csv", "growth/distribution_machines.csv")],
    "launch": [("csv", "evals/eval_status.csv")],
    "market-attack": [
        ("csv", "market_attack/beachhead_sector_scorecard.csv"),
        ("csv", "market_attack/strategic_accounts.csv"),
    ],
    "campaigns": [("csv", "campaigns/campaign_registry.csv")],
    "sales-assets": [("csv", "sales/sales_asset_registry.csv")],
    "authority": [("csv", "campaigns/campaign_assets.csv")],
    "revenue-intelligence": [
        ("csv", "graph/accounts.csv"),
        ("csv", "graph/messages.csv"),
        ("csv", "graph/learnings.csv"),
    ],
    "moat": [("csv", "metrics/hypergrowth_metrics.csv")],
    "playbooks": [("md", "graph/revenue_intelligence_graph_report.md")],
    "proof-library": [
        ("csv", "proof/proof_library.csv"),
        ("csv", "proof/proof_approval_queue.csv"),
    ],
    "partner-ecosystem": [
        ("csv", "partners/partner_pipeline.csv"),
        ("csv", "partners/partner_ecosystem.csv"),
    ],
    "productization": [("csv", "product/productization_pipeline.csv")],
    "customer-success": [
        ("csv", "customer_success/client_health.csv"),
        ("csv", "customer_success/expansion_opportunities.csv"),
    ],
    "delivery": [("csv", "runtime/worker_state.csv")],
    "retention": [("csv", "customer_success/renewal_risk.csv")],
    "proof": [("csv", "proof/proof_library.csv")],
    "data": [("csv", "intelligence/lead_intelligence_base.csv")],
    "experiments": [("csv", "market_attack/offer_market_fit_tests.csv")],
    "security": [("csv", "security/security_status.csv")],
    "audit": [
        ("csv", "founder/decision_log.csv"),
        ("csv", "trust/approval_decisions.csv"),
    ],
    "metrics": [("csv", "metrics/hypergrowth_metrics.csv")],
    "legal": [("csv", "legal/commercial_guardrails.csv")],
    "advisor": [("md", "founder/ceo_weekly_review.md")],
    "settings": [],
}


@router.get("/{slug}", dependencies=[Depends(require_internal_key)])
def get_snapshot(slug: str) -> dict[str, Any]:
    if slug not in PAGE_SOURCES:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="unknown_slug")
    parts = []
    latest_freshness = ""
    for kind, rel_path in PAGE_SOURCES[slug]:
        part = read_csv(rel_path) if kind == "csv" else read_markdown(rel_path)
        parts.append(part)
        latest_freshness = max(latest_freshness, part["freshness_iso"])
    return {
        "source": "api / private_ops_csv",
        "freshness_iso": latest_freshness or datetime.datetime.utcnow().isoformat(timespec="seconds"),
        "data": {"slug": slug, "parts": parts},
    }


class ApprovalQueueRequest(BaseModel):
    action_id: str = Field(min_length=1, max_length=128)
    reason: str = Field(min_length=1, max_length=2048)
    payload: dict[str, Any] | None = None


@router.post("/approvals/queue", dependencies=[Depends(require_internal_key)])
def queue_for_approval(req: ApprovalQueueRequest) -> dict[str, Any]:
    text_blob = f"{req.action_id} {req.reason} {req.payload or {}}"
    forbidden = contains_forbidden_claim(text_blob)
    if forbidden:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": "forbidden_claim", "matches": forbidden},
        )
    root: Path = workspace_root()
    queue_path = root / "approvals" / "approval_queue.csv"
    queue_path.parent.mkdir(parents=True, exist_ok=True)
    is_new = not queue_path.exists()
    queue_id = f"apt-{uuid.uuid4().hex[:10]}"
    record = {
        "id": queue_id,
        "action_id": req.action_id,
        "reason": req.reason,
        "payload": str(req.payload or {}),
        "queued_at": datetime.datetime.utcnow().isoformat(timespec="seconds"),
        "decision": "pending",
        "external_action_allowed": "false",
    }
    with queue_path.open("a", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(record.keys()))
        if is_new:
            writer.writeheader()
        writer.writerow(record)
    audit = audit_record("founder_console", req.action_id, req.reason, "queued")
    return {"queued": True, "id": queue_id, "audit": audit}
