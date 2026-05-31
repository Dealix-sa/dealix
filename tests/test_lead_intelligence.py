"""Tests for the lead_intelligence API router — 50 tests.

Covers:
  TestLeadScoring:         unit tests for the scoring formula
  TestScoreBreakdown:      per-component breakdown helper
  TestFunnelCategorization: funnel stage classification
  TestEnrichment:          enrich endpoint
  TestBatchScoring:        batch of 3 leads, scores returned
  TestTopOpportunities:    top 10 returned, sorted by score
  TestSectorHeatMap:       all sectors present, values >= 0
  TestFunnelCategorizationEndpoint: lead categorized into correct stage
  TestConversionPatterns:  patterns returned per sector
"""

from __future__ import annotations

import sys
import types

# ---------------------------------------------------------------------------
# Stub api.security.api_key BEFORE importing anything that touches it.
# ---------------------------------------------------------------------------
_mock_security = types.ModuleType("api.security.api_key")
_mock_security.require_admin_key = lambda: None  # no-op dependency
sys.modules.setdefault("api.security.api_key", _mock_security)

if "api.security" not in sys.modules:
    _api_security = types.ModuleType("api.security")
    sys.modules["api.security"] = _api_security

import pytest  # noqa: E402
from fastapi import FastAPI  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

from api.routers.lead_intelligence import (  # noqa: E402
    ICP_CITIES,
    ICP_SECTORS,
    _CONVERSION_PATTERNS,
    _DEMO_LEADS,
    _LEAD_INDEX,
    _enrich_lead,
    _label,
    categorize_funnel_stage,
    compute_lead_score,
    router,
    score_breakdown,
)

# ---------------------------------------------------------------------------
# Test client setup
# ---------------------------------------------------------------------------

app = FastAPI()
app.include_router(router)
client = TestClient(app, headers={"X-Admin-API-Key": "test-admin-key"})


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_lead(**overrides) -> dict:
    """Return a minimal passing lead dict with optional overrides."""
    base: dict = {
        "lead_id": "T-001",
        "company_name_ar": "شركة اختبار",
        "company_name_en": "Test Co",
        "sector": "technology",
        "city": "riyadh",
        "employees": 100,
        "annual_revenue_sar": 2_000_000,
        "has_zatca_issue": False,
        "has_pdpl_concern": False,
        "engaged": False,
        "meeting_booked": False,
        "proposal_sent": False,
        "pilot_started": False,
        "signed": False,
        "is_customer": False,
    }
    base.update(overrides)
    return base


# ===========================================================================
# TestLeadScoring — unit tests for compute_lead_score
# ===========================================================================


