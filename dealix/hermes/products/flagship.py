"""Flagship product definitions (section 138).

Three productized offers the kernel ships out of the box:

1. Revenue Hunter Pilot
2. AI Trust Kit
3. Agency White-label Kit

Each is exported as a ready-to-register Offer + Capability descriptor.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class FlagshipOffer:
    name: str
    buyer: str
    pain: str
    promise: str
    deliverables: tuple[str, ...]
    price_sar: float
    timeline_weeks: int
    metric: str
    upsell: str
    trust_risks: tuple[str, ...]
    capabilities: tuple[str, ...]


REVENUE_HUNTER_PILOT = FlagshipOffer(
    name="Revenue Hunter Pilot",
    buyer="B2B founder / VP Sales (SAR 5M–200M revenue)",
    pain="No predictable pipeline; sales relies on personal network.",
    promise="30 qualified leads + 10 messages + 3 proposals + follow-up plan in 14 days.",
    deliverables=(
        "30 verified target accounts",
        "10 personalized outreach messages",
        "3 proposal drafts",
        "Follow-up plan",
        "Opportunity report",
    ),
    price_sar=14_900.0,
    timeline_weeks=2,
    metric="qualified meetings booked within 30 days",
    upsell="Monthly Managed Ops",
    trust_risks=("external send", "scraping risk", "PDPL data scope"),
    capabilities=("money.revenue_hunter", "money.proposal_factory", "core.outcome_logger"),
)

AI_TRUST_KIT = FlagshipOffer(
    name="AI Trust Kit",
    buyer="CIO / CISO / Head of Risk at mid-market Saudi firm",
    pain="Teams use AI without policy; risk of leaks, hallucinated decisions, tool sprawl.",
    promise="Live trust layer: registries, approvals, evidence packs, audit logs in 4 weeks.",
    deliverables=(
        "AI use policy",
        "Agent registry template",
        "Tool permission matrix",
        "Approval workflow",
        "Risk register",
        "Evidence pack template",
    ),
    price_sar=49_000.0,
    timeline_weeks=4,
    metric="Trust audit pass rate ≥95%",
    upsell="Governance OS retainer",
    trust_risks=("data scope", "PDPL alignment", "MCP server review"),
    capabilities=("trust.agent_registry", "trust.tool_registry", "trust.evidence", "trust.audit"),
)

AGENCY_WHITE_LABEL_KIT = FlagshipOffer(
    name="Agency White-label Kit",
    buyer="Boutique agency owner (10–50 clients)",
    pain="No AI-powered revenue service to sell; cannot deliver consistently.",
    promise="White-label revenue service: lead packs + proposal packs + client reports.",
    deliverables=(
        "White-label offer pack",
        "Client report templates",
        "Lead packs (weekly)",
        "Proposal packs (per client)",
        "Revenue share model",
    ),
    price_sar=29_000.0,
    timeline_weeks=3,
    metric="agency-attributed revenue per month",
    upsell="Annual partner retainer",
    trust_risks=("brand misuse", "data scope leakage between clients"),
    capabilities=("partners.scout", "partners.revenue_share", "money.proposal_factory"),
)


FLAGSHIP_OFFERS: tuple[FlagshipOffer, ...] = (
    REVENUE_HUNTER_PILOT,
    AI_TRUST_KIT,
    AGENCY_WHITE_LABEL_KIT,
)


__all__ = [
    "AGENCY_WHITE_LABEL_KIT",
    "AI_TRUST_KIT",
    "FLAGSHIP_OFFERS",
    "FlagshipOffer",
    "REVENUE_HUNTER_PILOT",
]
