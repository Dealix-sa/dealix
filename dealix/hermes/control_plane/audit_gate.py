"""
Audit Gate — كل stage يكتب AuditEvent. لا يُتجاوز.

التخزين خلف واجهة `AuditSink` حتى نقدر نوصّل Postgres لاحقًا دون لمس الـ
runtime. الافتراض في الذاكرة (in-process) لاختبارات سريعة وبدء التشغيل.
"""

from __future__ import annotations

import threading
import uuid
from collections.abc import Iterable
from datetime import datetime, timezone
from typing import Any, Protocol

from ..contracts import AuditEvent


class AuditSink(Protocol):
    def write(self, event: AuditEvent) -> None: ...

    def query(
        self,
        *,
        request_id: str | None = None,
        stage: str | None = None,
        limit: int = 100,
    ) -> list[AuditEvent]: ...


class InMemoryAuditSink:
    def __init__(self) -> None:
        self._events: list[AuditEvent] = []
        self._lock = threading.Lock()

    def write(self, event: AuditEvent) -> None:
        with self._lock:
            self._events.append(event)

    def query(
        self,
        *,
        request_id: str | None = None,
        stage: str | None = None,
        limit: int = 100,
    ) -> list[AuditEvent]:
        with self._lock:
            events: Iterable[AuditEvent] = self._events
            if request_id is not None:
                events = (e for e in events if e.request_id == request_id)
            if stage is not None:
                events = (e for e in events if e.stage == stage)
            return list(events)[-limit:]


class AuditGate:
    def __init__(self, sink: AuditSink | None = None) -> None:
        self._sink: AuditSink = sink or InMemoryAuditSink()

    def record(
        self,
        *,
        request_id: str,
        stage: str,
        outcome: str,
        actor_id: str | None,
        payload_summary: dict[str, Any] | None = None,
    ) -> AuditEvent:
        event = AuditEvent(
            event_id=f"evt_{uuid.uuid4().hex[:16]}",
            request_id=request_id,
            stage=stage,
            actor_id=actor_id,
            outcome=outcome,  # type: ignore[arg-type]
            payload_summary=payload_summary or {},
            created_at=datetime.now(timezone.utc),
        )
        self._sink.write(event)
        return event

    def trace(self, request_id: str) -> list[AuditEvent]:
        return self._sink.query(request_id=request_id, limit=1000)


__all__ = ["AuditGate", "AuditSink", "InMemoryAuditSink"]