class TestLeadScoring:
    def test_perfect_icp_score_is_100(self):
        lead = _make_lead(
            sector="technology",
            city="riyadh",
            employees=100,
            annual_revenue_sar=3_000_000,
            has_zatca_issue=True,
            has_pdpl_concern=True,
        )
        assert compute_lead_score(lead) == 100

    def test_icp_sector_adds_25(self):
        lead = _make_lead(sector="technology", city="unknown", employees=0,
                          annual_revenue_sar=0, has_zatca_issue=False, has_pdpl_concern=False)
        assert compute_lead_score(lead) == 25

    def test_non_icp_sector_adds_0(self):
        lead = _make_lead(sector="construction", city="unknown", employees=0,
                          annual_revenue_sar=0, has_zatca_issue=False, has_pdpl_concern=False)
        assert compute_lead_score(lead) == 0

    def test_icp_city_adds_20(self):
        lead = _make_lead(sector="construction", city="riyadh", employees=0,
                          annual_revenue_sar=0, has_zatca_issue=False, has_pdpl_concern=False)
        assert compute_lead_score(lead) == 20

    def test_non_icp_city_adds_0(self):
        lead = _make_lead(sector="construction", city="madinah", employees=0,
                          annual_revenue_sar=0, has_zatca_issue=False, has_pdpl_concern=False)
        assert compute_lead_score(lead) == 0

    def test_employees_20_to_500_adds_20(self):
        lead = _make_lead(sector="construction", city="madinah", employees=50,
                          annual_revenue_sar=0, has_zatca_issue=False, has_pdpl_concern=False)
        assert compute_lead_score(lead) == 20

    def test_employees_below_20_adds_0(self):
        lead = _make_lead(sector="construction", city="madinah", employees=10,
                          annual_revenue_sar=0, has_zatca_issue=False, has_pdpl_concern=False)
        assert compute_lead_score(lead) == 0

    def test_employees_above_500_adds_0(self):
        lead = _make_lead(sector="construction", city="madinah", employees=600,
                          annual_revenue_sar=0, has_zatca_issue=False, has_pdpl_concern=False)
        assert compute_lead_score(lead) == 0

    def test_zatca_issue_adds_15(self):
        lead = _make_lead(sector="construction", city="madinah", employees=0,
                          annual_revenue_sar=0, has_zatca_issue=True, has_pdpl_concern=False)
        assert compute_lead_score(lead) == 15

    def test_pdpl_concern_adds_10(self):
        lead = _make_lead(sector="construction", city="madinah", employees=0,
                          annual_revenue_sar=0, has_zatca_issue=False, has_pdpl_concern=True)
        assert compute_lead_score(lead) == 10

    def test_revenue_in_band_adds_10(self):
        lead = _make_lead(sector="construction", city="madinah", employees=0,
                          annual_revenue_sar=2_000_000, has_zatca_issue=False, has_pdpl_concern=False)
        assert compute_lead_score(lead) == 10

    def test_revenue_below_band_adds_0(self):
        lead = _make_lead(sector="construction", city="madinah", employees=0,
                          annual_revenue_sar=200_000, has_zatca_issue=False, has_pdpl_concern=False)
        assert compute_lead_score(lead) == 0

    def test_revenue_above_band_adds_0(self):
        lead = _make_lead(sector="construction", city="madinah", employees=0,
                          annual_revenue_sar=15_000_000, has_zatca_issue=False, has_pdpl_concern=False)
        assert compute_lead_score(lead) == 0

    def test_score_capped_at_100(self):
        lead = _make_lead(
            sector="technology",
            city="riyadh",
            employees=100,
            annual_revenue_sar=3_000_000,
            has_zatca_issue=True,
            has_pdpl_concern=True,
        )
        assert compute_lead_score(lead) <= 100

    def test_zero_lead_scores_zero(self):
        lead = _make_lead(sector="other", city="other", employees=0,
                          annual_revenue_sar=0, has_zatca_issue=False, has_pdpl_concern=False)
        assert compute_lead_score(lead) == 0

    def test_all_icp_sectors_score_25(self):
        for sector in ICP_SECTORS:
            lead = _make_lead(sector=sector, city="other", employees=0,
                              annual_revenue_sar=0, has_zatca_issue=False, has_pdpl_concern=False)
            assert compute_lead_score(lead) == 25, f"Sector {sector} should score 25"

    def test_all_icp_cities_score_20(self):
        for city in ICP_CITIES:
            lead = _make_lead(sector="other", city=city, employees=0,
                              annual_revenue_sar=0, has_zatca_issue=False, has_pdpl_concern=False)
            assert compute_lead_score(lead) == 20, f"City {city} should score 20"


# ===========================================================================
# TestScoreBreakdown — per-component breakdown
# ===========================================================================


class TestScoreBreakdown:
    def test_breakdown_keys_present(self):
        lead = _make_lead()
        bd = score_breakdown(lead)
        for key in ("icp_sector", "icp_city", "employee_count", "zatca_urgency",
                    "pdpl_urgency", "revenue_band"):
            assert key in bd, f"Missing breakdown key: {key}"

    def test_breakdown_sums_to_score(self):
        lead = _make_lead(
            sector="healthcare",
            city="jeddah",
            employees=80,
            annual_revenue_sar=1_500_000,
            has_zatca_issue=True,
            has_pdpl_concern=False,
        )
        bd = score_breakdown(lead)
        total = sum(bd.values())
        assert total == compute_lead_score(lead)

    def test_breakdown_values_non_negative(self):
        lead = _make_lead()
        bd = score_breakdown(lead)
        for key, val in bd.items():
            assert val >= 0, f"Negative breakdown for {key}"


# ===========================================================================
# TestFunnelCategorization — pure function
# ===========================================================================


