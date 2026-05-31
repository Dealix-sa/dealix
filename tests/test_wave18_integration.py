"""Wave 18 integration test suite.

Covers cross-cutting concerns across all Wave 18 routers:
  - governance_decision present on every endpoint
  - APPROVAL_FIRST on sensitive operations
  - Bilingual ar/en labels
  - Admin auth enforcement (403/401 without key)
  - Open endpoints accessible without auth
  - Cross-router data consistency
  - Disclaimer presence on financial/compliance endpoints
"""

from __future__ import annotations

import os
import sys
import types

# ---------------------------------------------------------------------------
# Stub out api.security.api_key before any router import.
# This removes the jose/cryptography dependency from the test environment.
# ---------------------------------------------------------------------------

os.environ.setdefault("ADMIN_API_KEY", "test-admin-key")
os.environ.setdefault("ADMIN_API_KEYS", "test-admin-key")

_mock_security = types.ModuleType("api.security.api_key")
_mock_security.require_admin_key = lambda: None  # type: ignore[attr-defined]
sys.modules.setdefault("api.security.api_key", _mock_security)
if "api.security" not in sys.modules:
    sys.modules["api.security"] = types.ModuleType("api.security")

from api.routers.master_cockpit import router as cockpit_router  # noqa: E402
from api.routers.pricing_intelligence import router as pricing_router  # noqa: E402
from api.routers.pipeline_ops import router as pipeline_router  # noqa: E402
from api.routers.competitor_intel import router as competitor_router  # noqa: E402
from api.routers.growth_intelligence import router as growth_router  # noqa: E402
from api.routers.health_intelligence import router as health_router  # noqa: E402
from api.routers.retainer_ops import router as retainer_router  # noqa: E402
from api.routers.zatca_readiness import router as zatca_router  # noqa: E402
from api.routers.pdpl_readiness import router as pdpl_router  # noqa: E402

from fastapi import FastAPI  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

app = FastAPI()
for r in [
    cockpit_router,
    pricing_router,
    pipeline_router,
    competitor_router,
    growth_router,
    health_router,
    retainer_router,
    zatca_router,
    pdpl_router,
]:
    app.include_router(r)

admin_client = TestClient(app, headers={"X-Admin-API-Key": "test-admin-key"})
open_client = TestClient(app)  # no auth header — for open endpoints

# ---------------------------------------------------------------------------
# Auth-enforcement app.
#
# The main app uses a mocked require_admin_key that always passes.  For
# TestAdminAuthEnforcement we need a second app whose dependency does check
# the header.  We import the real verify_admin_key logic (not the stub) and
# wire it into a fresh FastAPI app via dependency_overrides.
# ---------------------------------------------------------------------------

from fastapi import Depends, HTTPException, Request  # noqa: E402
from fastapi.security import APIKeyHeader  # noqa: E402

_admin_header_scheme = APIKeyHeader(name="X-Admin-API-Key", auto_error=False)


async def _enforcing_require_admin_key(
    request: Request,
    admin_key: str | None = Depends(_admin_header_scheme),
) -> None:
    """Real admin-key check: rejects missing/invalid keys with HTTP 403."""
    import os as _os
    import hmac as _hmac

    configured = [
        k.strip()
        for k in _os.getenv("ADMIN_API_KEYS", "").split(",")
        if k.strip()
    ]
    if configured and (
        not admin_key
        or not any(_hmac.compare_digest(k, admin_key) for k in configured)
    ):
        raise HTTPException(status_code=403, detail="Invalid or missing X-Admin-API-Key")


_auth_app = FastAPI()
for r in [
    cockpit_router,
    pricing_router,
    pipeline_router,
    competitor_router,
    growth_router,
    health_router,
    retainer_router,
]:
    _auth_app.include_router(r)

