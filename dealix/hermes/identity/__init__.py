"""
Agent identity — richer than OAuth/OIDC.

Each identity carries:
- capability scope (positive whitelist)
- forbidden capabilities (explicit denylist that always wins)
- workspace scope (which logical tenant / data boundary it lives in)
- session policy (TTL, idle timeout, refresh behavior)
- revocation status (revocable at runtime)
"""

from __future__ import annotations

from dealix.hermes.identity.agent_identity import (
    AgentIdentity,
    IdentityStatus,
    build_identity,
)
from dealix.hermes.identity.capability_scope import (
    CapabilityCheck,
    check_capability,
)
from dealix.hermes.identity.revocation import (
    RevocationLedger,
    is_revoked,
    revoke,
)
from dealix.hermes.identity.session_policy import (
    SessionPolicy,
    SessionState,
    start_session,
    validate_session,
)
from dealix.hermes.identity.workspace_scope import (
    WorkspaceViolation,
    enforce_workspace,
)

__all__ = [
    "AgentIdentity",
    "IdentityStatus",
    "build_identity",
    "CapabilityCheck",
    "check_capability",
    "RevocationLedger",
    "is_revoked",
    "revoke",
    "SessionPolicy",
    "SessionState",
    "start_session",
    "validate_session",
    "WorkspaceViolation",
    "enforce_workspace",
]
