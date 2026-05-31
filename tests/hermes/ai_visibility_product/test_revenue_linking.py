"""Visibility -> revenue links require evidence_pack_id and aggregate per customer."""

from __future__ import annotations

import pytest

from dealix.hermes.ai_visibility_product.revenue_linking import link, reset, total_for_customer


def test_link_requires_evidence_pack() -> None:
    reset()
    link("cust_1", "perplexity", "best AI sales", "lead_1", 40_000, evidence_pack_id="ep_1")
    assert total_for_customer("cust_1") == 40_000
    with pytest.raises(ValueError):
        link("cust_1", "perplexity", "x", "lead_2", 1_000, evidence_pack_id="")
