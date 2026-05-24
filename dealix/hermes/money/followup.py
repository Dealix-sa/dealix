"""Follow-up Commander — schedules and drafts follow-ups for outcomes-in-flight."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

from dealix.hermes.core.outcomes import get_outcome_store
from dealix.hermes.core.schemas import OutcomeStatus


class FollowupCommander:
    def due_today(self, *, sla_hours: int = 48) -> list[dict]:
        now = datetime.now(timezone.utc)
        out = []
        for o in get_outcome_store().list():
            if o.status not in {OutcomeStatus.SENT.value, OutcomeStatus.REPLIED.value}:
                continue
            age = now - o.created_at
            if age >= timedelta(hours=sla_hours):
                out.append(
                    {
                        "outcome_id": o.id,
                        "execution_id": o.execution_id,
                        "status": o.status,
                        "age_hours": round(age.total_seconds() / 3600, 1),
                        "draft": (
                            "Friendly nudge: any feedback on the proposal? "
                            "Happy to adjust scope or timing."
                        ),
                        "external_send": False,
                    }
                )
        return out
