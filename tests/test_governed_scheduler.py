"""Tests for the in-process governed-day scheduler (M2)."""
from __future__ import annotations

from datetime import UTC, datetime

from auto_client_acquisition.orchestrator.governed_scheduler import (
    GovernedScheduler,
    _next_run_utc,
    get_governed_scheduler,
    start_governed_scheduler,
    stop_governed_scheduler,
)


def test_next_run_is_in_the_future() -> None:
    now = datetime(2026, 5, 19, 12, 0, tzinfo=UTC)  # 15:00 KSA
    nxt = _next_run_utc(6, now_utc=now)  # 06:00 KSA target
    assert nxt > now
    # 06:00 KSA == 03:00 UTC, and 03:00 UTC tomorrow since 15:00 KSA passed it
    assert nxt.hour == 3


def test_next_run_later_today_when_hour_not_yet_passed() -> None:
    now = datetime(2026, 5, 19, 0, 0, tzinfo=UTC)  # 03:00 KSA
    nxt = _next_run_utc(6, now_utc=now)  # 06:00 KSA later today
    assert (nxt - now).total_seconds() == 3 * 3600  # 3 hours away


def test_run_once_executes_the_governed_day() -> None:
    scheduler = GovernedScheduler(hour_ksa=6)
    scheduler._run_once()
    assert scheduler.last_verdict in ("ok", "degraded", "blocked")
    assert scheduler.last_run_at  # timestamp recorded


def test_start_and_stop_lifecycle() -> None:
    scheduler = GovernedScheduler(hour_ksa=6)
    assert not scheduler.running
    scheduler.start()
    assert scheduler.running
    scheduler.stop()
    assert not scheduler.running


def test_disabled_by_default_returns_none() -> None:
    stop_governed_scheduler()
    # settings default: inprocess_scheduler_enabled = False
    assert start_governed_scheduler() is None


def test_force_start_overrides_disabled_setting() -> None:
    try:
        scheduler = start_governed_scheduler(force=True)
        assert scheduler is not None
        assert scheduler.running
        assert get_governed_scheduler() is scheduler
    finally:
        stop_governed_scheduler()


def test_status_shape() -> None:
    scheduler = GovernedScheduler(hour_ksa=8)
    status = scheduler.status()
    assert status["running"] is False
    assert status["hour_ksa"] == 8
