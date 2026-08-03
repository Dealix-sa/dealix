"""Customer-safe Client Value Room adapter.

This router extends the canonical customer portal namespace. It composes
existing Dealix sources into the Client Value Room contract; it does not
create a second store or execute external actions.
"""
from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from fastapi import APIRouter

from scripts.commercial.build_client_value_room import build_client_value_room

router = APIRouter(prefix="/api/v1/customer-portal", tags=["customer-portal"])


def _iso(value: Any) -> str | None:
    if value is None:
        return None
    if isinstance(value, datetime):
        return value.astimezone(UTC).isoformat()
    isoformat = getattr(value, "isoformat", None)
    if callable(isoformat):
        try:
            return str(isoformat())
        except Exception:
            return None
    text = str(value).strip()
    return text or None


def _enum_value(value: Any) -> str:
    raw = getattr(value, "value", value)
    return str(raw).strip()


def _safe_text(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _customer_profile(customer_handle: str) -> dict[str, Any]:
    profile: dict[str, Any] = {}
    try:
        from auto_client_acquisition.customer_brain import get_snapshot

        snapshot = get_snapshot(customer_handle=customer_handle)
        if snapshot:
            raw = getattr(snapshot, "profile", {})
            if isinstance(raw, dict):
                profile = raw
    except Exception:
        pass
    return {
        "client_name": _safe_text(profile.get("company_name")) or customer_handle,
        "sector": _safe_text(profile.get("sector")),
        "country": _safe_text(profile.get("country")) or "Saudi Arabia",
    }


def _service_sessions(customer_handle: str) -> list[Any]:
    try:
        from auto_client_acquisition.service_sessions import list_sessions

        return list(list_sessions(customer_handle=customer_handle, limit=100))
    except Exception:
        return []


def _work_items_and_deliverables(sessions: list[Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    work_items: list[dict[str, Any]] = []
    deliverables: list[dict[str, Any]] = []
    for session in sessions:
        session_id = _safe_text(getattr(session, "id", None)) or _safe_text(
            getattr(session, "session_id", None)
        )
        status = _enum_value(getattr(session, "status", "unknown"))
        updated_at = _iso(getattr(session, "updated_at", None))
        work_items.append(
            {
                "work_item_id": session_id,
                "title": _safe_text(getattr(session, "service_name", None))
                or _safe_text(getattr(session, "service_type", None))
                or "Customer engagement",
                "stage": status,
                "owner": _safe_text(getattr(session, "owner", None)),
                "status": "blocked" if status in {"blocked", "failed"} else status,
                "due_date": _iso(getattr(session, "due_at", None)),
                "dependencies": [],
                "evidence_refs": [],
                "last_updated_at": updated_at,
            }
        )
        completion_evidence = []
        proof_ref = _safe_text(getattr(session, "proof_ref", None))
        if proof_ref:
            completion_evidence.append(proof_ref)
        deliverables.append(
            {
                "deliverable": _safe_text(getattr(session, "service_name", None))
                or _safe_text(getattr(session, "service_type", None))
                or "Customer engagement",
                "completion_status": "completed"
                if status in {"delivered", "completed", "proof_pending"}
                else "in_progress"
                if status in {"active", "in_progress"}
                else status,
                "completion_evidence": completion_evidence,
                "acceptance_status": "not_requested",
                "acceptance_evidence": [],
                "exceptions": [],
            }
        )
    return work_items, deliverables


def _decisions(customer_handle: str) -> list[dict[str, Any]]:
    try:
        from auto_client_acquisition.approval_center import get_default_approval_store

        pending = get_default_approval_store().list_pending()
    except Exception:
        pending = []

    scoped: list[dict[str, Any]] = []
    for item in pending:
        searchable = " ".join(
            filter(
                None,
                [
                    _safe_text(getattr(item, "customer_handle", None)),
                    _safe_text(getattr(item, "proof_impact", None)),
                    _safe_text(getattr(item, "summary_ar", None)),
                    _safe_text(getattr(item, "summary_en", None)),
                ],
            )
        )
        if customer_handle not in searchable:
            continue
        scoped.append(
            {
                "decision_id": _safe_text(getattr(item, "id", None)),
                "decision": _safe_text(getattr(item, "summary_en", None))
                or _safe_text(getattr(item, "summary_ar", None))
                or "Approval required",
                "reason": _safe_text(getattr(item, "reason", None)),
                "options": [],
                "recommended_option": None,
                "impact": _safe_text(getattr(item, "proof_impact", None)),
                "risk": _safe_text(getattr(item, "risk_level", None)),
                "deadline": _iso(getattr(item, "expires_at", None)),
                "approver": None,
                "rollback": None,
                "status": "pending",
            }
        )
    return scoped


def _proof_timeline(customer_handle: str) -> list[dict[str, Any]]:
    try:
        from auto_client_acquisition.proof_ledger.factory import get_default_ledger

        events = get_default_ledger().list_events(customer_handle=customer_handle, limit=100)
    except Exception:
        events = []

    timeline: list[dict[str, Any]] = []
    for event in events:
        is_synthetic = bool(getattr(event, "is_synthetic", False))
        payload = getattr(event, "payload", {})
        if isinstance(payload, dict):
            is_synthetic = is_synthetic or bool(
                payload.get("is_synthetic") or payload.get("synthetic")
            )
        timeline.append(
            {
                "event_id": _safe_text(getattr(event, "id", None)),
                "event_type": _enum_value(getattr(event, "event_type", "unknown")),
                "occurred_at": _iso(getattr(event, "created_at", None)),
                "actor": "Dealix",
                "object": _safe_text(getattr(event, "entity_type", None)),
                "summary": "Evidence event recorded",
                "source": "proof_ledger",
                "evidence_refs": [
                    ref
                    for ref in [_safe_text(getattr(event, "evidence_source", None))]
                    if ref
                ],
                "visibility": "customer_safe",
                "is_synthetic": is_synthetic,
            }
        )
    return timeline


def _value_metrics(customer_handle: str) -> list[dict[str, Any]]:
    try:
        from auto_client_acquisition.value_os.value_ledger import list_events

        events = list_events(customer_id=customer_handle)
    except Exception:
        events = []

    metrics: list[dict[str, Any]] = []
    for event in events:
        raw = event.to_dict() if hasattr(event, "to_dict") else getattr(event, "__dict__", {})
        if not isinstance(raw, dict):
            continue
        metrics.append(
            {
                "metric": raw.get("metric") or raw.get("metric_name") or raw.get("kind"),
                "baseline": raw.get("baseline"),
                "target": raw.get("target"),
                "current": raw.get("current") or raw.get("value"),
                "unit": raw.get("unit"),
                "measurement_window": raw.get("measurement_window") or raw.get("period"),
                "source": raw.get("source") or raw.get("source_ref"),
                "confidence": raw.get("confidence"),
                "verified": raw.get("verified") is True,
                "customer_accepted": raw.get("customer_accepted") is True,
                "evidence_refs": raw.get("evidence_refs")
                if isinstance(raw.get("evidence_refs"), list)
                else [],
            }
        )
    return metrics


def _risk_summary(customer_handle: str) -> list[dict[str, Any]]:
    try:
        from auto_client_acquisition.friction_log.store import list_events

        events = list_events(customer_id=customer_handle, since_days=90, limit=100)
    except Exception:
        events = []

    risks: list[dict[str, Any]] = []
    for event in events:
        severity = _enum_value(getattr(event, "severity", "low"))
        risks.append(
            {
                "risk_id": _safe_text(getattr(event, "id", None)),
                "severity": severity,
                "business_impact": _safe_text(getattr(event, "notes", None)),
                "root_cause_status": "under_review",
                "owner": "Dealix",
                "mitigation": None,
                "target_resolution": None,
                "customer_action": None,
            }
        )
    return risks


def compose_client_value_room(customer_handle: str) -> dict[str, Any]:
    """Compose a customer-safe room from canonical existing sources only."""
    handle = (customer_handle or "").strip() or "Slot-A"
    profile = _customer_profile(handle)
    sessions = _service_sessions(handle)
    work_items, deliverables = _work_items_and_deliverables(sessions)
    decisions = _decisions(handle)
    timeline = _proof_timeline(handle)
    value_metrics = _value_metrics(handle)
    risks = _risk_summary(handle)
    source_times = [item.get("occurred_at") for item in timeline if item.get("occurred_at")]

    engagement = {
        **profile,
        "engagement_id": handle,
        "pilot_id": None,
        "current_phase": _enum_value(getattr(sessions[0], "status", "diagnostic"))
        if sessions
        else "diagnostic",
        "overall_status": "at_risk"
        if any(item.get("severity") in {"high", "critical"} for item in risks)
        else "on_track",
        "scope_in": [],
        "scope_out": [],
        "owner_matrix": {},
        "baseline": None,
        "target_metrics": [],
        "acceptance_criteria": [],
        "stop_rule": None,
        "top_outcomes": [],
        "next_checkpoint": None,
        "work_items": work_items,
        "decisions": decisions,
        "risks": risks,
        "deliverables": deliverables,
        "value_metrics": value_metrics,
        "timeline": timeline,
        "renewal_recommendation": "withheld_pending_evidence",
        "renewal_evidence": [],
        "future_scope": [],
        "renewal_approval_status": "not_requested",
        "source_last_updated_at": max(source_times) if source_times else None,
        "stale_sources": [],
        "synthetic_evidence_present": any(item.get("is_synthetic") for item in timeline),
    }
    room = build_client_value_room(engagement)
    room["client_context"]["customer_handle"] = handle
    room["source_summary"] = {
        "service_sessions": len(sessions),
        "approval_items": len(decisions),
        "proof_events": len(timeline),
        "value_events": len(value_metrics),
        "risk_events": len(risks),
    }
    room["disclosures"]["customer_safe_adapter"] = True
    room["disclosures"]["no_duplicate_storage"] = True
    return room


@router.get("/{customer_handle}/value-room")
async def client_value_room(customer_handle: str) -> dict[str, Any]:
    """Read-only client value room. Missing evidence is disclosed, never invented."""
    return compose_client_value_room(customer_handle)
