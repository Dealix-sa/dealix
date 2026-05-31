"""
Context Packets — the only data an agent ever sees.

Doctrine: an agent never reads the database directly. The gateway
hydrates a scoped, time-boxed Context Packet that names purpose,
sensitivity, and allowed uses.
"""

from __future__ import annotations

import uuid
from datetime import UTC, datetime, timedelta
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from dealix.hermes.data.classification import DataClass


def _now() -> str:
    return datetime.now(UTC).isoformat()


def _cid() -> str:
    return f"ctx_{uuid.uuid4().hex[:16]}"


class ContextPacket(BaseModel):
    model_config = ConfigDict(extra="forbid")

    context_id: str = Field(default_factory=_cid)
    agent_id: str
    purpose: str
    sensitivity: DataClass
    allowed_use: list[str]
    data: dict[str, Any] = Field(default_factory=dict)
    workspace_id: str = "dealix_internal"
    issued_at: str = Field(default_factory=_now)
    expires_at: str


def build_context_packet(
    *,
    agent_id: str,
    purpose: str,
    sensitivity: DataClass,
    allowed_use: list[str],
    data: dict[str, Any],
    workspace_id: str = "dealix_internal",
    ttl_seconds: int = 3600,
) -> ContextPacket:
    expires = (datetime.now(UTC) + timedelta(seconds=ttl_seconds)).isoformat()
    return ContextPacket(
        agent_id=agent_id,
        purpose=purpose,
        sensitivity=sensitivity,
        allowed_use=allowed_use,
        data=data,
        workspace_id=workspace_id,
        expires_at=expires,
    )
