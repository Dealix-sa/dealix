"""
Agent-to-agent communication gate.

Every cross-agent message passes through:

    Message Sanitizer
        → Source Trust Level
            → Capability Check
                → Delegation Policy
                    → Output Validator
                        → Audit

Hard rule: a lower-privilege agent can never delegate an externally-visible
action to a higher-privilege agent (the "second-order prompt injection" attack).
"""

from __future__ import annotations

from dealix.hermes.agent_comms.cross_agent_validator import (
    CrossAgentValidation,
    validate_cross_agent_message,
)
from dealix.hermes.agent_comms.delegation_policy import (
    DelegationDecision,
    check_delegation,
)
from dealix.hermes.agent_comms.message_sanitizer import (
    SanitizationResult,
    sanitize_message,
)
from dealix.hermes.agent_comms.provenance import (
    AgentMessage,
    build_agent_message,
)
from dealix.hermes.agent_comms.source_trust import (
    PrivilegeLevel,
    rank_privilege,
)

__all__ = [
    "SanitizationResult",
    "sanitize_message",
    "DelegationDecision",
    "check_delegation",
    "CrossAgentValidation",
    "validate_cross_agent_message",
    "AgentMessage",
    "build_agent_message",
    "PrivilegeLevel",
    "rank_privilege",
]
