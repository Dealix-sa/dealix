"""Sovereign Memory — the long-term store only Sami may write to.

Agents may **read** at most a redacted subset; nobody but Sami may write.
This module enforces that via a simple author tag at the API surface.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass(frozen=True)
class MemoryEntry:
    key: str
    value: str
    author: str
    written_at: datetime
    sensitive: bool


@dataclass
class SovereignMemory:
    """In-memory implementation. Production should swap the storage layer."""

    _entries: dict[str, MemoryEntry] = field(default_factory=dict)
    sovereign_author: str = "sami"

    def write(self, key: str, value: str, *, author: str, sensitive: bool = False) -> None:
        if author != self.sovereign_author:
            raise PermissionError(
                f"Only sovereign author '{self.sovereign_author}' may write sovereign memory; got '{author}'."
            )
        self._entries[key] = MemoryEntry(
            key=key,
            value=value,
            author=author,
            written_at=datetime.now(timezone.utc),
            sensitive=sensitive,
        )

    def read(self, key: str, *, agent_id: str | None = None) -> str | None:
        entry = self._entries.get(key)
        if not entry:
            return None
        # Agents only get redacted reads of sensitive entries.
        if entry.sensitive and agent_id is not None:
            return "[REDACTED]"
        return entry.value

    def keys(self) -> list[str]:
        return sorted(self._entries.keys())


__all__ = ["MemoryEntry", "SovereignMemory"]
