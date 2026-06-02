"""Distribution metrics — deterministic counts over the draft + follow-up queues.

Counts only what the system can observe (drafts/follow-ups it generated).
Funnel outcomes (replies, calls booked, won/lost, revenue) are NOT invented
here — they come from prospect status the founder maintains, and revenue is
only ever recognised from paid evidence elsewhere in the platform.
"""

from __future__ import annotations

from collections import Counter
from typing import Any

from auto_client_acquisition.distribution_os.models import (
    Draft,
    Followup,
    FollowupStatus,
    Prospect,
)


def compute_metrics(
    drafts: list[Draft],
    followups: list[Followup],
    prospects: list[Prospect] | None = None,
) -> dict[str, Any]:
    by_status = Counter(d.status for d in drafts)
    by_type = Counter(d.draft_type for d in drafts)
    by_channel = Counter(d.channel for d in drafts)
    fu_due = sum(1 for f in followups if f.status == FollowupStatus.DUE.value)

    funnel: dict[str, int] = {}
    if prospects is not None:
        stage = Counter(p.status for p in prospects)
        funnel = dict(stage)

    return {
        "drafts_total": len(drafts),
        "drafts_by_status": dict(by_status),
        "drafts_by_type": dict(by_type),
        "drafts_by_channel": dict(by_channel),
        "followups_total": len(followups),
        "followups_due": fu_due,
        "prospect_funnel": funnel,
    }


__all__ = ["compute_metrics"]
