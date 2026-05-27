"""Global / per-domain kill switch.

When tripped, no execution may proceed in the affected scope until Sami
explicitly clears it. The switch is in-memory by default; persistence
plugs in by replacing the storage hook.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum


class KillScope(str, Enum):
    GLOBAL = "global"
    MONEY = "money"
    PRODUCT = "product"
    PARTNER = "partner"
    MARKET = "market"
    CUSTOMER = "customer"
    TRUST = "trust"
    API = "api"
    MARKETPLACE = "marketplace"
    VENTURE = "venture"

    @classmethod
    def from_domain(cls, domain: str) -> "KillScope":
        try:
            return cls(domain)
        except ValueError:
            return cls.GLOBAL


@dataclass
class _KillState:
    active: bool = False
    reason: str = ""
    activated_at: datetime | None = None
    activated_by: str = ""


@dataclass
class KillSwitch:
    """In-memory kill switch. One per kernel instance is plenty."""

    _states: dict[KillScope, _KillState] = field(default_factory=dict)

    def activate(self, scope: KillScope, *, reason: str, by: str = "sami") -> None:
        self._states[scope] = _KillState(
            active=True,
            reason=reason,
            activated_at=datetime.now(timezone.utc),
            activated_by=by,
        )

    def deactivate(self, scope: KillScope, *, by: str = "sami") -> None:
        if scope in self._states:
            self._states[scope] = _KillState(active=False, activated_by=by)

    def is_killed(self, scope: KillScope) -> bool:
        return self._states.get(scope, _KillState()).active

    def status(self, scope: KillScope) -> _KillState:
        return self._states.get(scope, _KillState())


__all__ = ["KillScope", "KillSwitch"]