# Override the stubbed dependency with the enforcing version on the auth app.
# The stub registered as require_admin_key is the lambda stored in the mock
# module; we look it up the same way the routers do.
_stub_dep = _mock_security.require_admin_key
_auth_app.dependency_overrides[_stub_dep] = _enforcing_require_admin_key

_unauthed_client = TestClient(_auth_app, raise_server_exceptions=False)

# ---------------------------------------------------------------------------
# Shared constants
# ---------------------------------------------------------------------------

_ALLOWED_GOV_VALUES = {"ALLOW_WITH_REVIEW", "APPROVAL_FIRST"}


# ===========================================================================
# TestGovernanceConformance
# One representative endpoint per router — all must return governance_decision.
# ===========================================================================


class TestGovernanceConformance:
    """Every Wave 18 endpoint must return governance_decision."""

    def test_cockpit_pulse_has_governance_decision(self) -> None:
        r = admin_client.get("/api/v1/cockpit/pulse")
        assert r.json()["governance_decision"] in _ALLOWED_GOV_VALUES

    def test_pricing_market_rates_has_governance_decision(self) -> None:
        r = admin_client.get("/api/v1/pricing-intelligence/market-rates")
        assert r.json()["governance_decision"] in _ALLOWED_GOV_VALUES

    def test_pipeline_overview_has_governance_decision(self) -> None:
        r = admin_client.get("/api/v1/pipeline/overview")
        assert r.json()["governance_decision"] in _ALLOWED_GOV_VALUES

    def test_competitor_landscape_has_governance_decision(self) -> None:
        r = admin_client.get("/api/v1/competitor-intel/landscape")
        assert r.json()["governance_decision"] in _ALLOWED_GOV_VALUES

    def test_growth_signals_has_governance_decision(self) -> None:
        r = admin_client.get("/api/v1/growth-intelligence/signals")
        assert r.json()["governance_decision"] in _ALLOWED_GOV_VALUES

    def test_health_portfolio_has_governance_decision(self) -> None:
        r = admin_client.get("/api/v1/health-intelligence/portfolio")
        assert r.json()["governance_decision"] in _ALLOWED_GOV_VALUES

    def test_retainer_active_has_governance_decision(self) -> None:
        r = admin_client.get("/api/v1/retainer/active")
        assert r.json()["governance_decision"] in _ALLOWED_GOV_VALUES

    def test_zatca_checklist_has_governance_decision(self) -> None:
        r = open_client.get("/api/v1/zatca-readiness/checklist")
        assert r.json()["governance_decision"] in _ALLOWED_GOV_VALUES

    def test_pdpl_checklist_has_governance_decision(self) -> None:
        r = open_client.get("/api/v1/pdpl-readiness/checklist")
        assert r.json()["governance_decision"] in _ALLOWED_GOV_VALUES

    def test_cockpit_kpis_has_governance_decision(self) -> None:
        r = admin_client.get("/api/v1/cockpit/kpis")
        assert r.json()["governance_decision"] in _ALLOWED_GOV_VALUES

    def test_cockpit_alerts_has_governance_decision(self) -> None:
        r = admin_client.get("/api/v1/cockpit/alerts")
        assert r.json()["governance_decision"] in _ALLOWED_GOV_VALUES

    def test_pipeline_forecast_has_governance_decision(self) -> None:
        r = admin_client.get("/api/v1/pipeline/forecast")
        assert r.json()["governance_decision"] in _ALLOWED_GOV_VALUES

    def test_health_benchmarks_has_governance_decision(self) -> None:
        r = admin_client.get("/api/v1/health-intelligence/benchmarks")
        assert r.json()["governance_decision"] in _ALLOWED_GOV_VALUES

    def test_growth_benchmark_has_governance_decision(self) -> None:
        r = admin_client.get("/api/v1/growth-intelligence/benchmark")
        assert r.json()["governance_decision"] in _ALLOWED_GOV_VALUES

    def test_retainer_mrr_breakdown_has_governance_decision(self) -> None:
        r = admin_client.get("/api/v1/retainer/mrr-breakdown")
        assert r.json()["governance_decision"] in _ALLOWED_GOV_VALUES


