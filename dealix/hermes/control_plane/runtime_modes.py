"""
RuntimeMode — global behaviour gate for the control plane.

Dealix always boots in ``DRAFT_ONLY``. Modes can only be promoted by a
sovereign actor (Sami). Downgrades (e.g. to ``SOVEREIGN_LOCKDOWN``) can
be triggered by the kill switch.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class RuntimeMode(StrEnum):
    DRAFT_ONLY = "DRAFT_ONLY"
    APPROVAL_GATED = "APPROVAL_GATED"
    LOW_RISK_AUTONOMY = "LOW_RISK_AUTONOMY"
    ENTERPRISE_CONTROLLED = "ENTERPRISE_CONTROLLED"
    SOVEREIGN_LOCKDOWN = "SOVEREIGN_LOCKDOWN"

    @property
    def allows_external_actions(self) -> bool:
        return self in (
            RuntimeMode.APPROVAL_GATED,
            RuntimeMode.LOW_RISK_AUTONOMY,
            RuntimeMode.ENTERPRISE_CONTROLLED,
        )

    @property
    def requires_approval_for_every_external(self) -> bool:
        return self in (RuntimeMode.DRAFT_ONLY, RuntimeMode.APPROVAL_GATED)

    @property
    def is_lockdown(self) -> bool:
        return self == RuntimeMode.SOVEREIGN_LOCKDOWN


@dataclass
class RuntimeModeState:
    """Mutable holder so the mode can be swapped without re-importing."""

    current: RuntimeMode = RuntimeMode.DRAFT_ONLY

    def set(self, mode: RuntimeMode, *, sovereign: bool) -> None:
        if not sovereign and mode != RuntimeMode.SOVEREIGN_LOCKDOWN:
            raise PermissionError("Only a sovereign actor can promote runtime mode.")
        self.current = mode


STATE = RuntimeModeState()
