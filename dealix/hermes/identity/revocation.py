"""
Revocation ledger — in-memory ledger of revoked agent identities.
"""

from __future__ import annotations

import time
from dataclasses import dataclass

from dealix.hermes.identity.agent_identity import AgentIdentity, IdentityStatus


@dataclass
class RevocationEntry:
    agent_id: str
    revoked_at: float
    revoked_by: str
    reason: str


class RevocationLedger:
    def __init__(self) -> None:
        self._entries: dict[str, RevocationEntry] = {}

    def revoke(self, identity: AgentIdentity, revoked_by: str, reason: str) -> RevocationEntry:
        if not identity.revocable:
            raise ValueError(f"identity {identity.agent_id} is marked non-revocable")
        if not revoked_by or not reason:
            raise ValueError("revocation requires revoked_by and reason")
        entry = RevocationEntry(
            agent_id=identity.agent_id,
            revoked_at=time.time(),
            revoked_by=revoked_by,
            reason=reason,
        )
        self._entries[identity.agent_id] = entry
        identity.status = IdentityStatus.REVOKED
        return entry

    def is_revoked(self, agent_id: str) -> bool:
        return agent_id in self._entries

    def get(self, agent_id: str) -> RevocationEntry | None:
        return self._entries.get(agent_id)


def revoke(
    ledger: RevocationLedger,
    identity: AgentIdentity,
    *,
    revoked_by: str,
    reason: str,
) -> RevocationEntry:
    return ledger.revoke(identity, revoked_by=revoked_by, reason=reason)


def is_revoked(ledger: RevocationLedger, agent_id: str) -> bool:
    return ledger.is_revoked(agent_id)
