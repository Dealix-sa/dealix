"""Tests for api/routers/pricing_intelligence.py.

Covers all five endpoints: market-rates, competitor-landscape,
win-rate-simulator, tier-optimization, and discount-policy.
"""

from __future__ import annotations

import os
import sys
import types

os.environ.setdefault("ADMIN_API_KEY", "test-admin-key")
os.environ.setdefault("ADMIN_API_KEYS", "test-admin-key")
_mock_security = types.ModuleType("api.security.api_key")
_mock_security.require_admin_key = lambda: None  # type: ignore[attr-defined]
sys.modules.setdefault("api.security.api_key", _mock_security)
if "api.security" not in sys.modules:
    sys.modules["api.security"] = types.ModuleType("api.security")

from api.routers.pricing_intelligence import (  # noqa: E402
    WinRateSimulatorInput,
    _predict_win_rate,
    router,
)

from fastapi import FastAPI
from fastapi.testclient import TestClient

app = FastAPI()
app.include_router(router)
client = TestClient(app, headers={"X-Admin-API-Key": "test-admin-key"})

_GOV = "ALLOW_WITH_REVIEW"
_GOV_APPROVAL = "APPROVAL_FIRST"


# ---------------------------------------------------------------------------
# TestMarketRatesEndpoint
# ---------------------------------------------------------------------------


class TestMarketRatesEndpoint:
    def test_market_rates_returns_200(self):
        r = client.get("/api/v1/pricing-intelligence/market-rates")
        assert r.status_code == 200

    def test_market_rates_governance_decision(self):
        body = client.get("/api/v1/pricing-intelligence/market-rates").json()
        assert body["governance_decision"] == _GOV

    def test_market_rates_has_sectors_key(self):
        body = client.get("/api/v1/pricing-intelligence/market-rates").json()
        assert "sectors" in body

    def test_market_rates_sectors_non_empty(self):
        body = client.get("/api/v1/pricing-intelligence/market-rates").json()
        assert len(body["sectors"]) > 0

    def test_market_rates_currency_is_sar(self):
        body = client.get("/api/v1/pricing-intelligence/market-rates").json()
        assert body["currency"] == "SAR"

    def test_market_rates_each_sector_has_market_avg(self):
        body = client.get("/api/v1/pricing-intelligence/market-rates").json()
        for s in body["sectors"]:
            assert "market_avg_sar" in s

    def test_market_rates_each_sector_has_dealix_recommended(self):
        body = client.get("/api/v1/pricing-intelligence/market-rates").json()
        for s in body["sectors"]:
            assert "dealix_recommended_sar" in s

    def test_market_rates_each_sector_has_ar_label(self):
        body = client.get("/api/v1/pricing-intelligence/market-rates").json()
        for s in body["sectors"]:
            assert "sector_ar" in s

    def test_market_rates_recommended_below_market(self):
        body = client.get("/api/v1/pricing-intelligence/market-rates").json()
        for s in body["sectors"]:
            assert s["dealix_recommended_sar"] <= s["market_avg_sar"]

    def test_market_rates_note_en_present(self):
        body = client.get("/api/v1/pricing-intelligence/market-rates").json()
        assert "note_en" in body

    def test_market_rates_note_ar_present(self):
        body = client.get("/api/v1/pricing-intelligence/market-rates").json()
        assert "note_ar" in body

    def test_market_rates_all_prices_positive(self):
        body = client.get("/api/v1/pricing-intelligence/market-rates").json()
        for s in body["sectors"]:
            assert s["market_avg_sar"] > 0
            assert s["dealix_recommended_sar"] > 0


# ---------------------------------------------------------------------------
# TestCompetitorLandscapeEndpoint
# ---------------------------------------------------------------------------


