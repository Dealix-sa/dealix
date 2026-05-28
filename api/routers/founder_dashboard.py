"""Founder dashboard router — the daily/weekly view for the solo founder.

GET /api/v1/founder/dashboard
  Consolidates: leads waiting > 24h, friction events last 7 days, retainer
  renewals due in next 7 days, pending approvals, recent proof events,
  capital assets registered this week. Admin-key gated.

This is the operator-facing "command center" — NOT the public portal.
"""
from __future__ import annotations

from datetime import UTC, datetime, timedelta, timezone
from typing import Any

from fastapi import APIRouter, Depends

from api.security.api_key import require_admin_key

router = APIRouter(prefix="/api/v1/founder", tags=["founder"])


def _leads_waiting() -> dict[str, Any]:
    try:
        from auto_client_acquisition import lead_inbox
        records = lead_inbox.list_records(limit=200) if hasattr(lead_inbox, "list_records") else []
        if not records:
            return {"count": 0, "items": []}
        cutoff = datetime.now(UTC) - timedelta(hours=24)
        items: list[dict[str, Any]] = []
        for r in records:
            try:
                created = datetime.fromisoformat(getattr(r, "created_at", "") or "")
                if created.tzinfo is None:
                    created = created.replace(tzinfo=UTC)
            except Exception:
                continue
            if created < cutoff:
                items.append({
                    "id": getattr(r, "id", ""),
                    "name": getattr(r, "name", ""),
                    "company": getattr(r, "company", ""),
                    "sector": getattr(r, "sector", ""),
                    "created_at": created.isoformat(),
                })
        return {"count": len(items), "items": items[:20]}
    except Exception:
        return {"count": 0, "items": [], "note": "lead_inbox_unavailable"}


def _friction_last_7d(customer_id: str | None = None) -> dict[str, Any]:
    try:
        from auto_client_acquisition.friction_log.aggregator import aggregate
        agg = aggregate(customer_id=customer_id or "dealix_internal", window_days=7)
        return agg.to_dict()
    except Exception:
        return {"total": 0, "note": "friction_log_unavailable"}


def _renewals_due() -> dict[str, Any]:
    try:
        from auto_client_acquisition.payment_ops.renewal_scheduler import list_due
        due = list_due()
        return {
            "count": len(due),
            "items": [
                {"customer_id": s.customer_id, "plan": s.plan, "amount_sar": s.amount_sar,
                 "next_attempt_at": s.next_attempt_at, "cycle": s.cycle_count}
                for s in due[:10]
            ],
        }
    except Exception:
        return {"count": 0, "items": [], "note": "renewal_scheduler_unavailable"}


def _pending_approvals() -> dict[str, Any]:
    try:
        from auto_client_acquisition.approval_center.approval_store import (
            get_default_approval_store,
        )
        store = get_default_approval_store()
        items = store.list_pending() if hasattr(store, "list_pending") else []
        return {"count": len(items), "items": items[:20]}
    except Exception:
        return {"count": 0, "items": [], "note": "approval_center_unavailable"}


def _recent_proof_events() -> dict[str, Any]:
    try:
        from auto_client_acquisition.proof_ledger.file_backend import get_default_ledger
        ledger = get_default_ledger()
        events = ledger.list_events(limit=20)
        return {
            "count": len(events),
            "items": [
                {"id": e.id, "event_type": str(e.event_type),
                 "customer_handle": e.customer_handle,
                 "created_at": e.created_at.isoformat()}
                for e in events
            ],
        }
    except Exception:
        return {"count": 0, "items": [], "note": "proof_ledger_unavailable"}


