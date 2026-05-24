"""خادم الثقة — incident response.

Four severities (SEV1..SEV4). SEV1 incidents automatically pause every
implicated agent on declaration. State machine:

    OPEN → MITIGATING → RESOLVED → POSTMORTEM
"""

from __future__ import annotations

from datetime import datetime
from enum import StrEnum
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field, model_validator

from dealix.hermes.core.schemas import utcnow
from dealix.trust.agent_registry import AgentRegistry
from dealix.trust.tool_registry import ToolRegistry


class IncidentSeverity(StrEnum):
    SEV1 = "sev1"
    SEV2 = "sev2"
    SEV3 = "sev3"
    SEV4 = "sev4"

    @property
    def numeric(self) -> int:
        return {"sev1": 1, "sev2": 2, "sev3": 3, "sev4": 4}[self.value]

    @property
    def auto_pause(self) -> bool:
        """SEV1 and SEV2 automatically pause implicated agents."""
        return self in {IncidentSeverity.SEV1, IncidentSeverity.SEV2}


class IncidentStatus(StrEnum):
    OPEN = "open"
    MITIGATING = "mitigating"
    RESOLVED = "resolved"
    POSTMORTEM = "postmortem"


_VALID_TRANSITIONS: dict[IncidentStatus, set[IncidentStatus]] = {
    IncidentStatus.OPEN: {IncidentStatus.MITIGATING, IncidentStatus.RESOLVED},
    IncidentStatus.MITIGATING: {IncidentStatus.RESOLVED},
    IncidentStatus.RESOLVED: {IncidentStatus.POSTMORTEM},
    IncidentStatus.POSTMORTEM: set(),
}


def _new_incident_id() -> str:
    return f"inc_{uuid4().hex}"


class Incident(BaseModel):
    """A single incident record."""

    model_config = ConfigDict(extra="forbid")

    incident_id: str = Field(default_factory=_new_incident_id)
    severity: IncidentSeverity
    summary: str = Field(..., min_length=1, max_length=600)
    detected_at: datetime = Field(default_factory=utcnow)
    owner: str = Field(..., min_length=1, max_length=128)
    status: IncidentStatus = IncidentStatus.OPEN
    agents_paused: list[str] = Field(default_factory=list, max_length=64)
    tools_blocked: list[str] = Field(default_factory=list, max_length=64)
    evidence_refs: list[str] = Field(default_factory=list, max_length=32)
    postmortem_ref: str | None = None
    resolved_at: datetime | None = None
    notes: list[str] = Field(default_factory=list, max_length=64)

    @model_validator(mode="after")
    def _resolved_requires_time(self) -> Incident:
        if self.status in {IncidentStatus.RESOLVED, IncidentStatus.POSTMORTEM}:
            if self.resolved_at is None:
                # Allow create-and-immediately-resolve by stamping now.
                self.resolved_at = utcnow()
        return self


# ─────────────────────────────────────────────────────────────
# Response orchestrator
# ─────────────────────────────────────────────────────────────


class IncidentResponse:
    """Track incidents and enforce auto-pause for SEV1/SEV2."""

    def __init__(
        self,
        agent_registry: AgentRegistry | None = None,
        tool_registry: ToolRegistry | None = None,
    ) -> None:
        self._incidents: dict[str, Incident] = {}
        self._agents = agent_registry
        self._tools = tool_registry

    def declare(
        self,
        severity: IncidentSeverity | str,
        summary: str,
        owner: str = "sami",
        implicated_agents: list[str] | None = None,
        implicated_tools: list[str] | None = None,
        evidence_refs: list[str] | None = None,
    ) -> Incident:
        sev = IncidentSeverity(severity) if isinstance(severity, str) else severity
        agents = list(implicated_agents or [])
        tools = list(implicated_tools or [])
        incident = Incident(
            severity=sev,
            summary=summary,
            owner=owner,
            agents_paused=[],
            tools_blocked=[],
            evidence_refs=list(evidence_refs or []),
        )

        if sev.auto_pause and self._agents is not None:
            for agent_id in agents:
                try:
                    self._agents.pause(agent_id, f"incident:{incident.incident_id}")
                    incident.agents_paused.append(agent_id)
                except KeyError:
                    incident.notes.append(f"agent not registered: {agent_id}")

        if sev == IncidentSeverity.SEV1 and self._tools is not None:
            for tool_id in tools:
                try:
                    self._tools.block(tool_id, f"incident:{incident.incident_id}")
                    incident.tools_blocked.append(tool_id)
                except KeyError:
                    incident.notes.append(f"tool not registered: {tool_id}")

        self._incidents[incident.incident_id] = incident
        return incident

    def get(self, incident_id: str) -> Incident:
        try:
            return self._incidents[incident_id]
        except KeyError as exc:
            raise KeyError(f"unknown incident: {incident_id}") from exc

    def all(self) -> list[Incident]:
        return list(self._incidents.values())

    def open(self) -> list[Incident]:
        return [i for i in self._incidents.values() if i.status != IncidentStatus.POSTMORTEM]

    def mitigate(self, incident_id: str, action: str) -> Incident:
        incident = self.get(incident_id)
        if IncidentStatus.MITIGATING not in _VALID_TRANSITIONS[incident.status]:
            raise ValueError(
                f"cannot transition {incident.status.value} → mitigating"
            )
        incident.status = IncidentStatus.MITIGATING
        incident.notes.append(action)
        return incident

    def resolve(self, incident_id: str, postmortem_ref: str | None = None) -> Incident:
        incident = self.get(incident_id)
        if IncidentStatus.RESOLVED not in _VALID_TRANSITIONS[incident.status]:
            raise ValueError(
                f"cannot transition {incident.status.value} → resolved"
            )
        incident.status = IncidentStatus.RESOLVED
        incident.resolved_at = utcnow()
        if postmortem_ref:
            incident.postmortem_ref = postmortem_ref
            incident.status = IncidentStatus.POSTMORTEM
        return incident

    def close_with_postmortem(self, incident_id: str, postmortem_ref: str) -> Incident:
        incident = self.get(incident_id)
        if incident.status != IncidentStatus.RESOLVED:
            raise ValueError(
                f"cannot file postmortem from status {incident.status.value}"
            )
        incident.status = IncidentStatus.POSTMORTEM
        incident.postmortem_ref = postmortem_ref
        return incident

    def to_dict(self) -> dict[str, Any]:
        return {
            "count": len(self._incidents),
            "open": len(self.open()),
            "incidents": [i.model_dump(mode="json") for i in self._incidents.values()],
        }


__all__ = [
    "Incident",
    "IncidentResponse",
    "IncidentSeverity",
    "IncidentStatus",
]
