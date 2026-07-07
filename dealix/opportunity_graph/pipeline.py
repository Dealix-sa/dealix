"""Daily targeting pipeline + approval gate for the Opportunity Command Room.

The pipeline is draft-only end to end:

    collect -> normalize -> score -> segment -> draft -> queue -> report

Nothing in this module performs a live send. The only way a draft becomes
``sent`` is ``mark_sent`` — which requires an already-approved draft and an
explicit human sender, and merely records that a human sent it manually.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from dealix.opportunity_graph.collectors import load_seed_companies
from dealix.opportunity_graph.drafting import generate_draft_for_company
from dealix.opportunity_graph.schemas import (
    ApprovalStatus,
    OpportunityCompany,
    OutreachDraft,
)
from dealix.opportunity_graph.scoring import recommended_next_action, score_company
from dealix.opportunity_graph.segmentation import segment_company
from dealix.opportunity_graph.store import OpportunityGraphStore, get_store


def score_and_segment(company: OpportunityCompany) -> OpportunityCompany:
    fields = company.model_dump()
    scores = score_company(fields)
    company = company.model_copy(update=scores)
    company.segment = segment_company(fields)
    company.recommended_next_action = recommended_next_action(
        company.score_class, company.segment
    )
    if company.status in ("new",):
        company.status = "scored"
    company.updated_at = datetime.now(UTC)
    return company


def run_daily_targeting(
    *,
    store: OpportunityGraphStore | None = None,
    limit: int = 50,
    mode: str = "draft-only",
    draft_top: int = 20,
) -> dict[str, Any]:
    """Run one targeting cycle. Always draft-only; ``mode`` is validated.

    Returns a summary dict (also used by the daily report builder).
    """
    if mode != "draft-only":
        raise ValueError(
            f"Only draft-only mode is supported (got {mode!r}). "
            "Live send is disabled by policy."
        )
    store = store or get_store()

    companies = load_seed_companies(store)
    scored = [score_and_segment(c) for c in companies]
    scored.sort(key=lambda c: c.total_score, reverse=True)
    scored = scored[:limit] if limit else scored
    store.upsert_companies(scored)

    existing_draft_company_ids = {d.company_id for d in store.load_drafts()}
    new_drafts: list[OutreachDraft] = []
    for company in scored[: draft_top or len(scored)]:
        if company.id in existing_draft_company_ids:
            continue
        draft = generate_draft_for_company(company)
        if draft is not None:
            new_drafts.append(draft)
            company.status = "drafted"
    if new_drafts:
        store.upsert_drafts(new_drafts)
        store.upsert_companies(scored)

    drafts = store.load_drafts()
    summary = {
        "mode": mode,
        "total_companies_scored": len(scored),
        "hot": sum(1 for c in scored if c.score_class == "hot"),
        "warm": sum(1 for c in scored if c.score_class == "warm"),
        "research": sum(1 for c in scored if c.score_class == "research"),
        "not_fit": sum(1 for c in scored if c.score_class == "not_fit"),
        "new_drafts": len(new_drafts),
        "pending_approvals": sum(1 for d in drafts if d.approval_status == "pending"),
        "approved_drafts": sum(1 for d in drafts if d.approval_status == "approved"),
        "generated_at": datetime.now(UTC).isoformat(),
    }
    return summary


# ── Approval gate ──────────────────────────────────────────────────────────

_VALID_DECISIONS: dict[str, ApprovalStatus] = {
    "approve": "approved",
    "reject": "rejected",
    "revise": "revise",
}


def decide_draft(
    draft_id: str,
    decision: str,
    *,
    actor: str,
    note: str = "",
    store: OpportunityGraphStore | None = None,
) -> OutreachDraft:
    """Record an approve/reject/revise decision on a draft (audited)."""
    store = store or get_store()
    if decision not in _VALID_DECISIONS:
        raise ValueError(f"Unknown decision {decision!r}")
    if not actor.strip():
        raise ValueError("A human actor is required to decide on a draft.")

    draft = store.get_draft(draft_id)
    if draft is None:
        raise KeyError(f"Draft not found: {draft_id}")

    status = _VALID_DECISIONS[decision]
    draft = draft.model_copy(
        update={
            "approval_status": status,
            "approved_by": actor if status == "approved" else draft.approved_by,
            "approved_at": datetime.now(UTC) if status == "approved" else draft.approved_at,
            "updated_at": datetime.now(UTC),
        }
    )
    store.upsert_drafts([draft])
    store.append_approval(
        {
            "kind": "draft_decision",
            "draft_id": draft_id,
            "company_id": draft.company_id,
            "decision": decision,
            "actor": actor,
            "note": note,
        }
    )
    return draft


def mark_sent(
    draft_id: str,
    *,
    human_sender: str,
    store: OpportunityGraphStore | None = None,
) -> OutreachDraft:
    """Record that a human manually sent an APPROVED draft.

    This does NOT send anything. It only stamps ``sent_at`` / ``human_sender``
    after a human confirms they sent it via their own channel. Guard rails:
      * draft must be ``approved``
      * ``human_sender`` must be provided
    There is deliberately no automated live-send path anywhere in this package.
    """
    store = store or get_store()
    if not human_sender.strip():
        raise ValueError("human_sender is required to record a manual send.")

    draft = store.get_draft(draft_id)
    if draft is None:
        raise KeyError(f"Draft not found: {draft_id}")
    if draft.approval_status != "approved":
        raise PermissionError(
            "Draft is not approved — cannot record a send. "
            "Approve it first via the approval gate."
        )

    draft = draft.model_copy(
        update={
            "sent_at": datetime.now(UTC),
            "human_sender": human_sender,
            "updated_at": datetime.now(UTC),
        }
    )
    store.upsert_drafts([draft])
    store.append_approval(
        {
            "kind": "manual_send_recorded",
            "draft_id": draft_id,
            "company_id": draft.company_id,
            "human_sender": human_sender,
        }
    )
    return draft
