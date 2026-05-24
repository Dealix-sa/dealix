"""Tests for `dealix.partners.fit_score.PartnerFitScorer`."""

from __future__ import annotations

from dealix.money.offer_matcher import SEED_OFFERS
from dealix.partners.fit_score import PartnerFitScorer
from dealix.partners.scout import PartnerCandidate


def _candidate(trust: float, why: str = "agency match") -> PartnerCandidate:
    return PartnerCandidate(
        name="Sigma Studios",
        segment="agency",
        why_relevant=why,
        fit_signals=["rule:partner:agency"],
        trust_score=trust,
        source_signal_id="sig_q",
    )


def _offer():
    return next(o for o in SEED_OFFERS if o.name == "Agency White-label Kit")


def test_strong_candidate_scores_high() -> None:
    scorer = PartnerFitScorer()
    result = scorer.score(_candidate(trust=4.5, why="strong agency white-label fit reseller"), _offer())
    assert result.score >= 3.5
    assert result.classification == "strong"


def test_weak_candidate_scores_lower_than_strong_one() -> None:
    scorer = PartnerFitScorer()
    weak = _candidate(trust=0.5, why="unclear relevance, off-segment")
    strong = _candidate(trust=4.5, why="strong agency white-label fit reseller")
    weak_result = scorer.score(weak, _offer())
    strong_result = scorer.score(strong, _offer())
    assert weak_result.score < strong_result.score
    assert weak_result.score <= 2.5
    assert weak_result.classification in {"weak", "viable"}


def test_score_components_carry_inputs() -> None:
    scorer = PartnerFitScorer()
    cand = _candidate(trust=3.0, why="agency white-label demand reseller")
    result = scorer.score(cand, _offer())
    assert result.components["trust_score"] == 3.0
    assert 0.0 <= result.components["value_overlap"] <= 1.0
