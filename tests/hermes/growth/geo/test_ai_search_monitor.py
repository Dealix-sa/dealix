"""AI search monitor records observations and computes per-query coverage."""

from __future__ import annotations

from dealix.hermes.growth.geo.ai_search_monitor import coverage, record_observation, reset, watch


def test_coverage_reflects_mention_ratio() -> None:
    reset()
    watch("best CRM saudi", engines=["perplexity", "you.com"])
    record_observation("best CRM saudi", "perplexity", True)
    record_observation("best CRM saudi", "perplexity", False)
    record_observation("best CRM saudi", "you.com", True)
    assert coverage("best CRM saudi") == round(2 / 3, 4)
