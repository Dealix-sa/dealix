"""Distribution OS — catalog surface reuses the existing product ladder."""

from __future__ import annotations

from auto_client_acquisition.distribution_os import catalog
from autonomous_growth.product_catalog import PRODUCT_CATALOG


def test_all_products_match_existing_catalog() -> None:
    ids = {p.id for p in catalog.all_products()}
    assert ids == {p.id for p in PRODUCT_CATALOG.values()}
    # ladder order is rung 0 → 4
    ladder = catalog.all_products()
    assert ladder[0].id == "prod_diagnostic_v1"
    assert ladder[-1].id == "prod_custom_ai_v1"


def test_price_band_reads_from_catalog_not_invented() -> None:
    assert catalog.price_band("prod_sprint_v1") == (499, 499)
    assert catalog.price_band("prod_managed_ops_v1") == (2999, 4999)
    assert catalog.price_band("prod_custom_ai_v1") == (5000, 25000)


def test_unknown_product_id_is_invalid() -> None:
    assert catalog.is_valid_product_id("prod_sprint_v1") is True
    assert catalog.is_valid_product_id("prod_made_up") is False


def test_next_rung_is_the_upsell() -> None:
    assert catalog.next_rung("prod_diagnostic_v1").id == "prod_sprint_v1"
    assert catalog.next_rung("prod_custom_ai_v1") is None


def test_ladder_summary_serialisable() -> None:
    summary = catalog.ladder_summary()
    assert len(summary) == 5
    assert summary[0]["rung"] == 0
    assert all("price_min_sar" in row and "price_max_sar" in row for row in summary)
