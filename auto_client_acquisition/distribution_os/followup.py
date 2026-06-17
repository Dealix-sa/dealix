"""Follow-up Engine — deterministic cadence + due-queue over a JSONL store.

Cadence (plan section 7): Day 0 first outreach, Day 2 follow-up 1, Day 4
follow-up 2, Day 7 close-the-loop. Later stages (post-reply, post-proposal,
etc.) are scheduled explicitly by the calling workflow. Follow-ups are
reminders for the founder — nothing is sent automatically.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime, timedelta
from enum import StrEnum
from typing import Any
from uuid import uuid4

from auto_client_acquisition.distribution_os._store import JsonlStore, now_iso
from auto_client_acquisition.distribution_os.draft_factory import DraftType

# (offset_days, draft_type) — the opening outreach cadence.
CADENCE: tuple[tuple[int, str], ...] = (
    (0, DraftType.OUTREACH_FIRST.value),
    (2, DraftType.OUTREACH_FOLLOWUP_1.value),
    (4, DraftType.OUTREACH_FOLLOWUP_2.value),
    (7, DraftType.BREAKUP.value),
)


class FollowupStatus(StrEnum):
    DUE = "due"
    SCHEDULED = "scheduled"
    COMPLETED = "completed"
    SKIPPED = "skipped"


@dataclass
class Followup:
    id: str = field(default_factory=lambda: f"fu_{uuid4().hex[:12]}")
    prospect_id: str = ""
    due_date: str = ""
    channel: str = "email"
    draft_type: str = DraftType.OUTREACH_FOLLOWUP_1.value
    message_ref: str = ""  # draft id once a draft exists
    status: str = FollowupStatus.SCHEDULED.value
    risk: str = "low"
    created_at: str = field(default_factory=now_iso)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


_store = JsonlStore(
    env_var="DEALIX_FOLLOWUPS_PATH", default_rel="var/followups.jsonl", id_field="id"
)


def _parse(date_str: str) -> datetime:
    dt = datetime.fromisoformat(date_str)
    return dt if dt.tzinfo else dt.replace(tzinfo=UTC)


def schedule_cadence(
    *,
    prospect_id: str,
    channel: str = "email",
    start_date: str | None = None,
) -> list[Followup]:
    """Schedule the full opening cadence for one prospect."""
    start = _parse(start_date) if start_date else datetime.now(UTC)
    out: list[Followup] = []
    for offset, dtype in CADENCE:
        fu = Followup(
            prospect_id=prospect_id,
            due_date=(start + timedelta(days=offset)).isoformat(),
            channel=channel,
            draft_type=dtype,
            status=FollowupStatus.SCHEDULED.value,
        )
        _store.append(fu.to_dict())
        out.append(fu)
    return out


def schedule_one(
    *,
    prospect_id: str,
    draft_type: str,
    offset_days: int,
    channel: str = "email",
    start_date: str | None = None,
) -> Followup:
    start = _parse(start_date) if start_date else datetime.now(UTC)
    fu = Followup(
        prospect_id=prospect_id,
        due_date=(start + timedelta(days=offset_days)).isoformat(),
        channel=channel,
        draft_type=draft_type,
    )
    _store.append(fu.to_dict())
    return fu


def due_followups(*, on_date: str | None = None) -> list[Followup]:
    """Follow-ups whose due_date has arrived and are not yet completed."""
    target = _parse(on_date) if on_date else datetime.now(UTC)
    latest: dict[str, dict[str, Any]] = {}
    for rec in _store.list():
        latest[str(rec.get("id"))] = rec
    out: list[Followup] = []
    for rec in latest.values():
        fu = Followup(**rec)
        if fu.status in {FollowupStatus.SCHEDULED.value, FollowupStatus.DUE.value}:
            try:
                if _parse(fu.due_date) <= target:
                    out.append(fu)
            except Exception:  # noqa: S112 — skip an unparseable due_date, keep scanning
                continue
    out.sort(key=lambda f: f.due_date)
    return out


def complete_followup(followup_id: str, *, message_ref: str = "") -> Followup | None:
    patch: dict[str, Any] = {"status": FollowupStatus.COMPLETED.value}
    if message_ref:
        patch["message_ref"] = message_ref
    rec = _store.patch(followup_id, patch)
    return Followup(**rec) if rec else None


def skip_followup(followup_id: str) -> Followup | None:
    rec = _store.patch(followup_id, {"status": FollowupStatus.SKIPPED.value})
    return Followup(**rec) if rec else None


def clear_for_test() -> None:
    _store.clear_for_test()


__all__ = [
    "CADENCE",
    "Followup",
    "FollowupStatus",
    "clear_for_test",
    "complete_followup",
    "due_followups",
    "schedule_cadence",
    "schedule_one",
    "skip_followup",
]
