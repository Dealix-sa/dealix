"""
Policy engine.

Composes the approval matrix, autonomy policy, suppression list, and
claim guard into a single `evaluate(action, context)` call the action
router uses before any side effect.
"""
from __future__ import annotations

from dataclasses import dataclass

from . import autonomy_policy
from .approval_matrix import ApprovalMatrix
from .claim_guard import ClaimGuard
from .suppression import SuppressionList


@dataclass(frozen=True, slots=True)
class PolicyResult:
    allowed: bool
    reasons: list[str]
    approval_class: str


class PolicyEngine:
    def __init__(
        self,
        *,
        approval_matrix: ApprovalMatrix | None = None,
        claim_guard: ClaimGuard | None = None,
        suppression: SuppressionList | None = None,
    ) -> None:
        self.approval_matrix = approval_matrix or ApprovalMatrix.from_register()
        self.claim_guard = claim_guard or ClaimGuard.from_register()
        self.suppression = suppression or SuppressionList()

    def evaluate(
        self,
        action: str,
        *,
        target_contact: str | None = None,
        public_text: str | None = None,
    ) -> PolicyResult:
        reasons: list[str] = []
        policy = self.approval_matrix.classify(action)
        if policy.approval_class == "blocked":
            return PolicyResult(False, [f"action '{action}' is blocked"], "blocked")

        autonomy = autonomy_policy.evaluate(action)
        if not autonomy.allowed and policy.approval_class == "auto":
            return PolicyResult(False, [autonomy.reason], policy.approval_class)

        if target_contact and self.suppression.contains(target_contact):
            reasons.append(f"contact '{target_contact}' is suppressed")
            return PolicyResult(False, reasons, policy.approval_class)

        if public_text:
            violations = self.claim_guard.scan(public_text)
            if violations:
                reasons.extend(f"claim violation: {v.matched}" for v in violations[:5])
                return PolicyResult(False, reasons, policy.approval_class)

        return PolicyResult(True, ["ok"], policy.approval_class)
