"""
Revocation — runtime cancellation of an agent, session, or capability.

Revocations are write-once: once an identity is revoked, every subsequent
control-plane call referencing it is denied at the boundary.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum


class RevocationTarget(StrEnum):
    AGENT = "agent"
    SESSION = "session"
    CAPABILITY = "capability"
    PARTNER = "partner"


@dataclass(frozen=True)
class Revocation:
    target_type: RevocationTarget
    target_id: str
    reason: str
    revoked_by: str
    revoked_at: datetime = field(default_factory=lambda: datetime.now(UTC))


REVOCATION_LIST: dict[tuple[RevocationTarget, str], Revocation] = {}


def revoke(
    target_type: RevocationTarget,
    target_id: str,
    *,
    reason: str,
    by: str,
) -> Revocation:
    record = Revocation(target_type=target_type, target_id=target_id, reason=reason, revoked_by=by)
    REVOCATION_LIST[(target_type, target_id)] = record
    return record


def is_revoked(target_type: RevocationTarget, target_id: str) -> bool:
    return (target_type, target_id) in REVOCATION_LIST
