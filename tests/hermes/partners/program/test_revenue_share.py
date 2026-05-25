"""Revenue share percentages map per tier and compute payouts."""

from __future__ import annotations

from dealix.hermes.partners.program.revenue_share import compute, share_pct


def test_white_label_tier_pays_30_pct() -> None:
    assert share_pct("white_label") == 0.30
    payout = compute("p_alpha", "white_label", 100_000)
    assert payout.payout_sar == 30_000


def test_unknown_tier_pays_zero() -> None:
    assert share_pct("ghost") == 0.0
