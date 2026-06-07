"""Single-source-of-truth guard for offers & pricing (Article 11).

The registry ``auto_client_acquisition/service_catalog/registry.py`` is the ONE
place prices live. This test locks:
  1. the 7 canonical offerings + their prices match the doctrine numbers, and
  2. the exported ``landing/assets/data/services-catalog.json`` matches the
     in-code registry (the same invariant the CI drift gate enforces).
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from auto_client_acquisition.service_catalog.registry import get_offering, list_offerings
from scripts.dealix_export_service_catalog_json import build_catalog_dict, check_json

# Canonical ladder — docs/OFFER_LADDER_AND_PRICING.md + registry base prices.
EXPECTED = {
    "free_mini_diagnostic": (0.0, "one_time"),
    "revenue_proof_sprint_499": (499.0, "one_time"),
    "data_to_revenue_pack_1500": (1500.0, "one_time"),
    "growth_ops_monthly_2999": (2999.0, "per_month"),
    "support_os_addon_1500": (1500.0, "per_month"),
    "executive_command_center_7500": (7500.0, "per_month"),
    "agency_partner_os": (0.0, "custom"),
}


def test_registry_has_exactly_the_canonical_offerings():
    ids = {o.id for o in list_offerings()}
    assert ids == set(EXPECTED), f"offering set drifted: {ids ^ set(EXPECTED)}"


def test_registry_prices_match_canonical():
    for oid, (price, unit) in EXPECTED.items():
        o = get_offering(oid)
        assert o is not None, f"missing offering {oid}"
        assert o.price_sar == price, f"{oid}: price {o.price_sar} != {price}"
        assert o.price_unit == unit, f"{oid}: unit {o.price_unit} != {unit}"


def test_no_outlier_25000_tier():
    """The wrong 5,000–25,000 'enterprise' tier must not reappear in the catalog."""
    for o in list_offerings():
        assert o.price_sar <= 7500.0 or o.price_unit == "custom", (
            f"unexpected high fixed price on {o.id}: {o.price_sar}"
        )


def test_exported_json_matches_registry():
    """The committed services-catalog.json must equal the in-code registry
    (mirror of the CI 'Service Catalog single-source drift gate')."""
    assert check_json(build_catalog_dict()), (
        "landing/assets/data/services-catalog.json is stale — run "
        "`python scripts/dealix_export_service_catalog_json.py` and commit."
    )
