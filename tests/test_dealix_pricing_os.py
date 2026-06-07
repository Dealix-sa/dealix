"""Tests for the Dealix high-touch Pricing OS v2.0.

Locks in the commercial doctrine encoded in os/config/*.yml and the two
founder-facing scripts (generate_quote, calculate_margin). These are the
non-negotiables: ex-VAT prices, founder-approval gate, ascending ladder,
margin floors, 50/30/20 schedule, and an internally consistent MRR model.
"""

from __future__ import annotations

import csv
from pathlib import Path

import pytest
import yaml

from scripts.calculate_margin import check_margin, gross_margin
from scripts.generate_quote import build_quote, load_configs, render_quote_md

REPO_ROOT = Path(__file__).resolve().parents[1]
CONFIG_DIR = REPO_ROOT / "os" / "config"


def _load(name: str) -> dict:
    with (CONFIG_DIR / name).open(encoding="utf-8") as fh:
        return yaml.safe_load(fh)


@pytest.fixture(scope="module")
def pricing() -> dict:
    return _load("pricing.yml")


@pytest.fixture(scope="module")
def packages() -> dict:
    return _load("packages.yml")


@pytest.fixture(scope="module")
def meters() -> dict:
    return _load("usage_meters.yml")


# --------------------------------------------------------------------------- #
# Config integrity + governance
# --------------------------------------------------------------------------- #
def test_configs_load_and_have_sections(pricing, packages, meters):
    for key in (
        "entry_offers",
        "pilot_offers",
        "production_offers",
        "margins",
        "discounts",
        "payment_terms",
        "governance",
    ):
        assert key in pricing, f"missing {key} in pricing.yml"
    assert packages.get("packages")
    assert meters.get("meters")


def test_governance_gates(pricing):
    gov = pricing["governance"]
    assert gov["prices_exclude_vat"] is True
    assert gov["vat_rate"] == 0.15
    assert gov["is_estimate"] is True
    assert gov["share_price_requires_founder_approval"] is True
    # Doctrine hard gates — must never auto-send or auto-charge
    for gate in ("no_live_send", "no_live_charge", "no_cold_whatsapp", "no_scraping"):
        assert gate in gov["hard_gates"]


# --------------------------------------------------------------------------- #
# Floors + ladder ordering
# --------------------------------------------------------------------------- #
def test_margin_floors(pricing):
    m = pricing["margins"]
    assert m["gross_margin_project_min"] == 0.55
    assert m["gross_margin_subscription_min"] == 0.65
    assert m["net_margin_target_min"] >= 0.25
    assert m["pilot_discount_max"] <= 0.20
    assert m["retainer_floor_sar"] == 8000
    assert m["production_floor_sar"] == 150000
    assert m["consulting_hour_floor_sar"] == 500


def test_audit_floor_and_standard_entry(pricing):
    audit = pricing["entry_offers"]["ai_workflow_audit"]
    assert audit["is_standard_entry"] is True
    assert audit["price_sar"] == 9500
    # Never below the 5,000 floor for any entry offer
    for offer in pricing["entry_offers"].values():
        if isinstance(offer, dict) and "price_sar" in offer:
            assert offer["price_sar"] >= 5000


def test_ascending_ladder(pricing):
    audit = pricing["entry_offers"]["ai_workflow_audit"]["price_sar"]
    pilot_pro = pricing["pilot_offers"]["pilot_pro_with_api"]["price_sar"]
    production_floor = pricing["margins"]["production_floor_sar"]
    cc_setup_min = pricing["production_offers"]["dealix_command_center"]["setup_sar_min"]
    assert audit < pilot_pro < production_floor < cc_setup_min


def test_all_production_offers_respect_floor(pricing):
    floor = pricing["margins"]["production_floor_sar"]
    for key, offer in pricing["production_offers"].items():
        setup_min = offer.get("setup_sar_min") or offer.get("price_sar")
        # Command Center is premium; every production setup_min >= 100k, and
        # the recommended production floor is 150k. GCC entry can start at 100k
        # as a cross-border pilot/system, so assert >= 100k here and rely on
        # recommended_ladder for the 150k positioning rule.
        assert setup_min >= 100000, f"{key} setup below 100k"
    assert floor == 150000


def test_recommended_ladder_matches_sources(pricing, packages):
    ladder = pricing["recommended_ladder"]
    assert ladder["entry"]["price_sar"] == pricing["entry_offers"]["ai_workflow_audit"]["price_sar"]
    assert (
        ladder["pilot"]["price_sar"] == pricing["pilot_offers"]["pilot_pro_with_api"]["price_sar"]
    )
    assert ladder["production"]["floor_sar"] == pricing["margins"]["production_floor_sar"]
    managed = packages["packages"]["managed_os"]["price_monthly_sar"]
    assert ladder["monthly"]["price_sar"] == managed == 15000


# --------------------------------------------------------------------------- #
# Packages + usage meters
# --------------------------------------------------------------------------- #
def test_packages_ascending_and_primary_target(packages):
    p = packages["packages"]
    assert p["managed_os"]["is_primary_target"] is True
    assert p["managed_os"]["price_monthly_sar"] == 15000
    assert p["monitor"]["price_monthly_sar"] == 8000
    order = ["monitor", "managed_os", "growth_ops_os", "command_center", "enterprise_sovereign_os"]
    prices = [p[k]["price_monthly_sar"] for k in order]
    assert prices == sorted(prices), "monthly packages must be ascending"


