"""Attribution tests — only real revenue is counted."""

from __future__ import annotations

from pathlib import Path

import pytest

from dealix.revenue_marketing.attribution import (
    attribution_chain_for_deal,
    record_attribution,
    revenue_by_dimension,
)
from dealix.revenue_marketing.schemas import MarketingTouch
from dealix.revenue_marketing.store import (
    reset_revenue_marketing_store_for_tests,
    uid,
)


@pytest.fixture
def fresh_store(tmp_path: Path):
    return reset_revenue_marketing_store_for_tests(path=tmp_path / "rm.json")


def test_record_attribution_raises_when_neither_flag(fresh_store) -> None:
    with pytest.raises(ValueError, match="revenue_not_real_yet"):
        record_attribution(
            deal_id="deal_x",
            revenue_sar=10_000,
            sources={"campaign_id": "camp_1"},
            payment_received=False,
            signed_agreement=False,
            store=fresh_store,
        )


def test_record_attribution_allows_pipeline_only(fresh_store) -> None:
    attr = record_attribution(
        deal_id="deal_p",
        revenue_sar=5_000,
        sources={"campaign_id": "camp_p"},
        payment_received=False,
        signed_agreement=False,
        attribution_type="pipeline_only",
        store=fresh_store,
    )
    assert attr.is_real_revenue is False


def test_record_attribution_payment_or_signed_works(fresh_store) -> None:
    a = record_attribution(
        deal_id="d1",
        revenue_sar=1_000,
        sources={"campaign_id": "c1"},
        payment_received=True,
        signed_agreement=False,
        store=fresh_store,
    )
    b = record_attribution(
        deal_id="d2",
        revenue_sar=2_000,
        sources={"campaign_id": "c2"},
        payment_received=False,
        signed_agreement=True,
        store=fresh_store,
    )
    assert a.is_real_revenue is True
    assert b.is_real_revenue is True


def test_revenue_by_dimension_only_counts_real(fresh_store) -> None:
    record_attribution(
        deal_id="d_real_1",
        revenue_sar=1_000,
        sources={"channel": "linkedin"},
        payment_received=True,
        signed_agreement=False,
        store=fresh_store,
    )
    record_attribution(
        deal_id="d_real_2",
        revenue_sar=2_000,
        sources={"channel": "linkedin"},
        payment_received=False,
        signed_agreement=True,
        store=fresh_store,
    )
    record_attribution(
        deal_id="d_pipeline",
        revenue_sar=9_999_999,
        sources={"channel": "linkedin"},
        payment_received=False,
        signed_agreement=False,
        attribution_type="pipeline_only",
        store=fresh_store,
    )
    totals = revenue_by_dimension("channel", store=fresh_store)
    assert totals.get("linkedin") == pytest.approx(3_000.0)


def test_attribution_chain_order(fresh_store) -> None:
    deal_id = "deal_chain_1"
    campaign_id = "camp_chain"
    t1 = MarketingTouch(
        id=uid("tch"),
        campaign_id=campaign_id,
        lead_id=deal_id,
        touch_type="view",
        channel="linkedin",
    )
    fresh_store.append_touch(t1)
    t2 = MarketingTouch(
        id=uid("tch"),
        campaign_id=campaign_id,
        lead_id=deal_id,
        touch_type="reply",
        channel="email",
    )
    fresh_store.append_touch(t2)
    record_attribution(
        deal_id=deal_id,
        revenue_sar=5_000,
        sources={"campaign_id": campaign_id, "offer_id": "off_1"},
        payment_received=True,
        signed_agreement=False,
        store=fresh_store,
    )
    chain = attribution_chain_for_deal(deal_id, store=fresh_store)
    kinds = [c["kind"] for c in chain]
    # Two touches, then optional campaign/offer entries, then attribution.
    assert kinds[0] == "touch"
    assert kinds[1] == "touch"
    assert "attribution" in kinds
