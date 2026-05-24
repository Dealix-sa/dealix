"""Tests for `dealix.money.proposal_factory.ProposalFactory`."""

from __future__ import annotations

import pytest

from dealix.hermes.core.opportunities import Opportunity, OpportunityType
from dealix.hermes.core.schemas import Money
from dealix.hermes.sovereignty import SovereigntyLevel
from dealix.money.offer_matcher import SEED_OFFERS, OfferMatcher
from dealix.money.proposal_factory import ProposalDraft, ProposalFactory


def _revenue_opp(narrative: str = "Founder needs pipeline help.") -> Opportunity:
    return Opportunity(
        signal_id="sig_test",
        opp_type=OpportunityType.REVENUE,
        title="Revenue lead",
        narrative=narrative,
        expected_value=Money.sar(6000),
        urgency=4,
        fit_score=4,
    )


def test_render_clean_proposal_passes_guardrails() -> None:
    factory = ProposalFactory()
    matcher = OfferMatcher()
    opp = _revenue_opp()
    offer = matcher.match(opp)
    draft = factory.render(opp, offer, customer_meta={"name": "Acme"})
    assert isinstance(draft, ProposalDraft)
    assert draft.offer_name == offer.name
    assert draft.guardrails_passed is True
    # All nine §41 quality-gate fields populated:
    assert draft.buyer
    assert draft.pain
    assert draft.deliverables
    assert draft.price.amount > 0
    assert draft.timeline
    assert draft.risks
    assert draft.trust_status
    assert draft.approval_status


def test_render_with_overclaim_marketing_meta_is_blocked() -> None:
    # Use a custom Offer whose name carries an overclaim phrase to force
    # the guardrail to flag it. The factory still renders a draft but
    # marks `guardrails_passed=False`.
    from dealix.money.offer_matcher import Offer
    from decimal import Decimal

    bad_offer = Offer(
        name="Best in Saudi Revenue Engine",
        buyer="Founder",
        pain="No leads at all",
        deliverable="100 % guaranteed pipeline ramp",
        price_band=(Money.sar(Decimal("5000")), Money.sar(Decimal("9000"))),
        success_metric="At least 3 meetings",
        keywords=("pipeline",),
        opportunity_types=(OpportunityType.REVENUE,),
    )
    factory = ProposalFactory()
    opp = _revenue_opp()
    draft = factory.render(opp, bad_offer, customer_meta={})
    assert draft.guardrails_passed is False
    blocking = [
        r for r in draft.guardrail_results
        if r["guardrail"] == "no_overclaim" and r["passed"] is False
    ]
    assert blocking, draft.guardrail_results


def test_render_sensitive_opportunity_lifts_sovereignty() -> None:
    factory = ProposalFactory()
    opp = Opportunity(
        signal_id="sig_s",
        opp_type=OpportunityType.REVENUE,
        title="Regulated lead",
        narrative="patient data regulated",
        expected_value=Money.sar(8000),
        sensitive=True,
    )
    offer = OfferMatcher().match(opp)
    draft = factory.render(opp, offer)
    assert draft.sovereignty_level.numeric >= SovereigntyLevel.S1_NOTIFY_SAMI.numeric
    assert draft.requires_approval is True


def test_render_rejects_offer_missing_fields() -> None:
    factory = ProposalFactory()
    opp = _revenue_opp()
    offer = next(o for o in SEED_OFFERS if o.name == "Revenue Hunter Pilot")
    # Force missing offer name via direct field mutation: pydantic raises.
    with pytest.raises(Exception):
        # An empty deliverable should fail downstream validation.
        from dealix.money.offer_matcher import Offer
        from decimal import Decimal

        Offer(
            name="bad",
            buyer="bad",
            pain="",
            deliverable="ok",
            price_band=(Money.sar(Decimal("100")), Money.sar(Decimal("200"))),
            success_metric="ok",
        )
    # And a valid offer renders correctly.
    draft = factory.render(opp, offer)
    assert draft.offer_name == "Revenue Hunter Pilot"
