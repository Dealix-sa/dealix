"""
Incident response.

Standardizes incident records and the post-mortem template. The full
playbook lives at `docs/trust/INCIDENT_RESPONSE.md`.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone

_SEVERITY_SLA_MINUTES = {"P0": 60, "P1": 24 * 60, "P2": 72 * 60, "P3": 7 * 24 * 60}


@dataclass(slots=True)
class Incident:
    id: str
    title: str
    severity: str   # P0..P3
    opened_at: datetime
    closed_at: datetime | None = None
    summary: str = ""
    lessons: list[str] = field(default_factory=list)

    @property
    def sla_minutes(self) -> int:
        return _SEVERITY_SLA_MINUTES.get(self.severity, 7 * 24 * 60)

    def close(self, summary: str, lessons: list[str] | None = None) -> None:
        self.closed_at = datetime.now(timezone.utc)
        self.summary = summary
        if lessons:
            self.lessons.extend(lessons)


def new_incident(incident_id: str, title: str, severity: str = "P2") -> Incident:
    severity = severity if severity in _SEVERITY_SLA_MINUTES else "P2"
    return Incident(
        id=incident_id,
        title=title,
        severity=severity,
        opened_at=datetime.now(timezone.utc),
    )
