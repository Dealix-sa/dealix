"""Auto-execution gate for the Full Ops Sales System.

The single safety spine: an action may auto-execute only when it needs no
approval, is cheaply reversible, is not regulated/personal-data, and is not
on the never-auto list. Everything else is routed to ``approval_center``.

    auto_exec_allowed = A0
                        AND reversibility in {R0, R1}
                        AND sensitivity   in {S0, S1, S2}
                        AND action not in NEVER_AUTO_EXECUTE
"""

from __future__ import annotations

from dataclasses import dataclass

from dealix.classifications import (
    NEVER_AUTO_EXECUTE,
    ApprovalClass,
    ReversibilityClass,
    SensitivityClass,
    classify,
)

_AUTO_REVERSIBILITY: frozenset[ReversibilityClass] = frozenset(
    {ReversibilityClass.R0, ReversibilityClass.R1}
)
_AUTO_SENSITIVITY: frozenset[SensitivityClass] = frozenset(
    {SensitivityClass.S0, SensitivityClass.S1, SensitivityClass.S2}
)


@dataclass(frozen=True, slots=True)
class GateDecision:
    """The outcome of classifying one action against the auto-exec boundary."""

    action_type: str
    approval_class: ApprovalClass
    reversibility_class: ReversibilityClass
    sensitivity_class: SensitivityClass
    auto_exec_allowed: bool
    reason: str

    def to_dict(self) -> dict[str, object]:
        return {
            "action_type": self.action_type,
            "approval_class": self.approval_class.value,
            "reversibility_class": self.reversibility_class.value,
            "sensitivity_class": self.sensitivity_class.value,
            "auto_exec_allowed": self.auto_exec_allowed,
            "reason": self.reason,
        }


def evaluate_gate(action_type: str) -> GateDecision:
    """Classify ``action_type`` and decide whether it may auto-execute."""
    approval, reversibility, sensitivity = classify(action_type)

    if action_type in NEVER_AUTO_EXECUTE:
        return GateDecision(
            action_type, approval, reversibility, sensitivity,
            auto_exec_allowed=False, reason="never_auto_execute",
        )

    failures: list[str] = []
    if approval != ApprovalClass.A0:
        failures.append(f"approval={approval.value}")
    if reversibility not in _AUTO_REVERSIBILITY:
        failures.append(f"reversibility={reversibility.value}")
    if sensitivity not in _AUTO_SENSITIVITY:
        failures.append(f"sensitivity={sensitivity.value}")

    if failures:
        return GateDecision(
            action_type, approval, reversibility, sensitivity,
            auto_exec_allowed=False,
            reason="approval_required:" + ",".join(failures),
        )

    return GateDecision(
        action_type, approval, reversibility, sensitivity,
        auto_exec_allowed=True, reason="internal_safe",
    )


def auto_exec_allowed(action_type: str) -> bool:
    """True iff the action may auto-execute without human approval."""
    return evaluate_gate(action_type).auto_exec_allowed


__all__ = ["GateDecision", "evaluate_gate", "auto_exec_allowed"]