class TestFunnelCategorization:
    def test_no_signals_is_awareness(self):
        lead = _make_lead(engaged=False, meeting_booked=False, proposal_sent=False,
                          pilot_started=False, signed=False, is_customer=False)
        assert categorize_funnel_stage(lead) == "awareness"

    def test_engaged_is_consideration(self):
        lead = _make_lead(engaged=True, meeting_booked=False)
        assert categorize_funnel_stage(lead) == "consideration"

    def test_meeting_booked_is_evaluation(self):
        lead = _make_lead(engaged=True, meeting_booked=True, proposal_sent=False)
        assert categorize_funnel_stage(lead) == "evaluation"

    def test_proposal_sent_is_intent(self):
        lead = _make_lead(engaged=True, meeting_booked=True, proposal_sent=True, pilot_started=False)
        assert categorize_funnel_stage(lead) == "intent"

    def test_pilot_started_is_decision(self):
        lead = _make_lead(engaged=True, meeting_booked=True, proposal_sent=True,
                          pilot_started=True, signed=False)
        assert categorize_funnel_stage(lead) == "decision"

    def test_signed_is_customer(self):
        lead = _make_lead(signed=True)
        assert categorize_funnel_stage(lead) == "customer"

    def test_is_customer_flag_is_customer(self):
        lead = _make_lead(is_customer=True)
        assert categorize_funnel_stage(lead) == "customer"


# ===========================================================================
# TestEnrichment — POST /enrich endpoint
# ===========================================================================


class TestEnrichment:
    def test_returns_200(self):
        r = client.post("/api/v1/leads/intelligence/enrich", json=_make_lead())
        assert r.status_code == 200

    def test_governance_decision_present(self):
        r = client.post("/api/v1/leads/intelligence/enrich", json=_make_lead())
        assert r.json()["governance_decision"] == "ALLOW_WITH_REVIEW"

    def test_score_is_integer(self):
        r = client.post("/api/v1/leads/intelligence/enrich", json=_make_lead())
        assert isinstance(r.json()["score"], int)

    def test_inferred_pain_signals_present(self):
        r = client.post("/api/v1/leads/intelligence/enrich", json=_make_lead(sector="technology"))
        enriched = r.json()["enriched"]
        assert "inferred_pain_signals" in enriched
        assert len(enriched["inferred_pain_signals"]) > 0

    def test_vision_2030_relevance_high_for_icp_sector(self):
        r = client.post("/api/v1/leads/intelligence/enrich", json=_make_lead(sector="healthcare"))
        enriched = r.json()["enriched"]
        assert enriched["vision_2030_relevance"] == "high"

    def test_sme_class_small_for_50_employees(self):
        r = client.post("/api/v1/leads/intelligence/enrich", json=_make_lead(employees=100))
        enriched = r.json()["enriched"]
        assert enriched["sme_class"] == "small"

    def test_funnel_stage_in_response(self):
        r = client.post("/api/v1/leads/intelligence/enrich", json=_make_lead())
        assert "funnel_stage" in r.json()

    def test_breakdown_in_response(self):
        r = client.post("/api/v1/leads/intelligence/enrich", json=_make_lead())
        data = r.json()
        assert "breakdown" in data


# ===========================================================================
# TestBatchScoring — POST /score-batch
# ===========================================================================


class TestBatchScoring:
    def _three_leads(self):
        return [
            _make_lead(lead_id="B-001", sector="technology", city="riyadh",
                       employees=100, annual_revenue_sar=2_000_000,
                       has_zatca_issue=True, has_pdpl_concern=True),
            _make_lead(lead_id="B-002", sector="logistics", city="madinah",
                       employees=600, annual_revenue_sar=500_000,
                       has_zatca_issue=False, has_pdpl_concern=False),
            _make_lead(lead_id="B-003", sector="healthcare", city="jeddah",
                       employees=80, annual_revenue_sar=3_000_000,
                       has_zatca_issue=False, has_pdpl_concern=True),
        ]

    def test_returns_200(self):
        r = client.post("/api/v1/leads/intelligence/score-batch", json={"leads": self._three_leads()})
        assert r.status_code == 200

    def test_returns_3_results(self):
        r = client.post("/api/v1/leads/intelligence/score-batch", json={"leads": self._three_leads()})
        assert r.json()["total_scored"] == 3

    def test_results_sorted_by_score_desc(self):
        r = client.post("/api/v1/leads/intelligence/score-batch", json={"leads": self._three_leads()})
        scores = [item["score"] for item in r.json()["results"]]
        assert scores == sorted(scores, reverse=True)

    def test_governance_decision_present(self):
        r = client.post("/api/v1/leads/intelligence/score-batch", json={"leads": self._three_leads()})
        assert r.json()["governance_decision"] == "ALLOW_WITH_REVIEW"

    def test_each_result_has_breakdown(self):
        r = client.post("/api/v1/leads/intelligence/score-batch", json={"leads": self._three_leads()})
        for result in r.json()["results"]:
            assert "breakdown" in result

    def test_score_between_0_and_100(self):
        r = client.post("/api/v1/leads/intelligence/score-batch", json={"leads": self._three_leads()})
        for result in r.json()["results"]:
            assert 0 <= result["score"] <= 100

    def test_empty_batch_returns_400_or_validation_error(self):
        r = client.post("/api/v1/leads/intelligence/score-batch", json={"leads": []})
        # FastAPI validation returns 422 for empty list with min_length=1;
        # our custom limit check would return 400 — accept either.
        assert r.status_code in (400, 422)

    def test_b001_highest_score(self):
        r = client.post("/api/v1/leads/intelligence/score-batch", json={"leads": self._three_leads()})
        top = r.json()["results"][0]
        assert top["lead_id"] == "B-001"


