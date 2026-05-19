"""Persistent follow-up sequencing engine (M7).

The ``FollowUpAgent`` plans a cadence in memory only — nothing was ever
scheduled or persisted, so a process restart lost every follow-up. This
engine materializes a lead's cadence into durable ``follow_up_tasks`` rows,
exposes the due ones, and tracks status as they move through the governed
queue: scheduled → drafted → queued → done | skipped.

Nothing here sends. A governed-day phase picks due tasks, drafts them via
``FollowUpAgent``, and queues an ``ApprovalRequest`` — the founder approves.

The cadence planner is pure (no DB) and reuses ``FollowUpAgent``'s
``DEFAULT_CADENCE_DAYS`` so the two never drift. Persistence helpers take a
SQLAlchemy ``Session`` so they test cleanly against sqlite.
"""
from __future__ import annotations

import uuid
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from typing import Any

from auto_client_acquisition.agents.followup import DEFAULT_CADENCE_DAYS


@dataclass
class PlannedTask:
    """A follow-up touch before it is persisted."""

    attempt: int
    channel: str
    scheduled_for: datetime


def plan_cadence(
    *,
    start: datetime | None = None,
    channel: str = "email",
    touches: int = len(DEFAULT_CADENCE_DAYS),
) -> list[PlannedTask]:
    """Pure: produce the cadence schedule for one lead.

    Touch ``n`` is offset by ``DEFAULT_CADENCE_DAYS[n]`` days from ``start``;
    attempts beyond the table reuse the final interval.
    """
    base = start or datetime.now(UTC)
    out: list[PlannedTask] = []
    for attempt in range(touches):
        idx = min(attempt, len(DEFAULT_CADENCE_DAYS) - 1)
        offset = DEFAULT_CADENCE_DAYS[idx]
        out.append(
            PlannedTask(
                attempt=attempt + 1,
                channel=channel,
                scheduled_for=base + timedelta(days=offset),
            )
        )
    return out


# ── Persistence helpers (session-injected) ────────────────────────

def materialize_tasks(
    session: Any,
    *,
    lead_id: str,
    start: datetime | None = None,
    channel: str = "email",
    touches: int = len(DEFAULT_CADENCE_DAYS),
) -> list[str]:
    """Persist a fresh cadence for ``lead_id`` as follow_up_tasks rows.

    Returns the new task ids. Caller commits the session.
    """
    from db.models import FollowUpTask

    now = datetime.now(UTC)
    ids: list[str] = []
    for planned in plan_cadence(start=start, channel=channel, touches=touches):
        task_id = f"fut_{uuid.uuid4().hex[:16]}"
        session.add(
            FollowUpTask(
                id=task_id,
                lead_id=lead_id,
                attempt=planned.attempt,
                channel=planned.channel,
                scheduled_for=planned.scheduled_for,
                status="scheduled",
                created_at=now,
                updated_at=now,
            )
        )
        ids.append(task_id)
    return ids


def due_tasks(session: Any, *, now: datetime | None = None, limit: int = 100) -> list[Any]:
    """Scheduled tasks whose time has come, oldest first."""
    from sqlalchemy import select

    from db.models import FollowUpTask

    cutoff = now or datetime.now(UTC)
    stmt = (
        select(FollowUpTask)
        .where(FollowUpTask.status == "scheduled")
        .where(FollowUpTask.scheduled_for <= cutoff)
        .order_by(FollowUpTask.scheduled_for)
        .limit(limit)
    )
    return list(session.execute(stmt).scalars().all())


def mark_task(
    session: Any,
    task_id: str,
    *,
    status: str,
    draft_approval_id: str | None = None,
) -> None:
    """Move a task to a new status (drafted | queued | done | skipped)."""
    from db.models import FollowUpTask

    task = session.get(FollowUpTask, task_id)
    if task is None:
        raise ValueError(f"follow_up_task {task_id} not found")
    task.status = status
    if draft_approval_id is not None:
        task.draft_approval_id = draft_approval_id
    task.updated_at = datetime.now(UTC)
    session.add(task)


__all__ = [
    "PlannedTask",
    "plan_cadence",
    "materialize_tasks",
    "due_tasks",
    "mark_task",
]
