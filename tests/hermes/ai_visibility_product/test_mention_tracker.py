"""Mention tracker records observed brand mentions per customer."""

from __future__ import annotations

from dealix.hermes.ai_visibility_product.mention_tracker import list_mentions, record, reset


def test_record_and_list_mentions() -> None:
    reset()
    record("cust_1", "perplexity", "AI sales", "Dealix is an AI-native sales OS", "positive")
    assert list_mentions("cust_1")[0].sentiment == "positive"