def _capital_this_week() -> dict[str, Any]:
    try:
        from auto_client_acquisition.capital_os.capital_ledger import list_assets
        assets = list_assets(limit=100)
        cutoff = datetime.now(UTC) - timedelta(days=7)
        recent: list[dict[str, Any]] = []
        for a in assets:
            try:
                created = datetime.fromisoformat(a.created_at)
                if created.tzinfo is None:
                    created = created.replace(tzinfo=UTC)
            except Exception:
                continue
            if created >= cutoff:
                recent.append({
                    "asset_id": a.asset_id,
                    "asset_type": a.asset_type,
                    "owner": a.owner,
                    "engagement_id": a.engagement_id,
                    "created_at": a.created_at,
                })
        return {"count": len(recent), "items": recent[:20]}
    except Exception:
        return {"count": 0, "items": [], "note": "capital_ledger_unavailable"}


def _subscription_summary() -> dict[str, Any]:
    """Aggregate active managed-ops subscriptions into MRR snapshot."""
    try:
        from auto_client_acquisition.payment_ops.renewal_scheduler import list_due
        # list_due returns schedules whose next_attempt_at has elapsed;
        # for MRR snapshot we also want the in-flight count
        due = list_due()
        return {
            "due_count": len(due),
            "due_mrr_sar": sum(s.amount_sar for s in due),
            "is_estimate": True,
        }
    except Exception:
        return {"due_count": 0, "due_mrr_sar": 0, "note": "renewal_scheduler_unavailable"}


def _hermes_summary() -> dict[str, Any]:
    """7-day Hermes run summary for the cockpit (no PII, counts only)."""
    try:
        import json as _json
        from pathlib import Path as _Path
        from datetime import timedelta as _timedelta
        p = _Path("var/hermes-runs.jsonl")
        if not p.is_absolute():
            from dealix.hermes import audit as _audit
            p = _audit._path()  # noqa: SLF001
        if not p.is_file():
            return {"total_runs": 0, "by_decision": {}, "note": "no_runs_yet"}
        cutoff = (datetime.now(UTC) - _timedelta(days=7)).isoformat()
        by_decision: dict[str, int] = {}
        by_sub_agent: dict[str, int] = {}
        total = 0
        for line in p.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            try:
                row = _json.loads(line)
            except _json.JSONDecodeError:
                continue
            if row.get("occurred_at", "") < cutoff:
                continue
            total += 1
            gd = row.get("governance_decision") or {}
            d = gd.get("decision", "unknown")
            by_decision[d] = by_decision.get(d, 0) + 1
            sub = row.get("sub_agent") or "unrouted"
            by_sub_agent[sub] = by_sub_agent.get(sub, 0) + 1
        return {
            "window_days": 7,
            "total_runs": total,
            "by_decision": by_decision,
            "by_sub_agent": by_sub_agent,
        }
    except Exception:
        return {"total_runs": 0, "by_decision": {}, "note": "hermes_audit_unavailable"}


@router.get("/dashboard", dependencies=[Depends(require_admin_key)])
async def founder_dashboard() -> dict[str, Any]:
    """Single consolidated founder view. Admin-key gated."""
    friction = _friction_last_7d()
    return {
        "generated_at": datetime.now(UTC).isoformat(),
        "leads_waiting_24h_plus": _leads_waiting(),
        "friction_last_7d": friction,
        "frictions_top": friction.get("top_signals", [])[:5] if isinstance(friction, dict) else [],
        "renewals_due_next_7d": _renewals_due(),
        "subscription_summary": _subscription_summary(),
        "pending_approvals": _pending_approvals(),
        "recent_proof_events": _recent_proof_events(),
        "capital_assets_this_week": _capital_this_week(),
        "hermes_last_7d": _hermes_summary(),
        "governance_decision": "allow",
        "is_estimate": True,
    }


@router.get("/dashboard/{customer_id}", dependencies=[Depends(require_admin_key)])
async def founder_customer_view(customer_id: str) -> dict[str, Any]:
    """Per-customer drill-down."""
    return {
        "customer_id": customer_id,
        "generated_at": datetime.now(UTC).isoformat(),
        "friction_last_30d": _friction_last_7d(customer_id),
        "governance_decision": "allow",
    }
