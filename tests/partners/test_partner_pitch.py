"""Tests for `dealix.partners.pitch.PartnerPitchFactory`."""

from __future__ import annotations

from dealix.money.offer_matcher import SEED_OFFERS
from dealix.partners.pitch import PartnerPitchFactory
from dealix.partners.scout import PartnerCandidate


def _candidate(name: str = "Sigma Studios") -> PartnerCandidate:
    return PartnerCandidate(
        name=name,
        segment="agency",
        why_relevant="aligned on white-label motion",
        fit_signals=["rule:partner:agency"],
        trust_score=4.0,
        source_signal_id="sig_q",
    )


def _offer():
    return next(o for o in SEED_OFFERS if o.name == "Agency White-label Kit")


def test_draft_requires_approval_and_passes_guardrails_on_clean_inputs() -> None:
    factory = PartnerPitchFactory()
    draft = factory.draft(_candidate(), _offer())
    assert draft.requires_approval is True
    assert draft.guardrails_passed is True
    assert draft.partner_name == "Sigma Studios"


def test_draft_carries_partner_and_offer_specific_fields() -> None:
    factory = PartnerPitchFactory()
    draft = factory.draft(_candidate("Nimbus Group"), _offer())
    assert "Nimbus Group" in draft.headline
    assert draft.why_partner_wins
    assert draft.why_we_win
    assert draft.proposed_next_step


def test_draft_records_guardrail_chain_results() -> None:
    factory = PartnerPitchFactory()
    draft = factory.draft(_candidate(), _offer())
    # All four canonical guardrails recorded.
    names = {r["guardrail"] for r in draft.guardrail_results}
    assert {
        "no_overclaim",
        "no_sensitive_data",
        "no_unauthorized_pricing",
        "no_false_partnership",
    }.issubset(names)