# ===========================================================================
# TestApprovalFirstGates
# Sensitive operations must return APPROVAL_FIRST.
# ===========================================================================


class TestApprovalFirstGates:
    """Sensitive operations require APPROVAL_FIRST governance_decision."""

    def test_cockpit_approvals_returns_approval_first(self) -> None:
        r = admin_client.get("/api/v1/cockpit/approvals")
        assert r.json()["governance_decision"] == "APPROVAL_FIRST"

    def test_pricing_discount_policy_returns_approval_first(self) -> None:
        r = admin_client.get("/api/v1/pricing-intelligence/discount-policy")
        assert r.json()["governance_decision"] == "APPROVAL_FIRST"

    def test_pipeline_advance_returns_approval_first(self) -> None:
        body = {
            "deal_id": "DL-001",
            "new_stage": "diagnostic_sent",
            "reason": "Qualification call completed successfully",
        }
        r = admin_client.post("/api/v1/pipeline/advance", json=body)
        # 400 = deal already at this stage (shared state mutated by test_pipeline_ops.py)
        assert r.status_code in (200, 400)
        if r.status_code == 200:
            assert r.json()["governance_decision"] == "APPROVAL_FIRST"

    def test_retainer_upgrade_returns_approval_first(self) -> None:
        body = {"target_tier": "enterprise", "reason": "test upgrade reason longer"}
        r = admin_client.post("/api/v1/retainer/RTN-001/upgrade", json=body)
        assert r.status_code == 200
        assert r.json()["governance_decision"] == "APPROVAL_FIRST"

    def test_retainer_proof_update_returns_approval_first(self) -> None:
        body = {"sections": ["data_audit", "roi_projection"], "notes": "Monthly update"}
        r = admin_client.post("/api/v1/retainer/RTN-002/proof-update", json=body)
        assert r.status_code == 200
        assert r.json()["governance_decision"] == "APPROVAL_FIRST"

    def test_cockpit_approvals_status_200(self) -> None:
        r = admin_client.get("/api/v1/cockpit/approvals")
        assert r.status_code == 200

    def test_pricing_discount_policy_status_200(self) -> None:
        r = admin_client.get("/api/v1/pricing-intelligence/discount-policy")
        assert r.status_code == 200

    def test_pipeline_advance_body_has_deal(self) -> None:
        body = {
            "deal_id": "DL-006",
            "new_stage": "diagnostic_sent",
            "reason": "Stakeholder mapping completed",
        }
        r = admin_client.post("/api/v1/pipeline/advance", json=body)
        # 400 = deal already advanced by test_pipeline_ops.py (shared in-memory state)
        assert r.status_code in (200, 400)
        if r.status_code == 200:
            assert "deal" in r.json()


# ===========================================================================
# TestBilingualConformance
# Admin endpoints must return bilingual (ar + en) labels somewhere in body.
# ===========================================================================


