"""Wave 17 integration test suite — golden path + conformance + bilingual coverage.

Covers:
  - End-to-end golden path: sector match → lifecycle advance → ZATCA → retainer renewal
  - API conformance: every endpoint returns governance_decision
  - Bilingual coverage: AR+EN labels on all key response objects
  - Sector-to-lifecycle cohesion: deal sizes, recommended offers, at-risk actions
  - Performance baseline: structural / shape assertions on data volumes
"""

from __future__ import annotations

import sys
import types

# ---------------------------------------------------------------------------
# Stub out api.security before any router import so jose/cryptography is not
# required in the CI environment.
# ---------------------------------------------------------------------------

_mock_security = types.ModuleType("api.security.api_key")
_mock_security.require_admin_key = lambda: None  # type: ignore[attr-defined]
sys.modules.setdefault("api.security.api_key", _mock_security)
if "api.security" not in sys.modules:
    import types as _t
    _sec_pkg = _t.ModuleType("api.security")
    _sec_pkg.require_admin_key = _mock_security.require_admin_key  # type: ignore[attr-defined]
    _sec_pkg.APIKeyMiddleware = object  # type: ignore[attr-defined]
    _sec_pkg.setup_rate_limit = lambda app: None  # type: ignore[attr-defined]
    sys.modules["api.security"] = _sec_pkg

# ---------------------------------------------------------------------------
# Router imports — all Wave 17 routers
# ---------------------------------------------------------------------------

from api.routers import (  # noqa: E402
    customer_lifecycle,
    kpi_dashboard,
    retainer_ops,
    sector_intelligence,
    zatca_readiness,
)

# weekly_reports imports an internal dealix package that may not be present in
# the test environment; catch and skip gracefully.
try:
    from api.routers import weekly_reports as _weekly_reports_mod  # noqa: E402

    _WEEKLY_REPORTS_AVAILABLE = True
except Exception:
    _weekly_reports_mod = None  # type: ignore[assignment]
    _WEEKLY_REPORTS_AVAILABLE = False

# lead_intelligence and growth_intelligence are also Wave 17 routers
try:
    from api.routers import lead_intelligence as _lead_intelligence_mod  # noqa: E402

    _LEAD_INTELLIGENCE_AVAILABLE = True
except Exception:
    _lead_intelligence_mod = None  # type: ignore[assignment]
    _LEAD_INTELLIGENCE_AVAILABLE = False

try:
    from api.routers import growth_intelligence as _growth_intelligence_mod  # noqa: E402

    _GROWTH_INTELLIGENCE_AVAILABLE = True
except Exception:
    _growth_intelligence_mod = None  # type: ignore[assignment]
    _GROWTH_INTELLIGENCE_AVAILABLE = False

from fastapi import FastAPI  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

# ---------------------------------------------------------------------------
# Build the test application — register all available Wave 17 routers
# ---------------------------------------------------------------------------


def _build_app() -> FastAPI:
    app = FastAPI(title="Dealix Wave 17 Integration Test App")
    app.include_router(sector_intelligence.router)
    app.include_router(customer_lifecycle.router)
    app.include_router(retainer_ops.router)
    app.include_router(kpi_dashboard.router)
    app.include_router(zatca_readiness.router)
    if _WEEKLY_REPORTS_AVAILABLE and _weekly_reports_mod is not None:
        app.include_router(_weekly_reports_mod.router)
    if _LEAD_INTELLIGENCE_AVAILABLE and _lead_intelligence_mod is not None:
        app.include_router(_lead_intelligence_mod.router)
    if _GROWTH_INTELLIGENCE_AVAILABLE and _growth_intelligence_mod is not None:
        app.include_router(_growth_intelligence_mod.router)
    return app


_app = _build_app()
_client = TestClient(_app, headers={"X-Admin-API-Key": "test-admin-key"})

# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------


def _get(path: str) -> dict:
    resp = _client.get(path)
    assert resp.status_code == 200, f"GET {path} returned {resp.status_code}: {resp.text}"
    return resp.json()


def _post(path: str, json: dict) -> dict:
    resp = _client.post(path, json=json)
    assert resp.status_code == 200, f"POST {path} returned {resp.status_code}: {resp.text}"
    return resp.json()


# ---------------------------------------------------------------------------
# TestGoldenPath — end-to-end scenario
# ---------------------------------------------------------------------------


