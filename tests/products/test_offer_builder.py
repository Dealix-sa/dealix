"""Tests for `dealix.products.offer_builder.OfferBuilder`."""

from __future__ import annotations

from decimal import Decimal

import pytest

from dealix.hermes.core.schemas import Money
from dealix.products.offer_builder import OfferBuilder, OfferBuilderError


def test_build_clean_offer() -> None:
    builder = OfferBuilder()
    offer = builder.build(
        name="Pipeline Spark",
        buyer="SME founder",
        pain="No outbound rhythm at all",
        deliverable="30-day rolling outbound + weekly review",
        price_band=(Money.sar(Decimal("4500")), Money.sar(Decimal("9000"))),
    )
    assert offer.name == "Pipeline Spark"
    assert offer.price_band[0].amount == Decimal("4500")


def test_build_blocks_overclaim_in_pain() -> None:
    builder = OfferBuilder()
    with pytest.raises(OfferBuilderError) as excinfo:
        builder.build(
            name="Trust Bundle",
            buyer="CTO",
            pain="Guaranteed 100 % audit coverage",
            deliverable="Audit pack",
            price_band=(Money.sar(Decimal("5000")), Money.sar(Decimal("10000"))),
        )
    assert "overclaim" in str(excinfo.value).lower()


def test_build_rejects_inverted_price_band() -> None:
    builder = OfferBuilder()
    with pytest.raises(OfferBuilderError):
        builder.build(
            name="Misordered",
            buyer="CTO",
            pain="Risk gap",
            deliverable="Audit",
            price_band=(Money.sar(Decimal("9000")), Money.sar(Decimal("5000"))),
        )
