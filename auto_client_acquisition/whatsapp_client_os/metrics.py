"""Conversion / funnel metrics for the WhatsApp Client OS.

Computed from the JSONL ledgers (no invented numbers). Returns rates and
counts suitable for the founder Ops UI and the weekly metrics report.
"""

from __future__ import annotations

from typing import Any

from auto_client_acquisition.whatsapp_client_os import client_profile_store as store


def _rate(num: int, den: int) -> float:
    return round(num / den, 3) if den else 0.0


def compute_metrics() -> dict[str, Any]:
    sessions = store.list_sessions(limit=10_000)
    assessments = store.list_assessments(limit=10_000)
    permissions = store.list_permissions(limit=10_000)
    handoffs = store.list_handoffs(limit=10_000)

    n_sessions = len(sessions)
    completed_assessments = sum(1 for a in assessments if a.completed)
    proposal_sessions = sum(
        1 for s in sessions if s.stage in {"proposal", "payment_handoff", "onboarding"}
    )
    payment_sessions = sum(1 for s in sessions if s.stage in {"payment_handoff", "onboarding"})
    handoff_sessions = sum(1 for s in sessions if s.handoff_requested or s.stage == "human_handoff")
    granted = sum(1 for p in permissions if p.granted)

    return {
        "schema_version": "1.0",
        "new_sessions": n_sessions,
        "assessments_started": len(assessments),
        "assessments_completed": completed_assessments,
        "assessment_completion_rate": _rate(completed_assessments, len(assessments)),
        "permission_requests": len(permissions),
        "permission_approval_rate": _rate(granted, len(permissions)),
        "proposal_request_rate": _rate(proposal_sessions, n_sessions),
        "payment_handoff_rate": _rate(payment_sessions, n_sessions),
        "human_handoff_count": len(handoffs),
        "human_handoff_rate": _rate(handoff_sessions, n_sessions),
        "handoff_reasons": _count_by(handoffs, "reason"),
        "stages": _count_by(sessions, "stage"),
        "recommended_offers": _count_by(assessments, "recommended_offer"),
    }


def _count_by(rows: list[Any], attr: str) -> dict[str, int]:
    out: dict[str, int] = {}
    for r in rows:
        key = str(getattr(r, attr, "") or "")
        if not key:
            continue
        out[key] = out.get(key, 0) + 1
    return dict(sorted(out.items(), key=lambda kv: kv[1], reverse=True))


__all__ = ["compute_metrics"]
