"""خادم الشركاء — PartnerPitchFactory.

Produces a structured pitch draft for a partner candidate. Always
requires approval (Sami sign-off) and runs the full GuardrailChain to
flag overclaims, sensitive data, or unauthorized pricing.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from dealix.money.offer_matcher import Offer
from dealix.partners.scout import PartnerCandidate
from dealix.trust.guardrails import GuardrailChain


class PartnerPitchDraft(BaseModel):
    """A pitch draft ready for Sami review."""

    model_config = ConfigDict(extra="forbid")

    partner_name: str = Field(..., min_length=1, max_length=200)
    offer_name: str = Field(..., min_length=1, max_length=200)
    headline: str = Field(..., min_length=1, max_length=200)
    why_partner_wins: list[str] = Field(..., min_length=1, max_length=8)
    why_we_win: list[str] = Field(..., min_length=1, max_length=8)
    proposed_next_step: str = Field(..., min_length=1, max_length=300)
    body: str = Field(..., min_length=1, max_length=4000)
    requires_approval: bool = True
    guardrail_results: list[dict[str, Any]] = Field(default_factory=list)
    guardrails_passed: bool = True


class PartnerPitchFactory:
    """Render a `PartnerPitchDraft` from a candidate + offer."""

    def __init__(self, guardrail_chain: GuardrailChain | None = None) -> None:
        self._guards = guardrail_chain or GuardrailChain()

    def draft(
        self,
        candidate: PartnerCandidate,
        our_offer: Offer,
    ) -> PartnerPitchDraft:
        headline = (
            f"{candidate.name} × Dealix — {our_offer.name}"
        )
        why_partner_wins = [
            f"Access to Dealix {our_offer.deliverable.split('.')[0].lower()}",
            f"Success metric: {our_offer.success_metric}",
            f"Tier-based revenue share (STANDARD / PREFERRED / STRATEGIC)",
        ]
        why_we_win = [
            f"{candidate.name} is segment-relevant ({candidate.segment})",
            f"trust score {candidate.trust_score:.1f}",
            f"source signal indicators: {', '.join(candidate.fit_signals[:3]) or 'baseline scout'}",
        ]
        next_step = (
            f"Schedule a 30-minute scoping call with {candidate.name}'s lead "
            f"and Sami to confirm scope + pilot timeline."
        )
        body = (
            f"Hello {candidate.name} team,\n\n"
            f"Dealix would like to explore a partnership around the "
            f"{our_offer.name}. {candidate.why_relevant}\n\n"
            f"Our pitch is intentionally short — see attached deck for the "
            f"full deliverable + pricing band. We propose: {next_step}\n\n"
            f"— Dealix"
        )

        payload = {
            "title": headline,
            "body": body,
            "summary": our_offer.pain,
            "fields": {
                "partner": candidate.name,
                "segment": candidate.segment,
                "next_step": next_step,
            },
        }
        results = self._guards.run_all(payload)
        passed = GuardrailChain.passed(results)
        return PartnerPitchDraft(
            partner_name=candidate.name,
            offer_name=our_offer.name,
            headline=headline,
            why_partner_wins=why_partner_wins,
            why_we_win=why_we_win,
            proposed_next_step=next_step,
            body=body,
            requires_approval=True,
            guardrail_results=[r.to_dict() for r in results],
            guardrails_passed=passed,
        )


__all__ = ["PartnerPitchDraft", "PartnerPitchFactory"]
