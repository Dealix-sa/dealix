"""Access control evaluator — pure function for unit testability."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from dealix.hermes.identity.permissions import PermissionSet


class AccessDecision(StrEnum):
    allow = "allow"
    deny = "deny"


@dataclass(frozen=True)
class AccessRequest:
    actor_id: str
    resource: str
    action: str
    workspace_id: str | None = None


def evaluate_access(request: AccessRequest, permissions: PermissionSet) -> AccessDecision:
    if permissions.owner_id != request.actor_id:
        return AccessDecision.deny
    if permissions.grants(request.resource, request.action):
        return AccessDecision.allow
    return AccessDecision.deny
