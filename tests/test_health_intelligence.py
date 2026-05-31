"""Tests for the Health Intelligence API.

Covers: weighted scoring, dimension computation, health tiers,
trend labels, alerts, portfolio, leaderboard, benchmarks, compute endpoint.
"""

from __future__ import annotations

import os
import sys
import types

os.environ.setdefault("ADMIN_API_KEY", "test-admin-key")
os.environ.setdefault("ADMIN_API_KEYS", "test-admin-key")

# Stub jose before importing security-dependent modules
_mock_security = types.ModuleType("api.security.api_key")
_mock_security.require_admin_key = lambda: None
sys.modules.setdefault("api.security.api_key", _mock_security)
if "api.security" not in sys.modules:
    sys.modules["api.security"] = types.ModuleType("api.security")

from api.routers.health_intelligence import (  # noqa: E402
    DIMENSIONS,
    _PORTFOLIO,
    _compute_weighted_score,
    _enrich_client,
    _health_tier,
    _trend_label,
    router,
)
from fastapi import FastAPI  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

app = FastAPI()
app.include_router(router)
client = TestClient(app, headers={"X-Admin-API-Key": "test-admin-key"})


# ---------------------------------------------------------------------------
# Unit: weighted scoring
# ---------------------------------------------------------------------------


class TestWeightedScoring:
    def test_all_100_gives_100(self):
        dims = {d["id"]: 100 for d in DIMENSIONS}
        assert _compute_weighted_score(dims) == 100.0

    def test_all_0_gives_0(self):
        dims = {d["id"]: 0 for d in DIMENSIONS}
        assert _compute_weighted_score(dims) == 0.0

    def test_all_50_gives_50(self):
        dims = {d["id"]: 50 for d in DIMENSIONS}
        assert _compute_weighted_score(dims) == 50.0

    def test_weights_sum_to_1(self):
        total = sum(d["weight"] for d in DIMENSIONS)
        assert abs(total - 1.0) < 0.001

    def test_six_dimensions_present(self):
        assert len(DIMENSIONS) == 6

    def test_missing_dimension_treated_as_zero(self):
        score = _compute_weighted_score({"data_readiness": 100})
        assert 0 < score < 100

    def test_score_bounded_0_100(self):
        dims = {d["id"]: 75 for d in DIMENSIONS}
        score = _compute_weighted_score(dims)
        assert 0 <= score <= 100


class TestHealthTier:
    def test_healthy_at_75(self):
        assert _health_tier(75)["tier"] == "healthy"

    def test_moderate_at_65(self):
        assert _health_tier(65)["tier"] == "moderate"

    def test_at_risk_at_45(self):
        assert _health_tier(45)["tier"] == "at_risk"

    def test_critical_at_30(self):
        assert _health_tier(30)["tier"] == "critical"

    def test_bilingual_labels(self):
        tier = _health_tier(80)
        assert "ar" in tier
        assert "en" in tier

    def test_color_present(self):
        assert "color" in _health_tier(75)
        assert "color" in _health_tier(30)


class TestTrendLabel:
    def test_improving(self):
        label = _trend_label(+7)
        assert "تحسن" in label["ar"]
        assert "improvement" in label["en"].lower()

    def test_stable(self):
        label = _trend_label(0)
        assert "مستقر" in label["ar"]
        assert "Stable" in label["en"]

    def test_declining(self):
        label = _trend_label(-8)
        assert "تراجع" in label["ar"]
        assert "decline" in label["en"].lower()


class TestEnrichClient:
    def _first_client(self):
        return _PORTFOLIO[0]

    def test_enrich_returns_health_score(self):
        result = _enrich_client(self._first_client())
        assert "health_score" in result
        assert 0 <= result["health_score"] <= 100

    def test_enrich_returns_health_tier(self):
        result = _enrich_client(self._first_client())
        assert "health_tier" in result
        assert result["health_tier"]["tier"] in ("healthy", "moderate", "at_risk", "critical")

    def test_enrich_has_bilingual_company(self):
        result = _enrich_client(self._first_client())
        assert "ar" in result["company"]
        assert "en" in result["company"]

    def test_enrich_has_weakest_dimension(self):
        result = _enrich_client(self._first_client())
        assert "weakest_dimension" in result

    def test_enrich_dimensions_count(self):
        result = _enrich_client(self._first_client())
        assert len(result["dimensions"]) == 6


