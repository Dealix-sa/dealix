"""Governance event log (M4) — durable, queryable record of governed-ops
decisions: blocked actions, policy violations, approval decisions, and
governed-day phase outcomes.

Built on the append-only :mod:`revenue_memory` event store (which already
has an in-memory and a Postgres backend) — this module is a thin,
governance-focused facade, not a new storage engine. It answers the
founder question the proof ledger cannot: *which gate blocked what, when,
and why.*

Events are recorded under the sentinel customer id ``"dealix"`` (the
company itself) so they form one queryable stream independent of any
single customer.
"""
from __future__ import annotations

from typing import Any

from auto_client_acquisition.revenue_memory.event_store import (
    EventStore,
    get_default_store,
)
from auto_client_acquisition.revenue_memory.events import (
    RevenueEvent,
    event_to_dict,
    make_event,
)

GOVERNANCE_EVENT_TYPES: tuple[str, ...] = (
    "governance.action_blocked",
    "governance.policy_violated",
    "governance.approval_created",
    "governance.approval_decision",
    "governance.phase_started",
    "governance.phase_completed",
    "governance.phase_degraded",
)

_GOVERNANCE_CUSTOMER_ID = "dealix"
_SUBJECT_TYPE = "governance"

_STORE: EventStore | None = None


def set_governance_store(store: EventStore | None) -> None:
    """Wire a specific store (production points this at the Postgres store;
    tests inject an in-memory one). ``None`` reverts to the process default."""
    global _STORE
    _STORE = store


def _store() -> EventStore:
    return _STORE if _STORE is not None else get_default_store()


def _emit(
    event_type: str,
    *,
    subject_id: str,
    payload: dict[str, Any],
    actor: str = "system",
    correlation_id: str | None = None,
) -> RevenueEvent:
    event = make_event(
        event_type=event_type,
        customer_id=_GOVERNANCE_CUSTOMER_ID,
        subject_type=_SUBJECT_TYPE,
        subject_id=subject_id or event_type,
        payload=payload,
        actor=actor,
        correlation_id=correlation_id,
    )
    _store().append(event)
    return event


# ─── Recorders ───────────────────────────────────────────────────

def record_blocked(
    *,
    action_type: str,
    reason: str,
    actor: str = "system",
    subject_id: str = "",
    correlation_id: str | None = None,
    extra: dict[str, Any] | None = None,
) -> RevenueEvent:
    """An action was stopped by a governance gate."""
    return _emit(
        "governance.action_blocked",
        subject_id=subject_id or action_type,
        payload={"action_type": action_type, "reason": reason, **(extra or {})},
        actor=actor,
        correlation_id=correlation_id,
    )


def record_policy_violation(
    *,
    policy: str,
    detail: str,
    actor: str = "system",
    subject_id: str = "",
    correlation_id: str | None = None,
) -> RevenueEvent:
    """A non-negotiable / policy was violated (caught before any external effect)."""
    return _emit(
        "governance.policy_violated",
        subject_id=subject_id or policy,
        payload={"policy": policy, "detail": detail},
        actor=actor,
        correlation_id=correlation_id,
    )


def record_approval_created(
    *,
    approval_id: str,
    action_type: str,
    risk_level: str = "low",
    actor: str = "system",
) -> RevenueEvent:
    """An approval request entered the governed queue."""
    return _emit(
        "governance.approval_created",
        subject_id=approval_id,
        payload={"action_type": action_type, "risk_level": risk_level},
        actor=actor,
    )


def record_approval_decision(
    *,
    approval_id: str,
    decision: str,
    who: str,
    reason: str = "",
) -> RevenueEvent:
    """A human (or founder rule) approved / rejected an approval request."""
    return _emit(
        "governance.approval_decision",
        subject_id=approval_id,
        payload={"decision": decision, "reason": reason},
        actor=who,
    )


def record_phase(
    *,
    phase: str,
    status: str,
    summary: str = "",
    error: str = "",
    correlation_id: str | None = None,
) -> RevenueEvent:
    """A governed-day phase outcome. ``status`` is started | ok | degraded."""
    if status == "started":
        event_type = "governance.phase_started"
    elif status == "degraded":
        event_type = "governance.phase_degraded"
    else:
        event_type = "governance.phase_completed"
    return _emit(
        event_type,
        subject_id=phase,
        payload={"phase": phase, "status": status, "summary": summary, "error": error},
        correlation_id=correlation_id,
    )


# ─── Queries ─────────────────────────────────────────────────────

def query(
    *,
    event_types: tuple[str, ...] | None = None,
    limit: int = 100,
) -> list[dict[str, Any]]:
    """Recent governance events, newest first, as JSON dicts."""
    limit = max(1, min(int(limit), 1000))
    types = event_types or GOVERNANCE_EVENT_TYPES
    rows = list(
        _store().read_for_customer(_GOVERNANCE_CUSTOMER_ID, event_types=types)
    )
    rows.sort(key=lambda e: (e.occurred_at, e.event_id), reverse=True)
    return [event_to_dict(e) for e in rows[:limit]]


def query_blocked(limit: int = 100) -> list[dict[str, Any]]:
    """The blocked-actions audit log — what gates stopped, newest first."""
    return query(
        event_types=("governance.action_blocked", "governance.policy_violated"),
        limit=limit,
    )


def query_recent(limit: int = 100) -> list[dict[str, Any]]:
    """All governance events, newest first."""
    return query(limit=limit)


__all__ = [
    "GOVERNANCE_EVENT_TYPES",
    "set_governance_store",
    "record_blocked",
    "record_policy_violation",
    "record_approval_created",
    "record_approval_decision",
    "record_phase",
    "query",
    "query_blocked",
    "query_recent",
]
