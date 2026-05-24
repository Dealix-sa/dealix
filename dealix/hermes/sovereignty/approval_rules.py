"""Rules that turn a sovereignty level into a concrete approval verdict."""

from __future__ import annotations

from dataclasses import dataclass

from dealix.hermes.sovereignty.kill_switch import KillScope, KillSwitch
from dealix.hermes.sovereignty.levels import SovereigntyLevel


@dataclass(frozen=True)
class ApprovalDecision:
    allowed: bool
    auto: bool                   # true = no human in the loop
    requires_approver: str | None  # 'sami' usually, None when auto
    reason: str


class ApprovalRules:
    """Tiny rule engine. Keep this dumb on purpose — every nuance becomes
    a new explicit rule, not a clever heuristic."""

    def __init__(self, kill_switch: KillSwitch | None = None) -> None:
        self._kill = kill_switch or KillSwitch()

    @property
    def kill_switch(self) -> KillSwitch:
        return self._kill

    def evaluate(
        self,
        *,
        action: str,
        level: SovereigntyLevel,
        domain: str = "core",
    ) -> ApprovalDecision:
        # Kill switch always wins.
        if self._kill.is_killed(KillScope.GLOBAL) or self._kill.is_killed(KillScope.from_domain(domain)):
            return ApprovalDecision(
                allowed=False,
                auto=False,
                requires_approver=None,
                reason=f"Kill switch active (global or {domain}).",
            )

        if level == SovereigntyLevel.S5_NEVER_AUTONOMOUS:
            return ApprovalDecision(
                allowed=False,
                auto=False,
                requires_approver=None,
                reason="S5 is never autonomous and never delegated.",
            )

        if level == SovereigntyLevel.S4_SOVEREIGN_ONLY:
            return ApprovalDecision(
                allowed=False,
                auto=False,
                requires_approver="sami",
                reason="S4 — Sami acts directly; agents only prepare.",
            )

        if level == SovereigntyLevel.S3_SOVEREIGN_MEMO:
            return ApprovalDecision(
                allowed=True,
                auto=False,
                requires_approver="sami",
                reason="S3 — needs written sovereign memo + Sami approval.",
            )

        if level == SovereigntyLevel.S2_SAMI_APPROVAL:
            return ApprovalDecision(
                allowed=True,
                auto=False,
                requires_approver="sami",
                reason="S2 — external action requires Sami approval.",
            )

        # S1 / S0 auto-run.
        return ApprovalDecision(
            allowed=True,
            auto=True,
            requires_approver=None,
            reason=f"{level.label} — safe to auto-execute.",
        )


__all__ = ["ApprovalDecision", "ApprovalRules"]
