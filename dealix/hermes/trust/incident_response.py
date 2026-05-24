"""Incident Register.

Captures incidents detected by guardrails, audit, or operators. Every
incident moves through OPEN → INVESTIGATING → MITIGATED → CLOSED.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any


class IncidentSeverity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class IncidentStatus(str, Enum):
    OPEN = "open"
    INVESTIGATING = "investigating"
    MITIGATED = "mitigated"
    CLOSED = "closed"


@dataclass
class Incident:
    id: str
    title: str
    detail: str
    severity: IncidentSeverity
    status: IncidentStatus = IncidentStatus.OPEN
    opened_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    closed_at: datetime | None = None
    mitigation: str = ""
    refs: list[str] = field(default_factory=list)
    payload: dict[str, Any] = field(default_factory=dict)


@dataclass
class IncidentRegister:
    _by_id: dict[str, Incident] = field(default_factory=dict)

    def open(
        self,
        *,
        title: str,
        detail: str,
        severity: IncidentSeverity,
        refs: list[str] | None = None,
    ) -> Incident:
        inc = Incident(
            id=f"inc_{uuid.uuid4().hex[:10]}",
            title=title,
            detail=detail,
            severity=severity,
            refs=list(refs or []),
        )
        self._by_id[inc.id] = inc
        return inc

    def investigate(self, incident_id: str) -> Incident:
        inc = self._by_id[incident_id]
        if inc.status != IncidentStatus.OPEN:
            raise ValueError(f"Incident {incident_id} is not OPEN.")
        inc.status = IncidentStatus.INVESTIGATING
        return inc

    def mitigate(self, incident_id: str, *, mitigation: str) -> Incident:
        inc = self._by_id[incident_id]
        inc.status = IncidentStatus.MITIGATED
        inc.mitigation = mitigation
        return inc

    def close(self, incident_id: str) -> Incident:
        inc = self._by_id[incident_id]
        inc.status = IncidentStatus.CLOSED
        inc.closed_at = datetime.now(timezone.utc)
        return inc

    def open_incidents(self) -> list[Incident]:
        return [
            i for i in self._by_id.values()
            if i.status in {IncidentStatus.OPEN, IncidentStatus.INVESTIGATING}
        ]

    def all(self) -> list[Incident]:
        return list(self._by_id.values())


__all__ = ["Incident", "IncidentRegister", "IncidentSeverity", "IncidentStatus"]
