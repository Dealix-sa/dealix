"""Upsell suggester — given a recent outcome, propose the next offer.

Tiny rule engine. Designed to be inspected and edited by the founder.
"""

from __future__ import annotations

from dataclasses import dataclass

from dealix.hermes.core.schemas import Outcome, OutcomeKind

UPSELL_PATHS: dict[str, list[str]] = {
    "Revenue Hunter Pilot": ["Agency White-label Kit", "Founder OS Setup"],
    "AI Trust Kit": ["Executive PMO Lite", "Agency White-label Kit"],
    "Market Radar Report": ["Revenue Hunter Pilot", "AI Trust Kit"],
    "Founder OS Setup": ["AI Trust Kit", "Executive PMO Lite"],
    "Agency White-label Kit": ["Executive PMO Lite"],
}


@dataclass
class UpsellSuggestion:
    current_offer: str
    next_offers: list[str]
    rationale: str
    confidence: float


def suggest(outcome: Outcome) -> UpsellSuggestion:
    current = outcome.offer or "Revenue Hunter Pilot"
    next_offers = UPSELL_PATHS.get(current, ["AI Trust Kit"])

    if outcome.kind == OutcomeKind.DEAL_WON:
        confidence = 0.7
        rationale = "Customer just paid — highest receptivity window."
    elif outcome.kind == OutcomeKind.PILOT_STARTED:
        confidence = 0.55
        rationale = "Pilot active — set up the conversion path now."
    elif outcome.kind == OutcomeKind.UPSELL_ACCEPTED:
        confidence = 0.6
        rationale = "Pattern of buying — recommend next tier."
    else:
        confidence = 0.35
        rationale = "Neutral signal — propose as a soft option only."

    return UpsellSuggestion(
        current_offer=current,
        next_offers=next_offers,
        rationale=rationale,
        confidence=confidence,
    )
