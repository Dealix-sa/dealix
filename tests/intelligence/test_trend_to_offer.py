"""Tests for `dealix.intelligence.trend_to_offer.TrendToOfferTranslator`."""

from __future__ import annotations

from dealix.intelligence.trend_to_offer import TrendToOfferTranslator


def test_translate_known_trend_returns_seeded_idea() -> None:
    translator = TrendToOfferTranslator()
    ideas = translator.translate("ai governance")
    assert ideas
    names = {idea.name for idea in ideas}
    assert "AI Trust Kit" in names


def test_translate_unknown_trend_returns_empty_list() -> None:
    translator = TrendToOfferTranslator()
    assert translator.translate("crypto winter") == []


def test_translate_loose_match_via_substring() -> None:
    translator = TrendToOfferTranslator()
    # "agency consolidation surge" contains "agency consolidation"
    ideas = translator.translate("agency consolidation surge")
    assert ideas
    assert ideas[0].name == "Agency White-label Kit"
