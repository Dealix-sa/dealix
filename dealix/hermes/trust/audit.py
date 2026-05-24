"""Append-only audit log for Hermes events.

The audit log records every gate decision, approval transition, and outcome
write. It never modifies past entries. A SHA-256 hash chain over `prev_hash
+ payload` lets us detect tampering even before the durable backend
lands.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any
from uuid import uuid4


@dataclass(slots=True)
class AuditEntry:
    entry_id: str
    event_type: str
    actor: str
    payload: dict[str, Any]
    prev_hash: str
    entry_hash: str
    recorded_at: datetime


class AuditLog:
    def __init__(self) -> None:
        self._entries: list[AuditEntry] = []

    def append(self, *, event_type: str, actor: str, payload: dict[str, Any]) -> AuditEntry:
        prev_hash = self._entries[-1].entry_hash if self._entries else "0" * 64
        recorded_at = datetime.now(UTC)
        body = {
            "event_type": event_type,
            "actor": actor,
            "payload": payload,
            "prev_hash": prev_hash,
            "recorded_at": recorded_at.isoformat(),
        }
        entry_hash = hashlib.sha256(
            json.dumps(body, sort_keys=True, default=str).encode("utf-8")
        ).hexdigest()
        entry = AuditEntry(
            entry_id=str(uuid4()),
            event_type=event_type,
            actor=actor,
            payload=payload,
            prev_hash=prev_hash,
            entry_hash=entry_hash,
            recorded_at=recorded_at,
        )
        self._entries.append(entry)
        return entry

    def verify_chain(self) -> bool:
        prev = "0" * 64
        for e in self._entries:
            if e.prev_hash != prev:
                return False
            body = {
                "event_type": e.event_type,
                "actor": e.actor,
                "payload": e.payload,
                "prev_hash": e.prev_hash,
                "recorded_at": e.recorded_at.isoformat(),
            }
            recomputed = hashlib.sha256(
                json.dumps(body, sort_keys=True, default=str).encode("utf-8")
            ).hexdigest()
            if recomputed != e.entry_hash:
                return False
            prev = e.entry_hash
        return True

    def all(self) -> list[AuditEntry]:
        return list(self._entries)

    def __len__(self) -> int:
        return len(self._entries)


__all__ = ["AuditEntry", "AuditLog"]
