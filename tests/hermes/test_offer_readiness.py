"""Product Readiness Gate — checks every default offer scores reasonably,
and that missing critical fields lower the score."""

from __future__ import annotations

from dataclasses import replace

from dealix.hermes.products import (
    DEFAULT_OFFERS,
    ProductReadinessGate,
)


def test_every_default_offer_scores_at_least_60() -> None:
    gate = ProductReadinessGate()
    for offer in DEFAULT_OFFERS:
        result = gate.assess(offer)
        assert result.score >= 60, (
            f"offer `{offer.offer_id}` scored {result.score}: "
            f"missing={result.missing}"
        )
        assert result.offer_id == offer.offer_id


def test_offer_missing_pain_scores_lower_than_complete_offer() -> None:
    gate = ProductReadinessGate()
    baseline = DEFAULT_OFFERS[0]
    full_score = gate.assess(baseline).score

    stripped = replace(baseline, pain="")
    stripped_score = gate.assess(stripped).score

    assert stripped_score < full_score
    assert "pain" in gate.assess(stripped).missing
