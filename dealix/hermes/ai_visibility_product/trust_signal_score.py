"""Customer-facing trust signal score for AI engine visibility."""

from __future__ import annotations

from dataclasses import dataclass

from .citation_tracker import citations_for
from .mention_tracker import list_mentions


@dataclass(frozen=True)
class TrustSignalScore:
    customer_id: str
    mentions: int
    citations: int
    score: float
    band: str


def _band(score: float) -> str:
    if score >= 0.75:
        return "strong"
    if score >= 0.5:
        return "fair"
    if score >= 0.25:
        return "weak"
    return "absent"


def compute(customer_id: str) -> TrustSignalScore:
    """Compute a 0-1 trust signal score from recorded mentions + citations."""
    mentions = len(list_mentions(customer_id))
    citations = len(citations_for(customer_id))
    raw = min(1.0, 0.4 * (mentions / 20.0) + 0.6 * (citations / 15.0))
    return TrustSignalScore(
        customer_id=customer_id,
        mentions=mentions,
        citations=citations,
        score=round(raw, 4),
        band=_band(raw),
    )