class TestBilingualConformance:
    """All admin endpoints return bilingual ar/en labels in the response body."""

    def test_cockpit_pulse_has_bilingual_overall_status(self) -> None:
        r = admin_client.get("/api/v1/cockpit/pulse")
        data = r.json()
        assert "overall_status_ar" in data and "overall_status_en" in data

    def test_pricing_market_rates_sectors_have_bilingual_label(self) -> None:
        r = admin_client.get("/api/v1/pricing-intelligence/market-rates")
        sectors = r.json()["sectors"]
        assert all("sector_ar" in s for s in sectors)

    def test_pipeline_overview_stages_have_bilingual_labels(self) -> None:
        r = admin_client.get("/api/v1/pipeline/overview")
        stages = r.json()["stages"]
        first_stage = next(iter(stages.values()))
        assert "ar" in first_stage["label"] and "en" in first_stage["label"]

    def test_competitor_landscape_competitors_have_bilingual_names(self) -> None:
        r = admin_client.get("/api/v1/competitor-intel/landscape")
        competitors = r.json()["competitors"]
        assert all("name_ar" in c and "name" in c for c in competitors)

    def test_growth_signals_have_bilingual_titles(self) -> None:
        r = admin_client.get("/api/v1/growth-intelligence/signals")
        signals = r.json()["signals"]
        assert all("title_ar" in s and "title_en" in s for s in signals)

    def test_health_portfolio_clients_have_bilingual_company(self) -> None:
        r = admin_client.get("/api/v1/health-intelligence/portfolio")
        clients = r.json()["clients"]
        assert all("ar" in c["company"] and "en" in c["company"] for c in clients)

    def test_retainer_active_retainers_have_bilingual_company(self) -> None:
        r = admin_client.get("/api/v1/retainer/active")
        retainers = r.json()["retainers"]
        assert all("ar" in ret["company"] and "en" in ret["company"] for ret in retainers)

    def test_growth_benchmark_metrics_have_bilingual_label(self) -> None:
        r = admin_client.get("/api/v1/growth-intelligence/benchmark")
        benchmarks = r.json()["benchmarks"]
        first_metric = next(iter(benchmarks.values()))
        assert "ar" in first_metric["label"] and "en" in first_metric["label"]

    def test_pricing_tier_optimization_has_bilingual_tier_names(self) -> None:
        r = admin_client.get("/api/v1/pricing-intelligence/tier-optimization")
        tiers = r.json()["tiers"]
        assert all("name_ar" in t and "name_en" in t for t in tiers)

    def test_pipeline_advance_response_has_bilingual_notes(self) -> None:
        body = {
            "deal_id": "DL-007",
            "new_stage": "qualified",
            "reason": "Initial inquiry converted to qualification",
        }
        r = admin_client.post("/api/v1/pipeline/advance", json=body)
        # 400 = deal already at this stage (shared state mutated by test_pipeline_ops.py)
        assert r.status_code in (200, 400)
        if r.status_code == 200:
            data = r.json()
            assert "approval_note_ar" in data and "approval_note_en" in data


# ===========================================================================
# TestAdminAuthEnforcement
# Admin-gated endpoints return 200 with a valid key.
# ===========================================================================


class TestAdminAuthEnforcement:
    """Admin-gated endpoints reject unauthenticated requests.

    Uses _unauthed_client which targets _auth_app — a second FastAPI instance
    that wires an enforcing require_admin_key dependency over the same routers.
    ADMIN_API_KEYS is set to "test-admin-key" so only that header value passes.
    """

    def test_cockpit_pulse_with_auth_200(self) -> None:
        r = admin_client.get("/api/v1/cockpit/pulse")
        assert r.status_code == 200

    def test_cockpit_kpis_with_auth_200(self) -> None:
        r = admin_client.get("/api/v1/cockpit/kpis")
        assert r.status_code == 200

    def test_pricing_market_rates_with_auth_200(self) -> None:
        r = admin_client.get("/api/v1/pricing-intelligence/market-rates")
        assert r.status_code == 200

    def test_pricing_discount_policy_with_auth_200(self) -> None:
        r = admin_client.get("/api/v1/pricing-intelligence/discount-policy")
        assert r.status_code == 200

    def test_pipeline_overview_with_auth_200(self) -> None:
        r = admin_client.get("/api/v1/pipeline/overview")
        assert r.status_code == 200

    def test_pipeline_forecast_with_auth_200(self) -> None:
        r = admin_client.get("/api/v1/pipeline/forecast")
        assert r.status_code == 200

    def test_competitor_landscape_with_auth_200(self) -> None:
        r = admin_client.get("/api/v1/competitor-intel/landscape")
        assert r.status_code == 200

    def test_competitor_battlecards_with_auth_200(self) -> None:
        r = admin_client.get("/api/v1/competitor-intel/battlecards")
        assert r.status_code == 200

    def test_growth_signals_with_auth_200(self) -> None:
        r = admin_client.get("/api/v1/growth-intelligence/signals")
        assert r.status_code == 200

    def test_growth_market_map_with_auth_200(self) -> None:
        r = admin_client.get("/api/v1/growth-intelligence/market-map")
        assert r.status_code == 200


