"""Draft Quality Gate — approval-first safety enforcement.

Reuses the platform's governance primitives instead of re-inventing keyword
lists, so the gate stays in lock-step with the doctrine guard tests:
  * ``governance_os.policy_check_draft`` — forbidden claims / channels / terms
  * ``governance_os.audit_claim_safety`` — guarantee / fake-proof → BLOCK

It then adds Distribution-OS-specific invariants:
  * every draft must be ``approval_required=True``
  * every draft must sit in a queueable status (never an external-send status —
    none exists in the model, so this also fails closed on tampered data)
  * evidence level must be L0–L5
  * channel must be a known manual channel
"""

from __future__ import annotations

from dataclasses import dataclass

from auto_client_acquisition.distribution_os.models import (
    EVIDENCE_LEVELS,
    QUEUEABLE_STATUSES,
    Channel,
    Draft,
    DraftStatus,
)
from auto_client_acquisition.governance_os import audit_claim_safety, policy_check_draft

_VALID_CHANNELS = {c.value for c in Channel}
#: A human may move a draft to these after acting on it.
_POST_REVIEW_STATUSES = {
    DraftStatus.APPROVED.value,
    DraftStatus.REJECTED.value,
    DraftStatus.COPIED_MANUALLY.value,
    DraftStatus.REPLIED.value,
    DraftStatus.ARCHIVED.value,
}
_ALLOWED_STATUSES = {s.value for s in QUEUEABLE_STATUSES} | _POST_REVIEW_STATUSES


@dataclass(frozen=True)
class GateViolation:
    draft_id: str
    code: str
    detail: str


def check_draft(draft: Draft) -> list[GateViolation]:
    """Return the list of violations for a single draft (empty = clean)."""
    out: list[GateViolation] = []

    verdict = policy_check_draft(draft.body)
    if not verdict.allowed:
        for issue in verdict.issues:
            out.append(GateViolation(draft.id, "policy_block", issue))

    claim = audit_claim_safety(draft.body)
    for issue in claim.issues:
        if issue.startswith("forbidden_claim:"):
            out.append(GateViolation(draft.id, "forbidden_claim", issue))

    if draft.approval_required is not True:
        out.append(
            GateViolation(draft.id, "approval_required_false", "approval_required must be true")
        )

    if draft.status not in _ALLOWED_STATUSES:
        out.append(
            GateViolation(
                draft.id,
                "illegal_status",
                f"status '{draft.status}' is not an approval-first status (no auto-send allowed)",
            )
        )

    if draft.evidence_level not in EVIDENCE_LEVELS:
        out.append(
            GateViolation(
                draft.id, "invalid_evidence_level", f"evidence_level '{draft.evidence_level}'"
            )
        )

    if draft.channel not in _VALID_CHANNELS:
        out.append(GateViolation(draft.id, "invalid_channel", f"channel '{draft.channel}'"))

    return out


@dataclass(frozen=True)
class GateResult:
    checked: int
    violations: tuple[GateViolation, ...]

    @property
    def ok(self) -> bool:
        return not self.violations


def check_drafts(drafts: list[Draft]) -> GateResult:
    """Run the gate across a queue of drafts."""
    violations: list[GateViolation] = []
    for d in drafts:
        violations.extend(check_draft(d))
    return GateResult(checked=len(drafts), violations=tuple(violations))


__all__ = ["GateResult", "GateViolation", "check_draft", "check_drafts"]
