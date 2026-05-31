"""
ActorIdentity — resolves *who* (or *what*) is making a request.

Actors are the only things that can hold capabilities. There are five
actor kinds:

    sami     — the founder. Sovereign over S2+ actions.
    agent    — a registered software agent (see hermes.identity.agent_identity).
    customer — a paying user on a customer workspace.
    partner  — a referral / white-label / strategic partner.
    system   — internal scheduled jobs and platform services.

Anything that is not one of these is rejected at the boundary.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class ActorKind(StrEnum):
    SAMI = "sami"
    AGENT = "agent"
    CUSTOMER = "customer"
    PARTNER = "partner"
    SYSTEM = "system"


@dataclass(frozen=True)
class ActorIdentity:
    actor_id: str
    kind: ActorKind
    display_name: str
    workspace_scope: tuple[str, ...]
    is_sovereign: bool = False

    def can_access_workspace(self, workspace_id: str) -> bool:
        return workspace_id in self.workspace_scope or "*" in self.workspace_scope


SAMI = ActorIdentity(
    actor_id="sami",
    kind=ActorKind.SAMI,
    display_name="Sami (Founder)",
    workspace_scope=("*",),
    is_sovereign=True,
)


def resolve(actor_id: str, kind: str | ActorKind) -> ActorIdentity:
    """Resolve an actor id and kind into an ActorIdentity.

    Real implementations look this up from an identity store. The default
    here returns a minimal identity scoped to a single workspace named
    after the actor kind.
    """
    kind_enum = ActorKind(kind) if isinstance(kind, str) else kind
    if kind_enum == ActorKind.SAMI:
        return SAMI
    scope = ("dealix_internal",) if kind_enum in (ActorKind.AGENT, ActorKind.SYSTEM) else (actor_id,)
    return ActorIdentity(
        actor_id=actor_id,
        kind=kind_enum,
        display_name=actor_id,
        workspace_scope=scope,
        is_sovereign=False,
    )
