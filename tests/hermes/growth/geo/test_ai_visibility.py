"""AI visibility records and rate computation."""

from __future__ import annotations

from dealix.hermes.growth.geo.ai_visibility import record_mention, reset, visibility_rate


def test_visibility_rate_reflects_citation_ratio() -> None:
    reset()
    record_mention("Dealix", "perplexity", "best AI sales", 1, True)
    record_mention("Dealix", "perplexity", "best AI sales", 2, False)
    assert visibility_rate("Dealix") == 0.5
