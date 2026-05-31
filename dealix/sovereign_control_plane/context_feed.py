"""
Context Feed — §85.

Minted context packets are the only way data reaches an agent. Every
packet carries a sensitivity, an allowed-use list, and a TTL.

SOVEREIGN packets only flow to agents on the explicit allowlist; all
other agents are refused even if asked.
"""

from __future__ import annotations

import threading
import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta
from typing import Any

from dealix.sovereign_control_plane.types import DataSensitivity


_SOVEREIGN_AGENTS: set[str] = {"hermes", "sami_assistant", "sovereign_auditor"}


@dataclass
class ContextPacket:
    context_id: str
    agent_id: str
    workspace_id: str
    purpose: str
    sensitivity: DataSensitivity
    allowed_use: list[str]
    expires_at: str
    data: dict[str, Any] = field(default_factory=dict)
    revoked: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "context_id": self.context_id,
            "agent_id": self.agent_id,
            "workspace_id": self.workspace_id,
            "purpose": self.purpose,
            "sensitivity": self.sensitivity.value,
            "allowed_use": list(self.allowed_use),
            "expires_at": self.expires_at,
            "data": dict(self.data),
            "revoked": self.revoked,
        }


class ContextFeedEngine:
    def __init__(self) -> None:
        self._packets: dict[str, ContextPacket] = {}
        self._lock = threading.Lock()

    def mint(
        self,
        agent_id: str,
        workspace_id: str,
        purpose: str,
        sensitivity: DataSensitivity,
        allowed_use: list[str],
        data: dict[str, Any],
        ttl_seconds: int = 900,
    ) -> ContextPacket:
        if sensitivity == DataSensitivity.SOVEREIGN and agent_id not in _SOVEREIGN_AGENTS:
            raise PermissionError(
                f"agent '{agent_id}' is not in the sovereign allowlist"
            )
        expires = datetime.now(UTC) + timedelta(seconds=ttl_seconds)
        pkt = ContextPacket(
            context_id=f"ctx_{uuid.uuid4().hex[:12]}",
            agent_id=agent_id,
            workspace_id=workspace_id,
            purpose=purpose,
            sensitivity=sensitivity,
            allowed_use=list(allowed_use),
            expires_at=expires.isoformat(),
            data=dict(data),
        )
        with self._lock:
            self._packets[pkt.context_id] = pkt
        return pkt

    def revoke(self, context_id: str) -> bool:
        with self._lock:
            pkt = self._packets.get(context_id)
            if pkt is None:
                return False
            pkt.revoked = True
            return True

    def is_active(self, context_id: str) -> bool:
        pkt = self._packets.get(context_id)
        if pkt is None or pkt.revoked:
            return False
        try:
            exp = datetime.fromisoformat(pkt.expires_at)
        except ValueError:
            return False
        return datetime.now(UTC) < exp

    def get(self, context_id: str) -> ContextPacket | None:
        return self._packets.get(context_id)
