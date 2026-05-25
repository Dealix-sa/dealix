"""
End-to-end cross-agent validator — sanitize + delegation + provenance.
"""

from __future__ import annotations

from dataclasses import dataclass

from dealix.hermes.agent_comms.delegation_policy import (
    DelegationDecision,
    check_delegation,
)
from dealix.hermes.agent_comms.message_sanitizer import (
    SanitizationResult,
    sanitize_message,
)
from dealix.hermes.agent_comms.provenance import AgentMessage
from dealix.hermes.identity.agent_identity import AgentIdentity
from dealix.hermes.provenance.trust_level import TrustLevel


@dataclass
class CrossAgentValidation:
    allowed: bool
    sanitization: SanitizationResult
    delegation: DelegationDecision
    reasons: list[str]


def validate_cross_agent_message(
    message: AgentMessage,
    sender_identity: AgentIdentity,
    receiver_identity: AgentIdentity,
) -> CrossAgentValidation:
    if message.sender_agent_id != sender_identity.agent_id:
        return CrossAgentValidation(
            allowed=False,
            sanitization=SanitizationResult(False, "", ["identity_mismatch"]),
            delegation=DelegationDecision(False, "sender identity mismatch"),
            reasons=["sender_identity_mismatch"],
        )
    if message.receiver_agent_id != receiver_identity.agent_id:
        return CrossAgentValidation(
            allowed=False,
            sanitization=SanitizationResult(False, "", ["identity_mismatch"]),
            delegation=DelegationDecision(False, "receiver identity mismatch"),
            reasons=["receiver_identity_mismatch"],
        )

    sanitization = sanitize_message(message.text)
    message.sanitized = True
    message.sanitization_findings = tuple(sanitization.findings)

    delegation = check_delegation(
        sender_identity, receiver_identity, message.requested_capability
    )

    reasons: list[str] = []
    if not sanitization.safe:
        reasons.append(f"sanitization_findings={sanitization.findings}")
    if not delegation.allowed:
        reasons.append(f"delegation_blocked: {delegation.reason}")
    if (
        message.source_metadata.trust_level
        in (TrustLevel.UNTRUSTED, TrustLevel.QUARANTINED)
        and message.requested_capability
        in (
            "send_external",
            "sign_contract",
            "export_data",
            "issue_refund",
            "approve_price",
            "modify_production_config",
        )
    ):
        reasons.append(
            "untrusted_source_cannot_trigger_external_or_monetary_action"
        )

    return CrossAgentValidation(
        allowed=not reasons,
        sanitization=sanitization,
        delegation=delegation,
        reasons=reasons,
    )
