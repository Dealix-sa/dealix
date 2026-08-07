"""Canonical PlaybookVersion contracts for Company Intelligence self-improvement.

A PlaybookVersion records a versioned change to an operational playbook,
grounded in evidence from outcomes, failures, and learning events. Every
playbook change requires evidence references and an approval status —
preventing ungrounded strategy drift.

The models are persistence-neutral: no database, network, or LLM calls.

Entity ownership: PlaybookVersion → self_improvement
    (versioned playbook changes with evidence and approval).
Required fields: tenant_id, playbook_name, version, change_reason,
    evidence_refs, approval_status.
Forbidden parallel names: StrategyVersion, WorkflowVersion.
"""
from __future__ import annotations

import json
from datetime import UTC, datetime
from enum import StrEnum
from hashlib import sha256
from typing import Annotated, Any

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    StringConstraints,
    model_validator,
)

NonEmptyString = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------


class PlaybookApprovalStatus(StrEnum):
    """Approval states for a playbook version change."""

    PROPOSED = "proposed"
    UNDER_REVIEW = "under_review"
    APPROVED = "approved"
    REJECTED = "rejected"
    SUPERSEDED = "superseded"


# ---------------------------------------------------------------------------
# Stable ID generation
# ---------------------------------------------------------------------------


def _stable_playbook_id(payload: dict[str, Any]) -> str:
    canonical = json.dumps(
        payload,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
        default=str,
    )
    return f"playbook_{sha256(canonical.encode('utf-8')).hexdigest()[:16]}"


# ---------------------------------------------------------------------------
# Canonical PlaybookVersion contract
# ---------------------------------------------------------------------------