class TestGoldenPath:
    """End-to-end scenario: lead intake through retainer renewal."""

    def test_sector_match_then_deep_brief(self) -> None:
        """POST /sectors/match with technology profile → GET /sectors/technology."""
        match_payload = {
            "company_name": "Alphatech Solutions",
            "sector_hint": "technology",
            "employee_count": 120,
            "city": "Riyadh",
        }
        match_data = _post("/api/v1/sectors/match", match_payload)
        assert match_data["governance_decision"] == "ALLOW_WITH_REVIEW"
        assert match_data["top_match"] is not None
        top_sector_id = match_data["top_match"]["sector_id"]

        # Follow up with deep brief on the matched sector
        brief_data = _get(f"/api/v1/sectors/{top_sector_id}")
        assert brief_data["governance_decision"] == "ALLOW_WITH_REVIEW"
        assert "sector" in brief_data
        assert "deal_economics" in brief_data
        assert brief_data["sector"]["id"] == top_sector_id

    def test_lifecycle_advance_then_health(self) -> None:
        """Advance CLT-005 (diagnostic) → sprint_active, then verify stage changed."""
        advance_data = _post(
            "/api/v1/lifecycle/CLT-005/advance",
            {"reason": "Diagnostic complete, client ready for sprint"},
        )
        assert advance_data["governance_decision"] == "ALLOW_WITH_REVIEW"
        assert advance_data["from_stage"] == "diagnostic"
        assert advance_data["to_stage"] == "sprint_active"

        # Verify lifecycle state reflects new stage
        state_data = _get("/api/v1/lifecycle/CLT-005")
        assert state_data["governance_decision"] == "ALLOW_WITH_REVIEW"
        assert state_data["client"]["stage"] == "sprint_active"

    def test_zatca_assess_then_sprint_flow(self) -> None:
        """ZATCA assessment showing gaps → recommended offer is Sprint 499 SAR."""
        assess_payload = {
            "company_name": "Gap Corp",
            "annual_revenue_sar": 5_000_000,
            "has_csid": False,
            "has_xml_ubl": False,
            "has_qr_code": False,
            "has_digital_stamp": False,
            "has_fatoora_integration": False,
            "has_realtime_submission": False,
            "has_correct_trn": True,
            "has_complete_data": True,
            "has_rejection_process": False,
            "has_team_training": False,
        }
        assess_data = _post("/api/v1/zatca-readiness/assess", assess_payload)
        assert assess_data["governance_decision"] == "ALLOW_WITH_REVIEW"
        assert assess_data["critical_gaps"]  # should have critical gaps
        # Sprint offer should be recommended
        offer = assess_data["next_step"]
        assert "499" in offer["offer_en"] or "499" in offer["offer_ar"]

        # Match a company with ZATCA pain → same sprint offer
        match_data = _post(
            "/api/v1/sectors/match",
            {
                "company_name": "Gap Corp",
                "has_zatca_issue": True,
                "sector_hint": "logistics",
            },
        )
        rec_offer = match_data["recommended_entry_offer"]
        assert rec_offer["price_sar"] == 499

    def test_retainer_renewal_flow(self) -> None:
        """GET retainer RTN-002 → renew with payment confirmed → months_active incremented."""
        before_data = _get("/api/v1/retainer/RTN-002")
        months_before = before_data["months_active"]
        assert before_data["governance_decision"] == "ALLOW_WITH_REVIEW"

        renew_data = _post(
            "/api/v1/retainer/RTN-002/renew",
            {"payment_confirmed": True, "notes": "Integration test renewal"},
        )
        assert renew_data["governance_decision"] == "ALLOW_WITH_REVIEW"
        assert renew_data["status"] == "renewed"
        assert renew_data["months_active"] == months_before + 1

    def test_kpi_summary_has_mrr(self) -> None:
        """GET /kpi/summary → mrr present in metrics."""
        summary_data = _get("/api/v1/kpi/summary")
        assert summary_data["governance_decision"] == "ALLOW_WITH_REVIEW"
        assert "metrics" in summary_data
        assert "mrr" in summary_data["metrics"]
        assert summary_data["metrics"]["mrr"]["value_sar"] > 0


# ---------------------------------------------------------------------------
# TestAPIConformance — governance_decision on every endpoint
# ---------------------------------------------------------------------------


