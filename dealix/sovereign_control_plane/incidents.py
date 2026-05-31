"""
Incident log — §92.

Eight incident types (agent_behavior_anomaly, tool_abuse,
mcp_server_compromise, data_exfiltration_attempt, policy_violation,
approval_bypass_attempt, partner_trust_breach, customer_data_incident).
Creating a high/critical incident force-flips the security mode to
SOVEREIGN_LOCKDOWN.
"""

from __future__ import annotations

import threading
import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any

from dealix.sovereign_control_plane.events import EventBus, make_event
from dealix.sovereign_control_plane.security_modes import SecurityModeManager
from dealix.sovereign_control_plane.types import IncidentSeverity, IncidentType


@dataclass
class Incident:
    incident_id: str
    incident_type: IncidentType
    severity: IncidentSeverity
    source: str
    summary: str
    payload: dict[str, Any]
    created_at: str
    resolved_at: str | None = None
    resolution_notes: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "incident_id": self.incident_id,
            "incident_type": self.incident_type.value,
            "severity": self.severity.value,
            "source": self.source,
            "summary": self.summary,
            "payload": dict(self.payload),
            "created_at": self.created_at,
            "resolved_at": self.resolved_at,
            "resolution_notes": self.resolution_notes,
        }


class IncidentLog:
    def __init__(
        self,
        event_bus: EventBus,
        security_modes: SecurityModeManager,
    ) -> None:
        self._items: dict[str, Incident] = {}
        self._lock = threading.Lock()
        self._bus = event_bus
        self._security = security_modes

    def create(
        self,
        incident_type: IncidentType | str,
        severity: IncidentSeverity | str,
        source: str,
        summary: str,
        payload: dict[str, Any] | None = None,
    ) -> Incident:
        if isinstance(incident_type, str):
            incident_type = IncidentType(incident_type)
        if isinstance(severity, str):
            severity = IncidentSeverity(severity)
        inc = Incident(
            incident_id=f"inc_{uuid.uuid4().hex[:12]}",
            incident_type=incident_type,
            severity=severity,
            source=source,
            summary=summary,
            payload=dict(payload or {}),
            created_at=datetime.now(UTC).isoformat(),
        )
        with self._lock:
            self._items[inc.incident_id] = inc
        self._bus.publish(make_event(
            event_type="incident.created", source="incident_log",
            payload=inc.to_dict(), sensitivity="CONFIDENTIAL",
        ))
        if severity in (IncidentSeverity.HIGH, IncidentSeverity.CRITICAL):
            self._security.force_lockdown(
                reason=f"incident {inc.incident_id} severity={severity.value}"
            )
        return inc

    def list(
        self,
        severity: IncidentSeverity | None = None,
        incident_type: IncidentType | None = None,
    ) -> list[Incident]:
        items = list(self._items.values())
        if severity is not None:
            items = [i for i in items if i.severity == severity]
        if incident_type is not None:
            items = [i for i in items if i.incident_type == incident_type]
        return items

    def get(self, incident_id: str) -> Incident | None:
        return self._items.get(incident_id)

    def resolve(self, incident_id: str, notes: str) -> Incident | None:
        with self._lock:
            inc = self._items.get(incident_id)
            if inc is None:
                return None
            inc.resolved_at = datetime.now(UTC).isoformat()
            inc.resolution_notes = notes
            return inc