class TestPortfolioDataIntegrity:
    def test_portfolio_not_empty(self):
        assert len(_PORTFOLIO) >= 6

    def test_all_clients_have_6_dimensions(self):
        for client in _PORTFOLIO:
            assert len(client["dimensions"]) == 6, f"Client {client['client_id']} missing dimensions"

    def test_all_scores_in_range(self):
        for client in _PORTFOLIO:
            for dim_id, score in client["dimensions"].items():
                assert 0 <= score <= 100, f"Out-of-range score {score} for {client['client_id']}.{dim_id}"

    def test_at_least_one_at_risk_or_worse_client(self):
        at_risk = [c for c in _PORTFOLIO if _compute_weighted_score(c["dimensions"]) < 55]
        assert len(at_risk) >= 1

    def test_at_least_one_healthy_client(self):
        healthy = [c for c in _PORTFOLIO if _compute_weighted_score(c["dimensions"]) >= 75]
        assert len(healthy) >= 1


# ---------------------------------------------------------------------------
# API integration tests
# ---------------------------------------------------------------------------


class TestPortfolioEndpoint:
    def test_returns_200(self):
        assert client.get("/api/v1/health-intelligence/portfolio").status_code == 200

    def test_governance_decision(self):
        data = client.get("/api/v1/health-intelligence/portfolio").json()
        assert data["governance_decision"] == "ALLOW_WITH_REVIEW"

    def test_portfolio_summary_present(self):
        data = client.get("/api/v1/health-intelligence/portfolio").json()
        summary = data["portfolio_summary"]
        assert "total_clients" in summary
        assert "avg_health_score" in summary
        assert "at_risk_count" in summary

    def test_clients_sorted_descending(self):
        data = client.get("/api/v1/health-intelligence/portfolio").json()
        scores = [c["health_score"] for c in data["clients"]]
        assert scores == sorted(scores, reverse=True)

    def test_clients_have_required_fields(self):
        data = client.get("/api/v1/health-intelligence/portfolio").json()
        for c in data["clients"]:
            assert "health_score" in c
            assert "health_tier" in c
            assert "dimensions" in c
            assert "trend_30d" in c

    def test_dimension_definitions_present(self):
        data = client.get("/api/v1/health-intelligence/portfolio").json()
        assert len(data["dimension_definitions"]) == 6


class TestLeaderboardEndpoint:
    def test_returns_200(self):
        assert client.get("/api/v1/health-intelligence/leaderboard").status_code == 200

    def test_default_top_5(self):
        data = client.get("/api/v1/health-intelligence/leaderboard").json()
        assert len(data["leaderboard"]) == 5

    def test_custom_top_3(self):
        data = client.get("/api/v1/health-intelligence/leaderboard?top=3").json()
        assert len(data["leaderboard"]) == 3

    def test_first_has_top_performer_badge(self):
        data = client.get("/api/v1/health-intelligence/leaderboard").json()
        first = data["leaderboard"][0]
        assert first["badge_en"] == "Top Performer"

    def test_sorted_descending(self):
        data = client.get("/api/v1/health-intelligence/leaderboard").json()
        scores = [c["health_score"] for c in data["leaderboard"]]
        assert scores == sorted(scores, reverse=True)


class TestAlertsEndpoint:
    def test_returns_200(self):
        assert client.get("/api/v1/health-intelligence/alerts").status_code == 200

    def test_governance_decision(self):
        data = client.get("/api/v1/health-intelligence/alerts").json()
        assert data["governance_decision"] == "ALLOW_WITH_REVIEW"

    def test_alert_count_matches_list(self):
        data = client.get("/api/v1/health-intelligence/alerts").json()
        assert data["alert_count"] == len(data["alerts"])

    def test_alerts_have_recommended_actions(self):
        data = client.get("/api/v1/health-intelligence/alerts").json()
        for alert in data["alerts"]:
            assert "recommended_action_ar" in alert
            assert "recommended_action_en" in alert

    def test_alerts_sorted_by_severity(self):
        data = client.get("/api/v1/health-intelligence/alerts").json()
        order = {"critical": 0, "high": 1, "medium": 2}
        severities = [order.get(a["severity"], 9) for a in data["alerts"]]
        assert severities == sorted(severities)


