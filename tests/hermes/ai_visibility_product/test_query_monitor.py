"""Customer-tracked queries register per customer."""

from __future__ import annotations

from dealix.hermes.ai_visibility_product.query_monitor import list_tracked, reset, track


def test_track_lists_per_customer() -> None:
    reset()
    track("cust_1", "best AI sales saudi", priority=2)
    track("cust_1", "AI CRM riyadh", priority=1)
    track("cust_2", "AI logistics", priority=1)
    assert {t.query for t in list_tracked("cust_1")} == {"best AI sales saudi", "AI CRM riyadh"}
