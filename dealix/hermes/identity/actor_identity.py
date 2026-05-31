"""
identity.actor_identity — re-export of the control_plane.actor_identity
helpers so callers can ``from dealix.hermes.identity import actor_identity``
without crossing into the runtime module.
"""

from dealix.hermes.control_plane.actor_identity import (
    SAMI,
    ActorIdentity,
    ActorKind,
    resolve,
)

__all__ = ["SAMI", "ActorIdentity", "ActorKind", "resolve"]
