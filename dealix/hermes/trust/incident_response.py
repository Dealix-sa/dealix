"""Incident register and response."""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class IncidentSeverity(StrEnum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"


class IncidentState(StrEnum):
    open = "open"
    triaged = "triaged"
    contained = "contained"
    resolved = "resolved"
    postmortem_done = "postmortem_done"


def _iid() -> str:
    return f"inc_{uuid.uuid4().hex[:16]}"


def _now() -> str:
    return datetime.now(UTC).isoformat()


class Incident(BaseModel):
    model_config = ConfigDict(extra="forbid")

    incident_id: str = Field(default_factory=_iid)
    title: str
    description: str = ""
    severity: IncidentSeverity = IncidentSeverity.medium
    state: IncidentState = IncidentState.open
    detected_by: str = "system"
    owner: str = "Sami"
    related_agents: list[str] = Field(default_factory=list)
    related_tools: list[str] = Field(default_factory=list)
    postmortem_uri: str | None = None
    created_at: str = Field(default_factory=_now)
    updated_at: str = Field(default_factory=_now)


@dataclass
class IncidentRegister:
    _incidents: dict[str, Incident] = field(default_factory=dict)

    def open(self, incident: Incident) -> Incident:
        self._incidents[incident.incident_id] = incident
        return incident

    def transition(self, incident_id: str, state: IncidentState) -> Incident:
        i = self._incidents[incident_id]
        updated = i.model_copy(update={"state": state, "updated_at": _now()})
        self._incidents[incident_id] = updated
        return updated

    def get(self, incident_id: str) -> Incident:
        return self._incidents[incident_id]

    def open_incidents(self) -> list[Incident]:
        return [i for i in self._incidents.values() if i.state != IncidentState.postmortem_done]

    def all(self) -> list[Incident]:
        return list(self._incidents.values())