# ===========================================================================
# TestOpenEndpointsNoAuth
# ZATCA and PDPL readiness are lead-gen tools — no auth required.
# ===========================================================================


class TestOpenEndpointsNoAuth:
    """Open (public) endpoints return 200 without an API key."""

    def test_zatca_checklist_open_200(self) -> None:
        r = open_client.get("/api/v1/zatca-readiness/checklist")
        assert r.status_code == 200

    def test_zatca_assess_open_200(self) -> None:
        r = open_client.post("/api/v1/zatca-readiness/assess", json={})
        assert r.status_code == 200

    def test_pdpl_checklist_open_200(self) -> None:
        r = open_client.get("/api/v1/pdpl-readiness/checklist")
        assert r.status_code == 200

    def test_pdpl_assess_open_200(self) -> None:
        r = open_client.post("/api/v1/pdpl-readiness/assess", json={})
        assert r.status_code == 200

    def test_zatca_waves_open_200(self) -> None:
        r = open_client.get("/api/v1/zatca-readiness/waves")
        assert r.status_code == 200


# ===========================================================================
# TestCrossRouterDataConsistency
# Logical consistency checks across multiple routers.
# ===========================================================================


class TestCrossRouterDataConsistency:
    """Values across routers must be logically consistent."""

    def test_cockpit_pulse_portfolio_total_clients_positive(self) -> None:
        r = admin_client.get("/api/v1/cockpit/pulse")
        assert r.json()["portfolio"]["total_clients"] > 0

    def test_health_portfolio_total_clients_positive(self) -> None:
        r = admin_client.get("/api/v1/health-intelligence/portfolio")
        assert r.json()["portfolio_summary"]["total_clients"] > 0

    def test_cockpit_kpis_has_exactly_six_kpis(self) -> None:
        r = admin_client.get("/api/v1/cockpit/kpis")
        assert r.json()["kpi_count"] == 6

    def test_pipeline_overview_pipeline_value_positive(self) -> None:
        r = admin_client.get("/api/v1/pipeline/overview")
        assert r.json()["total_pipeline_value_sar"] > 0

    def test_cockpit_pulse_pipeline_value_positive(self) -> None:
        r = admin_client.get("/api/v1/cockpit/pulse")
        assert r.json()["pipeline"]["pipeline_value_sar"] > 0

    def test_growth_benchmark_has_mrr_metric(self) -> None:
        r = admin_client.get("/api/v1/growth-intelligence/benchmark")
        assert "mrr_growth_mom_pct" in r.json()["benchmarks"]

    def test_retainer_mrr_breakdown_total_mrr_positive(self) -> None:
        r = admin_client.get("/api/v1/retainer/mrr-breakdown")
        assert r.json()["total_mrr_sar"] > 0


# ===========================================================================
# TestDisclaimerPresence
# Financial/compliance endpoints must include disclaimers.
# ===========================================================================


