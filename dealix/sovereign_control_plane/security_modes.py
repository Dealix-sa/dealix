"""
Security mode manager — §91.

Holds the global security posture and decides whether actions of a
given risk level are allowed to execute under that posture. Only Sami
may elevate autonomy.
"""

from __future__ import annotations

import threading
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any

from dealix.sovereign_control_plane.identity import IdentityRegistry
from dealix.sovereign_control_plane.types import (
    IdentityKind,
    RiskLevel,
    SecurityMode,
)


_AUTONOMY_ORDER: dict[SecurityMode, int] = {
    SecurityMode.SOVEREIGN_LOCKDOWN: 0,
    SecurityMode.DRAFT_ONLY: 1,
    SecurityMode.APPROVAL_GATED: 2,
    SecurityMode.ENTERPRISE_CONTROLLED: 3,
    SecurityMode.LOW_RISK_AUTONOMY: 4,
}


_CAN_EXECUTE: dict[SecurityMode, set[RiskLevel]] = {
    SecurityMode.SOVEREIGN_LOCKDOWN: set(),
    SecurityMode.DRAFT_ONLY: {RiskLevel.NONE},
    SecurityMode.APPROVAL_GATED: {RiskLevel.NONE, RiskLevel.LOW},
    SecurityMode.ENTERPRISE_CONTROLLED: {RiskLevel.NONE, RiskLevel.LOW, RiskLevel.MEDIUM},
    SecurityMode.LOW_RISK_AUTONOMY: {RiskLevel.NONE, RiskLevel.LOW, RiskLevel.MEDIUM},
}


@dataclass
class SecurityModeChange:
    from_mode: SecurityMode
    to_mode: SecurityMode
    actor_id: str
    at: str
    reason: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "from_mode": self.from_mode.value,
            "to_mode": self.to_mode.value,
            "actor_id": self.actor_id,
            "at": self.at,
            "reason": self.reason,
        }


class SecurityModeManager:
    def __init__(self, identity_registry: IdentityRegistry) -> None:
        self._mode: SecurityMode = SecurityMode.DRAFT_ONLY
        self._history: list[SecurityModeChange] = []
        self._identities = identity_registry
        self._lock = threading.Lock()

    @property
    def current_mode(self) -> SecurityMode:
        return self._mode

    def set_mode(
        self, mode: SecurityMode, actor_id: str, reason: str = ""
    ) -> SecurityModeChange:
        with self._lock:
            current = self._mode
            target_rank = _AUTONOMY_ORDER[mode]
            current_rank = _AUTONOMY_ORDER[current]
            if target_rank > current_rank:
                # Elevation requires Sami.
                actor = self._identities.get(actor_id)
                if actor is None or actor.kind != IdentityKind.SAMI:
                    raise PermissionError("only Sami may elevate autonomy")
            change = SecurityModeChange(
                from_mode=current, to_mode=mode, actor_id=actor_id,
                at=datetime.now(UTC).isoformat(), reason=reason,
            )
            self._mode = mode
            self._history.append(change)
            return change

    def force_lockdown(self, reason: str) -> SecurityModeChange:
        """Lower-only transition — always allowed (system action)."""
        with self._lock:
            change = SecurityModeChange(
                from_mode=self._mode, to_mode=SecurityMode.SOVEREIGN_LOCKDOWN,
                actor_id="system", at=datetime.now(UTC).isoformat(),
                reason=reason,
            )
            self._mode = SecurityMode.SOVEREIGN_LOCKDOWN
            self._history.append(change)
            return change

    def can_execute(self, action_risk: RiskLevel) -> bool:
        return action_risk in _CAN_EXECUTE[self._mode]

    def history(self) -> list[SecurityModeChange]:
        return list(self._history)
