"""Distribution Metrics — daily + weekly KPI snapshot across the OS stores.

Read-only aggregation. Numbers come only from the JSONL stores (never
invented). Used by ``scripts/distribution_metrics.py`` and the distribution
API overview.
"""

from __future__ import annotations

from typing import Any

from auto_client_acquisition.distribution_os import (
    draft_factory,
    followup,
    payment_handoff,
    proof_pack,
    proposal,
    prospect,
    win_loss,
)
from auto_client_acquisition.distribution_os.draft_factory import DraftStatus
from auto_client_acquisition.distribution_os.prospect import ProspectStatus


def daily_kpis() -> dict[str, int]:
    """The daily KPI counters (plan section 14)."""
    prospects = prospect.list_prospects()
    drafts = draft_factory.list_drafts()
    proposals = proposal.list_proposals()
    packs = proof_pack.list_proof_packs()
    handoffs = payment_handoff.list_handoffs()
    wl = win_loss.list_entries()
    due = followup.due_followups()

    def _count(items: list[Any], attr: str, value: str) -> int:
        return sum(1 for i in items if getattr(i, attr) == value)

    return {
        "prospects_total": len(prospects),
        "prospects_qualified": _count(prospects, "status", ProspectStatus.QUALIFIED.value),
        "drafts_generated": len(drafts),
        "drafts_pending_approval": _count(drafts, "status", DraftStatus.PENDING_APPROVAL.value),
        "drafts_approved": _count(drafts, "status", DraftStatus.APPROVED.value),
        "drafts_needs_edit": _count(drafts, "status", DraftStatus.NEEDS_EDIT.value),
        "drafts_blocked": sum(1 for d in drafts if d.governance_status == "blocked"),
        "drafts_copied_manually": _count(drafts, "status", DraftStatus.COPIED_MANUALLY.value),
        "followups_due": len(due),
        "proposals_generated": len(proposals),
        "proposals_approved": _count(proposals, "approval_status", "approved"),
        "proof_packs_generated": len(packs),
        "payment_handoffs": len(handoffs),
        "payment_handoffs_approved": _count(handoffs, "status", "approved"),
        "won_deals": sum(1 for e in wl if e.outcome == "won"),
        "lost_deals": sum(1 for e in wl if e.outcome == "lost"),
    }


def weekly_kpis() -> dict[str, Any]:
    """Weekly rollups — rates + learning signals (plan section 14)."""
    daily = daily_kpis()
    wl_summary = win_loss.summarize()
    drafts = draft_factory.list_drafts()
    decided_drafts = [d for d in drafts if d.status in {"approved", "rejected"}]
    approval_rate = (
        round(sum(1 for d in decided_drafts if d.status == "approved") / len(decided_drafts), 3)
        if decided_drafts
        else 0.0
    )
    proposals = proposal.list_proposals()
    close_rate = wl_summary.get("win_rate", 0.0)
    return {
        "approval_rate": approval_rate,
        "proposal_count": len(proposals),
        "close_rate": close_rate,
        "best_sector": wl_summary.get("best_sector", ""),
        "top_objection": wl_summary.get("top_objection", ""),
        "won_deals": daily["won_deals"],
        "lost_deals": daily["lost_deals"],
    }


def snapshot() -> dict[str, Any]:
    """Combined daily + weekly snapshot for the founder cockpit / API."""
    return {"daily": daily_kpis(), "weekly": weekly_kpis()}


__all__ = ["daily_kpis", "snapshot", "weekly_kpis"]
