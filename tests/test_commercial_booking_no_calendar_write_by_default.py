"""Booking Desk proposes meetings but never writes a calendar by default."""

from __future__ import annotations

import pytest

from app.commercial import booking_desk, safety


@pytest.fixture(autouse=True)
def _clear_flags(monkeypatch):
    for key in safety.SAFE_DEFAULT_FLAGS:
        monkeypatch.delenv(key, raising=False)
    yield


def test_booking_option_has_three_slots_and_agenda():
    opt = booking_desk.build_booking_option("c1", "sales_prospecting")
    assert len(opt.suggested_slots) == 3
    assert opt.agenda
    assert opt.preparation_notes


def test_calendar_write_disabled_by_default():
    opt = booking_desk.build_booking_option("c1")
    assert opt.calendar_write_enabled is False
    assert opt.booking_status == "proposed"


def test_can_write_calendar_denied_by_default():
    decision = safety.can_write_calendar(
        {"owner_decision": "book"}, account={"contactability_status": "contactable"}
    )
    assert decision.allowed is False
    assert any("CALENDAR_WRITE_ENABLED" in b for b in decision.blocked_by)


def test_calendar_write_needs_flag_mode_and_decision(monkeypatch):
    monkeypatch.setenv("CALENDAR_WRITE_ENABLED", "true")
    monkeypatch.setenv("OUTBOUND_MODE", "controlled_live")
    decision = safety.can_write_calendar(
        {"owner_decision": "book"}, account={"contactability_status": "contactable"}
    )
    assert decision.allowed is True
