"""Portfolio tests — 5 rungs + concentration warnings."""

from __future__ import annotations

from pathlib import Path

import pytest

from dealix.revenue_marketing.attribution import record_attribution
from dealix.revenue_marketing.revenue_portfolio import (
    current_streams,
    portfolio_health,
)
from dealix.revenue_marketing.schemas import Offer
from dealix.revenue_marketing.store import reset_revenue_marketing_store_for_tests


@pytest.fixture
def fresh_store(tmp_path: Path):
    return reset_revenue_marketing_store_for_tests(path=tmp_path / "rm.json")


def test_current_streams_returns_all_five_rungs(fresh_store) -> None:
    streams = current_streams(store=fresh_store)
    rung_names = {s.stream_name for s in streams}
    assert rung_names == {"free", "entry", "core", "expansion", "enterprise"}


def test_portfolio_health_warns_on_concentration(fresh_store) -> None:
    fresh_store.upsert_offer(
        Offer(
            id="off_entry",
            name_ar="ا",
            name_en="Entry",
            rung="entry",
            target_segment="x",
            pain_addressed="y",
            success_metric="z",
            scale_kill_rule="k",
        ),
    )
    fresh_store.upsert_offer(
        Offer(
            id="off_core",
            name_ar="ا",
            name_en="Core",
            rung="core",
            target_segment="x",
            pain_addressed="y",
            success_metric="z",
            scale_kill_rule="k",
        ),
    )
    # 90% of revenue concentrated in one stream.
    record_attribution(
        deal_id="d1",
        revenue_sar=90_000,
        sources={"offer_id": "off_entry"},
        payment_received=True,
        signed_agreement=False,
        store=fresh_store,
    )
    record_attribution(
        deal_id="d2",
        revenue_sar=10_000,
        sources={"offer_id": "off_core"},
        payment_received=True,
        signed_agreement=False,
        store=fresh_store,
    )
    health = portfolio_health(store=fresh_store)
    assert any(w.startswith("single_stream_over_60_pct:entry") for w in health["warnings"])
    assert health["total_revenue_sar"] == pytest.approx(100_000.0)


def test_portfolio_health_warns_missing_streams(fresh_store) -> None:
    health = portfolio_health(store=fresh_store)
    # All rungs empty → all warnings for missing streams.
    missing = [w for w in health["warnings"] if w.startswith("missing_stream:")]
    assert len(missing) == 5
