"""
AgentIdentity — the canonical machine-readable identity for an agent.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum


class IdentityStatus(StrEnum):
    DRAFT_ONLY = "draft_only"
    ACTIVE = "active"
    REVOKED = "revoked"
    SUSPENDED = "suspended"


@dataclass
class AgentIdentity:
    agent_id: str
    owner: str
    origin: str
    capability_scope: tuple[str, ...]
    forbidden_capabilities: tuple[str, ...]
    workspace_scope: tuple[str, ...]
    revocable: bool = True
    status: IdentityStatus = IdentityStatus.DRAFT_ONLY
    posture_attestations: tuple[str, ...] = field(default_factory=tuple)

    def to_dict(self) -> dict[str, object]:
        return {
            "agent_id": self.agent_id,
            "owner": self.owner,
            "origin": self.origin,
            "capability_scope": list(self.capability_scope),
            "forbidden_capabilities": list(self.forbidden_capabilities),
            "workspace_scope": list(self.workspace_scope),
            "revocable": self.revocable,
            "status": self.status.value,
            "posture_attestations": list(self.posture_attestations),
        }


def build_identity(
    agent_id: str,
    owner: str,
    capability_scope: list[str] | tuple[str, ...],
    *,
    origin: str = "dealix_internal",
    forbidden_capabilities: list[str] | tuple[str, ...] = (),
    workspace_scope: list[str] | tuple[str, ...] = ("dealix_internal",),
    revocable: bool = True,
    posture_attestations: list[str] | tuple[str, ...] = (),
) -> AgentIdentity:
    if not agent_id:
        raise ValueError("agent_id required")
    if not owner:
        raise ValueError("owner required")
    if not capability_scope:
        raise ValueError("capability_scope must contain at least one capability")
    overlap = set(capability_scope) & set(forbidden_capabilities)
    if overlap:
        raise ValueError(
            f"capability_scope overlaps forbidden_capabilities: {sorted(overlap)}"
        )
    return AgentIdentity(
        agent_id=agent_id,
        owner=owner,
        origin=origin,
        capability_scope=tuple(capability_scope),
        forbidden_capabilities=tuple(forbidden_capabilities),
        workspace_scope=tuple(workspace_scope),
        revocable=revocable,
        status=IdentityStatus.DRAFT_ONLY,
        posture_attestations=tuple(posture_attestations),
    )