class TestAPIConformance:
    """Every Wave 17 endpoint must return a governance_decision field."""

    def _assert_gov(self, path: str, method: str = "GET", json: dict | None = None) -> None:
        if method == "GET":
            resp = _client.get(path)
        else:
            resp = _client.post(path, json=json or {})
        assert resp.status_code == 200, f"{method} {path} → {resp.status_code}: {resp.text}"
        data = resp.json()
        assert "governance_decision" in data, (
            f"{method} {path} response missing 'governance_decision'. Keys: {list(data.keys())}"
        )

    def test_kpi_summary_has_governance(self) -> None:
        self._assert_gov("/api/v1/kpi/summary")

    def test_kpi_commercial_has_governance(self) -> None:
        self._assert_gov("/api/v1/kpi/commercial")

    def test_kpi_nps_has_governance(self) -> None:
        self._assert_gov("/api/v1/kpi/nps")

    def test_kpi_health_score_has_governance(self) -> None:
        self._assert_gov("/api/v1/kpi/health-score")

    def test_sectors_list_has_governance(self) -> None:
        self._assert_gov("/api/v1/sectors/")

    def test_sectors_technology_deep_brief_has_governance(self) -> None:
        self._assert_gov("/api/v1/sectors/technology")

    def test_sectors_technology_signals_has_governance(self) -> None:
        self._assert_gov("/api/v1/sectors/technology/signals")

    def test_retainer_active_has_governance(self) -> None:
        self._assert_gov("/api/v1/retainer/active")

    def test_retainer_at_risk_has_governance(self) -> None:
        self._assert_gov("/api/v1/retainer/at-risk")

    def test_retainer_mrr_breakdown_has_governance(self) -> None:
        self._assert_gov("/api/v1/retainer/mrr-breakdown")

    def test_zatca_checklist_has_governance(self) -> None:
        self._assert_gov("/api/v1/zatca-readiness/checklist")

    def test_zatca_waves_has_governance(self) -> None:
        self._assert_gov("/api/v1/zatca-readiness/waves")

    def test_zatca_penalties_has_governance(self) -> None:
        self._assert_gov("/api/v1/zatca-readiness/penalties")

    def test_lifecycle_stages_has_governance(self) -> None:
        self._assert_gov("/api/v1/lifecycle/stages")

    def test_lifecycle_at_risk_has_governance(self) -> None:
        self._assert_gov("/api/v1/lifecycle/at-risk")

    def test_sector_match_has_governance(self) -> None:
        self._assert_gov(
            "/api/v1/sectors/match",
            method="POST",
            json={"company_name": "TestCo"},
        )

    def test_zatca_assess_has_governance(self) -> None:
        self._assert_gov(
            "/api/v1/zatca-readiness/assess",
            method="POST",
            json={"company_name": "TestCo"},
        )


# ---------------------------------------------------------------------------
# TestBilingualCoverage — AR+EN labels on all key response objects
# ---------------------------------------------------------------------------


class TestBilingualCoverage:
    """Verify that key response objects carry both Arabic and English labels."""

    def test_sectors_list_each_sector_has_ar_en_name(self) -> None:
        data = _get("/api/v1/sectors/")
        for sector in data["sectors"]:
            assert "name" in sector, f"Sector {sector.get('id')} missing 'name'"
            assert "ar" in sector["name"] and sector["name"]["ar"], (
                f"Sector {sector.get('id')} missing Arabic name"
            )
            assert "en" in sector["name"] and sector["name"]["en"], (
                f"Sector {sector.get('id')} missing English name"
            )

    def test_sector_deep_brief_has_ar_en_pain_points(self) -> None:
        data = _get("/api/v1/sectors/technology")
        pain = data["pain_points"]
        assert isinstance(pain["ar"], list) and pain["ar"]
        assert isinstance(pain["en"], list) and pain["en"]

    def test_sector_deep_brief_value_proposition_bilingual(self) -> None:
        data = _get("/api/v1/sectors/financial_services")
        vp = data["dealix_value_proposition"]
        assert vp["ar"]
        assert vp["en"]

    def test_retainer_active_tier_has_ar_en(self) -> None:
        data = _get("/api/v1/retainer/active")
        for retainer in data["retainers"]:
            tier = retainer["tier"]
            assert "ar" in tier and tier["ar"], f"Retainer {retainer['client_id']} missing AR tier"
            assert "en" in tier and tier["en"], f"Retainer {retainer['client_id']} missing EN tier"

    def test_retainer_active_company_has_ar_en(self) -> None:
        data = _get("/api/v1/retainer/active")
        for retainer in data["retainers"]:
            company = retainer["company"]
            assert "ar" in company and company["ar"]
            assert "en" in company and company["en"]

    def test_lifecycle_stages_labels_bilingual(self) -> None:
        data = _get("/api/v1/lifecycle/stages")
        for stage in data["stages"]:
            label = stage["label"]
            assert "ar" in label and label["ar"], f"Stage {stage['id']} missing AR label"
            assert "en" in label and label["en"], f"Stage {stage['id']} missing EN label"

    def test_lifecycle_at_risk_health_tier_bilingual(self) -> None:
        data = _get("/api/v1/lifecycle/at-risk")
        for client in data["clients"]:
            health = client["health_tier"]
            assert "ar" in health and health["ar"]
            assert "en" in health and health["en"]

    def test_retainer_at_risk_actions_bilingual(self) -> None:
        data = _get("/api/v1/retainer/at-risk")
        for item in data["interventions"]:
            assert "recommended_action_ar" in item and item["recommended_action_ar"]
            assert "recommended_action_en" in item and item["recommended_action_en"]

    def test_zatca_checklist_items_bilingual(self) -> None:
        data = _get("/api/v1/zatca-readiness/checklist")
        for category_items in data["checklist_by_category"].values():
            for item in category_items:
                assert "title_ar" in item and item["title_ar"]
                assert "title_en" in item and item["title_en"]

    def test_kpi_summary_mrr_label_bilingual(self) -> None:
        data = _get("/api/v1/kpi/summary")
        mrr_label = data["metrics"]["mrr"]["label"]
        assert "ar" in mrr_label and mrr_label["ar"]
        assert "en" in mrr_label and mrr_label["en"]

    def test_kpi_nps_label_bilingual(self) -> None:
        data = _get("/api/v1/kpi/nps")
        label = data["label"]
        assert "ar" in label and label["ar"]
        assert "en" in label and label["en"]

    def test_kpi_health_score_label_bilingual(self) -> None:
        data = _get("/api/v1/kpi/health-score")
        label = data["label"]
        assert "ar" in label and label["ar"]
        assert "en" in label and label["en"]

    def test_zatca_penalties_have_bilingual_violations(self) -> None:
        data = _get("/api/v1/zatca-readiness/penalties")
        for penalty in data["penalties"]:
            assert "violation_ar" in penalty and penalty["violation_ar"]
            assert "violation_en" in penalty and penalty["violation_en"]


