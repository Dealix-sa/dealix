"""
identity — agent, actor, and workspace identity for Hermes.

Identities are first-class objects: no agent may run without one, no
capability may be granted that isn't in the registry, and every identity
can be revoked at runtime.
"""

from dealix.hermes.identity.agent_identity import (
    AGENT_REGISTRY,
    AgentIdentity,
    register_agent,
)
from dealix.hermes.identity.capability_scope import (
    CAPABILITY_REGISTRY,
    Capability,
    register_capability,
)
from dealix.hermes.identity.revocation import REVOCATION_LIST, revoke
from dealix.hermes.identity.workspace_identity import (
    WORKSPACE_REGISTRY,
    WorkspaceIdentity,
    register_workspace,
)

__all__ = [
    "AGENT_REGISTRY",
    "AgentIdentity",
    "CAPABILITY_REGISTRY",
    "Capability",
    "REVOCATION_LIST",
    "WORKSPACE_REGISTRY",
    "WorkspaceIdentity",
    "register_agent",
    "register_capability",
    "register_workspace",
    "revoke",
]
