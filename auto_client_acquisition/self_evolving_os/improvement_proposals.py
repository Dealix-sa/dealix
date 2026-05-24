"""Improvement proposals — the human-gated path from suggestion → applied change.

Every suggestion from :mod:`.decision_improver` may be turned into an
:class:`ImprovementProposal`. Proposals carry an ``approval_required=True``
flag by construction and pass through a strict state machine:

    pending_approval → approved → applied
                    ↘ rejected

Proposals are visible to founders via the proposals endpoint and the
``/ar/ops/approvals`` UI. The state machine is enforced at the repository
level — :class:`InMemoryProposalRepository` raises on illegal transitions.
"""

from __future__ import annotations

import threading
import uuid
from collections.abc import Mapping, Sequence
from dataclasses import asdict, dataclass, field, replace
from datetime import UTC, datetime, timezone
from enum import StrEnum
from typing import Any

from auto_client_acquisition.self_evolving_os.decision_improver import ImprovementSuggestion


class ProposalState(StrEnum):
    PENDING = "pending_approval"
    APPROVED = "approved"
    APPLIED = "applied"
    REJECTED = "rejected"


class IllegalProposalTransition(RuntimeError):  # noqa: N818 — domain-specific exception name
    """Raised when callers try to skip or reverse a proposal state."""

    status_code = 409


@dataclass(frozen=True, slots=True)
class ImprovementProposal:
    """A human-gated improvement proposal awaiting review."""

    proposal_id: str
    tenant_id: str
    title: str
    rationale: str
    target_layer: str
    proposed_change: Mapping[str, Any]
    evidence_event_ids: tuple[str, ...] = field(default_factory=tuple)
    state: str = ProposalState.PENDING.value
    approved_by: str | None = None
    applied_by: str | None = None
    created_at: str = ""
    updated_at: str = ""

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["proposed_change"] = dict(self.proposed_change)
        data["evidence_event_ids"] = list(self.evidence_event_ids)
        return data


def _now_iso() -> str:
    return datetime.now(UTC).isoformat()


def proposal_from_suggestion(
    suggestion: ImprovementSuggestion,
    *,
    evidence_event_ids: Sequence[str] = (),
) -> ImprovementProposal:
    """Wrap an improver suggestion in a pending-approval proposal record."""
    now = _now_iso()
    return ImprovementProposal(
        proposal_id=f"prop_{uuid.uuid4().hex[:16]}",
        tenant_id=suggestion.tenant_id,
        title=suggestion.title,
        rationale=suggestion.rationale,
        target_layer=suggestion.target_layer,
        proposed_change=dict(suggestion.proposed_change),
        evidence_event_ids=tuple(evidence_event_ids),
        state=ProposalState.PENDING.value,
        created_at=now,
        updated_at=now,
    )


class InMemoryProposalRepository:
    """Thread-safe in-memory store for improvement proposals.

    Enforces the proposal state machine on every transition. Production
    deployments inject a Postgres-backed repository (table
    ``ai_improvement_proposals``) that shares the same surface.
    """

    __slots__ = ("_by_tenant", "_lock")

    def __init__(self) -> None:
        self._by_tenant: dict[str, dict[str, ImprovementProposal]] = {}
        self._lock = threading.RLock()

    def submit(self, proposal: ImprovementProposal) -> ImprovementProposal:
        with self._lock:
            self._by_tenant.setdefault(proposal.tenant_id, {})[proposal.proposal_id] = proposal
            return proposal

    def get(self, *, tenant_id: str, proposal_id: str) -> ImprovementProposal | None:
        with self._lock:
            return self._by_tenant.get(tenant_id, {}).get(proposal_id)

    def list_proposals(
        self,
        *,
        tenant_id: str,
        state: ProposalState | None = None,
    ) -> list[ImprovementProposal]:
        with self._lock:
            items = list(self._by_tenant.get(tenant_id, {}).values())
        if state is not None:
            items = [p for p in items if p.state == state.value]
        items.sort(key=lambda p: p.created_at, reverse=True)
        return items

    def approve(
        self,
        *,
        tenant_id: str,
        proposal_id: str,
        approved_by: str,
    ) -> ImprovementProposal:
        if not approved_by or not approved_by.strip():
            raise ValueError("approved_by is required")
        with self._lock:
            current = self._require(tenant_id, proposal_id)
            if current.state != ProposalState.PENDING.value:
                raise IllegalProposalTransition(
                    f"cannot approve from state {current.state!r}"
                )
            updated = replace(
                current,
                state=ProposalState.APPROVED.value,
                approved_by=approved_by.strip(),
                updated_at=_now_iso(),
            )
            self._by_tenant[tenant_id][proposal_id] = updated
            return updated

    def apply(
        self,
        *,
        tenant_id: str,
        proposal_id: str,
        applied_by: str,
    ) -> ImprovementProposal:
        if not applied_by or not applied_by.strip():
            raise ValueError("applied_by is required")
        with self._lock:
            current = self._require(tenant_id, proposal_id)
            if current.state != ProposalState.APPROVED.value:
                raise IllegalProposalTransition(
                    f"cannot apply from state {current.state!r} "
                    f"(must be {ProposalState.APPROVED.value!r})"
                )
            updated = replace(
                current,
                state=ProposalState.APPLIED.value,
                applied_by=applied_by.strip(),
                updated_at=_now_iso(),
            )
            self._by_tenant[tenant_id][proposal_id] = updated
            return updated

    def reject(
        self,
        *,
        tenant_id: str,
        proposal_id: str,
        rejected_by: str,
        reason: str = "",
    ) -> ImprovementProposal:
        if not rejected_by or not rejected_by.strip():
            raise ValueError("rejected_by is required")
        with self._lock:
            current = self._require(tenant_id, proposal_id)
            if current.state in (ProposalState.APPLIED.value, ProposalState.REJECTED.value):
                raise IllegalProposalTransition(
                    f"cannot reject from terminal state {current.state!r}"
                )
            updated = replace(
                current,
                state=ProposalState.REJECTED.value,
                updated_at=_now_iso(),
            )
            self._by_tenant[tenant_id][proposal_id] = updated
            return updated

    def clear_for_test(self, *, tenant_id: str | None = None) -> None:
        with self._lock:
            if tenant_id is None:
                self._by_tenant.clear()
            else:
                self._by_tenant.pop(tenant_id, None)

    def _require(self, tenant_id: str, proposal_id: str) -> ImprovementProposal:
        bucket = self._by_tenant.get(tenant_id, {})
        if proposal_id not in bucket:
            raise KeyError(f"proposal not found: {proposal_id!r}")
        return bucket[proposal_id]


# Module-level default repository for convenience.
_DEFAULT_REPO: InMemoryProposalRepository | None = None
_lock = threading.Lock()


def get_default_repository() -> InMemoryProposalRepository:
    global _DEFAULT_REPO
    with _lock:
        if _DEFAULT_REPO is None:
            _DEFAULT_REPO = InMemoryProposalRepository()
        return _DEFAULT_REPO


def reset_default_repository() -> None:
    global _DEFAULT_REPO
    with _lock:
        _DEFAULT_REPO = None


__all__ = [
    "IllegalProposalTransition",
    "ImprovementProposal",
    "InMemoryProposalRepository",
    "ProposalState",
    "get_default_repository",
    "proposal_from_suggestion",
    "reset_default_repository",
]
