"""Incident Response — records risk incidents and triggers containment."""

from __future__ import annotations

from datetime import datetime, timezone
from threading import RLock
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from dealix.hermes.core.schemas import RiskLevel


class Incident(BaseModel):
    model_config = ConfigDict(extra="forbid", use_enum_values=True)

    id: str
    title: str
    severity: RiskLevel
    description: str = ""
    detected_by: str = "Sami"
    detected_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    contained: bool = False
    contained_at: datetime | None = None
    actions_taken: list[str] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)


class IncidentLog:
    def __init__(self) -> None:
        self._items: dict[str, Incident] = {}
        self._lock = RLock()

    def report(
        self,
        *,
        title: str,
        severity: RiskLevel | str,
        description: str = "",
        detected_by: str = "Sami",
        metadata: dict[str, Any] | None = None,
    ) -> Incident:
        from uuid import uuid4

        inc = Incident(
            id=f"inc_{uuid4().hex[:12]}",
            title=title,
            severity=RiskLevel(severity),
            description=description,
            detected_by=detected_by,
            metadata=metadata or {},
        )
        with self._lock:
            self._items[inc.id] = inc
        return inc

    def contain(self, incident_id: str, actions_taken: list[str]) -> Incident | None:
        with self._lock:
            inc = self._items.get(incident_id)
            if inc is None:
                return None
            updated = inc.model_copy(
                update={
                    "contained": True,
                    "contained_at": datetime.now(timezone.utc),
                    "actions_taken": list(actions_taken),
                }
            )
            self._items[incident_id] = updated
            return updated

    def list(self, *, open_only: bool = False) -> list[Incident]:
        with self._lock:
            items = list(self._items.values())
        if open_only:
            items = [i for i in items if not i.contained]
        return sorted(items, key=lambda i: i.detected_at, reverse=True)

    def clear(self) -> None:
        with self._lock:
            self._items.clear()


_default_log: IncidentLog | None = None


def get_incident_log() -> IncidentLog:
    global _default_log
    if _default_log is None:
        _default_log = IncidentLog()
    return _default_log
