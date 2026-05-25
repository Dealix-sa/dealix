"""Append-only audit log."""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


def _now() -> str:
    return datetime.now(UTC).isoformat()


def _eid() -> str:
    return f"aud_{uuid.uuid4().hex[:16]}"


class AuditEntry(BaseModel):
    model_config = ConfigDict(extra="forbid")

    entry_id: str = Field(default_factory=_eid)
    actor: str
    action: str
    subject_id: str
    subject_type: str
    outcome: str  # "ok" | "blocked" | "failed"
    details: dict[str, Any] = Field(default_factory=dict)
    occurred_at: str = Field(default_factory=_now)


@dataclass
class AuditLog:
    _entries: list[AuditEntry] = field(default_factory=list)

    def write(self, entry: AuditEntry) -> AuditEntry:
        self._entries.append(entry)
        return entry

    def search(self, *, actor: str | None = None, subject_id: str | None = None) -> list[AuditEntry]:
        results = self._entries
        if actor:
            results = [e for e in results if e.actor == actor]
        if subject_id:
            results = [e for e in results if e.subject_id == subject_id]
        return list(results)

    def all(self) -> list[AuditEntry]:
        return list(self._entries)
