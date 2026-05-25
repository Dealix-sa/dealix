"""Score (offer, ICP) pairs to a fit_score on [0, 1]."""

from __future__ import annotations

from dataclasses import dataclass

from .icp_registry import ICP


@dataclass(frozen=True)
class Offer:
    offer_id: str
    name: str
    addresses_pains: tuple[str, ...]
    price_band: str
    industries: tuple[str, ...] = ()
    regions: tuple[str, ...] = ()


@dataclass(frozen=True)
class FitScore:
    offer_id: str
    icp_id: str
    fit_score: float
    rationale: tuple[str, ...]


def score(offer: Offer, icp: ICP) -> FitScore:
    """Return FitScore combining industry, region, and pain overlap with the ICP."""
    rationale: list[str] = []
    total = 0.0

    if not offer.industries or icp.industry in offer.industries:
        total += 0.35
        rationale.append("industry-aligned")
    if not offer.regions or icp.region in offer.regions:
        total += 0.25
        rationale.append("region-aligned")
    if icp.pain_points and offer.addresses_pains:
        overlap = len(set(icp.pain_points).intersection(offer.addresses_pains))
        ratio = overlap / len(icp.pain_points)
        total += 0.4 * ratio
        if ratio > 0:
            rationale.append(f"pain-overlap={overlap}")
    return FitScore(offer_id=offer.offer_id, icp_id=icp.icp_id, fit_score=round(total, 4), rationale=tuple(rationale))