class TestCompetitorLandscapeEndpoint:
    def test_competitor_landscape_returns_200(self):
        r = client.get("/api/v1/pricing-intelligence/competitor-landscape")
        assert r.status_code == 200

    def test_competitor_landscape_governance_decision(self):
        body = client.get("/api/v1/pricing-intelligence/competitor-landscape").json()
        assert body["governance_decision"] == _GOV

    def test_competitor_landscape_has_competitors_key(self):
        body = client.get("/api/v1/pricing-intelligence/competitor-landscape").json()
        assert "competitors" in body

    def test_competitor_landscape_five_competitors(self):
        body = client.get("/api/v1/pricing-intelligence/competitor-landscape").json()
        assert len(body["competitors"]) == 5

    def test_competitor_landscape_each_has_name(self):
        body = client.get("/api/v1/pricing-intelligence/competitor-landscape").json()
        for c in body["competitors"]:
            assert "name" in c

    def test_competitor_landscape_each_has_entry_price(self):
        body = client.get("/api/v1/pricing-intelligence/competitor-landscape").json()
        for c in body["competitors"]:
            assert "entry_price_sar" in c

    def test_competitor_landscape_each_has_bilingual_positioning(self):
        body = client.get("/api/v1/pricing-intelligence/competitor-landscape").json()
        for c in body["competitors"]:
            assert "positioning_en" in c
            assert "positioning_ar" in c

    def test_competitor_landscape_each_has_strength_en(self):
        body = client.get("/api/v1/pricing-intelligence/competitor-landscape").json()
        for c in body["competitors"]:
            assert "strength_en" in c

    def test_competitor_landscape_each_has_weakness_en(self):
        body = client.get("/api/v1/pricing-intelligence/competitor-landscape").json()
        for c in body["competitors"]:
            assert "weakness_en" in c

    def test_competitor_landscape_disclaimer_present(self):
        body = client.get("/api/v1/pricing-intelligence/competitor-landscape").json()
        assert "disclaimer_en" in body

    def test_competitor_landscape_no_real_company_names(self):
        body = client.get("/api/v1/pricing-intelligence/competitor-landscape").json()
        real_names = {"salesforce", "hubspot", "oracle", "sap", "zoho"}
        for c in body["competitors"]:
            assert c["name"].lower() not in real_names


# ---------------------------------------------------------------------------
# TestWinRateSimulatorEndpoint
# ---------------------------------------------------------------------------


class TestWinRateSimulatorEndpoint:
    _BASE_BODY = {
        "proposed_price_sar": 3000.0,
        "sector": "technology",
        "company_size": "sme",
    }

    def test_win_rate_simulator_returns_200(self):
        r = client.post(
            "/api/v1/pricing-intelligence/win-rate-simulator", json=self._BASE_BODY
        )
        assert r.status_code == 200

    def test_win_rate_simulator_governance_decision(self):
        body = client.post(
            "/api/v1/pricing-intelligence/win-rate-simulator", json=self._BASE_BODY
        ).json()
        assert body["governance_decision"] == _GOV

    def test_win_rate_simulator_has_predicted_win_rate(self):
        body = client.post(
            "/api/v1/pricing-intelligence/win-rate-simulator", json=self._BASE_BODY
        ).json()
        assert "predicted_win_rate" in body

    def test_win_rate_in_valid_range(self):
        body = client.post(
            "/api/v1/pricing-intelligence/win-rate-simulator", json=self._BASE_BODY
        ).json()
        assert 0.0 <= body["predicted_win_rate"] <= 1.0

    def test_win_rate_has_confidence(self):
        body = client.post(
            "/api/v1/pricing-intelligence/win-rate-simulator", json=self._BASE_BODY
        ).json()
        assert "confidence" in body

    def test_win_rate_confidence_in_valid_range(self):
        body = client.post(
            "/api/v1/pricing-intelligence/win-rate-simulator", json=self._BASE_BODY
        ).json()
        assert 0.0 <= body["confidence"] <= 1.0

    def test_win_rate_has_recommended_range_en(self):
        body = client.post(
            "/api/v1/pricing-intelligence/win-rate-simulator", json=self._BASE_BODY
        ).json()
        assert "recommended_range_en" in body

    def test_win_rate_has_recommended_range_ar(self):
        body = client.post(
            "/api/v1/pricing-intelligence/win-rate-simulator", json=self._BASE_BODY
        ).json()
        assert "recommended_range_ar" in body

    def test_win_rate_note_en_mentions_not_guarantee(self):
        body = client.post(
            "/api/v1/pricing-intelligence/win-rate-simulator", json=self._BASE_BODY
        ).json()
        assert "guarantee" in body["note_en"].lower()

    def test_win_rate_missing_sector_returns_422(self):
        r = client.post(
            "/api/v1/pricing-intelligence/win-rate-simulator",
            json={"proposed_price_sar": 3000.0, "company_size": "sme"},
        )
        assert r.status_code == 422

    def test_win_rate_negative_price_returns_422(self):
        r = client.post(
            "/api/v1/pricing-intelligence/win-rate-simulator",
            json={"proposed_price_sar": -1, "sector": "technology", "company_size": "sme"},
        )
        assert r.status_code == 422

    def test_win_rate_pure_function_returns_dict(self):
        result = _predict_win_rate(3000.0, "technology", "sme")
        assert isinstance(result, dict)

    def test_win_rate_pure_function_rate_in_range(self):
        result = _predict_win_rate(3000.0, "technology", "sme")
        assert 0.0 <= result["predicted_win_rate"] <= 1.0

    def test_win_rate_pure_function_has_sector_avg(self):
        result = _predict_win_rate(3000.0, "technology", "sme")
        assert "sector_avg_deal_sar" in result


