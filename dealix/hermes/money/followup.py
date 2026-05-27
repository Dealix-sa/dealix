"""FollowUpTracker — schedules + tracks follow-up actions on proposals."""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone


@dataclass
class FollowUp:
    id: str
    proposal_id: str
    due_at: datetime
    note: str
    status: str = "pending"   # pending | done | skipped
    done_at: datetime | None = None


@dataclass
class FollowUpTracker:
    _by_id: dict[str, FollowUp] = field(default_factory=dict)

    def schedule(self, *, proposal_id: str, in_days: int, note: str) -> FollowUp:
        f = FollowUp(
            id=f"flw_{uuid.uuid4().hex[:10]}",
            proposal_id=proposal_id,
            due_at=datetime.now(timezone.utc) + timedelta(days=in_days),
            note=note,
        )
        self._by_id[f.id] = f
        return f

    def complete(self, follow_up_id: str) -> FollowUp:
        f = self._by_id[follow_up_id]
        f.status = "done"
        f.done_at = datetime.now(timezone.utc)
        return f

    def skip(self, follow_up_id: str, *, reason: str) -> FollowUp:
        f = self._by_id[follow_up_id]
        f.status = "skipped"
        f.note = f"{f.note} | skipped: {reason}"
        return f

    def due(self) -> list[FollowUp]:
        now = datetime.now(timezone.utc)
        return [f for f in self._by_id.values() if f.status == "pending" and f.due_at <= now]

    def all(self) -> list[FollowUp]:
        return list(self._by_id.values())


__all__ = ["FollowUp", "FollowUpTracker"]
