"""خادم المال — ProposalFactory (spec §41 quality gate).

Produces a `ProposalDraft` carrying the nine required §41 fields:

    1. Buyer            — who the proposal is for
    2. Pain             — pain we are solving
    3. Deliverables     — what we ship
    4. Price            — Money, transparent
    5. Timeline         — milestones in plain text
    6. Exclusions       — explicit out-of-scope items
    7. Risks            — known risks / mitigations
    8. Trust status     — guardrail verdict + Sami sovereignty level
    9. Approval status  — whether human approval is still required

Every draft is run through `GuardrailChain.run_all()` and the results
are embedded so callers can decide whether to escalate or auto-send.
"""

from __future__ import annotations

from decimal import Decimal
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator

from dealix.hermes.core.opportunities import Opportunity
from dealix.hermes.core.schemas import Money
from dealix.hermes.sovereignty import Sovereignty, SovereigntyLevel
from dealix.money.offer_matcher import Offer
from dealix.money.pricing import PricingEngine
from dealix.trust.guardrails import GuardrailChain, GuardrailResult


class ProposalDraft(BaseModel):
    """A draft proposal carrying the nine §41 quality-gate fields."""

    model_config = ConfigDict(extra="forbid")

    buyer: str = Field(..., min_length=1, max_length=160)
    pain: str = Field(..., min_length=1, max_length=600)
    deliverables: list[str] = Field(..., min_length=1, max_length=20)
    price: Money
    timeline: list[str] = Field(..., min_length=1, max_length=20)
    exclusions: list[str] = Field(default_factory=list, max_length=20)
    risks: list[str] = Field(default_factory=list, max_length=20)
    trust_status: str = Field(..., min_length=1, max_length=240)
    approval_status: str = Field(..., min_length=1, max_length=120)

    offer_name: str = Field(..., min_length=1, max_length=120)
    customer_meta: dict[str, str] = Field(default_factory=dict)
    sovereignty_level: SovereigntyLevel = SovereigntyLevel.S0_AUTONOMOUS
    requires_approval: bool = True
    guardrail_results: list[dict[str, Any]] = Field(default_factory=list)
    guardrails_passed: bool = True

    @field_validator("deliverables", "timeline", "exclusions", "risks")
    @classmethod
    def _strip_and_dedupe(cls, value: list[str]) -> list[str]:
        seen: set[str] = set()
        out: list[str] = []
        for item in value:
            cleaned = item.strip()
            if not cleaned or cleaned in seen:
                continue
            seen.add(cleaned)
            out.append(cleaned)
        return out


# ─────────────────────────────────────────────────────────────
# Factory
# ─────────────────────────────────────────────────────────────


class ProposalFactory:
    """Render a `ProposalDraft` from (opportunity, offer, customer meta)."""

    def __init__(
        self,
        pricing_engine: PricingEngine | None = None,
        guardrail_chain: GuardrailChain | None = None,
    ) -> None:
        self._pricing = pricing_engine or PricingEngine()
        self._guards = guardrail_chain or GuardrailChain()

    def render(
        self,
        opportunity: Opportunity,
        offer: Offer,
        customer_meta: dict[str, str] | None = None,
    ) -> ProposalDraft:
        meta = dict(customer_meta or {})
        buyer = meta.get("buyer") or offer.buyer
        price = self._pricing.quote(offer, opportunity)
        deliverables = _split_lines(offer.deliverable)
        timeline = self._timeline_for(offer)
        exclusions = self._exclusions_for(offer)
        risks = self._risks_for(opportunity)

        verdict = Sovereignty.evaluate(
            risk_level="medium" if opportunity.sensitive else "low",
            sensitivity="commercial",
            monetary_amount=price,
            external_visibility=True,
            entity_type="customer",
            flags={
                "strategic_partnership": offer.name == "Agency White-label Kit",
            },
        )
        requires_approval = verdict.level.numeric >= SovereigntyLevel.S1_NOTIFY_SAMI.numeric

        payload = {
            "title": offer.name,
            "body": offer.deliverable,
            "summary": offer.pain,
            "rationale": opportunity.narrative,
            "fields": {
                "buyer": buyer,
                "pain": offer.pain,
                "success_metric": offer.success_metric,
                "customer": meta.get("name", ""),
            },
            "approval_ref": meta.get("approval_ref"),
            "evidence_refs": meta.get("evidence_ref"),
        }
        results = self._guards.run_all(payload)
        passed = GuardrailChain.passed(results)

        trust_status = (
            f"sovereignty={verdict.level.value}; "
            f"guardrails={'PASS' if passed else 'BLOCK'}; "
            f"requires_evidence_pack={verdict.requires_evidence_pack}"
        )
        approval_status = (
            "approved" if not requires_approval else "pending_sami_review"
        )

        return ProposalDraft(
            buyer=buyer,
            pain=offer.pain,
            deliverables=deliverables,
            price=price,
            timeline=timeline,
            exclusions=exclusions,
            risks=risks,
            trust_status=trust_status,
            approval_status=approval_status,
            offer_name=offer.name,
            customer_meta=meta,
            sovereignty_level=verdict.level,
            requires_approval=requires_approval,
            guardrail_results=[r.to_dict() for r in results],
            guardrails_passed=passed,
        )

    @staticmethod
    def _timeline_for(offer: Offer) -> list[str]:
        if "pilot" in offer.name.lower():
            return [
                "Week 1: discovery + ICP baseline",
                "Week 2-3: first batch of qualified leads + proposal drafts",
                "Week 4: Friday revenue review + scope plan",
            ]
        if "sprint" in offer.name.lower():
            return [
                "Day 1-5: vertical card + ICP profile",
                "Day 6-10: pilot playbook + ProofPack draft",
                "Day 11-14: target list + outreach kickoff",
            ]
        if "trust" in offer.name.lower():
            return [
                "Week 1: policy + guardrail audit",
                "Week 2: evidence-pack wiring + MCP allowlist review",
                "Week 3: incident playbook + sign-off",
            ]
        if "renewal" in offer.name.lower():
            return [
                "Week 1: health audit",
                "Week 2: renewal brief + upsell shortlist",
            ]
        return [
            "Phase 1: kickoff + scope confirmation",
            "Phase 2: delivery",
            "Phase 3: review + handover",
        ]

    @staticmethod
    def _exclusions_for(offer: Offer) -> list[str]:
        base = [
            "Outbound on forbidden channels (cold WhatsApp / LinkedIn automation)",
            "Direct charging of customer payment methods",
            "Public press releases without Sami sign-off",
        ]
        if "white-label" in offer.name.lower():
            base.append("Resale of unreleased agents")
        return base

    @staticmethod
    def _risks_for(opportunity: Opportunity) -> list[str]:
        risks = ["Decision cycle slips beyond the proposal validity window"]
        if opportunity.sensitive:
            risks.append("Sensitive data — requires PDPL-compliant handling")
        if opportunity.urgency <= 2:
            risks.append("Low urgency — buyer may park the conversation")
        return risks


def _split_lines(text: str) -> list[str]:
    candidates: list[str] = []
    for chunk in text.replace("\n", ";").split(";"):
        for line in chunk.split(","):
            cleaned = line.strip(" .;")
            if cleaned:
                candidates.append(cleaned)
    if not candidates:
        candidates.append(text.strip())
    return candidates


__all__ = [
    "ProposalDraft",
    "ProposalFactory",
]
