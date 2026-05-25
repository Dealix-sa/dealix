"""
Delegation policy — hard rule against privilege escalation via delegation.
"""

from __future__ import annotations

from dataclasses import dataclass

from dealix.hermes.agent_comms.source_trust import PrivilegeLevel, rank_privilege
from dealix.hermes.identity.agent_identity import AgentIdentity


@dataclass
class DelegationDecision:
    allowed: bool
    reason: str


def check_delegation(
    sender: AgentIdentity,
    receiver: AgentIdentity,
    requested_capability: str,
    *,
    receiver_capability_floor_override: PrivilegeLevel | None = None,
) -> DelegationDecision:
    sender_level = rank_privilege(sender.capability_scope)
    receiver_level = receiver_capability_floor_override or rank_privilege(
        receiver.capability_scope
    )

    if requested_capability in receiver.forbidden_capabilities:
        return DelegationDecision(
            False,
            f"capability '{requested_capability}' is forbidden for receiver "
            f"{receiver.agent_id}",
        )

    if requested_capability not in receiver.capability_scope:
        return DelegationDecision(
            False,
            f"capability '{requested_capability}' is outside the receiver's scope",
        )

    if requested_capability in (
        "send_external",
        "sign_contract",
        "export_data",
        "approve_price",
        "issue_refund",
        "modify_production_config",
    ) and sender_level < PrivilegeLevel.APPROVER:
        return DelegationDecision(
            False,
            (
                "lower-privilege agent cannot delegate externally-visible or "
                "monetary actions (second-order prompt-injection guard)"
            ),
        )

    if sender_level < receiver_level - 10:
        return DelegationDecision(
            False,
            (
                f"sender privilege {int(sender_level)} too low to delegate to "
                f"receiver privilege {int(receiver_level)} "
                "(upward delegation not allowed without approval)"
            ),
        )

    return DelegationDecision(True, "ok")
