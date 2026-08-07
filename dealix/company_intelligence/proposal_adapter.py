"""Fail-closed adapter from distribution-OS Proposal to canonical Proposal.

Bridges ``auto_client_acquisition.distribution_os.proposal.Proposal``
into ``CanonicalProposal`` without escalating authority. The operational
proposal carries prospect context, catalog-linked pricing, and an
approval status; this adapter normalises it into the tenant-scoped,
version-tracked, approval-gated shape the Company Intelligence
commercial spine expects.

Key constraints:
  - Approval status maps to canonical ProposalStatus via an explicit
    mapping; unknown statuses fail-closed to DRAFT.
  - The adapter never marks a proposal as SENT — that requires a
    separate controlled-execution step with founder approval.
  - Evidence level (int) normalised to confidence (0–1) by clamping to
    [0, 100] and dividing by 100.
  - Content summary is composed from problem, proposed_solution, scope,
    out_of_scope, and timeline — never from external-action outputs.
  - Pricing note is assembled from the catalog price band, never
    invented.
"""
from __future__ import annotations

from typing import Any

from dealix.company_intelligence.proposal_contracts import (
    CanonicalProposal,
    ProposalStatus,
    build_proposal,
)

# ---------------------------------------------------------------------------
# Approval status mapping
# ---------------------------------------------------------------------------

_STATUS_MAP: dict[str, ProposalStatus] = {
    "pending_approval": ProposalStatus.PENDING_REVIEW,
    "approved": ProposalStatus.APPROVED,
    "rejected": ProposalStatus.REJECTED,
    # "sent" → APPROVED: the adapter never escalates to SENT because
    # sending requires controlled execution with sent_at evidence.
    # The operational "sent" status is acknowledged as APPROVED.
    "sent": ProposalStatus.APPROVED,
    # Canonical ProposalStatus values accepted directly
    "draft": ProposalStatus.DRAFT,
    "pending_review": ProposalStatus.PENDING_REVIEW,
    "accepted": ProposalStatus.ACCEPTED,
    "expired": ProposalStatus.EXPIRED,
    "withdrawn": ProposalStatus.WITHDRAWN,
}


def _resolve_status(raw: str) -> ProposalStatus:
    """Map an operational approval status to a canonical ProposalStatus.

    Unknown statuses fail-closed to ``DRAFT`` — never to SENT or beyond.
    """
    return _STATUS_MAP.get(raw.lower().strip(), ProposalStatus.DRAFT)


def _clamp(value: float, low: float = 0.0, high: float = 1.0) -> float:
    return max(low, min(high, value))


def _compose_content_summary(proposal: Any) -> str:
    """Build a content summary from proposal narrative fields.

    Only internal-facing fields are included — no external-action outputs.
    """
    parts: list[str] = []

    problem = str(getattr(proposal, "problem", "") or "").strip()
    if problem:
        parts.append(f"Problem: {problem}")

    solution = str(getattr(proposal, "proposed_solution", "") or "").strip()
    if solution:
        parts.append(f"Solution: {solution}")

    scope = list(getattr(proposal, "scope", []) or [])
    if scope:
        parts.append(f"Scope: {', '.join(str(s) for s in scope)}")

    out_of_scope = list(getattr(proposal, "out_of_scope", []) or [])
    if out_of_scope:
        parts.append(f"Exclusions: {', '.join(str(s) for s in out_of_scope)}")

    timeline = str(getattr(proposal, "timeline", "") or "").strip()
    if timeline:
        parts.append(f"Timeline: {timeline}")

    next_step = str(getattr(proposal, "next_step", "") or "").strip()
    if next_step:
        parts.append(f"Next step: {next_step}")

    return " | ".join(parts)


def _compose_pricing_note(proposal: Any) -> str:
    """Build a pricing note from the catalog-linked price band."""
    price_min = int(getattr(proposal, "price_min_sar", 0) or 0)
    price_max = int(getattr(proposal, "price_max_sar", 0) or 0)
    payment_terms = str(getattr(proposal, "payment_terms", "") or "").strip()

    parts: list[str] = []
    if price_min > 0 or price_max > 0:
        if price_min == price_max:
            parts.append(f"{price_min} SAR")
        else:
            parts.append(f"{price_min}–{price_max} SAR")

    if payment_terms:
        parts.append(f"Terms: {payment_terms}")

    return " | ".join(parts)


def normalize_proposal(
    proposal: Any,
    *,
    tenant_id: str,
    opportunity_id: str,
    approval_id: str,
    source_id: str = "distribution_os",
    version: int = 1,
) -> CanonicalProposal:
    """Normalize a distribution-OS ``Proposal`` into a ``CanonicalProposal``.

    Parameters
    ----------
    proposal:
        A ``Proposal`` or any duck-typed object with ``product_id``,
        ``prospect_id``, ``problem``, ``proposed_solution``, ``scope``,
        ``out_of_scope``, ``timeline``, ``price_min_sar``, ``price_max_sar``,
        ``evidence_level``, ``approval_status``, and optionally
        ``quality_issues``, ``payment_terms``, ``next_step``.
    tenant_id:
        The tenant scope for the resulting canonical proposal.
    opportunity_id:
        The canonical opportunity this proposal belongs to.
    approval_id:
        The approval record governing this proposal.
    source_id:
        Source identity for provenance tracking (default: "distribution_os").
    version:
        Proposal version number (default: 1).
    """
    # Required fields
    product_id = str(getattr(proposal, "product_id", "") or "").strip()
    if not product_id:
        raise ValueError("proposal must have a non-empty product_id")

    prospect_id = str(getattr(proposal, "prospect_id", "") or "").strip()

    # Status mapping — fail-closed to DRAFT
    raw_status = str(getattr(proposal, "approval_status", "draft") or "draft")
    status = _resolve_status(raw_status)

    # The adapter never escalates to SENT without explicit controlled-execution
    # Only map to SENT if the operational status is explicitly "sent"
    # (already handled in _resolve_status, but guard against future mapping drift)

    # Evidence level → confidence (normalize int to 0–1 float)
    raw_evidence = getattr(proposal, "evidence_level", 0)
    evidence_level = int(raw_evidence if raw_evidence is not None else 0)
    confidence = _clamp(evidence_level / 100.0)

    # Content summary and pricing note
    content_summary = _compose_content_summary(proposal)
    pricing_note = _compose_pricing_note(proposal)

    # Quality issues as evidence trail
    quality_issues = list(getattr(proposal, "quality_issues", []) or [])
    evidence_refs = tuple(f"quality:{q}" for q in quality_issues if q)

    # Risks as additional evidence trail
    risks = list(getattr(proposal, "risks", []) or [])
    risk_refs = tuple(f"risk:{r}" for r in risks if r)
    evidence_refs = evidence_refs + risk_refs

    return build_proposal(
        tenant_id=tenant_id,
        opportunity_id=opportunity_id,
        offer_id=product_id,
        approval_id=approval_id,
        source_id=source_id,
        company_id=prospect_id,
        version=version,
        status=status,
        content_summary=content_summary,
        pricing_note=pricing_note,
        confidence=confidence,
        evidence_refs=evidence_refs,
    )
