"""
ContextPacketBuilder — never hand an agent the database; hand it a
ContextPacket.

A ContextPacket is the *only* legal way an agent receives input. It
declares purpose, allowed uses, sensitivity, the set of included
objects, and the set of explicitly excluded objects. Without a packet,
an agent run is blocked.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta
from typing import Any

from dealix.hermes.data.classification import DataClassification


@dataclass(frozen=True)
class ContextPacket:
    context_id: str
    agent_id: str
    workspace_id: str
    purpose: str
    allowed_use: tuple[str, ...]
    sensitivity: DataClassification
    expires_at: datetime
    included_objects: tuple[str, ...]
    excluded_objects: tuple[str, ...]
    payload: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "context_id": self.context_id,
            "agent_id": self.agent_id,
            "workspace_id": self.workspace_id,
            "purpose": self.purpose,
            "allowed_use": list(self.allowed_use),
            "sensitivity": self.sensitivity.value,
            "expires_at": self.expires_at.isoformat(),
            "included_objects": list(self.included_objects),
            "excluded_objects": list(self.excluded_objects),
        }

    @property
    def expired(self) -> bool:
        return datetime.now(UTC) > self.expires_at


_GLOBAL_EXCLUDES = ("sovereign_memory", "internal_strategy", "payment_secrets")


@dataclass
class ContextPacketBuilder:
    agent_id: str
    workspace_id: str
    purpose: str
    sensitivity: DataClassification = DataClassification.INTERNAL
    ttl_minutes: int = 30

    def build(
        self,
        *,
        include: tuple[str, ...],
        exclude_extra: tuple[str, ...] = (),
        allowed_use: tuple[str, ...] = ("draft_only",),
        payload: dict[str, Any] | None = None,
    ) -> ContextPacket:
        excludes = tuple(sorted(set(_GLOBAL_EXCLUDES + exclude_extra)))
        included = tuple(o for o in include if o not in excludes)
        return ContextPacket(
            context_id=f"ctx_{uuid.uuid4().hex[:8]}",
            agent_id=self.agent_id,
            workspace_id=self.workspace_id,
            purpose=self.purpose,
            allowed_use=allowed_use,
            sensitivity=self.sensitivity,
            expires_at=datetime.now(UTC) + timedelta(minutes=self.ttl_minutes),
            included_objects=included,
            excluded_objects=excludes,
            payload=dict(payload or {}),
        )
