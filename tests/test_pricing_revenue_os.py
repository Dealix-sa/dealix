"""Tests for the Dealix Pricing & Revenue Operating System.

Pure unit tests — no network, no LLM, no DB. Validates the YAML single source of
truth (VAT, guardrails, ladder), the margin calculator, the quote generator
(drafts only), and the MRR forecast consistency.
"""
from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from scripts.calculate_margin import estimate_cost, evaluate, gross_margin
from scripts.generate_mrr_forecast import summarize as mrr_summarize
from scripts.generate_quote import build_quote, find_offer

_REPO = Path(__file__).resolve().parents[1]
_CONFIG = _REPO / "os" / "config"
_FINANCE = _REPO / "finance"


def _load(rel: str) -> dict:
    return yaml.safe_load((_REPO / rel).read_text(encoding="utf-8"))


# ---------------------------------------------------------------- config files

def test_all_config_files_exist_and_parse() -> None:
    files = [
        "os/config/pricing.yml",
        "os/config/packages.yml",
        "os/config/usage_meters.yml",
        "os/config/discount_policy.yml",
        "os/config/payment_terms.yml",
        "os/config/margin_guardrails.yml",
        "finance/mrr_targets.yml",
        "finance/unit_economics.yml",
    ]
    for f in files:
        data = _load(f)
        assert isinstance(data, dict) and data, f


def test_vat_is_15_percent_and_exclusive() -> None:
    pricing = _load("os/config/pricing.yml")
    assert pricing["vat"]["enabled"] is True
    assert pricing["vat"]["rate"] == 0.15
    assert pricing["price_basis"] == "exclusive_of_vat"


def test_anchor_offers_match_documented_prices() -> None:
    pricing = _load("os/config/pricing.yml")
    packages = _load("os/config/packages.yml")
    assert pricing["entry_offers"]["ai_workflow_audit"]["price"] == 9500
    assert pricing["pilots"]["pilot_pro_api"]["price"] == 60000
    assert packages["packages"]["managed_os"]["price"] == 15000
    assert packages["packages"]["managed_os"]["is_anchor"] is True


def test_no_live_charge_invariant() -> None:
    payment = _load("os/config/payment_terms.yml")
    assert payment["no_live_charge"] is True


def test_subscriptions_require_usage_cap() -> None:
    packages = _load("os/config/packages.yml")
    assert packages["rules"]["no_subscription_without_usage_cap"] is True


# ----------------------------------------------------------------- guardrails

def test_margin_guardrails_floors_raised() -> None:
    g = _load("os/config/margin_guardrails.yml")["margins"]
    assert g["project_gross_margin_min"] == 0.55
    assert g["subscription_gross_margin_min"] == 0.65
    assert g["retainer_gross_margin_min"] == 0.60


def test_margin_calc_passes_and_fails_correctly() -> None:
    ok = evaluate(60000, 21000, "pilot")        # 65% >= 55%
    assert ok["meets_guardrail"] is True
    bad = evaluate(60000, 40000, "pilot")       # 33% < 55%
    assert bad["meets_guardrail"] is False


def test_gross_margin_rejects_zero_revenue() -> None:
    with pytest.raises(ValueError):
        gross_margin(0, 0)


def test_estimate_cost_uses_unit_economics_ratio() -> None:
    unit = _load("finance/unit_economics.yml")
    cost = estimate_cost(100000, "production", unit)
    assert cost == 100000 * unit["assumed_direct_cost_ratio"]["production"]


# ------------------------------------------------------------------- quoting

def test_find_offer_across_groups() -> None:
    pricing = _load("os/config/pricing.yml")
    assert find_offer(pricing, "ai_workflow_audit")[0] == "entry_offers"
    assert find_offer(pricing, "pilot_pro_api")[0] == "pilots"
    assert find_offer(pricing, "maintenance_intelligence_os")[0] == "production"
    assert find_offer(pricing, "does_not_exist") is None


def test_build_quote_computes_vat_and_is_draft() -> None:
    quote, margin = build_quote("pilot_pro_api", "Acme FM", "ar", "managed_os")
    assert "60,000" in quote          # subtotal ex-VAT
    assert "9,000" in quote           # 15% VAT
    assert "69,000" in quote          # total incl VAT
    assert "مسودة" in quote           # draft marker (governance)
    assert margin["meets_guardrail"] is True


# ------------------------------------------------------------------ forecast

def test_mrr_milestones_are_internally_consistent() -> None:
    targets = _load("finance/mrr_targets.yml")
    summary = mrr_summarize(targets)
    assert summary["all_consistent"] is True, [
        m for m in summary["milestones"] if not m["consistent"]
    ]


def test_mrr_first_milestone_is_30k() -> None:
    targets = _load("finance/mrr_targets.yml")
    first = targets["milestones"][0]
    assert first["target_mrr"] == 30000
