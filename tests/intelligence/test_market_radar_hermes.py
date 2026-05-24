"""Tests for `dealix.intelligence.market_radar.MarketRadar` (Hermes wave)."""

from __future__ import annotations

from dealix.intelligence.market_radar import MarketRadar


def test_scan_returns_no_signals_for_noise() -> None:
    radar = MarketRadar()
    signals = radar.scan(
        [
            {"id": "n1", "headline": "Weather is sunny today", "source": "weather"},
        ]
    )
    assert signals == []


def test_scan_promotes_regulation_news() -> None:
    radar = MarketRadar()
    signals = radar.scan(
        [
            {
                "id": "r1",
                "headline": "PDPL compliance deadline announced",
                "body": "Regulator confirms tighter rules.",
                "source": "press",
            }
        ]
    )
    assert len(signals) == 1
    assert signals[0].category == "regulation"
    assert "pdpl" in signals[0].matched_terms


def test_scan_orders_by_descending_score() -> None:
    radar = MarketRadar()
    signals = radar.scan(
        [
            {"id": "a", "headline": "Competitor launches feature", "body": "competitor", "source": "blog"},
            {
                "id": "b",
                "headline": "AI governance + Responsible AI framework",
                "body": "ai governance ai policy responsible ai",
                "source": "press",
            },
        ]
    )
    assert len(signals) == 2
    assert signals[0].score >= signals[1].score
