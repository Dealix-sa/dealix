"""Lightweight tracing primitives."""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


def _now() -> str:
    return datetime.now(UTC).isoformat()


def _tid() -> str:
    return f"trc_{uuid.uuid4().hex[:16]}"


class TraceEvent(BaseModel):
    model_config = ConfigDict(extra="forbid")

    trace_id: str = Field(default_factory=_tid)
    span_id: str = Field(default_factory=lambda: f"spn_{uuid.uuid4().hex[:12]}")
    name: str
    actor: str
    attributes: dict[str, Any] = Field(default_factory=dict)
    started_at: str = Field(default_factory=_now)
    duration_ms: int = 0


@dataclass
class Tracer:
    _events: list[TraceEvent] = field(default_factory=list)

    def record(self, event: TraceEvent) -> TraceEvent:
        self._events.append(event)
        return event

    def all(self) -> list[TraceEvent]:
        return list(self._events)
