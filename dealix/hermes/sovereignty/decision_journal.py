"""Append-only log of every sovereign decision.

Once an entry is appended it is never mutated. The journal is read by
audit, evidence packs, weekly reviews, and (eventually) the proof OS.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Iterable, Optional


@dataclass(frozen=True)
class JournalEntry:
    timestamp: datetime
    actor: str
    action: str
    level: str
    outcome: str  # approved|rejected|auto_approved|blocked
    rationale: str
    refs: tuple[str, ...] = ()


@dataclass
class DecisionJournal:
    _entries: list[JournalEntry] = field(default_factory=list)

    def append(
        self,
        *,
        actor: str,
        action: str,
        level: str,
        outcome: str,
        rationale: str,
        refs: Iterable[str] = (),
    ) -> JournalEntry:
        entry = JournalEntry(
            timestamp=datetime.now(timezone.utc),
            actor=actor,
            action=action,
            level=level,
            outcome=outcome,
            rationale=rationale,
            refs=tuple(refs),
        )
        self._entries.append(entry)
        return entry

    def all(self) -> list[JournalEntry]:
        return list(self._entries)

    def latest(self, n: int = 50) -> list[JournalEntry]:
        return list(self._entries[-n:])

    def by_action(self, action: str) -> list[JournalEntry]:
        return [e for e in self._entries if e.action == action]

    def find(self, ref: str) -> Optional[JournalEntry]:
        for e in self._entries:
            if ref in e.refs:
                return e
        return None


__all__ = ["DecisionJournal", "JournalEntry"]
