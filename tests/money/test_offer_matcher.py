"""Tests for `dealix.money.offer_matcher.OfferMatcher`."""

from __future__ import annotations

import pytest

from dealix.hermes.core.opportunities import Opportunity, OpportunityType
from dealix.hermes.core.schemas import Money
from dealix.money.offer_matcher import SEED_OFFERS, Offer, OfferMatcher


def _opp(opp_type: OpportunityType, narrative: str, **kwargs) -> Opportunity:
    return Opportunity(
        signal_id="sig_test",
        opp_type=opp_type,
        title=f"Test {opp_type.value}",
        narrative=narrative,
        expected_value=kwargs.pop("expected_value", None),
        repeatable=kwargs.pop("repeatable", False),
        sensitive=kwargs.pop("sensitive", False),
        urgency=kwargs.pop("urgency", 3),
        fit_score=kwargs.pop("fit_score", 3),
    )


def test_seed_offers_contain_canonical_set() -> None:
    names = {o.name for o in SEED_OFFERS}
    assert "Revenue Hunter Pilot" in names
    assert "AI Trust Kit" in names
    assert "Agency White-label Kit" in names
    assert "Vertical Launch Sprint" in names
    assert "Renewal & Upsell Pack" in names
    assert len(SEED_OFFERS) >= 5


def test_revenue_lead_picks_revenue_hunter_pilot() -> None:
    matcher = OfferMatcher()
    opp = _opp(
        OpportunityType.REVENUE,
        "Founder asking about pipeline and meeting volume.",
    )
    best = matcher.match(opp)
    assert best.name == "Revenue Hunter Pilot"


def test_sensitive_governance_signal_picks_trust_kit() -> None:
    matcher = OfferMatcher()
    opp = _opp(
        OpportunityType.RISK_AVOIDANCE,
        "Regulator wants governance and audit trail for our agents.",
        sensitive=True,
    )
    best = matcher.match(opp)
    assert best.name == "AI Trust Kit"


def test_partner_opportunity_picks_white_label_kit() -> None:
    matcher = OfferMatcher()
    opp = _opp(
        OpportunityType.PARTNER,
        "Agency asking about reseller / white-label package.",
    )
    best = matcher.match(opp)
    assert best.name == "Agency White-label Kit"


def test_renewal_keywords_pick_renewal_pack() -> None:
    matcher = OfferMatcher()
    opp = _opp(
        OpportunityType.REVENUE,
        "Existing customer asking about renewal and retainer pricing.",
        repeatable=True,
    )
    best = matcher.match(opp)
    assert best.name == "Renewal & Upsell Pack"


def test_vertical_launch_signal_picks_vertical_sprint() -> None:
    matcher = OfferMatcher()
    opp = _opp(
        OpportunityType.PRODUCT,
        "Founder launching into the clinic vertical wants a sprint.",
    )
    best = matcher.match(opp)
    assert best.name == "Vertical Launch Sprint"


def test_empty_catalog_raises() -> None:
    with pytest.raises(ValueError):
        OfferMatcher(catalog=())


def test_rank_returns_ordered_pairs() -> None:
    matcher = OfferMatcher()
    opp = _opp(
        OpportunityType.REVENUE,
        "pipeline help wanted",
    )
    ranked = matcher.rank(opp)
    assert ranked
    assert ranked[0][1].name == "Revenue Hunter Pilot"
