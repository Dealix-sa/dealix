"""
Suppression list.

Authoritative store of contacts the system must never message. Addition
is auto-approved; removal requires founder approval (enforced by the
approval matrix).
"""
from __future__ import annotations

from dataclasses import dataclass, field


def _normalize(value: str) -> str:
    return value.strip().lower()


@dataclass(slots=True)
class SuppressionList:
    entries: set[str] = field(default_factory=set)

    def add(self, contact: str) -> bool:
        contact = _normalize(contact)
        if not contact:
            return False
        before = len(self.entries)
        self.entries.add(contact)
        return len(self.entries) > before

    def remove(self, contact: str) -> bool:
        """Removal returns True iff entry existed; caller MUST verify founder approval."""
        contact = _normalize(contact)
        if contact in self.entries:
            self.entries.discard(contact)
            return True
        return False

    def contains(self, contact: str) -> bool:
        return _normalize(contact) in self.entries

    def filter(self, contacts: list[str]) -> list[str]:
        """Return contacts that are *not* suppressed (safe to message)."""
        return [c for c in contacts if not self.contains(c)]
