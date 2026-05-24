"""Tests for `dealix.money.pricing.PricingEngine`."""

from __future__ import annotations

from decimal import Decimal

from dealix.hermes.core.opportunities import Opportunity, OpportunityType
from dealix.hermes.core.schemas import Money
from dealix.hermes.sovereignty import SovereigntyLevel
from dealix.money.offer_matcher import SEED_OFFERS
from dealix.money.pricing import DiscountVerdict, PricingEngine


def _opp(urgency: int = 3, fit: int = 3) -> Opportunity:
    return Opportunity(
        signal_id="sig_p",
        opp_type=OpportunityType.REVENUE,
        title="Test revenue opp",
        narrative="needs help",
        expected_value=Money.sar(6000),
        urgency=urgency,
        fit_score=fit,
    )


def _offer():
    return next(o for o in SEED_OFFERS if o.name == "Revenue Hunter Pilot")


def test_quote_stays_within_offer_band() -> None:
    engine = PricingEngine()
    offer = _offer()
    quote = engine.quote(offer, _opp(urgency=3, fit=3))
    low, high = offer.price_band
    assert low.amount <= quote.amount <= high.amount
    assert quote.currency == "SAR"


def test_quote_lifts_when_urgency_and_fit_are_high() -> None:
    engine = PricingEngine()
    offer = _offer()
    low_quote = engine.quote(offer, _opp(urgency=1, fit=1))
    high_quote = engine.quote(offer, _opp(urgency=5, fit=5))
    assert high_quote.amount >= low_quote.amount


def test_discount_advisory_in_autonomous_range() -> None:
    engine = PricingEngine()
    base = Money.sar(Decimal("10000"))
    quoted = Money.sar(Decimal("9500"))  # 5 % discount
    advisory = engine.discount_advisory(base, quoted)
    assert advisory.verdict == DiscountVerdict.AUTONOMOUS
    assert advisory.requires_sami_approval is False
    # Below the high-value threshold, so sovereignty remains the input default.
    assert advisory.suggested_sovereignty == SovereigntyLevel.S0_AUTONOMOUS


def test_discount_advisory_requires_approval_when_above_threshold() -> None:
    engine = PricingEngine()
    base = Money.sar(Decimal("10000"))
    quoted = Money.sar(Decimal("8500"))  # 15 % discount
    advisory = engine.discount_advisory(base, quoted)
    assert advisory.verdict == DiscountVerdict.REQUIRES_APPROVAL
    assert advisory.requires_sami_approval is True
    assert advisory.suggested_sovereignty == SovereigntyLevel.S2_SAMI_APPROVAL


def test_discount_advisory_blocks_above_hard_floor_and_lifts_high_value() -> None:
    engine = PricingEngine()
    base = Money.sar(Decimal("30000"))
    quoted = Money.sar(Decimal("19500"))  # 35 % discount + enterprise base
    advisory = engine.discount_advisory(base, quoted)
    assert advisory.verdict == DiscountVerdict.EXCEEDS_LIMIT
    assert advisory.requires_sami_approval is True
    assert advisory.suggested_sovereignty == SovereigntyLevel.S3_SAMI_ONLY
