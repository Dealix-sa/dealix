"""
Proposal Generator Agent

Builds a complete, governed commercial proposal for a Saudi prospect.
Combines ICP scoring, pricing, evidence, and delivery plan into one document.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from intelligence.pricing_engine import PricingEngine, PricingRecommendation
from intelligence.saudi_market_intelligence import SaudiCompanyProfile, SaudiMarketIntelligence


@dataclass
class ProposalSection:
    title: str
    body: str


@dataclass
class GeneratedProposal:
    proposal_id: str
    prospect_name: str
    package: str
    tier: str
    price_sar: float
    sections: list[ProposalSection]
    evidence_cited: list[str]
    next_steps: list[str]
    terms: str
    generated_at: str


class ProposalGeneratorAgent:
    """Generates structured commercial proposals for Saudi B2B prospects."""

    def __init__(self):
        self.market_intel = SaudiMarketIntelligence()
        self.pricing = PricingEngine()

    def generate(
        self,
        prospect: SaudiCompanyProfile,
        package: str,
        evidence_items: list[dict[str, Any]] | None = None,
    ) -> GeneratedProposal:
        """Generate a full proposal for a prospect and package."""
        icp = self.market_intel.score_icp(prospect)
        entry = self.market_intel.recommend_entry(prospect.sector, prospect.city)
        price = self.pricing.recommend(
            package=package,
            sector=prospect.sector,
            employees=prospect.employees_estimate or 50,
        )

        proposal_id = f"prop-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
        evidence_cited = [e.get("title", "Dealix track record") for e in (evidence_items or [])]
        if not evidence_cited:
            evidence_cited = ["Saudi B2B sector benchmarks", "PDPL-aware delivery methodology"]

        sections = [
            ProposalSection(
                title="Executive Summary",
                body=(
                    f"{prospect.company_name} is a {icp.score:.0f}/100 fit for Dealix {package}. "
                    f"We recommend the {price.tier.value} tier at SAR {price.adjusted_price_sar:,.0f} "
                    f"to deliver {price.value_anchor.lower()}."
                ),
            ),
            ProposalSection(
                title="Understanding Your Situation",
                body=(
                    f"As a {prospect.sector} company based in {prospect.city} "
                    f"with approximately {prospect.employees_estimate or 'unknown'} employees, "
                    f"you face the common Saudi B2B challenge of turning intent into repeatable revenue. "
                    f"Market momentum for {prospect.sector} is {entry['momentum']}."
                ),
            ),
            ProposalSection(
                title="Recommended Solution",
                body=(
                    f"Dealix {package} — {price.tier.value} tier. "
                    f"This includes Saudi lead intelligence, AI-assisted execution, "
                    f"and approval-first governance tailored to your sector."
                ),
            ),
            ProposalSection(
                title="Investment & ROI",
                body=(
                    f"Investment: SAR {price.adjusted_price_sar:,.0f}. "
                    f"Payment terms: {price.payment_terms}. "
                    f"Estimated first-year ROI: {price.roi_estimate_percent:.0f}%."
                ),
            ),
            ProposalSection(
                title="Why Dealix",
                body=(
                    "Saudi-first AI Business Operating System. PDPL-native. Approval-first. "
                    "Every recommendation tied to evidence; every external commitment gated by human approval."
                ),
            ),
        ]

        return GeneratedProposal(
            proposal_id=proposal_id,
            prospect_name=prospect.company_name,
            package=package,
            tier=price.tier.value,
            price_sar=price.adjusted_price_sar,
            sections=sections,
            evidence_cited=evidence_cited,
            next_steps=[
                "Schedule proposal review call within 48 hours",
                "Confirm scope and kickoff date",
                "Sign SOW and process kickoff payment",
            ],
            terms="Net 15. Work begins after kickoff payment and signed SOW.",
            generated_at=datetime.utcnow().isoformat(),
        )

    def to_markdown(self, proposal: GeneratedProposal) -> str:
        """Render proposal as markdown."""
        lines = [
            f"# Commercial Proposal: {proposal.prospect_name}",
            "",
            f"**Package:** {proposal.package} ({proposal.tier})  ",
            f"**Investment:** SAR {proposal.price_sar:,.0f}  ",
            f"**Proposal ID:** {proposal.proposal_id}  ",
            f"**Generated:** {proposal.generated_at}",
            "",
        ]
        for section in proposal.sections:
            lines.extend([f"## {section.title}", "", section.body, ""])

        lines.extend([
            "## Evidence Cited",
            "",
        ])
        for e in proposal.evidence_cited:
            lines.append(f"- {e}")

        lines.extend(["", "## Next Steps", ""])
        for step in proposal.next_steps:
            lines.append(f"1. {step}")

        lines.extend(["", "## Terms", "", proposal.terms, ""])
        return "\n".join(lines)

    def to_dict(self, proposal: GeneratedProposal) -> dict[str, Any]:
        return {
            "proposal_id": proposal.proposal_id,
            "prospect_name": proposal.prospect_name,
            "package": proposal.package,
            "tier": proposal.tier,
            "price_sar": proposal.price_sar,
            "sections": [{"title": s.title, "body": s.body} for s in proposal.sections],
            "evidence_cited": proposal.evidence_cited,
            "next_steps": proposal.next_steps,
            "terms": proposal.terms,
            "generated_at": proposal.generated_at,
        }
