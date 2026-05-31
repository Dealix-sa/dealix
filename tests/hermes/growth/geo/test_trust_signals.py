"""Trust signal score scales with backlinks, citations and case studies."""

from __future__ import annotations

from dealix.hermes.growth.geo.trust_signals import compute


def test_more_signals_yield_higher_score() -> None:
    low = compute("dealix.ai")
    high = compute(
        "dealix.ai",
        backlinks_authoritative=40,
        third_party_citations=20,
        case_studies_published=8,
        regulatory_endorsements=2,
    )
    assert high.score > low.score
    assert high.score <= 1.0
