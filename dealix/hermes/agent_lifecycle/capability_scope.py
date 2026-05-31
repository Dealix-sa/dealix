"""
Capability scope validation.

Every agent declares a positive `capability_scope` (whitelist) and a
`forbidden_capabilities` list (explicit denylist). At runtime, a requested
capability is allowed iff it is in the scope AND not forbidden.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class CapabilityScope:
    allowed: frozenset[str]
    forbidden: frozenset[str]

    @classmethod
    def from_lists(
        cls,
        allowed: list[str] | tuple[str, ...],
        forbidden: list[str] | tuple[str, ...] = (),
    ) -> CapabilityScope:
        return cls(allowed=frozenset(allowed), forbidden=frozenset(forbidden))


@dataclass
class ScopeViolation:
    capability: str
    reason: str


def validate_scope(
    scope: CapabilityScope, requested_capability: str
) -> ScopeViolation | None:
    if requested_capability in scope.forbidden:
        return ScopeViolation(
            capability=requested_capability,
            reason="capability is explicitly forbidden for this agent",
        )
    if requested_capability not in scope.allowed:
        return ScopeViolation(
            capability=requested_capability,
            reason="capability is not in the agent's declared capability_scope",
        )
    return None