class TestBenchmarksEndpoint:
    def test_returns_200(self):
        assert client.get("/api/v1/health-intelligence/benchmarks").status_code == 200

    def test_has_dealix_avg(self):
        data = client.get("/api/v1/health-intelligence/benchmarks").json()
        assert "dealix_portfolio_avg" in data
        assert data["dealix_portfolio_avg"] > 0

    def test_has_benchmark_comparison(self):
        data = client.get("/api/v1/health-intelligence/benchmarks").json()
        assert "saudi_b2b_benchmark" in data
        assert "dealix_vs_benchmark" in data

    def test_sector_benchmarks_present(self):
        data = client.get("/api/v1/health-intelligence/benchmarks").json()
        assert "technology" in data["sector_benchmarks"]

    def test_disclaimer_bilingual(self):
        data = client.get("/api/v1/health-intelligence/benchmarks").json()
        assert "disclaimer_ar" in data
        assert "disclaimer_en" in data


class TestTrendsEndpoint:
    def test_returns_200(self):
        assert client.get("/api/v1/health-intelligence/trends").status_code == 200

    def test_default_6_months(self):
        data = client.get("/api/v1/health-intelligence/trends").json()
        assert len(data["trend"]) == 6

    def test_custom_12_months(self):
        data = client.get("/api/v1/health-intelligence/trends?months=12").json()
        assert len(data["trend"]) == 12

    def test_trend_has_month_and_score(self):
        data = client.get("/api/v1/health-intelligence/trends").json()
        for t in data["trend"]:
            assert "month" in t
            assert "avg_score" in t


class TestComputeEndpoint:
    def test_returns_200(self):
        r = client.post("/api/v1/health-intelligence/compute", json={"company_name": "Test Co"})
        assert r.status_code == 200

    def test_governance_decision(self):
        data = client.post("/api/v1/health-intelligence/compute", json={"company_name": "Test Co"}).json()
        assert data["governance_decision"] == "ALLOW_WITH_REVIEW"

    def test_score_in_response(self):
        data = client.post("/api/v1/health-intelligence/compute", json={"company_name": "Test Co"}).json()
        assert "health_score" in data
        assert 0 <= data["health_score"] <= 100

    def test_high_scores_recommend_managed_ops_or_custom_ai(self):
        body = {
            "company_name": "Great Co",
            "data_readiness": 90, "onboarding_ops": 90, "delivery_quality": 90,
            "zatca_compliance": 90, "client_retention": 90, "recurring_revenue": 90,
        }
        data = client.post("/api/v1/health-intelligence/compute", json=body).json()
        assert data["recommended_tier_en"] in ("Managed Ops", "Custom AI")

    def test_low_scores_recommend_free_diagnostic(self):
        body = {
            "company_name": "Struggling Co",
            "data_readiness": 20, "onboarding_ops": 20, "delivery_quality": 20,
            "zatca_compliance": 20, "client_retention": 20, "recurring_revenue": 20,
        }
        data = client.post("/api/v1/health-intelligence/compute", json=body).json()
        assert data["recommended_tier_en"] == "Free Diagnostic"

    def test_weakest_dimension_identified(self):
        body = {
            "company_name": "Co",
            "data_readiness": 90, "onboarding_ops": 90, "delivery_quality": 90,
            "zatca_compliance": 10, "client_retention": 90, "recurring_revenue": 90,
        }
        data = client.post("/api/v1/health-intelligence/compute", json=body).json()
        assert data["weakest_dimension"]["id"] == "zatca_compliance"

    def test_benchmark_comparison_present(self):
        data = client.post("/api/v1/health-intelligence/compute", json={"company_name": "X"}).json()
        assert "vs_saudi_b2b_benchmark" in data

    def test_missing_company_name_422(self):
        r = client.post("/api/v1/health-intelligence/compute", json={})
        assert r.status_code == 422