# ===========================================================================
# TestTopOpportunities — GET /top-opportunities
# ===========================================================================


class TestTopOpportunities:
    def test_returns_200(self):
        r = client.get("/api/v1/leads/intelligence/top-opportunities")
        assert r.status_code == 200

    def test_returns_at_most_10(self):
        r = client.get("/api/v1/leads/intelligence/top-opportunities")
        assert r.json()["total"] <= 10

    def test_sorted_by_score_descending(self):
        r = client.get("/api/v1/leads/intelligence/top-opportunities")
        scores = [lead["score"] for lead in r.json()["leads"]]
        assert scores == sorted(scores, reverse=True)

    def test_governance_decision_present(self):
        r = client.get("/api/v1/leads/intelligence/top-opportunities")
        assert r.json()["governance_decision"] == "ALLOW_WITH_REVIEW"

    def test_each_lead_has_funnel_stage(self):
        r = client.get("/api/v1/leads/intelligence/top-opportunities")
        for lead in r.json()["leads"]:
            assert "funnel_stage" in lead

    def test_each_lead_has_urgency(self):
        r = client.get("/api/v1/leads/intelligence/top-opportunities")
        for lead in r.json()["leads"]:
            assert lead["urgency"] in ("high", "medium", "low")

    def test_scores_non_negative(self):
        r = client.get("/api/v1/leads/intelligence/top-opportunities")
        for lead in r.json()["leads"]:
            assert lead["score"] >= 0


# ===========================================================================
# TestSectorHeatMap — GET /sector-heat-map
# ===========================================================================


class TestSectorHeatMap:
    def test_returns_200(self):
        r = client.get("/api/v1/leads/intelligence/sector-heat-map")
        assert r.status_code == 200

    def test_governance_decision_present(self):
        r = client.get("/api/v1/leads/intelligence/sector-heat-map")
        assert r.json()["governance_decision"] == "ALLOW_WITH_REVIEW"

    def test_all_sectors_present_in_heat_map(self):
        r = client.get("/api/v1/leads/intelligence/sector-heat-map")
        data = r.json()
        heat_map = data["heat_map"]
        for sector in data["sectors"]:
            assert sector in heat_map, f"Sector {sector} missing from heat_map"

    def test_all_values_non_negative(self):
        r = client.get("/api/v1/leads/intelligence/sector-heat-map")
        heat_map = r.json()["heat_map"]
        for sector, cities in heat_map.items():
            for city, val in cities.items():
                assert val >= 0, f"Negative value for {sector}/{city}"

    def test_sector_avg_scores_present(self):
        r = client.get("/api/v1/leads/intelligence/sector-heat-map")
        assert "sector_avg_scores" in r.json()

    def test_icp_sectors_have_positive_avg_score(self):
        r = client.get("/api/v1/leads/intelligence/sector-heat-map")
        avgs = r.json()["sector_avg_scores"]
        for sector in ("technology", "financial_services", "healthcare", "real_estate"):
            if sector in avgs:
                assert avgs[sector] > 0, f"ICP sector {sector} should have positive avg score"


# ===========================================================================
# TestFunnelCategorizationEndpoint — POST /categorize
# ===========================================================================


