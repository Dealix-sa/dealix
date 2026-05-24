"""خادم المال — Offer catalog + Opportunity → Offer matcher (spec §43).

The seeded catalog mirrors spec §43's five paid offers:

  1. Revenue Hunter Pilot      → SME founder facing flat pipeline
  2. AI Trust Kit              → CTO worried about agent risk
  3. Agency White-label Kit    → Agency owner who needs a moat
  4. Vertical Launch Sprint    → Operator launching into a new sector
  5. Renewal & Upsell Pack     → Existing customer at renewal time

Each Offer carries the §41 quality-gate fields (Buyer / Pain /
Deliverable / Price / Success metric). The matcher is deterministic:
it inspects the opportunity's narrative + type and ranks offers by a
small heuristic score.
"""

from __future__ import annotations

from decimal import Decimal
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, model_validator

from dealix.hermes.core.opportunities import Opportunity, OpportunityType
from dealix.hermes.core.schemas import Money


class Offer(BaseModel):
    """A paid offer in Dealix's catalog (spec §41/§43 shape)."""

    model_config = ConfigDict(extra="forbid")

    name: str = Field(..., min_length=1, max_length=120)
    buyer: str = Field(..., min_length=1, max_length=120)
    pain: str = Field(..., min_length=1, max_length=600)
    deliverable: str = Field(..., min_length=1, max_length=600)
    price_band: tuple[Money, Money] = Field(...)
    success_metric: str = Field(..., min_length=1, max_length=300)
    keywords: tuple[str, ...] = Field(default_factory=tuple)
    opportunity_types: tuple[OpportunityType, ...] = Field(default_factory=tuple)

    @model_validator(mode="after")
    def _price_band_ordered(self) -> Offer:
        low, high = self.price_band
        if low.currency != high.currency:
            raise ValueError("price_band currencies must match")
        if low.amount > high.amount:
            raise ValueError("price_band low must be <= high")
        return self


# ─────────────────────────────────────────────────────────────
# Seed catalog — five canonical offers from spec §43
# ─────────────────────────────────────────────────────────────


SEED_OFFERS: tuple[Offer, ...] = (
    Offer(
        name="Revenue Hunter Pilot",
        buyer="SME founder",
        pain="Flat pipeline, manual outreach, no commercial rhythm",
        deliverable=(
            "30-day pilot: weekly hand-picked leads, proposal drafts, "
            "and a Friday revenue review with friction-log feedback."
        ),
        price_band=(Money.sar(Decimal("4500")), Money.sar(Decimal("9000"))),
        success_metric="At least 3 qualified meetings booked in 30 days",
        keywords=("pipeline", "lead", "outreach", "meeting", "founder", "sales"),
        opportunity_types=(OpportunityType.REVENUE,),
    ),
    Offer(
        name="AI Trust Kit",
        buyer="CTO / Head of AI",
        pain="Agents acting without governance, audit gaps, regulator pressure",
        deliverable=(
            "Trust pack: policy templates, guardrail bundle, evidence-pack "
            "wiring, incident-response playbook, MCP allowlist review."
        ),
        price_band=(Money.sar(Decimal("12000")), Money.sar(Decimal("24000"))),
        success_metric="Zero unreviewed agent action / 100 outbound steps",
        keywords=("governance", "trust", "guardrail", "compliance", "audit",
                  "regulator", "mcp", "agent"),
        opportunity_types=(
            OpportunityType.RISK_AVOIDANCE,
            OpportunityType.PRODUCT,
        ),
    ),
    Offer(
        name="Agency White-label Kit",
        buyer="Agency owner",
        pain="Want to resell Dealix capability under their brand",
        deliverable=(
            "White-label workspace, partner-portal access, branded "
            "proposal templates, tier-based revenue share."
        ),
        price_band=(Money.sar(Decimal("9000")), Money.sar(Decimal("18000"))),
        success_metric="At least 2 partner-sourced deals in first 60 days",
        keywords=("agency", "white-label", "reseller", "partner",
                  "branded", "wholesale"),
        opportunity_types=(OpportunityType.PARTNER,),
    ),
    Offer(
        name="Vertical Launch Sprint",
        buyer="Operator launching into a new sector",
        pain="Need quick category fit and a defensible offer for a new vertical",
        deliverable=(
            "2-week sprint: vertical card, ICP profile, pilot playbook, "
            "seeded ProofPack, 5 hand-curated target accounts."
        ),
        price_band=(Money.sar(Decimal("7500")), Money.sar(Decimal("15000"))),
        success_metric="Signed pilot with one target account in 21 days",
        keywords=("vertical", "sector", "launch", "category", "clinic",
                  "broker", "retail", "saas", "manufacturer"),
        opportunity_types=(OpportunityType.PRODUCT, OpportunityType.REVENUE),
    ),
    Offer(
        name="Renewal & Upsell Pack",
        buyer="Existing customer at renewal time",
        pain="Drifting from expected outcomes; renewal soft, upsell unclear",
        deliverable=(
            "Health audit, renewal brief, upsell shortlist, monthly value "
            "report and a one-page board summary."
        ),
        price_band=(Money.sar(Decimal("3500")), Money.sar(Decimal("8000"))),
        success_metric="Renewal closed on time + 1 documented upsell",
        keywords=("renewal", "upsell", "retainer", "subscription",
                  "expansion", "monthly"),
        opportunity_types=(OpportunityType.REVENUE, OpportunityType.KNOWLEDGE),
    ),
)


