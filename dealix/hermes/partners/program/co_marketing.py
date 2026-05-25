"""Draft co-marketing engagements — never sends, only queues."""

from __future__ import annotations

import time
import uuid
from dataclasses import dataclass, field

_PROPOSALS: dict[str, "CoMarketingProposal"] = {}


@dataclass(frozen=True)
class CoMarketingProposal:
    proposal_id: str
    partner_id: str
    title: str
    deliverables: tuple[str, ...]
    approved_claim_ids: tuple[str, ...]
    status: str
    requires_approval: bool
    created_at: float = 0.0
    notes: str = field(default="")


def draft(
    partner_id: str,
    title: str,
    deliverables: list[str],
    approved_claim_ids: list[str],
    notes: str = "",
) -> CoMarketingProposal:
    """Queue a co-marketing proposal as a DRAFT requiring approval."""
    p = CoMarketingProposal(
        proposal_id=f"com_{uuid.uuid4().hex[:8]}",
        partner_id=partner_id,
        title=title,
        deliverables=tuple(deliverables),
        approved_claim_ids=tuple(approved_claim_ids),
        status="draft",
        requires_approval=True,
        created_at=time.time(),
        notes=notes,
    )
    _PROPOSALS[p.proposal_id] = p
    return p


def list_drafts(partner_id: str | None = None) -> list[CoMarketingProposal]:
    """Return all co-marketing drafts, optionally filtered by partner."""
    if partner_id is None:
        return list(_PROPOSALS.values())
    return [p for p in _PROPOSALS.values() if p.partner_id == partner_id]


def reset() -> None:
    """Clear co-marketing proposal store (test helper)."""
    _PROPOSALS.clear()
