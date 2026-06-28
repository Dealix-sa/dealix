"""Booking Desk — generate meeting options without touching a calendar.

Produces three booking options with suggested slots, an agenda, attendees and
preparation notes. It NEVER writes to a calendar unless
``CALENDAR_WRITE_ENABLED=true`` and the owner has explicitly decided to book —
both gated by :mod:`app.commercial.safety`.
"""

from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any

from app.commercial.safety import can_write_calendar
from app.commercial.schemas import BookingOption

DEFAULT_TZ = "Asia/Riyadh"


def _next_business_slots(base: datetime, count: int, duration_minutes: int) -> list[str]:
    """Suggest the next ``count`` slots at 10:00, 13:00, 16:00 on coming days."""
    slots: list[str] = []
    hours = [10, 13, 16]
    day_offset = 1
    i = 0
    while len(slots) < count:
        day = base + timedelta(days=day_offset)
        if day.weekday() >= 5 and day.weekday() == 5:  # Saturday in KSA week — skip Fri/Sat
            day_offset += 1
            continue
        hour = hours[i % len(hours)]
        slot = day.replace(hour=hour, minute=0, second=0, microsecond=0)
        slots.append(slot.strftime("%Y-%m-%d %H:%M ") + DEFAULT_TZ)
        i += 1
        if i % len(hours) == 0:
            day_offset += 1
    return slots


def _agenda_for(motion: str) -> list[str]:
    common = ["Confirm goals & success criteria", "Walk through fit & scope", "Agree next step"]
    if motion == "partnership_outreach":
        return ["Mutual fit & shared clients", "Partner model options", "Pilot scope & next step"]
    if motion in ("proposal_push", "upsell", "renewal"):
        return ["Review proposal brief", "Scope, timeline & pricing range", "Approval path & next step"]
    return common


def build_booking_option(
    card_id: str,
    motion: str = "sales_prospecting",
    duration_minutes: int = 30,
    booking_index: int = 0,
    now: datetime | None = None,
) -> BookingOption:
    base = now or datetime(2026, 6, 28, 9, 0, 0)
    # Calendar write is decided by the safety gate, never assumed.
    decision = can_write_calendar({"owner_decision": "pending"}, account={}, client_rules={})
    return BookingOption(
        booking_id=f"booking_{card_id}_{booking_index:03d}",
        card_id=card_id,
        duration_minutes=duration_minutes,
        timezone=DEFAULT_TZ,
        suggested_slots=_next_business_slots(base, 3, duration_minutes),
        agenda=_agenda_for(motion),
        attendees=["Dealix (founder/SDR)", "Client decision-maker"],
        preparation_notes=[
            "Review account ICP score & pain hypothesis",
            "Bring relevant (truthful, non-fabricated) examples only",
            "Prepare pricing RANGE — not a final price",
        ],
        calendar_write_enabled=decision.allowed,
        booking_status="proposed",
    )


def build_booking_options(cards: list[Any]) -> list[BookingOption]:
    """Generate booking options for cards whose owner may want a meeting."""
    out: list[BookingOption] = []
    for i, card in enumerate(cards):
        motion = getattr(card, "motion", None) or (card.get("motion") if isinstance(card, dict) else "")
        card_id = getattr(card, "card_id", None) or (card.get("card_id") if isinstance(card, dict) else f"card_{i}")
        out.append(build_booking_option(card_id, motion or "sales_prospecting", booking_index=i))
    return out
