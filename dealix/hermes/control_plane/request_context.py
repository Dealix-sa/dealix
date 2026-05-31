"""
RequestContext — the immutable envelope describing a single control-plane call.

Built by ``ControlPlaneRuntime`` at the boundary. Every downstream gate
reads from this object; gates never mutate it. To attach decisions, use
``ControlPlaneDecision`` instead.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any

from dealix.classifications import SensitivityClass


@dataclass(frozen=True)
class RequestContext:
    request_id: str
    actor_id: str
    actor_type: str  # "sami" | "agent" | "customer" | "partner" | "system"
    workspace_id: str
    capability: str
    tool_id: str | None
    purpose: str
    sensitivity: SensitivityClass
    external_action: bool
    payload_summary: str
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    metadata: dict[str, Any] = field(default_factory=dict)

    @staticmethod
    def new(
        *,
        actor_id: str,
        actor_type: str,
        workspace_id: str,
        capability: str,
        purpose: str,
        sensitivity: SensitivityClass = SensitivityClass.S1,
        tool_id: str | None = None,
        external_action: bool = False,
        payload_summary: str = "",
        metadata: dict[str, Any] | None = None,
    ) -> RequestContext:
        return RequestContext(
            request_id=f"req_{uuid.uuid4().hex[:12]}",
            actor_id=actor_id,
            actor_type=actor_type,
            workspace_id=workspace_id,
            capability=capability,
            tool_id=tool_id,
            purpose=purpose,
            sensitivity=sensitivity,
            external_action=external_action,
            payload_summary=payload_summary,
            metadata=dict(metadata or {}),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "request_id": self.request_id,
            "actor_id": self.actor_id,
            "actor_type": self.actor_type,
            "workspace_id": self.workspace_id,
            "capability": self.capability,
            "tool_id": self.tool_id,
            "purpose": self.purpose,
            "sensitivity": self.sensitivity.value,
            "external_action": self.external_action,
            "payload_summary": self.payload_summary,
            "created_at": self.created_at.isoformat(),
            "metadata": self.metadata,
        }
