"""
Section 64 — Security Modes.

Five modes. Start in Draft-Only. Only Sami can change modes. Tool calls,
external sends, and approvals are all gated by the current mode.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum

from dealix.control_plane.identity_access import Identity, IdentityKind


class SecurityMode(StrEnum):
    DRAFT_ONLY = "draft_only"
    APPROVAL_GATED = "approval_gated"
    LOW_RISK_AUTONOMY = "low_risk_autonomy"
    ENTERPRISE_CONTROLLED = "enterprise_controlled"
    SOVEREIGN_LOCKDOWN = "sovereign_lockdown"


@dataclass(frozen=True)
class _ModeRules:
    allow_external_send: bool
    allow_high_risk_tools: bool
    allow_low_risk_tools: bool
    drafts_only: bool
    require_approval_for_external: bool


_MODE_RULES: dict[SecurityMode, _ModeRules] = {
    SecurityMode.DRAFT_ONLY: _ModeRules(False, False, False, True, True),
    SecurityMode.APPROVAL_GATED: _ModeRules(True, True, True, False, True),
    SecurityMode.LOW_RISK_AUTONOMY: _ModeRules(True, False, True, False, False),
    SecurityMode.ENTERPRISE_CONTROLLED: _ModeRules(True, True, True, False, True),
    SecurityMode.SOVEREIGN_LOCKDOWN: _ModeRules(False, False, False, True, True),
}


@dataclass
class SecurityModeTransition:
    from_mode: SecurityMode
    to_mode: SecurityMode
    actor_id: str
    note: str | None = None
    at: datetime = field(default_factory=lambda: datetime.now(UTC))


class SecurityModeManager:
    def __init__(self, initial: SecurityMode = SecurityMode.DRAFT_ONLY) -> None:
        self._mode = initial
        self._history: list[SecurityModeTransition] = []
        self._listeners: list[Callable[[SecurityMode], None]] = []

    @property
    def mode(self) -> SecurityMode:
        return self._mode

    @property
    def history(self) -> list[SecurityModeTransition]:
        return list(self._history)

    def rules(self) -> _ModeRules:
        return _MODE_RULES[self._mode]

    def listen(self, callback: Callable[[SecurityMode], None]) -> None:
        self._listeners.append(callback)

    def switch(self, *, actor: Identity, target: SecurityMode, note: str | None = None) -> None:
        if actor.kind is not IdentityKind.SAMI:
            raise PermissionError("only Sami may switch security mode")
        if target is self._mode:
            return
        transition = SecurityModeTransition(
            from_mode=self._mode, to_mode=target, actor_id=actor.identity_id, note=note
        )
        self._mode = target
        self._history.append(transition)
        for cb in self._listeners:
            cb(target)

    def allow_external_send(self) -> bool:
        return self.rules().allow_external_send

    def allow_tool(self, *, risk_high: bool) -> bool:
        rules = self.rules()
        if risk_high:
            return rules.allow_high_risk_tools
        return rules.allow_low_risk_tools

    def drafts_only(self) -> bool:
        return self.rules().drafts_only

    def require_approval_for_external(self) -> bool:
        return self.rules().require_approval_for_external