# ---------------------------------------------------------------------------
# TestSectorToLifecycleCohesion — cross-API logical consistency
# ---------------------------------------------------------------------------


class TestSectorToLifecycleCohesion:
    """Verify logical consistency across sector, lifecycle, and retainer APIs."""

    def test_technology_avg_deal_size_is_sar(self) -> None:
        """Technology sector avg_deal_size should be > 0 SAR."""
        data = _get("/api/v1/sectors/technology")
        avg_deal = data["deal_economics"]["avg_deal_size_sar"]
        assert isinstance(avg_deal, (int, float))
        assert avg_deal > 0, "avg_deal_size_sar should be positive"

    def test_technology_avg_deal_size_matches_sector_catalogue(self) -> None:
        """Deep brief deal size should match what the sector catalogue reports."""
        catalogue = _get("/api/v1/sectors/")
        tech_in_catalogue = next(
            s for s in catalogue["sectors"] if s["id"] == "technology"
        )
        brief = _get("/api/v1/sectors/technology")
        assert brief["deal_economics"]["avg_deal_size_sar"] == tech_in_catalogue["avg_deal_size_sar"]

    def test_match_company_with_zatca_issue_recommends_sprint_499(self) -> None:
        """A company with a ZATCA issue should get the 499 SAR Sprint offer."""
        data = _post(
            "/api/v1/sectors/match",
            {
                "company_name": "ZATCA Trouble Co",
                "has_zatca_issue": True,
                "sector_hint": "logistics",
            },
        )
        rec = data["recommended_entry_offer"]
        assert rec["price_sar"] == 499

    def test_match_company_with_zatca_issue_offer_ar_is_present(self) -> None:
        """Recommended offer AR text must be present for ZATCA-pain companies."""
        data = _post(
            "/api/v1/sectors/match",
            {
                "company_name": "ZATCA Trouble Two",
                "has_zatca_issue": True,
            },
        )
        assert data["recommended_entry_offer"].get("offer_ar")

    def test_at_risk_retainers_have_recommended_action_fields(self) -> None:
        """Every at-risk retainer must carry both recommended_action_ar and _en."""
        data = _get("/api/v1/retainer/at-risk")
        assert data["at_risk_count"] > 0, "Expected at least one at-risk retainer in demo data"
        for item in data["interventions"]:
            assert "recommended_action_ar" in item, (
                f"Retainer {item['client_id']} missing recommended_action_ar"
            )
            assert "recommended_action_en" in item, (
                f"Retainer {item['client_id']} missing recommended_action_en"
            )
            assert item["recommended_action_ar"]
            assert item["recommended_action_en"]

    def test_lifecycle_stages_include_sprint_active(self) -> None:
        """sprint_active stage must exist in the lifecycle stage catalogue."""
        data = _get("/api/v1/lifecycle/stages")
        stage_ids = [s["id"] for s in data["stages"]]
        assert "sprint_active" in stage_ids

    def test_lifecycle_stages_sprint_price_is_499(self) -> None:
        """The sprint_active stage must have price_sar of 499."""
        data = _get("/api/v1/lifecycle/stages")
        sprint = next((s for s in data["stages"] if s["id"] == "sprint_active"), None)
        assert sprint is not None
        assert sprint["price_sar"] == 499

    def test_sector_signals_include_zatca_signal(self) -> None:
        """Technology sector signals must include at least one ZATCA signal."""
        data = _get("/api/v1/sectors/technology/signals")
        sources = [sig["source"] for sig in data["signals"]]
        assert "ZATCA" in sources, "Expected a ZATCA signal in technology sector signals"

    def test_retainer_individual_record_has_months_active(self) -> None:
        """A specific retainer record must expose months_active."""
        data = _get("/api/v1/retainer/RTN-001")
        assert "months_active" in data
        assert data["months_active"] >= 0

    def test_retainer_individual_record_has_tier(self) -> None:
        """RTN-001 retainer must carry tier with ar/en labels."""
        data = _get("/api/v1/retainer/RTN-001")
        tier = data["tier"]
        assert "ar" in tier and tier["ar"]
        assert "en" in tier and tier["en"]
        assert "price_sar" in tier


