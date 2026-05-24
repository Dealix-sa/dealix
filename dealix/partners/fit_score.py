"""خادم الشركاء — PartnerFitScorer.

Thin wrapper around `dealix.hermes.core.scoring.partner_fit_score`.
Adapts the candidate/Offer pair into the kernel's expected shape.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from dealix.hermes.core.opportunities import (
    Opportunity,
    OpportunityType,
)
from dealix.hermes.core.schemas import Money, utcnow
from dealix.hermes.core.scoring import partner_fit_score
from dealix.money.offer_matcher import Offer
from dealix.partners.scout import PartnerCandidate


class PartnerFitResult(BaseModel):
    """Output of scoring a candidate against an offer."""

    model_config = ConfigDict(extra="forbid")

    partner_name: str = Field(..., min_length=1, max_length=200)
    offer_name: str = Field(..., min_length=1, max_length=200)
    score: float = Field(..., ge=0.0, le=5.0)
    components: dict[str, float] = Field(default_factory=dict)
    classification: str = Field(..., min_length=1, max_length=64)


class PartnerFitScorer:
    """Score a PartnerCandidate against one of our Offers."""

    def score(
        self,
        candidate: PartnerCandidate,
        our_offer: Offer,
    ) -> PartnerFitResult:
        # Build the dict shape `partner_fit_score` expects.
        partner_payload = {
            "categories": ["partnership", *(t.value for t in our_offer.opportunity_types)],
            "trust_score": candidate.trust_score,
            "value_overlap": _overlap(candidate, our_offer),
        }
        opportunity = Opportunity(
            signal_id=candidate.source_signal_id,
            opp_type=our_offer.opportunity_types[0]
            if our_offer.opportunity_types
            else OpportunityType.PARTNER,
            title=f"Partner fit: {candidate.name} / {our_offer.name}",
            narrative=candidate.why_relevant,
            expected_value=Money(
                amount=(our_offer.price_band[0].amount + our_offer.price_band[1].amount) / 2,
                currency=our_offer.price_band[0].currency,
            ),
            created_at=utcnow(),
        )
        score = partner_fit_score(partner_payload, opportunity)
        classification = _classify(score)
        return PartnerFitResult(
            partner_name=candidate.name,
            offer_name=our_offer.name,
            score=score,
            components={
                "trust_score": candidate.trust_score,
                "value_overlap": partner_payload["value_overlap"],
            },
            classification=classification,
        )


def _overlap(candidate: PartnerCandidate, our_offer: Offer) -> float:
    # Use only the natural-language `why_relevant` for keyword matching;
    # `fit_signals` are routing tags (e.g. "rule:partner:agency") whose
    # token form coincidentally collides with offer keywords and would
    # inflate overlap for off-segment candidates.
    bag = candidate.why_relevant.lower()
    hits = sum(1 for kw in our_offer.keywords if kw in bag)
    if not our_offer.keywords:
        return 0.5
    return max(0.0, min(1.0, hits / float(len(our_offer.keywords))))


def _classify(score: float) -> str:
    if score >= 3.5:
        return "strong"
    if score >= 2.0:
        return "viable"
    return "weak"


__all__ = ["PartnerFitResult", "PartnerFitScorer"]
