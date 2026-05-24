"""
Audit log — append-only record of every Kernel decision worth replaying.

Persistence is intentionally in-memory for v0.1; a durable backend can
replace ``_entries`` without changing the public API.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, Field


def _utcnow() -> datetime:
    return datetime.now(UTC)


class AuditEntry(BaseModel):
    actor: str
    action: str
    subject: str
    detail: dict[str, Any] = Field(default_factory=dict)
    at: datetime = Field(default_factory=_utcnow)


class AuditLog:
    def __init__(self) -> None:
        self._entries: list[AuditEntry] = []

    def record(self, entry: AuditEntry) -> None:
        self._entries.append(entry)

    def all(self) -> list[AuditEntry]:
        return list(self._entries)

    def for_subject(self, subject: str) -> list[AuditEntry]:
        return [e for e in self._entries if e.subject == subject]


_default_log = AuditLog()


def default_log() -> AuditLog:
    return _default_log
