"""
Follow-up cadence — recommends timing, never sends.

Cadence keeps a polite, sovereign-paced loop. Sami sends every message
manually; this module is just memory + suggestion.
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

from pydantic import BaseModel


class FollowUpStep(BaseModel):
    day_offset: int
    channel: str
    message_intent: str


DEFAULT_CADENCE: tuple[FollowUpStep, ...] = (
    FollowUpStep(day_offset=0, channel="manual_whatsapp", message_intent="initial intro"),
    FollowUpStep(day_offset=2, channel="manual_whatsapp", message_intent="light bump + asset link"),
    FollowUpStep(day_offset=5, channel="manual_email", message_intent="value recap + propose call"),
    FollowUpStep(day_offset=10, channel="manual_email", message_intent="final polite check-in"),
)


def schedule_from(start: datetime | None = None) -> list[tuple[datetime, FollowUpStep]]:
    base = start or datetime.now(UTC)
    return [(base + timedelta(days=step.day_offset), step) for step in DEFAULT_CADENCE]
