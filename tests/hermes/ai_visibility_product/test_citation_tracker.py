"""Citation tracker records AI engine citations per customer."""

from __future__ import annotations

from dealix.hermes.ai_visibility_product.citation_tracker import citations_for, record, reset


def test_record_citation() -> None:
    reset()
    record("cust_1", "perplexity", "https://dealix.ai/research/2026", "best AI sales", 1)
    assert citations_for("cust_1")[0].rank == 1
