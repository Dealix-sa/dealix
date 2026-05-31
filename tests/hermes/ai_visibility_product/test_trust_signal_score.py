"""Trust signal score grows with recorded citations and mentions."""

from __future__ import annotations

from dealix.hermes.ai_visibility_product import citation_tracker, mention_tracker
from dealix.hermes.ai_visibility_product.trust_signal_score import compute


def test_score_grows_with_citations() -> None:
    mention_tracker.reset()
    citation_tracker.reset()
    for i in range(10):
        mention_tracker.record("cust_1", "perplexity", "q", f"snippet {i}")
    for i in range(8):
        citation_tracker.record("cust_1", "perplexity", f"https://dealix.ai/p{i}", "q", i + 1)
    s = compute("cust_1")
    assert s.band in {"fair", "strong"}
    assert s.score > 0.4