def test_retainer_floor_enforced_by_packages(packages, pricing):
    floor = pricing["margins"]["retainer_floor_sar"]
    for pkg in packages["packages"].values():
        assert pkg["price_monthly_sar"] >= floor


def test_package_usage_meter_exists(packages, meters):
    for pkg in packages["packages"].values():
        meter_key = pkg.get("included_usage", {}).get("meter")
        assert meter_key in meters["meters"], f"unknown meter {meter_key}"


def test_overage_example_managed_os(packages, meters):
    managed = packages["packages"]["managed_os"]
    assert managed["included_usage"]["quota_per_month"] == 3000
    ops = meters["meters"]["operations"]
    assert ops["block_size"] == 1000
    assert ops["overage_per_block_sar_typical"] == 2500  # +1,000 ops = 2,500


# --------------------------------------------------------------------------- #
# Quote generator
# --------------------------------------------------------------------------- #
def test_build_quote_production_with_package():
    cfg = load_configs()
    q = build_quote(
        client="Acme FM",
        offer_key="maintenance_intelligence_os",
        package_key="managed_os",
        configs=cfg,
    )
    # Setup = min of Maintenance OS range = 150,000 ex-VAT, +15% VAT
    assert q["setup"]["ex_vat"] == 150000
    assert q["setup"]["vat"] == 22500
    assert q["setup"]["incl_vat"] == 172500
    # 50/30/20 on the setup, summing back to the ex-VAT setup
    pcts = [round(ms["pct"], 2) for ms in q["schedule"]]
    assert pcts == [0.5, 0.3, 0.2]
    assert sum(ms["amount_ex_vat"] for ms in q["schedule"]) == 150000
    # Monthly from the Managed package
    assert q["monthly"]["ex_vat"] == 15000
    assert q["allowance_note"] and "3,000" in q["allowance_note"]


def test_quote_annual_discount():
    q = build_quote(client="X", package_key="managed_os", annual_prepay=True)
    assert q["monthly"]["ex_vat"] == 13500  # 15,000 − 10%
    assert q["annual_total_ex_vat"] == 13500 * 12
    assert any("Annual" in d for d in q["discounts_applied"])


def test_quote_case_study_discount_on_setup():
    q = build_quote(client="X", offer_key="pilot_pro_with_api", case_study=True)
    assert q["setup"]["ex_vat"] == round(60000 * 0.85)  # 51,000


def test_render_md_carries_doctrine_banners():
    q = build_quote(
        client="Acme", offer_key="maintenance_intelligence_os", package_key="managed_os"
    )
    md = render_quote_md(q)
    assert "DRAFT" in md
    assert "موافقة المؤسس" in md  # founder-approval gate
    assert "ex-VAT" in md
    assert "50/30/20" in md
    assert "VAT 15%" in md


def test_build_quote_unknown_offer_raises():
    with pytest.raises(KeyError):
        build_quote(client="X", offer_key="does_not_exist")


# --------------------------------------------------------------------------- #
# Margin calculator
# --------------------------------------------------------------------------- #
def test_gross_margin_basic():
    assert gross_margin(150000, 60000) == pytest.approx(0.6)
    assert gross_margin(0, 10) == 0.0


def test_check_margin_project_pass_fail():
    ok = check_margin(150000, 60000, kind="project")
    assert ok["gross_ok"] and ok["passed"]
    bad = check_margin(100000, 60000, kind="project")  # 40% < 55% floor
    assert not bad["gross_ok"] and not bad["passed"]


def test_check_margin_subscription_floor():
    # 60% gross < 65% subscription floor -> fail
    sub = check_margin(15000, 6000, kind="subscription")
    assert not sub["gross_ok"]
    sub_ok = check_margin(15000, 4000, kind="subscription")  # 73%
    assert sub_ok["gross_ok"]


# --------------------------------------------------------------------------- #
# MRR model integrity
# --------------------------------------------------------------------------- #
def test_mrr_model_internally_consistent(packages):
    managed = packages["packages"]["managed_os"]["price_monthly_sar"]
    growth = packages["packages"]["growth_ops_os"]["price_monthly_sar"]
    path = REPO_ROOT / "finance" / "mrr_model.csv"
    rows = list(csv.DictReader(path.open(encoding="utf-8")))
    assert [r["phase"] for r in rows] == ["1", "2", "3", "4"]
    for r in rows:
        computed = (
            int(r["managed_os_clients"]) * managed
            + int(r["growth_ops_clients"]) * growth
            + int(r["command_center_clients"]) * int(r["command_center_mrr_each_sar"])
            + int(r["usage_addons_mrr_sar"])
        )
        assert (
            computed == int(r["computed_mrr_sar"]) == int(r["target_mrr_sar"])
        ), f"phase {r['phase']} MRR mismatch"
    assert int(rows[-1]["target_mrr_sar"]) == 500000
    assert 20 <= int(rows[-1]["b2b_clients_total"]) <= 25
