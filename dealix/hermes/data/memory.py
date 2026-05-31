"""Agent-scoped memory — durable but quarantined per agent + workspace."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime


@dataclass
class AgentMemory:
    agent_id: str
    workspace_id: str = "dealix_internal"
    _entries: dict[str, str] = field(default_factory=dict)
    _written_at: dict[str, str] = field(default_factory=dict)

    def write(self, key: str, value: str) -> None:
        self._entries[key] = value
        self._written_at[key] = datetime.now(UTC).isoformat()

    def read(self, key: str) -> str | None:
        return self._entries.get(key)

    def all(self) -> dict[str, str]:
        return dict(self._entries)

    def forget(self, key: str) -> None:
        self._entries.pop(key, None)
        self._written_at.pop(key, None)
