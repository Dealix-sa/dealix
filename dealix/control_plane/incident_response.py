"""
Section 65 — Incident Response.

Eight incident types, each with detect → block → log → notify → evidence
→ remediate → policy update → asset/learning. The IncidentLog turns each
event into structured `Incident` objects so the control plane can audit
and reuse them.
"""

from __future__ import annotations

import uuid
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from typing import Any


class IncidentType(StrEnum):
    PROMPT_INJECTION = "prompt_injection_detected"
    TOOL_POLICY_VIOLATION = "tool_policy_violation"
    SENSITIVE_DATA_ATTEMPT = "sensitive_data_attempt"
    UNAPPROVED_EXTERNAL_ACTION = "unapproved_external_action"
    OVERCLAIM = "overclaim_detected"
    MCP_DESCRIPTOR_CHANGED = "mcp_descriptor_changed"
    AGENT_BEHAVIOR_ANOMALY = "agent_behavior_anomaly"
    CUSTOMER_DATA_BOUNDARY_VIOLATION = "customer_data_boundary_violation"


class IncidentSeverity(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class Incident:
    incident_id: str
    type: IncidentType
    severity: IncidentSeverity
    agent_id: str | None
    action_id: str | None
    blocked: bool
    recommended_fix: str
    evidence_pack_id: str | None = None
    policy_update: str | None = None
    asset_learning: str | None = None
    notified: bool = False
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    resolved_at: datetime | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "incident_id": self.incident_id,
            "type": self.type.value,
            "severity": self.severity.value,
            "agent_id": self.agent_id,
            "action_id": self.action_id,
            "blocked": self.blocked,
            "recommended_fix": self.recommended_fix,
            "evidence_pack_id": self.evidence_pack_id,
            "policy_update": self.policy_update,
            "asset_learning": self.asset_learning,
            "notified": self.notified,
            "created_at": self.created_at.isoformat(),
            "resolved_at": self.resolved_at.isoformat() if self.resolved_at else None,
        }


IncidentSubscriber = Callable[[Incident], None]


class IncidentLog:
    def __init__(self) -> None:
        self._incidents: dict[str, Incident] = {}
        self._subscribers: list[IncidentSubscriber] = []

    def subscribe(self, subscriber: IncidentSubscriber) -> None:
        self._subscribers.append(subscriber)

    def report(
        self,
        *,
        type: IncidentType,
        severity: IncidentSeverity = IncidentSeverity.MEDIUM,
        agent_id: str | None = None,
        action_id: str | None = None,
        recommended_fix: str,
        blocked: bool = True,
        evidence_pack_id: str | None = None,
    ) -> Incident:
        incident = Incident(
            incident_id=f"inc_{uuid.uuid4().hex[:12]}",
            type=type,
            severity=severity,
            agent_id=agent_id,
            action_id=action_id,
            blocked=blocked,
            recommended_fix=recommended_fix,
            evidence_pack_id=evidence_pack_id,
        )
        self._incidents[incident.incident_id] = incident
        for sub in self._subscribers:
            sub(incident)
        incident.notified = True
        return incident

    def attach_policy_update(self, incident_id: str, *, policy_update: str) -> Incident:
        incident = self.get(incident_id)
        incident.policy_update = policy_update
        return incident

    def attach_asset_learning(self, incident_id: str, *, asset_learning: str) -> Incident:
        incident = self.get(incident_id)
        incident.asset_learning = asset_learning
        return incident

    def resolve(self, incident_id: str) -> Incident:
        incident = self.get(incident_id)
        incident.resolved_at = datetime.now(UTC)
        return incident

    def get(self, incident_id: str) -> Incident:
        try:
            return self._incidents[incident_id]
        except KeyError as exc:
            raise KeyError(f"unknown incident: {incident_id}") from exc

    def open(self) -> list[Incident]:
        return [i for i in self._incidents.values() if i.resolved_at is None]

    def all(self) -> list[Incident]:
        return list(self._incidents.values())
