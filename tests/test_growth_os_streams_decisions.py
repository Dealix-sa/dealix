"""Revenue stream decision tests."""

from __future__ import annotations

from dealix.growth_os.streams.decisions import decide_stream_action
from dealix.growth_os.streams.portfolio import (
    REVENUE_PORTFOLIO,
    STREAM_BUCKETS,
)
from dealix.growth_os.streams.stream_card import RevenueStreamCard


def test_portfolio_has_five_buckets_and_at_least_25_streams() -> None:
    assert set(STREAM_BUCKETS) == {
        "fast",
        "monthly",
        "partner",
        "enterprise",
        "platform",
    }
    assert len(REVENUE_PORTFOLIO.streams) >= 25


def test_high_margin_low_risk_retainer_scales() -> None:
    card = RevenueStreamCard(
        stream_key="x",
        bucket="monthly",
        label_ar="x",
        label_en="x",
        margin_pct=0.70,
        retainer_potential=0.9,
        risk="low",
        effort_hours_per_unit=5.0,
        repeatability="retainer_native",
    )
    decision = decide_stream_action(card)
    assert decision.action == "scale"


def test_low_margin_high_effort_kills_or_reprices() -> None:
    heavy = RevenueStreamCard(
        stream_key="bad",
        bucket="fast",
        label_ar="bad",
        label_en="bad",
        margin_pct=0.10,
        retainer_potential=0.1,
        risk="medium",
        effort_hours_per_unit=80.0,
    )
    decision = decide_stream_action(heavy)
    assert decision.action in {"kill", "reprice"}


def test_high_risk_pauses() -> None:
    card = RevenueStreamCard(
        stream_key="risky",
        bucket="enterprise",
        label_ar="r",
        label_en="r",
        margin_pct=0.50,
        retainer_potential=0.5,
        risk="high",
    )
    decision = decide_stream_action(card)
    assert decision.action == "pause"


def test_partner_bucket_high_retainer_is_partner_led() -> None:
    card = RevenueStreamCard(
        stream_key="agency",
        bucket="partner",
        label_ar="x",
        label_en="x",
        margin_pct=0.4,
        retainer_potential=0.8,
        risk="medium",
    )
    decision = decide_stream_action(card)
    assert decision.action == "partner_led"