# ---------------------------------------------------------------------------
# TestTierOptimizationEndpoint
# ---------------------------------------------------------------------------


class TestTierOptimizationEndpoint:
    def test_tier_optimization_returns_200(self):
        r = client.get("/api/v1/pricing-intelligence/tier-optimization")
        assert r.status_code == 200

    def test_tier_optimization_governance_decision(self):
        body = client.get("/api/v1/pricing-intelligence/tier-optimization").json()
        assert body["governance_decision"] == _GOV

    def test_tier_optimization_has_tiers_key(self):
        body = client.get("/api/v1/pricing-intelligence/tier-optimization").json()
        assert "tiers" in body

    def test_tier_optimization_five_tiers(self):
        body = client.get("/api/v1/pricing-intelligence/tier-optimization").json()
        assert len(body["tiers"]) == 5

    def test_tier_optimization_each_tier_has_floor(self):
        body = client.get("/api/v1/pricing-intelligence/tier-optimization").json()
        for t in body["tiers"]:
            assert "floor_sar" in t

    def test_tier_optimization_each_tier_has_ceiling(self):
        body = client.get("/api/v1/pricing-intelligence/tier-optimization").json()
        for t in body["tiers"]:
            assert "ceiling_sar" in t

    def test_tier_optimization_each_tier_has_upsell_trigger(self):
        body = client.get("/api/v1/pricing-intelligence/tier-optimization").json()
        for t in body["tiers"]:
            assert "upsell_trigger_score" in t

    def test_tier_optimization_floor_below_ceiling(self):
        body = client.get("/api/v1/pricing-intelligence/tier-optimization").json()
        for t in body["tiers"]:
            assert t["floor_sar"] < t["ceiling_sar"]

    def test_tier_optimization_upsell_trigger_in_range(self):
        body = client.get("/api/v1/pricing-intelligence/tier-optimization").json()
        for t in body["tiers"]:
            assert 0 <= t["upsell_trigger_score"] <= 100

    def test_tier_optimization_methodology_en_present(self):
        body = client.get("/api/v1/pricing-intelligence/tier-optimization").json()
        assert "methodology_en" in body

    def test_tier_optimization_methodology_ar_present(self):
        body = client.get("/api/v1/pricing-intelligence/tier-optimization").json()
        assert "methodology_ar" in body


# ---------------------------------------------------------------------------
# TestDiscountPolicyEndpoint
# ---------------------------------------------------------------------------


class TestDiscountPolicyEndpoint:
    def test_discount_policy_returns_200(self):
        r = client.get("/api/v1/pricing-intelligence/discount-policy")
        assert r.status_code == 200

    def test_discount_policy_governance_is_approval_first(self):
        body = client.get("/api/v1/pricing-intelligence/discount-policy").json()
        assert body["governance_decision"] == _GOV_APPROVAL

    def test_discount_policy_has_discount_policy_key(self):
        body = client.get("/api/v1/pricing-intelligence/discount-policy").json()
        assert "discount_policy" in body

    def test_discount_policy_five_entries(self):
        body = client.get("/api/v1/pricing-intelligence/discount-policy").json()
        assert len(body["discount_policy"]) == 5

    def test_discount_policy_each_requires_approval(self):
        body = client.get("/api/v1/pricing-intelligence/discount-policy").json()
        for entry in body["discount_policy"]:
            assert entry["requires_approval"] is True

    def test_discount_policy_each_has_max_discount_pct(self):
        body = client.get("/api/v1/pricing-intelligence/discount-policy").json()
        for entry in body["discount_policy"]:
            assert "max_discount_pct" in entry

    def test_discount_policy_max_discounts_reasonable(self):
        body = client.get("/api/v1/pricing-intelligence/discount-policy").json()
        for entry in body["discount_policy"]:
            assert 0 < entry["max_discount_pct"] <= 30

    def test_discount_policy_hard_gate_en_present(self):
        body = client.get("/api/v1/pricing-intelligence/discount-policy").json()
        assert "hard_gate_en" in body

    def test_discount_policy_hard_gate_ar_present(self):
        body = client.get("/api/v1/pricing-intelligence/discount-policy").json()
        assert "hard_gate_ar" in body

    def test_discount_policy_policy_en_present(self):
        body = client.get("/api/v1/pricing-intelligence/discount-policy").json()
        assert "policy_en" in body

    def test_discount_policy_policy_ar_present(self):
        body = client.get("/api/v1/pricing-intelligence/discount-policy").json()
        assert "policy_ar" in body
