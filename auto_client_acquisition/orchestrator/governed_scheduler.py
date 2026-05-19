"""In-process governed-day scheduler (M2) — the self-running loop.

Before this, the governed day ran only when a human invoked the CLI or a
GitHub Actions cron fired. This module gives the deployment its own
heartbeat: a daemon thread that runs :func:`run_governed_day` once per day
at a configured KSA hour.

Safety:
  * Default OFF — enabled only by ``DEALIX_INPROCESS_SCHEDULER=1``. GitHub
    Actions cron stays the fallback so nothing double-runs unless asked.
  * The governed day only prepares / sweeps / snapshots — it never sends
    anything externally. A scheduler that triggers it is therefore safe.
  * Stoppable at any time via :func:`stop_governed_scheduler` — the
    founder kill switch (Phase 3 UI) calls exactly this.
  * No new dependency: a plain daemon thread, not APScheduler/Celery.

Saudi Arabia observes no DST, so KSA is a fixed UTC+3 offset.
"""
from __future__ import annotations

import logging
import threading
from datetime import UTC, datetime, timedelta

from auto_client_acquisition.governance_os import governance_log
from auto_client_acquisition.orchestrator.governed_day import run_governed_day

_LOG = logging.getLogger(__name__)
_KSA_OFFSET = timedelta(hours=3)
_POLL_SECONDS = 30.0  # how often the thread wakes to check the clock


def _next_run_utc(hour_ksa: int, *, now_utc: datetime | None = None) -> datetime:
    """The next UTC instant at which it is ``hour_ksa``:00 in Saudi time."""
    now = now_utc or datetime.now(UTC)
    now_ksa = now + _KSA_OFFSET
    target_ksa = now_ksa.replace(hour=hour_ksa % 24, minute=0, second=0, microsecond=0)
    if target_ksa <= now_ksa:
        target_ksa += timedelta(days=1)
    return target_ksa - _KSA_OFFSET


class GovernedScheduler:
    """A daemon thread that runs the governed day once per KSA day."""

    def __init__(self, *, hour_ksa: int = 6) -> None:
        self.hour_ksa = hour_ksa
        self._stop = threading.Event()
        self._thread: threading.Thread | None = None
        self._next_run: datetime | None = None
        self.last_run_at: str | None = None
        self.last_verdict: str | None = None

    def start(self) -> None:
        if self._thread is not None and self._thread.is_alive():
            return
        self._stop.clear()
        self._next_run = _next_run_utc(self.hour_ksa)
        self._thread = threading.Thread(
            target=self._loop, name="dealix-governed-scheduler", daemon=True
        )
        self._thread.start()
        _LOG.info("governed_scheduler_started next_run_utc=%s", self._next_run)

    def stop(self, *, timeout: float = 5.0) -> None:
        """Halt the loop — the founder kill switch. Safe to call repeatedly."""
        self._stop.set()
        thread = self._thread
        if thread is not None and thread.is_alive():
            thread.join(timeout=timeout)
        self._thread = None
        _LOG.info("governed_scheduler_stopped")

    @property
    def running(self) -> bool:
        return self._thread is not None and self._thread.is_alive()

    def status(self) -> dict[str, object]:
        return {
            "running": self.running,
            "hour_ksa": self.hour_ksa,
            "next_run_utc": self._next_run.isoformat() if self._next_run else None,
            "last_run_at": self.last_run_at,
            "last_verdict": self.last_verdict,
        }

    def _loop(self) -> None:
        while not self._stop.is_set():
            if self._stop.wait(timeout=_POLL_SECONDS):
                break
            now = datetime.now(UTC)
            if self._next_run is not None and now >= self._next_run:
                self._run_once()
                self._next_run = _next_run_utc(self.hour_ksa, now_utc=now)

    def _run_once(self) -> None:
        try:
            result = run_governed_day()
            self.last_run_at = result.finished_at
            self.last_verdict = result.verdict
        except Exception as exc:  # noqa: BLE001 — the heartbeat must never die
            _LOG.warning("governed_scheduler_run_failed:%s", type(exc).__name__)
            try:
                governance_log.record_phase(
                    phase="scheduler", status="degraded",
                    error=f"{type(exc).__name__}: {exc}",
                )
            except Exception:  # noqa: BLE001
                pass


# ─── Process singleton ───────────────────────────────────────────

_SCHEDULER: GovernedScheduler | None = None


def _scheduler_config() -> tuple[bool, int]:
    """Resolve (enabled, hour_ksa) from settings — defensively."""
    try:
        from core.config.settings import get_settings

        settings = get_settings()
        return (
            bool(getattr(settings, "inprocess_scheduler_enabled", False)),
            int(getattr(settings, "governed_day_hour_ksa", 6)),
        )
    except Exception:  # noqa: BLE001
        return False, 6


def start_governed_scheduler(*, force: bool = False) -> GovernedScheduler | None:
    """Start the scheduler if enabled by settings (or ``force=True``).

    Returns the scheduler, or ``None`` when disabled. Idempotent.
    """
    global _SCHEDULER
    enabled, hour_ksa = _scheduler_config()
    if not enabled and not force:
        return None
    if _SCHEDULER is None:
        _SCHEDULER = GovernedScheduler(hour_ksa=hour_ksa)
    _SCHEDULER.start()
    return _SCHEDULER


def stop_governed_scheduler() -> None:
    """Stop the scheduler — the founder kill switch. Safe if never started."""
    if _SCHEDULER is not None:
        _SCHEDULER.stop()


def get_governed_scheduler() -> GovernedScheduler | None:
    """The current scheduler singleton (None if never started)."""
    return _SCHEDULER


__all__ = [
    "GovernedScheduler",
    "start_governed_scheduler",
    "stop_governed_scheduler",
    "get_governed_scheduler",
]
