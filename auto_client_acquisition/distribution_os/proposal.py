"""Proposal Factory — proposals bound to a real catalog product + approval gate.

Rules (plan section 8): no proposal without a qualified prospect, no final
price without approval, no open scope, no guarantees. The reference price is
read from the catalog — never invented. ``approval_status`` starts as
``pending_approval``; the final/sendable price is gated behind approval.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import StrEnum
from typing import Any
from uuid import uuid4

from auto_client_acquisition.distribution_os import catalog
from auto_client_acquisition.distribution_os._store import JsonlStore, now_iso
from auto_client_acquisition.distribution_os.draft_quality import check_draft


class ProposalStatus(StrEnum):
    PENDING_APPROVAL = "pending_approval"
    APPROVED = "approved"
    REJECTED = "rejected"
    SENT = "sent"  # reserved; set only after manual founder send


@dataclass
class Proposal:
    id: str = field(default_factory=lambda: f"prop_{uuid4().hex[:12]}")
    prospect_id: str = ""
    product_id: str = ""
    sector: str = ""
    problem: str = ""
    proposed_solution: str = ""
    scope: list[str] = field(default_factory=list)
    out_of_scope: list[str] = field(default_factory=list)
    timeline: str = ""
    price_min_sar: int = 0
    price_max_sar: int = 0
    assumptions: list[str] = field(default_factory=list)
    evidence_level: int = 0
    risks: list[str] = field(default_factory=list)
    payment_terms: str = ""
    next_step: str = ""
    approval_status: str = ProposalStatus.PENDING_APPROVAL.value
    quality_issues: list[str] = field(default_factory=list)
    created_at: str = field(default_factory=now_iso)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


_store = JsonlStore(
    env_var="DEALIX_PROPOSALS_PATH", default_rel="var/proposals.jsonl", id_field="id"
)


def generate_proposal(
    *,
    prospect_id: str,
    product_id: str,
    sector: str = "",
    problem: str = "",
    proposed_solution: str = "",
    scope: list[str] | None = None,
    out_of_scope: list[str] | None = None,
    timeline: str = "",
    assumptions: list[str] | None = None,
    evidence_level: int = 0,
    risks: list[str] | None = None,
    payment_terms: str = "",
    next_step: str = "",
) -> Proposal:
    """Build a proposal. ``product_id`` MUST be a valid catalog id; the price
    band is pulled from the catalog (no invented price). Requires a non-empty
    ``out_of_scope`` so scope is never left open.
    """
    if not prospect_id:
        raise ValueError("prospect_id is required (no proposal without a prospect)")
    if not catalog.is_valid_product_id(product_id):
        raise ValueError(f"unknown_product_id:{product_id} (link to a catalog product)")
    out_scope = out_of_scope or []
    if not out_scope:
        raise ValueError("out_of_scope must not be empty (no open scope)")
    pmin, pmax = catalog.price_band(product_id)

    proposal = Proposal(
        prospect_id=prospect_id,
        product_id=product_id,
        sector=sector,
        problem=problem,
        proposed_solution=proposed_solution,
        scope=scope or [],
        out_of_scope=out_scope,
        timeline=timeline,
        price_min_sar=pmin,
        price_max_sar=pmax,
        assumptions=assumptions or [],
        evidence_level=evidence_level,
        risks=risks or [],
        payment_terms=payment_terms,
        next_step=next_step,
    )
    # Guard the narrative fields against guaranteed-outcome language.
    narrative = " ".join([problem, proposed_solution, next_step, payment_terms])
    quality = check_draft(text=narrative, max_chars=10000)
    if quality.decision == "block":
        raise ValueError(f"proposal_narrative_blocked:{','.join(quality.issues)}")
    proposal.quality_issues = list(quality.issues)
    _store.append(proposal.to_dict())
    return proposal


def get_proposal(proposal_id: str) -> Proposal | None:
    rec = _store.get(proposal_id)
    return Proposal(**rec) if rec else None


def list_proposals(*, approval_status: str | None = None) -> list[Proposal]:
    latest: dict[str, dict[str, Any]] = {}
    for rec in _store.list():
        latest[str(rec.get("id"))] = rec
    proposals = [Proposal(**rec) for rec in latest.values()]
    if approval_status is not None:
        proposals = [p for p in proposals if p.approval_status == approval_status]
    return proposals


def approve_proposal(proposal_id: str) -> Proposal | None:
    rec = _store.patch(proposal_id, {"approval_status": ProposalStatus.APPROVED.value})
    return Proposal(**rec) if rec else None


def reject_proposal(proposal_id: str) -> Proposal | None:
    rec = _store.patch(proposal_id, {"approval_status": ProposalStatus.REJECTED.value})
    return Proposal(**rec) if rec else None


def clear_for_test() -> None:
    _store.clear_for_test()


__all__ = [
    "Proposal",
    "ProposalStatus",
    "approve_proposal",
    "clear_for_test",
    "generate_proposal",
    "get_proposal",
    "list_proposals",
    "reject_proposal",
]
