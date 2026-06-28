"""Follow-up Engine — generate D1 / D3 / D7 follow-up tasks.

Tasks are drafts only. Opt-out is always respected: a card whose account has
opted out produces no follow-up tasks. After D7 with no reply, the engine
recommends moving the account to nurture/hold rather than chasing.
"""

from __future__ import annotations

from typing import Any, Mapping

from app.commercial.schemas import FollowUpTask

# Cadence: (day, note).
_CADENCE = (
    (1, "D1: gentle nudge — confirm the message landed; offer a quick call."),
    (3, "D3: add value — share one relevant, truthful insight (no claims)."),
    (7, "D7: final touch — if no reply, move to nurture/hold. Do not chase."),
)


def build_followup_tasks(
    card_id: str,
    channel: str,
    owner: str = "unassigned",
    opted_out: bool = False,
) -> list[FollowUpTask]:
    if opted_out:
        return []
    tasks: list[FollowUpTask] = []
    for day, note in _CADENCE:
        tasks.append(
            FollowUpTask(
                task_id=f"task_{card_id}_d{day}",
                card_id=card_id,
                due_in_days=day,
                channel=channel,
                owner=owner,
                draft_note=note,
                status="open",
            )
        )
    return tasks


def build_followups_for_cards(
    cards: list[Any],
    accounts_by_id: Mapping[str, Any] | None = None,
) -> list[FollowUpTask]:
    accounts_by_id = accounts_by_id or {}
    out: list[FollowUpTask] = []
    for card in cards:
        card_id = _get(card, "card_id")
        channel = _get(card, "recommended_channel") or "email"
        account_id = _get(card, "account_id")
        account = accounts_by_id.get(account_id)
        opted_out = False
        if account is not None:
            status = str(_get(account, "contactability_status") or "").lower()
            opted_out = status in ("opted_out", "blocked") or bool(_get(account, "email_opt_out"))
        owner = (_get(account, "owner") if account else None) or "unassigned"
        out.extend(build_followup_tasks(card_id, channel, owner, opted_out))
    return out


def _get(obj: Any, key: str) -> Any:
    if isinstance(obj, Mapping):
        return obj.get(key)
    return getattr(obj, key, None)