class CanonicalPlaybookVersion(BaseModel):
    """One tenant-scoped, versioned playbook change record.

    PlaybookVersions form the self-improvement ledger — every strategy
    change is grounded in evidence from outcomes and learning events.
    A rejected change is still recorded for the audit trail.

    Key invariants:
      - Version must be positive.
      - At least one evidence reference is required.
      - Change reason cannot be empty.
      - Playbook ID is deterministic from name + version + tenant.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    # Identity
    tenant_id: NonEmptyString
    playbook_version_id: NonEmptyString

    # Playbook details
    playbook_name: NonEmptyString
    version: int = Field(default=1, ge=1)
    change_reason: NonEmptyString

    # Content
    description: str = ""
    changes_summary: str = ""

    # Approval
    approval_status: PlaybookApprovalStatus = PlaybookApprovalStatus.PROPOSED

    # Evidence
    evidence_refs: tuple[str, ...] = ()
    learning_event_ids: tuple[str, ...] = ()

    # Scoring
    confidence: float = Field(default=0.5, ge=0.0, le=1.0)

    # Provenance
    source_id: NonEmptyString

    # Timestamps
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    approved_at: datetime | None = None

    @model_validator(mode="after")
    def enforce_playbook_invariants(self) -> CanonicalPlaybookVersion:
        # At least one evidence reference
        if len(self.evidence_refs) == 0:
            raise ValueError(
                "playbook version requires at least one evidence reference"
            )

        # approved_at must be timezone-aware if set
        if self.approved_at is not None and self.approved_at.tzinfo is None:
            raise ValueError("approved_at must be timezone-aware")

        # Approved playbooks must have approved_at
        if (
            self.approval_status == PlaybookApprovalStatus.APPROVED
            and self.approved_at is None
        ):
            raise ValueError("approved playbook versions must have an approved_at timestamp")

        # Proposed/under-review playbooks must not have approved_at
        if (
            self.approval_status in {
                PlaybookApprovalStatus.PROPOSED,
                PlaybookApprovalStatus.UNDER_REVIEW,
            }
            and self.approved_at is not None
        ):
            raise ValueError(
                "proposed or under-review playbook versions must not have an approved_at timestamp"
            )

        # Verify deterministic ID
        expected_id = _stable_playbook_id({
            "playbook_name": self.playbook_name,
            "tenant_id": self.tenant_id,
            "version": self.version,
        })
        if self.playbook_version_id != expected_id:
            raise ValueError("playbook_version_id does not match the canonical payload")

        return self


# ---------------------------------------------------------------------------
# Builder
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# State machine
# ---------------------------------------------------------------------------

_PLAYBOOK_TRANSITIONS: dict[
    PlaybookApprovalStatus, frozenset[PlaybookApprovalStatus]
] = {
    PlaybookApprovalStatus.PROPOSED: frozenset(
        {PlaybookApprovalStatus.UNDER_REVIEW, PlaybookApprovalStatus.REJECTED}
    ),
    PlaybookApprovalStatus.UNDER_REVIEW: frozenset(
        {PlaybookApprovalStatus.APPROVED, PlaybookApprovalStatus.REJECTED}
    ),
    PlaybookApprovalStatus.APPROVED: frozenset(
        {PlaybookApprovalStatus.SUPERSEDED}
    ),
    PlaybookApprovalStatus.REJECTED: frozenset(),  # terminal
    PlaybookApprovalStatus.SUPERSEDED: frozenset(),  # terminal
}


def valid_playbook_transitions_from(
    status: PlaybookApprovalStatus,
) -> frozenset[PlaybookApprovalStatus]:
    """Return the set of valid target states from *status*."""
    return _PLAYBOOK_TRANSITIONS.get(status, frozenset())


def is_valid_playbook_transition(
    from_status: PlaybookApprovalStatus,
    to_status: PlaybookApprovalStatus,
) -> bool:
    """Check whether *from_status* → *to_status* is a valid transition."""
    return to_status in valid_playbook_transitions_from(from_status)


def transition_playbook(
    playbook: CanonicalPlaybookVersion,
    *,
    to_status: PlaybookApprovalStatus,
    approved_at: datetime | None = None,
) -> CanonicalPlaybookVersion:
    """Return a new CanonicalPlaybookVersion with *to_status* applied.

    Raises ValueError on invalid transitions. The original is never mutated.
    When transitioning to APPROVED, approved_at is set automatically if not
    provided.
    """
    if not is_valid_playbook_transition(playbook.approval_status, to_status):
        raise ValueError(
            f"invalid playbook transition: "
            f"{playbook.approval_status.value} → {to_status.value}"
        )
    updates: dict[str, Any] = {"approval_status": to_status}
    if to_status == PlaybookApprovalStatus.APPROVED:
        updates["approved_at"] = approved_at or datetime.now(UTC)
    return type(playbook).model_validate({**playbook.model_dump(), **updates})


# ---------------------------------------------------------------------------
# Builder
# ---------------------------------------------------------------------------


def build_playbook_version(
    *,
    tenant_id: str,
    playbook_name: str,
    version: int,
    change_reason: str,
    source_id: str,
    evidence_refs: tuple[str, ...] = ("manual_observation",),
    learning_event_ids: tuple[str, ...] = (),
    description: str = "",
    changes_summary: str = "",
    approval_status: PlaybookApprovalStatus = PlaybookApprovalStatus.PROPOSED,
    confidence: float = 0.5,
    approved_at: datetime | None = None,
) -> CanonicalPlaybookVersion:
    """Build a deterministic, versioned, evidence-grounded playbook change."""

    playbook_version_id = _stable_playbook_id({
        "playbook_name": playbook_name.strip(),
        "tenant_id": tenant_id.strip(),
        "version": version,
    })

    return CanonicalPlaybookVersion(
        tenant_id=tenant_id,
        playbook_version_id=playbook_version_id,
        playbook_name=playbook_name,
        version=version,
        change_reason=change_reason,
        description=description,
        changes_summary=changes_summary,
        approval_status=approval_status,
        evidence_refs=evidence_refs,
        learning_event_ids=learning_event_ids,
        confidence=confidence,
        source_id=source_id,
        approved_at=approved_at,
    )
