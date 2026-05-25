"""
Runtime capability check for an identity.
"""

from __future__ import annotations

from dataclasses import dataclass

from dealix.hermes.identity.agent_identity import AgentIdentity, IdentityStatus


@dataclass
class CapabilityCheck:
    allowed: bool
    reason: str


def check_capability(identity: AgentIdentity, capability: str) -> CapabilityCheck:
    if identity.status == IdentityStatus.REVOKED:
        return CapabilityCheck(False, "identity is revoked")
    if identity.status == IdentityStatus.SUSPENDED:
        return CapabilityCheck(False, "identity is suspended")
    if capability in identity.forbidden_capabilities:
        return CapabilityCheck(
            False, f"capability '{capability}' is explicitly forbidden"
        )
    if capability not in identity.capability_scope:
        return CapabilityCheck(
            False, f"capability '{capability}' is outside the declared scope"
        )
    return CapabilityCheck(True, "ok")
