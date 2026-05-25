"""Attribution grouping tests."""

from __future__ import annotations

from dealix.growth_os.attribution.analysis import (
    group_revenue_by_campaign,
    group_revenue_by_channel,
    group_revenue_by_offer,
)
from dealix.growth_os.revenue_proof.revenue_record import (
    RevenueRecord,
    VerificationDoc,
)


def _rec(
    rid: str,
    amount: float,
    offer: str,
    channels: list[str],
    campaigns: list[str],
) -> RevenueRecord:
    return RevenueRecord(
        record_id=rid,
        customer_id="cust_001",
        offer_key=offer,
        amount_usd=amount,
        status="paid",
        verification=VerificationDoc(kind="payment", reference=f"pay_{rid}"),
        attributed_channels=channels,
        attributed_campaigns=campaigns,
    )


def test_group_by_channel_sums_correctly() -> None:
    recs = [
        _rec("r1", 1000, "x", ["referral"], []),
        _rec("r2", 500, "x", ["referral"], []),
        _rec("r3", 800, "x", ["inbound"], []),
    ]
    by_channel = group_revenue_by_channel(recs)
    assert by_channel.totals["referral"] == 1500.0
    assert by_channel.totals["inbound"] == 800.0
    assert by_channel.counts["referral"] == 2


def test_group_by_offer_groups_scalars() -> None:
    recs = [
        _rec("r1", 1000, "ai_trust_kit", ["referral"], []),
        _rec("r2", 2000, "revenue_hunter", ["referral"], []),
        _rec("r3", 500, "ai_trust_kit", ["referral"], []),
    ]
    by_offer = group_revenue_by_offer(recs)
    assert by_offer.totals["ai_trust_kit"] == 1500.0
    assert by_offer.totals["revenue_hunter"] == 2000.0


def test_multi_touch_splits_revenue() -> None:
    recs = [
        _rec("r1", 1000, "x", ["a", "b"], []),  # split 500/500
    ]
    by_channel = group_revenue_by_channel(recs)
    assert by_channel.totals["a"] == 500.0
    assert by_channel.totals["b"] == 500.0


def test_unverified_records_are_excluded_by_default() -> None:
    bad = RevenueRecord(
        record_id="bad",
        customer_id="cust_001",
        offer_key="x",
        amount_usd=999.0,
        status="paid",
        verification=None,
        attributed_channels=["referral"],
        attributed_campaigns=["c1"],
    )
    out = group_revenue_by_campaign([bad])
    assert out.totals == {}
