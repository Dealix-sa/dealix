"""Proposal Factory — generate proposal *briefs*, never binding offers.

Every brief carries a pricing *range* (drawn from approved guardrails), an
explicit out-of-scope list, acceptance criteria, ``final_price_allowed=False``
and ``approval_required=True``. Finalising a binding price is A3-restricted and
handled only via :func:`app.commercial.safety.can_finalize_proposal`.
"""

from __future__ import annotations

from typing import Any, Mapping

from app.commercial.schemas import ProposalBrief

# Approved pricing ranges (SAR). These are *ranges for conversation*, not
# committed prices. Overridable via data/commercial/pricing_guardrails.sample.json.
DEFAULT_PRICING_GUARDRAILS: dict[str, dict[str, Any]] = {
    "growth_card_sprint": {
        "package_name": "7-Day Growth Card Sprint",
        "range_sar": "5,000–12,000",
        "timeline": "7 days",
        "deliverables": [
            "25–50 qualified Growth Cards",
            "10–20 bilingual outreach drafts (draft-only)",
            "5 proposal briefs",
            "Booking option sets",
            "Command-room proof report",
        ],
    },
    "commercial_os_sprint": {
        "package_name": "14-Day Commercial OS Sprint",
        "range_sar": "15,000–35,000",
        "timeline": "14 days",
        "deliverables": [
            "Full lead → pipeline workflow",
            "Smart Reply desk",
            "Negotiation guardrails",
            "Proposal Factory",
            "Command room",
        ],
    },
    "managed_growth_os": {
        "package_name": "Managed Growth OS (monthly)",
        "range_sar": "5,000–25,000 / month",
        "timeline": "Monthly, weekly operation",
        "deliverables": [
            "Weekly operation & follow-up",
            "Proposal review",
            "Pipeline updates",
            "Growth reporting",
        ],
    },
}

# Motion → default package.
_MOTION_PACKAGE = {
    "sales_prospecting": "growth_card_sprint",
    "proposal_push": "commercial_os_sprint",
    "partnership_outreach": "commercial_os_sprint",
    "upsell": "managed_growth_os",
    "renewal": "managed_growth_os",
    "retention": "managed_growth_os",
    "customer_success_expansion": "managed_growth_os",
}

_STANDARD_OUT_OF_SCOPE = [
    "Cold WhatsApp / unconsented messaging",
    "Guaranteed revenue or ROI commitments",
    "Final pricing, discounts or contract terms without founder approval",
    "Sending any external message without explicit approval",
    "Scraping prohibited or restricted sources",
]


def build_proposal_brief(
    card_id: str,
    motion: str = "sales_prospecting",
    proposal_index: int = 0,
    pricing_guardrails: Mapping[str, Any] | None = None,
) -> ProposalBrief:
    guardrails = {**DEFAULT_PRICING_GUARDRAILS, **(pricing_guardrails or {})}
    package_key = _MOTION_PACKAGE.get(motion, "growth_card_sprint")
    pkg = guardrails.get(package_key, DEFAULT_PRICING_GUARDRAILS["growth_card_sprint"])

    return ProposalBrief(
        proposal_id=f"prop_{card_id}_{proposal_index:03d}",
        card_id=card_id,
        package_name=pkg["package_name"],
        scope=[
            "Discovery & ICP confirmation",
            "Account qualification & sourcing review",
            "Draft outreach + reply/negotiation desk",
            "Booking options + command-room reporting",
        ],
        deliverables=list(pkg["deliverables"]),
        timeline=pkg["timeline"],
        pricing_range_sar=pkg["range_sar"],
        out_of_scope=list(_STANDARD_OUT_OF_SCOPE),
        acceptance_criteria=[
            "Agreed scope document signed off (founder approval)",
            "Client provides data & source access per kickoff checklist",
            "Success metrics defined before kickoff",
        ],
        final_price_allowed=False,
        approval_required=True,
        status="draft",
    )


def build_proposal_briefs(
    cards: list[Any],
    pricing_guardrails: Mapping[str, Any] | None = None,
    limit: int | None = None,
) -> list[ProposalBrief]:
    out: list[ProposalBrief] = []
    for i, card in enumerate(cards):
        if limit is not None and i >= limit:
            break
        motion = _get(card, "motion") or "sales_prospecting"
        card_id = _get(card, "card_id") or f"card_{i}"
        out.append(build_proposal_brief(card_id, motion, i, pricing_guardrails))
    return out


def _get(obj: Any, key: str) -> Any:
    if isinstance(obj, Mapping):
        return obj.get(key)
    return getattr(obj, key, None)
