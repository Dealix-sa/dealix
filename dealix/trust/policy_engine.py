"""
Policy Engine — generic policy hook for the Company OS Trust layer.

Other modules (`approval_matrix`, `claim_guard`, `suppression`,
`data_retention`, `evidence_pack`) are domain-specific. This module is a
small composition surface that lets a single call evaluate a candidate
external action against all the relevant Trust policies in one place.

Designed for the `send` paths (outreach, proposals, invoices, claims).
For internal-only artifacts (A0), this engine is a no-op pass.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

from dealix.trust import claim_guard, suppression
from dealix.trust.approval_matrix import (
    ApprovalRequired,
    ApprovalTier,
    ProhibitedAction,
    entry_for,
    require_approval,
)
from dealix.trust.evidence_pack import EvidencePack, assert_complete

PolicyOutcome = Literal["pass", "fail"]


@dataclass
class PolicyEvaluation:
    action_class: str
    outcome: PolicyOutcome
    tier: ApprovalTier
    blockers: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return self.outcome == "pass"


def evaluate_send(
    *,
    action_class: str,
    text: str,
    recipient_type: str | None = None,
    recipient_value: str | None = None,
    approvals: list[str] | None = None,
    evidence_pack: EvidencePack | None = None,
) -> PolicyEvaluation:
    """Evaluate a candidate external send against Trust policies.

    Returns a `PolicyEvaluation` rather than raising, so callers can
    decide their own enforcement posture. For the canonical
    "raise-or-pass" usage, see `assert_send`.
    """
    entry = entry_for(action_class)
    evaluation = PolicyEvaluation(
        action_class=action_class, outcome="pass", tier=entry.tier
    )

    # 1. Approval matrix.
    try:
        require_approval(
            action_class,
            approvals=approvals,
            has_evidence_pack=evidence_pack is not None,
        )
    except ProhibitedAction as exc:
        evaluation.outcome = "fail"
        evaluation.blockers.append(str(exc))
        return evaluation
    except ApprovalRequired as exc:
        evaluation.outcome = "fail"
        evaluation.blockers.append(str(exc))

    # 2. Evidence pack required for A3 claims.
    if entry.tier == ApprovalTier.A3 and evidence_pack is not None:
        try:
            assert_complete(evidence_pack)
        except ValueError as exc:
            evaluation.outcome = "fail"
            evaluation.blockers.append(str(exc))

    # 3. Suppression check on recipient (if a recipient is present).
    if recipient_type and recipient_value:
        try:
            suppression.assert_not_suppressed(recipient_type, recipient_value)
        except suppression.SuppressionViolation as exc:
            evaluation.outcome = "fail"
            evaluation.blockers.append(str(exc))

    # 4. Claim guard on outbound text.
    if text:
        report = claim_guard.check(text)
        if report.is_blocking:
            evaluation.outcome = "fail"
            for flag in report.flags:
                if flag.severity == claim_guard.FlagSeverity.BLOCK:
                    evaluation.blockers.append(
                        f"claim_guard:{flag.rule}:{flag.excerpt}"
                    )
        for flag in report.flags:
            if flag.severity == claim_guard.FlagSeverity.WARN:
                evaluation.warnings.append(
                    f"claim_guard:{flag.rule}:{flag.excerpt}"
                )

    return evaluation


def assert_send(
    *,
    action_class: str,
    text: str,
    recipient_type: str | None = None,
    recipient_value: str | None = None,
    approvals: list[str] | None = None,
    evidence_pack: EvidencePack | None = None,
) -> None:
    """Raise PolicyViolation if the candidate send fails any Trust policy."""
    evaluation = evaluate_send(
        action_class=action_class,
        text=text,
        recipient_type=recipient_type,
        recipient_value=recipient_value,
        approvals=approvals,
        evidence_pack=evidence_pack,
    )
    if not evaluation.passed:
        raise PolicyViolation(evaluation)


class PolicyViolation(Exception):  # noqa: N818 — matches incident vocabulary
    """Raised by `assert_send` when one or more Trust policies block."""

    def __init__(self, evaluation: PolicyEvaluation) -> None:
        super().__init__(
            f"Trust policy blocked action {evaluation.action_class!r} "
            f"(tier {evaluation.tier.value}): "
            + "; ".join(evaluation.blockers)
        )
        self.evaluation = evaluation


__all__ = [
    "PolicyEvaluation",
    "PolicyOutcome",
    "PolicyViolation",
    "assert_send",
    "evaluate_send",
]
