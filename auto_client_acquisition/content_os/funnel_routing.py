"""Public funnel auto-routing — qualify → offer rung → drafted proposal.

Given a deterministic ``QualificationResult`` (from ``sales_os.qualify``),
this routes the prospect to an offer-ladder rung and drafts a proposal
into the approval queue. Doctrine violations (``decision == "reject"``)
never produce a proposal. Every proposal lands ``approval_required`` —
it is never sent to the prospect automatically.
"""
from __future__ import annotations

from typing import Any

from auto_client_acquisition.approval_center.approval_store import (
    ApprovalStore,
    get_default_approval_store,
)
from auto_client_acquisition.approval_center.schemas import ApprovalRequest
from auto_client_acquisition.finance_os.pricing_catalog import get_pricing_tier
from auto_client_acquisition.sales_os.proposal_renderer import (
    ProposalContext,
    render_proposal,
)
from auto_client_acquisition.sales_os.qualification import QualificationResult

# qualify().recommended_offer → (pricing tier_id, approval action_type)
_OFFER_TO_TIER: dict[str, tuple[str, str]] = {
    "revenue_intelligence_sprint": ("growth_starter_pilot", "draft_email"),
    "data_to_revenue_diagnostic": ("data_to_revenue", "draft_email"),
    "capability_diagnostic": ("diagnostic", "prepare_diagnostic"),
}


def route_and_draft_proposal(
    qr: QualificationResult,
    *,
    lead_id: str | None,
    company: str,
    sector: str,
    email: str,
    city: str = "",
    store: ApprovalStore | None = None,
) -> dict[str, Any]:
    """Route a qualified lead to an offer and draft a proposal into the queue."""
    # Doctrine violation — never draft a proposal.
    if qr.decision == "reject":
        return {
            "status": "declined",
            "decision": qr.decision,
            "reason": qr.doctrine_violations or qr.reasons,
        }

    routing = _OFFER_TO_TIER.get(qr.recommended_offer)
    if routing is None:
        # refer_out / not-a-fit — no proposal, polite decline.
        return {
            "status": "refer_out",
            "decision": qr.decision,
            "recommended_offer": qr.recommended_offer,
        }

    tier_id, action_type = routing
    tier = get_pricing_tier(tier_id)
    engagement_id = f"funnel_{lead_id or email}"

    proposal = render_proposal(
        ProposalContext(
            customer_name=company,
            customer_handle=email,
            sector=sector or "b2b_services",
            city=city,
            engagement_id=engagement_id,
            price_sar=int(tier["price_sar"]),
        )
    )

    target = store or get_default_approval_store()
    req = target.create(
        ApprovalRequest(
            object_type="funnel_proposal",
            object_id=engagement_id,
            action_type=action_type,
            action_mode="approval_required",
            channel="email",
            summary_ar=proposal,
            summary_en=(
                f"Proposal: {tier['name_en']} ({int(tier['price_sar'])} SAR) "
                f"for {company} — review and approve before sending."
            ),
            risk_level="low",
            proof_impact=f"funnel:{tier_id}",
            lead_id=lead_id,
        )
    )
    return {
        "status": "queued",
        "decision": qr.decision,
        "offer": tier_id,
        "price_sar": tier["price_sar"],
        "approval_id": req.approval_id,
    }


__all__ = ["route_and_draft_proposal"]
