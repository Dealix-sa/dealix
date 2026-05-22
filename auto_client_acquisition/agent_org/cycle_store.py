"""In-memory store of daily executive cycle reports.

Thread-safe, insertion-ordered. Lets the API and the console show
"today's cycle", "yesterday's cycle", etc. without re-running. Swappable
for a persistent backend later (the API surface is intentionally narrow).

مخزن دورات اليوم التنفيذية في الذاكرة — يحتفظ بآخر تشغيل لتعرضه الواجهة.
"""

from __future__ import annotations

import threading
from collections import OrderedDict

from auto_client_acquisition.agent_org.orchestrator import DailyOrgReport

# Default cap on retained cycles (oldest evicted FIFO when exceeded).
DEFAULT_MAX_CYCLES = 60


class CycleStore:
    """Insertion-ordered store of daily cycle reports."""

    def __init__(self, max_cycles: int = DEFAULT_MAX_CYCLES) -> None:
        self._lock = threading.Lock()
        self._items: "OrderedDict[str, DailyOrgReport]" = OrderedDict()
        self._max = max_cycles

    def add(self, report: DailyOrgReport) -> DailyOrgReport:
        with self._lock:
            self._items[report.cycle_id] = report
            while len(self._items) > self._max:
                self._items.popitem(last=False)
        return report

    def get(self, cycle_id: str) -> DailyOrgReport | None:
        with self._lock:
            return self._items.get(cycle_id)

    def list_recent(self, limit: int = 20) -> list[DailyOrgReport]:
        """Most recent first."""
        with self._lock:
            return list(reversed(self._items.values()))[:limit]

    def latest(self) -> DailyOrgReport | None:
        with self._lock:
            if not self._items:
                return None
            return next(reversed(self._items.values()))

    def clear(self) -> None:
        with self._lock:
            self._items.clear()

    def __len__(self) -> int:
        with self._lock:
            return len(self._items)


_default_store: CycleStore | None = None
_default_lock = threading.Lock()


def get_default_cycle_store() -> CycleStore:
    """Process-wide default store. Lazy so tests can swap it cheaply."""
    global _default_store
    with _default_lock:
        if _default_store is None:
            _default_store = CycleStore()
        return _default_store


def reset_default_cycle_store() -> None:
    """Test helper — wipe the default store."""
    get_default_cycle_store().clear()


__all__ = [
    "DEFAULT_MAX_CYCLES",
    "CycleStore",
    "get_default_cycle_store",
    "reset_default_cycle_store",
]
