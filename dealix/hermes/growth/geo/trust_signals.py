"""Aggregate trust signals that influence AI answer-engine ranking."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class TrustSignals:
    domain: str
    backlinks_authoritative: int
    third_party_citations: int
    case_studies_published: int
    regulatory_endorsements: int
    score: float


def compute(
    domain: str,
    *,
    backlinks_authoritative: int = 0,
    third_party_citations: int = 0,
    case_studies_published: int = 0,
    regulatory_endorsements: int = 0,
) -> TrustSignals:
    """Compute a 0-1 trust score from weighted external signals."""
    raw = (
        0.3 * min(backlinks_authoritative / 50.0, 1.0)
        + 0.3 * min(third_party_citations / 25.0, 1.0)
        + 0.25 * min(case_studies_published / 10.0, 1.0)
        + 0.15 * min(regulatory_endorsements / 3.0, 1.0)
    )
    return TrustSignals(
        domain=domain,
        backlinks_authoritative=backlinks_authoritative,
        third_party_citations=third_party_citations,
        case_studies_published=case_studies_published,
        regulatory_endorsements=regulatory_endorsements,
        score=round(min(1.0, raw), 4),
    )
