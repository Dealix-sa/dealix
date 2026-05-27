"""SignalInbox — receives raw signals from any domain.

Signals must either be promoted to an Opportunity or explicitly archived.
The no-orphan rule (section 129) is enforced here: an inbox that contains
a NEW signal older than the cutoff fails the audit.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Iterable

from dealix.hermes.core.schemas import Signal, SignalStatus


class SignalInbox:
    def __init__(self) -> None:
        self._by_id: dict[str, Signal] = {}

    def receive(self, signal: Signal) -> Signal:
        if signal.id in self._by_id:
            raise ValueError(f"Duplicate signal id: {signal.id}")
        self._by_id[signal.id] = signal
        return signal

    def get(self, signal_id: str) -> Signal:
        return self._by_id[signal_id]

    def classify(self, signal_id: str) -> Signal:
        sig = self._by_id[signal_id]
        sig.status = SignalStatus.CLASSIFIED
        sig.touch()
        return sig

    def archive(self, signal_id: str, *, reason: str) -> Signal:
        sig = self._by_id[signal_id]
        sig.status = SignalStatus.ARCHIVED
        sig.payload.setdefault("archive_reason", reason)
        sig.touch()
        return sig

    def mark_converted(self, signal_id: str, *, opportunity_id: str) -> Signal:
        sig = self._by_id[signal_id]
        sig.status = SignalStatus.CONVERTED
        sig.payload["opportunity_id"] = opportunity_id
        sig.touch()
        return sig

    def all(self) -> list[Signal]:
        return list(self._by_id.values())

    def by_status(self, status: SignalStatus) -> list[Signal]:
        return [s for s in self._by_id.values() if s.status == status]

    def orphans(self, *, older_than: timedelta = timedelta(hours=24)) -> list[Signal]:
        """Signals stuck in NEW/CLASSIFIED beyond the cutoff."""
        threshold = datetime.now(timezone.utc) - older_than
        return [
            s
            for s in self._by_id.values()
            if s.status in {SignalStatus.NEW, SignalStatus.CLASSIFIED}
            and s.created_at < threshold
        ]

    def receive_many(self, signals: Iterable[Signal]) -> list[Signal]:
        return [self.receive(s) for s in signals]


__all__ = ["SignalInbox"]