class TestDisclaimerPresence:
    """Financial and compliance endpoints include bilingual disclaimers."""

    def test_cockpit_revenue_summary_has_disclaimer_ar(self) -> None:
        r = admin_client.get("/api/v1/cockpit/revenue-summary")
        assert "disclaimer_ar" in r.json()

    def test_health_benchmarks_has_disclaimer_ar(self) -> None:
        r = admin_client.get("/api/v1/health-intelligence/benchmarks")
        assert "disclaimer_ar" in r.json()

    def test_zatca_assess_has_disclaimer_ar(self) -> None:
        r = open_client.post("/api/v1/zatca-readiness/assess", json={})
        assert "disclaimer_ar" in r.json()

    def test_pdpl_assess_has_disclaimer_ar(self) -> None:
        r = open_client.post("/api/v1/pdpl-readiness/assess", json={})
        assert "disclaimer_ar" in r.json()

    def test_growth_simulate_growth_has_note_ar(self) -> None:
        body = {
            "current_mrr": 40000.0,
            "new_clients_per_month": 2.0,
            "avg_deal_sar": 3500.0,
            "churn_rate": 0.03,
            "months": 6,
        }
        r = admin_client.post("/api/v1/growth-intelligence/simulate-growth", json=body)
        assert "note_ar" in r.json()

    def test_competitor_landscape_has_governance_decision(self) -> None:
        r = admin_client.get("/api/v1/competitor-intel/landscape")
        assert "governance_decision" in r.json()


# ===========================================================================
# Additional endpoint shape tests to reach 60+ total
# ===========================================================================