# ---------------------------------------------------------------------------
# TestPerformanceBaseline — structural / shape assertions
# ---------------------------------------------------------------------------


class TestPerformanceBaseline:
    """No real performance measurement — structural shape assertions."""

    def test_kpi_summary_returns_6_months_history(self) -> None:
        """mrr_history in summary should contain exactly 6 entries."""
        data = _get("/api/v1/kpi/summary")
        history = data.get("mrr_history", [])
        assert len(history) == 6, (
            f"Expected 6 months of MRR history, got {len(history)}"
        )

    def test_mrr_history_each_entry_has_month_and_mrr(self) -> None:
        """Every entry in mrr_history must have 'month' and 'mrr_sar' keys."""
        data = _get("/api/v1/kpi/summary")
        for entry in data["mrr_history"]:
            assert "month" in entry, "mrr_history entry missing 'month'"
            assert "mrr_sar" in entry, "mrr_history entry missing 'mrr_sar'"
            assert entry["mrr_sar"] > 0

    def test_retainer_active_mrr_positive(self) -> None:
        """total monthly MRR across active retainers must be > 0."""
        data = _get("/api/v1/retainer/active")
        total_mrr = data["summary"]["monthly_mrr_sar"]
        assert total_mrr > 0, f"Expected positive MRR, got {total_mrr}"

    def test_retainer_mrr_breakdown_total_mrr_positive(self) -> None:
        """MRR breakdown total_mrr_sar must be > 0."""
        data = _get("/api/v1/retainer/mrr-breakdown")
        assert data["total_mrr_sar"] > 0

    def test_sector_catalogue_has_10_sectors(self) -> None:
        """Sector catalogue must list exactly 10 sectors."""
        data = _get("/api/v1/sectors/")
        assert data["total_sectors"] == 10, (
            f"Expected 10 sectors, got {data['total_sectors']}"
        )

    def test_lifecycle_stages_covers_all_forward_stages(self) -> None:
        """All 6 forward stages + churned must appear in the stage catalogue."""
        data = _get("/api/v1/lifecycle/stages")
        expected = {
            "diagnostic",
            "sprint_active",
            "sprint_complete",
            "data_pack",
            "managed_ops",
            "custom_ai",
            "churned",
        }
        returned = {s["id"] for s in data["stages"]}
        assert expected == returned, f"Stage mismatch. Missing: {expected - returned}"

    def test_zatca_waves_total_positive(self) -> None:
        """ZATCA waves endpoint must list at least one wave."""
        data = _get("/api/v1/zatca-readiness/waves")
        assert data["total_waves"] > 0

    def test_zatca_checklist_critical_items_present(self) -> None:
        """There must be at least one critical checklist item."""
        data = _get("/api/v1/zatca-readiness/checklist")
        assert data["critical_items"] > 0

    def test_kpi_nps_has_trend_entries(self) -> None:
        """NPS endpoint should return at least one period in the trend."""
        data = _get("/api/v1/kpi/nps")
        assert len(data["trend"]) > 0

    def test_kpi_health_score_is_in_range(self) -> None:
        """Health score must be between 0 and 100."""
        data = _get("/api/v1/kpi/health-score")
        score = data["health_score"]
        assert 0 <= score <= 100, f"Health score {score} out of expected 0-100 range"
