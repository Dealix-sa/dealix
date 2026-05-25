"""
Privilege levels for agents — used to decide if a delegation is upward,
sideways, or downward.
"""

from __future__ import annotations

from enum import IntEnum


class PrivilegeLevel(IntEnum):
    READ_ONLY = 10
    DRAFTER = 20
    INTERNAL_WRITER = 30
    EXTERNAL_DRAFTER = 40
    APPROVER = 50
    EXECUTOR = 60


# Capability → minimum privilege level required to hold that capability.
_CAPABILITY_FLOOR: dict[str, PrivilegeLevel] = {
    "read_approved_opportunity": PrivilegeLevel.READ_ONLY,
    "read_public_data": PrivilegeLevel.READ_ONLY,
    "read_internal_doc": PrivilegeLevel.READ_ONLY,
    "draft_proposal": PrivilegeLevel.DRAFTER,
    "draft_message": PrivilegeLevel.DRAFTER,
    "summarize_call": PrivilegeLevel.DRAFTER,
    "flag_risk": PrivilegeLevel.DRAFTER,
    "update_crm_internal": PrivilegeLevel.INTERNAL_WRITER,
    "create_workflow_internal": PrivilegeLevel.INTERNAL_WRITER,
    "send_external": PrivilegeLevel.EXTERNAL_DRAFTER,
    "approve_price": PrivilegeLevel.APPROVER,
    "sign_contract": PrivilegeLevel.EXECUTOR,
    "export_data": PrivilegeLevel.EXECUTOR,
    "issue_refund": PrivilegeLevel.EXECUTOR,
    "modify_production_config": PrivilegeLevel.EXECUTOR,
}


def rank_privilege(capability_scope: list[str] | tuple[str, ...]) -> PrivilegeLevel:
    """The agent's privilege level = highest floor across its capabilities."""
    if not capability_scope:
        return PrivilegeLevel.READ_ONLY
    return max(
        (_CAPABILITY_FLOOR.get(c, PrivilegeLevel.READ_ONLY) for c in capability_scope),
        default=PrivilegeLevel.READ_ONLY,
    )