# ─────────────────────────────────────────────────────────────
# Matcher
# ─────────────────────────────────────────────────────────────


class OfferMatcher:
    """Heuristic match of a domain opportunity to the best paid offer."""

    def __init__(self, catalog: tuple[Offer, ...] | None = None) -> None:
        if catalog is None:
            catalog = SEED_OFFERS
        if not catalog:
            raise ValueError("OfferMatcher catalog must not be empty")
        self._catalog: tuple[Offer, ...] = tuple(catalog)

    @property
    def catalog(self) -> tuple[Offer, ...]:
        return self._catalog

    def match(self, opportunity: Opportunity) -> Offer:
        """Return the best-fitting Offer for the opportunity (never None)."""
        scored = [
            (self._score(opportunity, offer), offer) for offer in self._catalog
        ]
        # Prefer higher score; break ties by lower price-band midpoint to
        # favour the cheapest workable pilot.
        scored.sort(key=lambda pair: (-pair[0], _midpoint(pair[1])))
        return scored[0][1]

    def rank(self, opportunity: Opportunity) -> list[tuple[float, Offer]]:
        scored = [
            (self._score(opportunity, offer), offer) for offer in self._catalog
        ]
        scored.sort(key=lambda pair: (-pair[0], _midpoint(pair[1])))
        return scored

    @staticmethod
    def _score(opportunity: Opportunity, offer: Offer) -> float:
        score = 0.0
        if opportunity.opp_type in offer.opportunity_types:
            score += 2.0
        narrative = f"{opportunity.title} {opportunity.narrative}".lower()
        for kw in offer.keywords:
            if kw in narrative:
                score += 0.5
        if opportunity.repeatable and offer.name == "Renewal & Upsell Pack":
            score += 1.0
        if opportunity.sensitive and offer.name == "AI Trust Kit":
            score += 1.0
        if opportunity.expected_value is not None:
            low, high = offer.price_band
            amount = opportunity.expected_value.amount
            if low.amount <= amount <= high.amount:
                score += 1.0
        return score


def _midpoint(offer: Offer) -> Decimal:
    low, high = offer.price_band
    return (low.amount + high.amount) / Decimal("2")


__all__ = [
    "Offer",
    "OfferMatcher",
    "SEED_OFFERS",
]


def offer_to_dict(offer: Offer) -> dict[str, Any]:
    """Serialisable view of an Offer (price band rendered as strings)."""
    return {
        "name": offer.name,
        "buyer": offer.buyer,
        "pain": offer.pain,
        "deliverable": offer.deliverable,
        "price_band_low_sar": str(offer.price_band[0].amount),
        "price_band_high_sar": str(offer.price_band[1].amount),
        "success_metric": offer.success_metric,
        "opportunity_types": [t.value for t in offer.opportunity_types],
    }