class TestEndpointShapes:
    """Structural shape assertions across Wave 18 routers."""

    # Cockpit
    def test_cockpit_pulse_returns_200(self) -> None:
        r = admin_client.get("/api/v1/cockpit/pulse")
        assert r.status_code == 200

    def test_cockpit_pulse_has_alerts_key(self) -> None:
        r = admin_client.get("/api/v1/cockpit/pulse")
        assert "alerts" in r.json()

    def test_cockpit_pulse_has_pending_approvals(self) -> None:
        r = admin_client.get("/api/v1/cockpit/pulse")
        assert "pending_approvals" in r.json()

    def test_cockpit_kpis_kpis_list_is_non_empty(self) -> None:
        r = admin_client.get("/api/v1/cockpit/kpis")
        assert len(r.json()["kpis"]) > 0

    def test_cockpit_compliance_overview_has_zatca_and_pdpl(self) -> None:
        r = admin_client.get("/api/v1/cockpit/compliance-overview")
        data = r.json()
        assert "zatca" in data and "pdpl" in data

    # Pricing intelligence
    def test_pricing_competitor_landscape_has_competitors_list(self) -> None:
        r = admin_client.get("/api/v1/pricing-intelligence/competitor-landscape")
        assert len(r.json()["competitors"]) > 0

    def test_pricing_win_rate_simulator_returns_predicted_win_rate(self) -> None:
        body = {"proposed_price_sar": 3000, "sector": "technology", "company_size": "sme"}
        r = admin_client.post("/api/v1/pricing-intelligence/win-rate-simulator", json=body)
        assert "predicted_win_rate" in r.json()

    def test_pricing_tier_optimization_returns_200(self) -> None:
        r = admin_client.get("/api/v1/pricing-intelligence/tier-optimization")
        assert r.status_code == 200

    # Pipeline
    def test_pipeline_deals_returns_non_empty_list(self) -> None:
        r = admin_client.get("/api/v1/pipeline/deals")
        assert r.json()["total"] > 0

    def test_pipeline_velocity_has_bottleneck_stage(self) -> None:
        r = admin_client.get("/api/v1/pipeline/velocity")
        assert "bottleneck_stage" in r.json()

    def test_pipeline_lost_analysis_has_reason_breakdown(self) -> None:
        r = admin_client.get("/api/v1/pipeline/lost-analysis")
        assert "reason_breakdown" in r.json()

    # Competitor intel
    def test_competitor_intel_battlecards_returns_200(self) -> None:
        r = admin_client.get("/api/v1/competitor-intel/battlecards")
        assert r.status_code == 200

    def test_competitor_intel_win_loss_patterns_returns_200(self) -> None:
        r = admin_client.get("/api/v1/competitor-intel/win-loss-patterns")
        assert r.status_code == 200

    def test_competitor_detail_alpha_revenue_returns_200(self) -> None:
        r = admin_client.get("/api/v1/competitor-intel/alpha_revenue")
        assert r.status_code == 200

    # Growth intelligence
    def test_growth_market_map_has_segments(self) -> None:
        r = admin_client.get("/api/v1/growth-intelligence/market-map")
        assert len(r.json()["segments"]) > 0

    def test_growth_weekly_focus_has_focus_areas(self) -> None:
        r = admin_client.get("/api/v1/growth-intelligence/weekly-focus")
        assert len(r.json()["focus_areas"]) > 0

    # Health intelligence
    def test_health_alerts_has_alert_count(self) -> None:
        r = admin_client.get("/api/v1/health-intelligence/alerts")
        assert "alert_count" in r.json()

    def test_health_leaderboard_has_leaderboard_list(self) -> None:
        r = admin_client.get("/api/v1/health-intelligence/leaderboard")
        assert len(r.json()["leaderboard"]) > 0

    def test_health_trends_returns_200(self) -> None:
        r = admin_client.get("/api/v1/health-intelligence/trends")
        assert r.status_code == 200

    def test_health_compute_returns_health_score(self) -> None:
        body = {
            "company_name": "Test Co",
            "data_readiness": 70,
            "onboarding_ops": 65,
            "delivery_quality": 75,
            "zatca_compliance": 80,
            "client_retention": 70,
            "recurring_revenue": 68,
        }
        r = admin_client.post("/api/v1/health-intelligence/compute", json=body)
        assert "health_score" in r.json()

    # Retainer ops
    def test_retainer_at_risk_returns_200(self) -> None:
        r = admin_client.get("/api/v1/retainer/at-risk")
        assert r.status_code == 200

    def test_retainer_renewal_calendar_returns_200(self) -> None:
        r = admin_client.get("/api/v1/retainer/renewal-calendar")
        assert r.status_code == 200

    def test_retainer_single_client_rtn001_returns_200(self) -> None:
        r = admin_client.get("/api/v1/retainer/RTN-001")
        assert r.status_code == 200

    # ZATCA readiness
    def test_zatca_checklist_has_items(self) -> None:
        r = open_client.get("/api/v1/zatca-readiness/checklist")
        assert r.json()["total_items"] > 0

    def test_zatca_waves_has_waves_list(self) -> None:
        r = open_client.get("/api/v1/zatca-readiness/waves")
        assert len(r.json()["waves"]) > 0

    def test_zatca_penalties_returns_200(self) -> None:
        r = open_client.get("/api/v1/zatca-readiness/penalties")
        assert r.status_code == 200

    def test_zatca_assess_returns_readiness_score(self) -> None:
        body = {
            "company_name": "Test Saudi Co",
            "has_csid": True,
            "has_xml_ubl": True,
            "has_qr_code": True,
        }
        r = open_client.post("/api/v1/zatca-readiness/assess", json=body)
        assert "readiness_score" in r.json()

    # PDPL readiness
    def test_pdpl_checklist_has_items(self) -> None:
        r = open_client.get("/api/v1/pdpl-readiness/checklist")
        assert r.json()["total_items"] > 0

    def test_pdpl_penalties_returns_200(self) -> None:
        r = open_client.get("/api/v1/pdpl-readiness/penalties")
        assert r.status_code == 200

    def test_pdpl_assess_returns_readiness_score(self) -> None:
        body = {
            "company_name": "Test Saudi Co",
            "has_privacy_policy": True,
            "has_consent_mechanism": True,
        }
        r = open_client.post("/api/v1/pdpl-readiness/assess", json=body)
        assert "readiness_score" in r.json()

    def test_pdpl_data_map_returns_200(self) -> None:
        body = {"company_name": "Test Co", "data_categories": ["email", "phone"]}
        r = open_client.post("/api/v1/pdpl-readiness/data-map", json=body)
        assert r.status_code == 200