class TestFunnelCategorizationEndpoint:
    def test_returns_200(self):
        r = client.post(
            "/api/v1/leads/intelligence/categorize",
            json={"lead": _make_lead()},
        )
        assert r.status_code == 200

    def test_awareness_for_cold_lead(self):
        r = client.post(
            "/api/v1/leads/intelligence/categorize",
            json={"lead": _make_lead(engaged=False, meeting_booked=False)},
        )
        assert r.json()["funnel_stage"] == "awareness"

    def test_evaluation_for_meeting_booked(self):
        r = client.post(
            "/api/v1/leads/intelligence/categorize",
            json={"lead": _make_lead(engaged=True, meeting_booked=True, proposal_sent=False)},
        )
        assert r.json()["funnel_stage"] == "evaluation"

    def test_customer_for_signed(self):
        r = client.post(
            "/api/v1/leads/intelligence/categorize",
            json={"lead": _make_lead(signed=True)},
        )
        assert r.json()["funnel_stage"] == "customer"

    def test_next_action_bilingual(self):
        r = client.post(
            "/api/v1/leads/intelligence/categorize",
            json={"lead": _make_lead()},
        )
        action = r.json()["next_recommended_action"]
        assert "ar" in action
        assert "en" in action

    def test_funnel_stage_label_bilingual(self):
        r = client.post(
            "/api/v1/leads/intelligence/categorize",
            json={"lead": _make_lead()},
        )
        label = r.json()["funnel_stage_label"]
        assert "ar" in label
        assert "en" in label

    def test_governance_decision_present(self):
        r = client.post(
            "/api/v1/leads/intelligence/categorize",
            json={"lead": _make_lead()},
        )
        assert r.json()["governance_decision"] == "ALLOW_WITH_REVIEW"


# ===========================================================================
# TestConversionPatterns — GET /conversion-patterns
# ===========================================================================


class TestConversionPatterns:
    def test_returns_200_all_sectors(self):
        r = client.get("/api/v1/leads/intelligence/conversion-patterns")
        assert r.status_code == 200

    def test_governance_decision_present(self):
        r = client.get("/api/v1/leads/intelligence/conversion-patterns")
        assert r.json()["governance_decision"] == "ALLOW_WITH_REVIEW"

    def test_all_sectors_present(self):
        r = client.get("/api/v1/leads/intelligence/conversion-patterns")
        data = r.json()["sectors"]
        for sector in _CONVERSION_PATTERNS.keys():
            assert sector in data, f"Sector {sector} missing"

    def test_filter_by_sector_returns_single(self):
        r = client.get("/api/v1/leads/intelligence/conversion-patterns?sector=technology")
        assert r.status_code == 200
        assert "pattern" in r.json()
        assert r.json()["sector"] == "technology"

    def test_unknown_sector_returns_404(self):
        r = client.get("/api/v1/leads/intelligence/conversion-patterns?sector=unknown_sector_xyz")
        assert r.status_code == 404

    def test_avg_sales_cycle_days_positive(self):
        r = client.get("/api/v1/leads/intelligence/conversion-patterns")
        for sector, pattern in r.json()["sectors"].items():
            assert pattern["avg_sales_cycle_days"] > 0, f"Invalid cycle for {sector}"

    def test_top_buying_trigger_present(self):
        r = client.get("/api/v1/leads/intelligence/conversion-patterns?sector=financial_services")
        pattern = r.json()["pattern"]
        assert "top_buying_trigger" in pattern
        assert len(pattern["top_buying_trigger"]) > 0


# ===========================================================================
# TestDemoLeadDataIntegrity — sanity checks on the 15 demo leads
# ===========================================================================


class TestDemoLeadDataIntegrity:
    def test_exactly_15_demo_leads(self):
        assert len(_DEMO_LEADS) == 15

    def test_all_leads_have_required_fields(self):
        required = ["lead_id", "company_name_ar", "company_name_en", "sector",
                    "city", "employees", "annual_revenue_sar"]
        for lead in _DEMO_LEADS:
            for field in required:
                assert field in lead, f"Missing {field} in {lead.get('lead_id')}"

    def test_all_scores_in_valid_range(self):
        for lead_id, lead in _LEAD_INDEX.items():
            assert 0 <= lead["score"] <= 100, f"Score out of range for {lead_id}"

    def test_at_least_one_perfect_icp_lead(self):
        perfect = [v for v in _LEAD_INDEX.values() if v["score"] >= 90]
        assert len(perfect) >= 1

    def test_label_helper_returns_bilingual(self):
        label = _label("score")
        assert "ar" in label
        assert "en" in label
