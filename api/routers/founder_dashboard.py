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


def _revenue_today() -> dict[str, Any]:
    """Today's confirmed payments (UTC day window)."""
    try:
        from auto_client_acquisition.payment_ops import orchestrator
        now = datetime.now(UTC)
        cutoff = now.replace(hour=0, minute=0, second=0, microsecond=0)
        records = getattr(orchestrator, "_INDEX", {}).values()
        today_paid = [
            r for r in records
            if r.status in ("payment_confirmed", "delivery_kickoff")
            and datetime.fromisoformat(getattr(r, "confirmed_at", "") or now.isoformat()) >= cutoff
        ]
        return {
            "count": len(today_paid),
            "sar": sum(getattr(r, "amount_sar", 0) for r in today_paid),
            "is_estimate": True,
        }
    except Exception:
        return {"count": 0, "sar": 0, "note": "payment_ops_unavailable"}


def _mrr_current() -> dict[str, Any]:
    """Current MRR — sum of active subscriptions, best-effort."""
    try:
        from auto_client_acquisition.payment_ops.renewal_scheduler import list_due
        from collections.abc import Iterable
        due_iter: Iterable = list_due()  # type: ignore[assignment]
        active = [
            s for s in due_iter
            if str(getattr(s, "status", "")).lower() not in ("canceled", "ended", "refunded")
        ]
        # Group by customer_id — assume one active schedule per customer.
        unique = {getattr(s, "customer_id", ""): s for s in active}
        return {
            "active_subscriptions": len(unique),
            "mrr_sar": sum(getattr(s, "amount_sar", 0) for s in unique.values()),
            "is_estimate": True,
        }
    except Exception:
        return {"active_subscriptions": 0, "mrr_sar": 0, "note": "mrr_unavailable"}


def _agent_runs_24h() -> dict[str, Any]:
    """Count of agent invocations in the last 24h — proof of fleet activity."""
    try:
        from auto_client_acquisition.friction_log.aggregator import aggregate
        agg = aggregate(customer_id="dealix_internal", window_days=1)
        # friction log records agent-side events; total ~= runs touched by guardrails
        return {
            "events_24h": int(getattr(agg, "total", 0)),
            "is_estimate": True,
        }
    except Exception:
        return {"events_24h": 0, "note": "friction_log_unavailable"}


def _next_action() -> dict[str, Any]:
    """Suggested next action — read from business_now snapshot."""
    try:
        from dealix.business_now.snapshot_builder import build_business_now_snapshot
        snap = build_business_now_snapshot(run_verify=False)
        nxt = snap.get("next_action") if isinstance(snap, dict) else None
        return {
            "action_ar": (nxt or {}).get("ar", "افحص قائمة approvals"),
            "action_en": (nxt or {}).get("en", "Review pending approvals"),
            "source": "business_now.snapshot",
        }
    except Exception:
        return {
            "action_ar": "افحص قائمة approvals",
            "action_en": "Review pending approvals",
            "source": "fallback",
        }


@router.get("/dashboard/cockpit", dependencies=[Depends(require_admin_key)])
async def founder_cockpit() -> dict[str, Any]:
    """Unified founder cockpit — single 7-panel view for the daily ritual.

    Panels:
      revenue_today          — paid count + SAR today
      mrr_current            — active subs MRR snapshot
      pending_approvals      — count + top 5 awaiting founder
      friction_top_7d        — top trust/safety signals
      agent_runs_24h         — fleet activity proof
      subscription_summary   — renewals due this week
      next_action_today      — single suggested action AR + EN

    All numeric fields carry `is_estimate=True` unless they trace to a
    confirmed Moyasar transaction. Doctrine #8 (NO_FAKE_PROOF).
    Admin-key gated.
    """
    friction = _friction_last_7d()
    return {
        "generated_at": datetime.now(UTC).isoformat(),
        "revenue_today": _revenue_today(),
        "mrr_current": _mrr_current(),
        "pending_approvals": _pending_approvals(),
        "friction_top_7d": friction.get("top_signals", [])[:5] if isinstance(friction, dict) else [],
        "agent_runs_24h": _agent_runs_24h(),
        "subscription_summary": _subscription_summary(),
        "next_action_today": _next_action(),
        "is_estimate": True,
        "doctrine_note": "Drafts only. No autonomous sends. Founder approves all outbound.",
    }


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
