"""Governed Day (M3) — the single canonical orchestration entrypoint.

Before this module the "autonomous day" was 6+ subprocess-chain scripts
that returned only exit codes. ``run_governed_day`` replaces that with one
observable, in-process call: it runs an ordered list of named phases, each
phase a callable that returns a structured result and **never raises**
(failures are recorded as ``degraded``, not crashes). Every phase outcome
is written to the durable governance log (M4).

A phase is a ``(name, fn)`` pair where ``fn() -> dict`` may return
``{"summary": str, "status": "ok"|"degraded"|"blocked", ...}``. New phases
(e.g. release-due-follow-ups from the sequencing engine) register by
extending :data:`DEFAULT_PHASES` or passing ``phases=`` explicitly.

Nothing here sends anything externally — phases only prepare, sweep, and
snapshot. External actions remain behind the approval gate.
"""
from __future__ import annotations

import uuid
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any

from auto_client_acquisition.governance_os import governance_log

Phase = tuple[str, Callable[[], dict[str, Any]]]


@dataclass
class PhaseResult:
    name: str
    status: str  # "ok" | "degraded" | "blocked"
    summary: str = ""
    error: str = ""
    started_at: str = ""
    finished_at: str = ""


@dataclass
class GovernedDayResult:
    correlation_id: str
    started_at: str
    finished_at: str = ""
    verdict: str = "ok"  # "ok" | "degraded" | "blocked"
    phases: list[PhaseResult] = field(default_factory=list)
    counts: dict[str, int] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "correlation_id": self.correlation_id,
            "started_at": self.started_at,
            "finished_at": self.finished_at,
            "verdict": self.verdict,
            "counts": self.counts,
            "phases": [
                {
                    "name": p.name,
                    "status": p.status,
                    "summary": p.summary,
                    "error": p.error,
                    "started_at": p.started_at,
                    "finished_at": p.finished_at,
                }
                for p in self.phases
            ],
        }


# ─── Built-in phases ─────────────────────────────────────────────

def _phase_expire_overdue_approvals() -> dict[str, Any]:
    from auto_client_acquisition.approval_center.approval_store import (
        get_default_approval_store,
    )

    expired = get_default_approval_store().expire_overdue()
    return {"summary": f"{expired} overdue approval(s) expired", "expired": expired}


def _phase_snapshot_pending_approvals() -> dict[str, Any]:
    from auto_client_acquisition.approval_center.approval_store import (
        get_default_approval_store,
    )

    pending = get_default_approval_store().list_pending()
    return {
        "summary": f"{len(pending)} approval(s) awaiting the founder",
        "pending": len(pending),
    }


def _phase_snapshot_blocked_actions() -> dict[str, Any]:
    blocked = governance_log.query_blocked(limit=200)
    return {
        "summary": f"{len(blocked)} blocked action(s) in the governance log",
        "blocked": len(blocked),
    }


DEFAULT_PHASES: list[Phase] = [
    ("expire_overdue_approvals", _phase_expire_overdue_approvals),
    ("snapshot_pending_approvals", _phase_snapshot_pending_approvals),
    ("snapshot_blocked_actions", _phase_snapshot_blocked_actions),
]


# ─── Entrypoint ──────────────────────────────────────────────────

def run_governed_day(
    *,
    phases: list[Phase] | None = None,
    dry_run: bool = False,
) -> GovernedDayResult:
    """Run one governed day. Observable, in-process, never raises.

    ``dry_run=True`` records every phase as planned without executing it —
    useful for verifying wiring without side effects.
    """
    correlation_id = f"govday_{uuid.uuid4().hex[:16]}"
    result = GovernedDayResult(
        correlation_id=correlation_id,
        started_at=datetime.now(UTC).isoformat(),
    )
    ran = phases if phases is not None else DEFAULT_PHASES

    for name, fn in ran:
        started = datetime.now(UTC)
        governance_log.record_phase(
            phase=name, status="started", correlation_id=correlation_id
        )
        if dry_run:
            result.phases.append(
                PhaseResult(
                    name=name,
                    status="ok",
                    summary="dry-run: not executed",
                    started_at=started.isoformat(),
                    finished_at=started.isoformat(),
                )
            )
            governance_log.record_phase(
                phase=name, status="ok", summary="dry-run",
                correlation_id=correlation_id,
            )
            continue
        try:
            out = fn() or {}
            status = str(out.get("status", "ok"))
            summary = str(out.get("summary", ""))
            error = ""
        except Exception as exc:  # noqa: BLE001 — phase failures must not crash the day
            status = "degraded"
            summary = ""
            error = f"{type(exc).__name__}: {exc}"
        finished = datetime.now(UTC)
        result.phases.append(
            PhaseResult(
                name=name,
                status=status,
                summary=summary,
                error=error,
                started_at=started.isoformat(),
                finished_at=finished.isoformat(),
            )
        )
        governance_log.record_phase(
            phase=name, status=status, summary=summary, error=error,
            correlation_id=correlation_id,
        )

    result.finished_at = datetime.now(UTC).isoformat()
    statuses = {p.status for p in result.phases}
    if "blocked" in statuses:
        result.verdict = "blocked"
    elif "degraded" in statuses:
        result.verdict = "degraded"
    else:
        result.verdict = "ok"
    result.counts = {
        "phases": len(result.phases),
        "ok": sum(1 for p in result.phases if p.status == "ok"),
        "degraded": sum(1 for p in result.phases if p.status == "degraded"),
        "blocked": sum(1 for p in result.phases if p.status == "blocked"),
    }
    global _LAST_RESULT
    _LAST_RESULT = result
    return result


_LAST_RESULT: GovernedDayResult | None = None


def get_last_governed_day_result() -> GovernedDayResult | None:
    """The most recent run in this process (None if the day has not run)."""
    return _LAST_RESULT


__all__ = [
    "Phase",
    "PhaseResult",
    "GovernedDayResult",
    "DEFAULT_PHASES",
    "run_governed_day",
    "get_last_governed_day_result",
]
