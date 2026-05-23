"""Internal API surface for the Founder Console.

Every endpoint is read-only, gated by X-Internal-Token, and returns a
fallback-safe payload when the private ops runtime is not bootstrapped.

Mount in api/main.py with:
    app.include_router(founder_console_router, prefix="/api/v1/internal")
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends

from api.internal.auth import require_internal_token
from api.internal.runtime_reader import count_csv, read_csv

router = APIRouter(tags=["internal", "founder-console"])


def _maybe_int(value: Any) -> int | None:
    if value is None or value == "":
        return None
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return None


def _maybe_float(value: Any) -> float | None:
    if value is None or value == "":
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


@router.get("/founder/ceo")
async def ceo_summary(_: str = Depends(require_internal_token)) -> dict[str, Any]:
    rows = read_csv("runtime", "ceo_summary.csv")
    last = rows[-1] if rows else {}
    return {
        "pipeline_weighted": _maybe_int(last.get("pipeline_weighted")),
        "cash_collected": _maybe_int(last.get("cash_collected")),
        "approvals_pending": _maybe_int(last.get("approvals_pending")),
        "trust_flags_open": _maybe_int(last.get("trust_flags_open")),
        "workers_fresh": _maybe_int(last.get("workers_fresh")),
    }


@router.get("/founder/sales")
async def sales_funnel(_: str = Depends(require_internal_token)) -> dict[str, Any]:
    rows = read_csv("runtime", "sales_funnel.csv")
    last = rows[-1] if rows else {}
    keys = [
        "leads_researched",
        "a_leads",
        "approved_outreach",
        "sent_actions",
        "replies",
        "positive_replies",
        "samples_sent",
        "proposals_sent",
    ]
    return {k: _maybe_int(last.get(k)) for k in keys}


@router.get("/founder/approvals")
async def approval_queue(_: str = Depends(require_internal_token)) -> dict[str, Any]:
    rows = read_csv("approvals", "approval_queue.csv")
    by_class = {"A1": 0, "A2": 0, "A3": 0}
    for r in rows:
        cls = (r.get("approval_class") or "").upper()
        if cls in by_class:
            by_class[cls] += 1
    return {
        "total": len(rows),
        "by_class": by_class,
        "avg_age_hours": None,
    }


@router.get("/founder/workers")
async def workers(_: str = Depends(require_internal_token)) -> list[dict[str, Any]]:
    rows = read_csv("runtime", "worker_state.csv")
    out: list[dict[str, Any]] = []
    for r in rows:
        out.append(
            {
                "worker": r.get("worker"),
                "last_run": r.get("last_run"),
                "status": r.get("status"),
                "failures_24h": _maybe_int(r.get("failures_24h")),
                "next_run": r.get("next_run"),
                "notes": r.get("notes"),
            }
        )
    return out


@router.get("/founder/trust")
async def trust_summary(_: str = Depends(require_internal_token)) -> dict[str, Any]:
    rows = read_csv("trust", "trust_flags.csv")
    open_flags = sum(1 for r in rows if (r.get("status") or "").lower() == "open")
    high = sum(
        1
        for r in rows
        if (r.get("severity") or "").lower() in ("high", "critical")
        and (r.get("status") or "").lower() == "open"
    )
    return {
        "flags_open": open_flags,
        "flags_resolved_30d": None,
        "high_risk_open": high,
        "policies_evaluated_24h": None,
    }


@router.get("/founder/finance")
async def finance_summary(_: str = Depends(require_internal_token)) -> dict[str, Any]:
    rows = read_csv("finance", "finance_summary.csv")
    last = rows[-1] if rows else {}
    return {
        "cash_collected": _maybe_int(last.get("cash_collected")),
        "mrr": _maybe_int(last.get("mrr")),
        "pipeline_weighted": _maybe_int(last.get("pipeline_weighted")),
        "ai_cost_per_lead": _maybe_float(last.get("ai_cost_per_lead")),
        "ai_cost_per_proposal": _maybe_float(last.get("ai_cost_per_proposal")),
        "ai_cost_per_paid_client": _maybe_float(last.get("ai_cost_per_paid_client")),
        "runway_months": _maybe_float(last.get("runway_months")),
    }


@router.get("/founder/distribution")
async def distribution_summary(_: str = Depends(require_internal_token)) -> dict[str, Any]:
    outbound = read_csv("outreach", "outbound_queue.csv")
    approvals = read_csv("approvals", "approval_decisions.csv")
    return {
        "outbound_drafts": len(outbound),
        "approved_today": sum(1 for r in approvals if (r.get("decision") or "").lower() == "approved"),
        "queued_linkedin": sum(1 for r in outbound if (r.get("channel") or "").lower() == "linkedin"),
        "queued_email": sum(1 for r in outbound if (r.get("channel") or "").lower() == "email"),
        "queued_contact_forms": sum(1 for r in outbound if (r.get("channel") or "").lower() == "contact_form"),
        "follow_ups_open": count_csv("outreach", "followup_queue.csv"),
    }


@router.get("/founder/delivery")
async def delivery_summary(_: str = Depends(require_internal_token)) -> dict[str, Any]:
    return {
        "active_engagements": count_csv("runtime", "engagements.csv"),
        "pending_qa": None,
        "handoffs_due_7d": None,
        "blockers_open": None,
    }


@router.get("/founder/retention")
async def retention_summary(_: str = Depends(require_internal_token)) -> dict[str, Any]:
    return {
        "active_clients": count_csv("runtime", "clients.csv"),
        "retainer_asks_open": None,
        "referral_asks_open": None,
        "nps_30d": None,
    }


@router.get("/founder/proof")
async def proof_summary(_: str = Depends(require_internal_token)) -> dict[str, Any]:
    return {
        "candidates": count_csv("runtime", "proof_candidates.csv"),
        "awaiting_client": None,
        "approved_published": None,
        "rejected": None,
    }


@router.get("/founder/audit")
async def audit_summary(_: str = Depends(require_internal_token)) -> dict[str, Any]:
    return {
        "events_24h": count_csv("runtime", "audit_events.csv"),
        "external_actions_24h": None,
        "policy_blocks_24h": None,
        "evidence_attached_pct": None,
    }


@router.get("/founder/evals")
async def eval_summary(_: str = Depends(require_internal_token)) -> dict[str, Any]:
    rows = read_csv("runtime", "eval_results.csv")
    return {
        "suites_total": 15,
        "passing": sum(1 for r in rows if (r.get("status") or "").lower() == "pass"),
        "failing": sum(1 for r in rows if (r.get("status") or "").lower() == "fail"),
        "last_run": rows[-1].get("when") if rows else None,
    }


@router.get("/founder/product")
async def product_summary(_: str = Depends(require_internal_token)) -> dict[str, Any]:
    return {
        "ladder_active": 7,
        "candidates_in_review": count_csv("runtime", "productization_candidates.csv"),
        "retainers_live": None,
    }


@router.get("/founder/security")
async def security_summary(_: str = Depends(require_internal_token)) -> dict[str, Any]:
    rows = read_csv("runtime", "security_findings.csv")
    return {
        "open_findings": sum(1 for r in rows if (r.get("status") or "").lower() == "open"),
        "critical_open": sum(
            1
            for r in rows
            if (r.get("severity") or "").lower() == "critical"
            and (r.get("status") or "").lower() == "open"
        ),
        "internal_api_unauth_24h": None,
        "last_secret_scan": None,
    }


@router.get("/founder/growth")
async def growth_summary(_: str = Depends(require_internal_token)) -> dict[str, Any]:
    rows = read_csv("runtime", "experiments.csv")
    return {
        "experiments_active": sum(1 for r in rows if (r.get("status") or "").lower() == "active"),
        "experiments_won_30d": sum(1 for r in rows if (r.get("status") or "").lower() == "won"),
        "experiments_killed_30d": sum(1 for r in rows if (r.get("status") or "").lower() == "killed"),
    }


@router.get("/founder/marketing")
async def marketing_summary(_: str = Depends(require_internal_token)) -> dict[str, Any]:
    return {
        "drafts_pending": count_csv("runtime", "content_drafts.csv"),
        "scheduled_posts": None,
        "landing_visits_30d": None,
        "email_subscribers": None,
    }


@router.get("/founder/sovereign")
async def sovereign_summary(_: str = Depends(require_internal_token)) -> dict[str, Any]:
    return {
        "layers_total": 18,
        "layers_pass": None,
        "layers_blocked": None,
        "last_run": None,
    }


# Control plane summary endpoints (mirrors apps/web/app/control-plane).
@router.get("/control/summary")
async def control_summary(_: str = Depends(require_internal_token)) -> dict[str, Any]:
    return {
        "policies_loaded": count_csv("runtime", "policy_results.csv"),
        "agents_registered": count_csv("runtime", "agent_registry_state.csv"),
        "open_risks": count_csv("runtime", "risk_register.csv"),
        "scorecard_score": None,
    }


@router.get("/control/policies")
async def control_policies(_: str = Depends(require_internal_token)) -> list[dict[str, Any]]:
    return read_csv("runtime", "policy_results.csv")


@router.get("/control/agents")
async def control_agents(_: str = Depends(require_internal_token)) -> list[dict[str, Any]]:
    return read_csv("runtime", "agent_registry_state.csv")


@router.get("/control/scorecard")
async def control_scorecard(_: str = Depends(require_internal_token)) -> dict[str, Any]:
    rows = read_csv("runtime", "operating_scorecard.csv")
    last = rows[-1] if rows else {}
    return {
        "score": _maybe_float(last.get("score")),
        "as_of": last.get("as_of"),
        "components": {k: v for k, v in last.items() if k not in ("score", "as_of")},
    }


@router.get("/control/risks")
async def control_risks(_: str = Depends(require_internal_token)) -> list[dict[str, Any]]:
    return read_csv("runtime", "risk_register.csv")
