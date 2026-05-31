"""Store tests — seed load + upsert + stats."""

from __future__ import annotations

from pathlib import Path

import pytest

from dealix.revenue_marketing.attribution import record_attribution
from dealix.revenue_marketing.schemas import (
    Lead,
    MarketingCampaign,
    MessageVariant,
    Offer,
)
from dealix.revenue_marketing.store import (
    reset_revenue_marketing_store_for_tests,
    uid,
)


@pytest.fixture
def fresh_store(tmp_path: Path):
    return reset_revenue_marketing_store_for_tests(path=tmp_path / "rm.json")


def test_seed_load_seeds_offers_and_messages(fresh_store) -> None:
    added = fresh_store.ensure_seed_loaded()
    assert added["offers"] > 0
    assert added["messages"] > 0
    offers = fresh_store.list_offers()
    assert any(o.rung == "free" for o in offers)
    assert any(o.rung == "enterprise" for o in offers)


def test_seed_load_idempotent(fresh_store) -> None:
    fresh_store.ensure_seed_loaded()
    again = fresh_store.ensure_seed_loaded()
    assert again["offers"] == 0
    assert again["messages"] == 0


def test_upsert_offer_replaces_existing(fresh_store) -> None:
    o1 = Offer(
        id="off_test",
        name_ar="ا",
        name_en="A",
        rung="entry",
        price_min_sar=999,
        price_max_sar=999,
        target_segment="x",
        pain_addressed="y",
        success_metric="z",
        scale_kill_rule="k",
    )
    fresh_store.upsert_offer(o1)
    o2 = o1.model_copy(update={"name_en": "B"})
    fresh_store.upsert_offer(o2)
    rows = [o for o in fresh_store.list_offers() if o.id == "off_test"]
    assert len(rows) == 1
    assert rows[0].name_en == "B"


def test_upsert_message(fresh_store) -> None:
    m = MessageVariant(
        id="msg_a",
        offer_id="off_1",
        angle="money",
        headline_ar="ع",
        headline_en="H",
        body_ar="ع",
        body_en="B",
        cta_ar="ك",
        cta_en="C",
    )
    fresh_store.upsert_message(m)
    assert any(x.id == "msg_a" for x in fresh_store.list_messages())


def test_upsert_campaign(fresh_store) -> None:
    c = MarketingCampaign(
        id="camp_a",
        campaign_name="A",
        target_segment="smb",
        offer_id="off_1",
        channel="linkedin",
        message_angle="money",
        success_metric="leads",
        scale_kill_rule="kill_if_under_x",
    )
    fresh_store.upsert_campaign(c)
    rows = fresh_store.list_campaigns()
    assert any(x.id == "camp_a" for x in rows)


def test_stats_counts_active_campaigns_and_vanity_only(fresh_store) -> None:
    fresh_store.ensure_seed_loaded()
    camp = MarketingCampaign(
        id="camp_active",
        campaign_name="Active",
        target_segment="smb",
        offer_id="off_1",
        channel="linkedin",
        message_angle="money",
        success_metric="leads",
        scale_kill_rule="kill_if_under_x",
        status="active",
    )
    fresh_store.upsert_campaign(camp)
    s = fresh_store.stats()
    assert s["active_campaigns"] == 1
    # Active campaign has zero leads and zero attributed revenue.
    assert s["vanity_only_campaigns"] == 1


def test_stats_unattributed_revenue(fresh_store) -> None:
    record_attribution(
        deal_id="deal_unattr",
        revenue_sar=500,
        sources={},
        payment_received=True,
        signed_agreement=False,
        store=fresh_store,
    )
    record_attribution(
        deal_id="deal_attr",
        revenue_sar=500,
        sources={"campaign_id": "camp_x"},
        payment_received=True,
        signed_agreement=False,
        store=fresh_store,
    )
    s = fresh_store.stats()
    assert s["unattributed_revenue_count"] == 1


def test_lead_overall_score_computed(fresh_store) -> None:
    lead = Lead(
        id=uid("lead"),
        source="referral",
        segment="smb",
        pain="leaking",
        fit_score=1.0,
        pain_score=1.0,
        ability_to_pay_score=1.0,
        urgency_score=1.0,
        partner_potential_score=1.0,
        trust_fit_score=1.0,
    )
    fresh_store.upsert_lead(lead)
    rows = fresh_store.list_leads()
    assert rows[0].overall_score == pytest.approx(1.0)
