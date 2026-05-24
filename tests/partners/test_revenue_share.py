"""Tests for `dealix.partners.revenue_share.RevenueShareCalculator`."""

from __future__ import annotations

from decimal import Decimal

import pytest

from dealix.hermes.core.schemas import Money
from dealix.partners.revenue_share import (
    PartnerTier,
    RevenueShareCalculator,
)


def test_standard_tier_splits_20_pct() -> None:
    calc = RevenueShareCalculator()
    split = calc.calc(Money.sar(Decimal("10000")), PartnerTier.STANDARD)
    assert split.partner_share.amount == Decimal("2000.00")
    assert split.dealix_share.amount == Decimal("8000.00")
    assert split.rate == pytest.approx(0.20)


def test_preferred_tier_splits_30_pct() -> None:
    calc = RevenueShareCalculator()
    split = calc.calc(Money.sar(Decimal("10000")), PartnerTier.PREFERRED)
    assert split.partner_share.amount == Decimal("3000.00")
    assert split.dealix_share.amount == Decimal("7000.00")
    assert split.rate == pytest.approx(0.30)


def test_strategic_tier_splits_40_pct() -> None:
    calc = RevenueShareCalculator()
    split = calc.calc(Money.sar(Decimal("10000")), "strategic")
    assert split.partner_share.amount == Decimal("4000.00")
    assert split.dealix_share.amount == Decimal("6000.00")
    assert split.rate == pytest.approx(0.40)


def test_invalid_tier_raises() -> None:
    calc = RevenueShareCalculator()
    with pytest.raises(ValueError):
        calc.calc(Money.sar(Decimal("100")), "platinum")
