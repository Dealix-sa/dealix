"""Comprehensive tests for the sector intelligence router.

Covers:
  - Sector catalogue (list_sectors)
  - Sector deep brief (sector_deep_brief) + 404 handling
  - Signal building (_build_sector_signals): ZATCA completed vs upcoming, PDPL high
  - Urgency scoring (_compute_urgency): 0, 3, 6 signal points
  - Sector match scoring (_score_sector_fit): hint, zatca, employee range
  - Offer recommendation (_recommend_offer): ZATCA pain, high deal size, no pain
  - Full FastAPI integration via TestClient

The api.security module depends on a native library (jose/cryptography) that
is unavailable in the CI environment.  We stub that module before any import
of the sector_intelligence router so the tests can run without it.
"""

from __future__ import annotations

import os
import sys
import types
from unittest.mock import AsyncMock

import pytest

# ---------------------------------------------------------------------------
# Stub out the api.security chain before it is imported.
# The router only uses require_admin_key (an async callable).
# ---------------------------------------------------------------------------

def _make_passthrough_dep():
    """Return an async dependency that always allows through."""
    async def _allow() -> None:
        return None
    return _allow


def _ensure_security_stubs() -> None:
    """Insert lightweight stubs for api.security if they are not yet loaded."""
    if "api.security.api_key" in sys.modules:
        return

    # Stub api.security.api_key
    api_key_mod = types.ModuleType("api.security.api_key")
    api_key_mod.require_admin_key = _make_passthrough_dep()  # type: ignore[attr-defined]
    api_key_mod.verify_admin_key = lambda key: True  # type: ignore[attr-defined]
    api_key_mod.verify_api_key = lambda key, allowed=None: True  # type: ignore[attr-defined]
    api_key_mod.APIKeyMiddleware = object  # type: ignore[attr-defined]
    sys.modules["api.security.api_key"] = api_key_mod

    # Stub parent package so Python doesn't try to execute __init__
    if "api.security" not in sys.modules:
        sec_pkg = types.ModuleType("api.security")
        sec_pkg.require_admin_key = api_key_mod.require_admin_key  # type: ignore[attr-defined]
        sec_pkg.APIKeyMiddleware = object  # type: ignore[attr-defined]
        sec_pkg.setup_rate_limit = lambda app: None  # type: ignore[attr-defined]
        sys.modules["api.security"] = sec_pkg


_ensure_security_stubs()

# Now we can safely import from the router.
from api.routers.sector_intelligence import (  # noqa: E402
    SECTORS,
    SectorMatchBody,
    _build_sector_signals,
    _compute_urgency,
    _recommend_offer,
    _score_sector_fit,
    router,
)
from fastapi import FastAPI  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

# ---------------------------------------------------------------------------
# TestClient setup
# ---------------------------------------------------------------------------

os.environ.setdefault("ADMIN_API_KEYS", "test-admin-key")

app = FastAPI()
app.include_router(router)
client = TestClient(app, headers={"X-Admin-API-Key": "test-admin-key"})


# ---------------------------------------------------------------------------
# TestSectorCatalogue
# ---------------------------------------------------------------------------


class TestSectorCatalogue:
    """Tests for list_sectors() endpoint."""

    def test_returns_all_ten_sectors(self) -> None:
        response = client.get("/api/v1/sectors/")
        assert response.status_code == 200
        data = response.json()
        assert data["total_sectors"] == 10
        assert len(data["sectors"]) == 10

    def test_response_has_governance_decision(self) -> None:
        response = client.get("/api/v1/sectors/")
        data = response.json()
        assert data["governance_decision"] == "ALLOW_WITH_REVIEW"

    def test_each_sector_has_required_keys(self) -> None:
        response = client.get("/api/v1/sectors/")
        data = response.json()
        required_keys = {
            "id",
            "name",
            "tam_sar_bn",
            "growth_pct",
            "priority",
            "avg_deal_size_sar",
            "zatca_wave",
            "pdpl_exposure",
        }
        for sector in data["sectors"]:
            for key in required_keys:
                assert key in sector, f"Missing key '{key}' in sector {sector.get('id')}"

    def test_name_is_bilingual(self) -> None:
        response = client.get("/api/v1/sectors/")
        data = response.json()
        for sector in data["sectors"]:
            assert "ar" in sector["name"]
            assert "en" in sector["name"]
            assert sector["name"]["ar"]
            assert sector["name"]["en"]

    def test_total_tam_is_positive(self) -> None:
        response = client.get("/api/v1/sectors/")
        data = response.json()
        assert data["total_tam_sar_bn"] > 0

    def test_all_expected_sector_ids_present(self) -> None:
        expected_ids = {
            "technology",
            "financial_services",
            "healthcare",
            "real_estate",
            "education",
            "logistics",
            "retail",
            "government_services",
            "professional_services",
            "manufacturing",
        }
        response = client.get("/api/v1/sectors/")
        data = response.json()
        returned_ids = {s["id"] for s in data["sectors"]}
        assert returned_ids == expected_ids

    def test_sectors_dict_has_ten_entries(self) -> None:
        assert len(SECTORS) == 10

    def test_has_generated_at(self) -> None:
        response = client.get("/api/v1/sectors/")
        data = response.json()
        assert "generated_at" in data
        assert data["generated_at"]


# ---------------------------------------------------------------------------
# TestSectorDeepBrief
# ---------------------------------------------------------------------------


class TestSectorDeepBrief:
    """Tests for sector_deep_brief() endpoint."""

    def test_technology_returns_correct_structure(self) -> None:
        response = client.get("/api/v1/sectors/technology")
        assert response.status_code == 200
        data = response.json()
        assert data["governance_decision"] == "ALLOW_WITH_REVIEW"
        assert "sector" in data
        assert "deal_economics" in data
        assert "compliance" in data
        assert "pain_points" in data
        assert "dealix_value_proposition" in data
        assert "target_companies" in data

    def test_technology_sector_id_matches(self) -> None:
        response = client.get("/api/v1/sectors/technology")
        data = response.json()
        assert data["sector"]["id"] == "technology"

    def test_technology_name_is_bilingual(self) -> None:
        response = client.get("/api/v1/sectors/technology")
        data = response.json()
        name = data["sector"]["name"]
        assert "ar" in name
        assert "en" in name
        assert "Technology" in name["en"]

    def test_technology_deal_economics_has_expected_keys(self) -> None:
        response = client.get("/api/v1/sectors/technology")
        data = response.json()
        econ = data["deal_economics"]
        assert "avg_deal_size_sar" in econ
        assert "typical_cycle_days" in econ
        assert "icp_employee_range" in econ
        assert "target_monthly_deals" in econ

    def test_technology_pain_points_bilingual(self) -> None:
        response = client.get("/api/v1/sectors/technology")
        data = response.json()
        pp = data["pain_points"]
        assert isinstance(pp["ar"], list)
        assert isinstance(pp["en"], list)
        assert len(pp["ar"]) > 0
        assert len(pp["en"]) > 0

    def test_technology_compliance_fields(self) -> None:
        response = client.get("/api/v1/sectors/technology")
        data = response.json()
        comp = data["compliance"]
        assert "zatca_wave" in comp
        assert "pdpl_exposure" in comp
        assert "key_regulations" in comp
        assert isinstance(comp["key_regulations"], list)

    def test_technology_target_companies_riyadh_jeddah(self) -> None:
        response = client.get("/api/v1/sectors/technology")
        data = response.json()
        targets = data["target_companies"]
        assert "riyadh" in targets
        assert "jeddah" in targets
        assert isinstance(targets["riyadh"], list)
        assert len(targets["riyadh"]) > 0

    def test_unknown_sector_returns_404(self) -> None:
        response = client.get("/api/v1/sectors/unknown_sector_xyz")
        assert response.status_code == 404

    def test_404_detail_includes_valid_sectors(self) -> None:
        response = client.get("/api/v1/sectors/invalid_sector")
        data = response.json()
        detail = data.get("detail", {})
        assert "valid_sectors" in detail
        assert len(detail["valid_sectors"]) == 10

    def test_404_detail_is_bilingual(self) -> None:
        response = client.get("/api/v1/sectors/bad_sector")
        data = response.json()
        detail = data.get("detail", {})
        assert "ar" in detail
        assert "en" in detail

    def test_case_insensitive_sector_lookup(self) -> None:
        response = client.get("/api/v1/sectors/TECHNOLOGY")
        assert response.status_code == 200


# ---------------------------------------------------------------------------
# TestSectorSignals
# ---------------------------------------------------------------------------


class TestSectorSignals:
    """Tests for _build_sector_signals() logic."""

    def _make_sector(self, zatca_wave: str, pdpl_exposure: str, growth_pct: float) -> dict:
        return {
            "zatca_wave": zatca_wave,
            "pdpl_exposure": pdpl_exposure,
            "growth_pct": growth_pct,
        }

    def test_zatca_completed_produces_medium_urgency_signal(self) -> None:
        sector = self._make_sector("Wave 2 (completed)", "low", 5.0)
        signals = _build_sector_signals(sector)
        zatca_signals = [s for s in signals if s["source"] == "ZATCA"]
        assert len(zatca_signals) == 1
        assert zatca_signals[0]["urgency"] == "medium"

    def test_zatca_completed_title_en(self) -> None:
        sector = self._make_sector("Wave 2 (completed)", "low", 5.0)
        signals = _build_sector_signals(sector)
        zatca_signal = next(s for s in signals if s["source"] == "ZATCA")
        assert "mandatory" in zatca_signal["title_en"].lower()

    def test_zatca_upcoming_produces_high_urgency_signal(self) -> None:
        sector = self._make_sector("Wave 4 (2024)", "low", 5.0)
        signals = _build_sector_signals(sector)
        zatca_signals = [s for s in signals if s["source"] == "ZATCA"]
        assert len(zatca_signals) == 1
        assert zatca_signals[0]["urgency"] == "high"

    def test_zatca_upcoming_title_en(self) -> None:
        sector = self._make_sector("Wave 4 (2024)", "low", 5.0)
        signals = _build_sector_signals(sector)
        zatca_signal = next(s for s in signals if s["source"] == "ZATCA")
        assert "approaching" in zatca_signal["title_en"].lower()

    def test_pdpl_high_exposure_adds_signal(self) -> None:
        sector = self._make_sector("Wave 2 (completed)", "high", 5.0)
        signals = _build_sector_signals(sector)
        pdpl_signals = [s for s in signals if s["source"] == "PDPL"]
        assert len(pdpl_signals) == 1

    def test_pdpl_high_exposure_urgency_is_medium(self) -> None:
        sector = self._make_sector("Wave 2 (completed)", "high", 5.0)
        signals = _build_sector_signals(sector)
        pdpl_signal = next(s for s in signals if s["source"] == "PDPL")
        assert pdpl_signal["urgency"] == "medium"

    def test_pdpl_critical_exposure_urgency_is_high(self) -> None:
        sector = self._make_sector("Wave 2 (completed)", "critical", 5.0)
        signals = _build_sector_signals(sector)
        pdpl_signal = next(s for s in signals if s["source"] == "PDPL")
        assert pdpl_signal["urgency"] == "high"

    def test_pdpl_low_exposure_no_pdpl_signal(self) -> None:
        sector = self._make_sector("Wave 2 (completed)", "low", 5.0)
        signals = _build_sector_signals(sector)
        pdpl_signals = [s for s in signals if s["source"] == "PDPL"]
        assert len(pdpl_signals) == 0

    def test_pdpl_medium_exposure_no_pdpl_signal(self) -> None:
        sector = self._make_sector("Wave 2 (completed)", "medium", 5.0)
        signals = _build_sector_signals(sector)
        pdpl_signals = [s for s in signals if s["source"] == "PDPL"]
        assert len(pdpl_signals) == 0

    def test_high_growth_adds_vision_2030_signal(self) -> None:
        sector = self._make_sector("Wave 2 (completed)", "low", 18.0)
        signals = _build_sector_signals(sector)
        v2030 = [s for s in signals if s["source"] == "Vision 2030"]
        assert len(v2030) == 1
        assert v2030[0]["urgency"] == "opportunity"

    def test_low_growth_no_vision_2030_signal(self) -> None:
        sector = self._make_sector("Wave 2 (completed)", "low", 10.0)
        signals = _build_sector_signals(sector)
        v2030 = [s for s in signals if s["source"] == "Vision 2030"]
        assert len(v2030) == 0

    def test_all_signals_have_required_keys(self) -> None:
        sector = self._make_sector("Wave 4 (2024)", "critical", 20.0)
        signals = _build_sector_signals(sector)
        required = {"type", "urgency", "source", "title_ar", "title_en", "detail_ar", "detail_en"}
        for sig in signals:
            for key in required:
                assert key in sig, f"Signal missing key '{key}': {sig}"

    def test_signals_endpoint_returns_correct_structure(self) -> None:
        response = client.get("/api/v1/sectors/technology/signals")
        assert response.status_code == 200
        data = response.json()
        assert "signals" in data
        assert "urgency_score" in data
        assert data["governance_decision"] == "ALLOW_WITH_REVIEW"


# ---------------------------------------------------------------------------
# TestUrgencyScore
# ---------------------------------------------------------------------------


class TestUrgencyScore:
    """Tests for _compute_urgency()."""

    def test_zero_signal_points_returns_low_tier(self) -> None:
        signals: list[dict] = []
        result = _compute_urgency(signals)
        assert result["score"] == 0
        assert result["tier"] == "low"
        assert result["signal_count"] == 0

    def test_three_signal_points_returns_high_tier(self) -> None:
        # one "high" signal = 3 points
        signals = [{"urgency": "high"}]
        result = _compute_urgency(signals)
        assert result["score"] == 3
        assert result["tier"] == "high"

    def test_six_signal_points_returns_critical_tier(self) -> None:
        # two "high" signals = 6 points
        signals = [{"urgency": "high"}, {"urgency": "high"}]
        result = _compute_urgency(signals)
        assert result["score"] == 6
        assert result["tier"] == "critical"

    def test_one_medium_signal_returns_medium_tier(self) -> None:
        signals = [{"urgency": "medium"}]
        result = _compute_urgency(signals)
        assert result["score"] == 2
        assert result["tier"] == "medium"

    def test_opportunity_urgency_counts_as_one(self) -> None:
        signals = [{"urgency": "opportunity"}]
        result = _compute_urgency(signals)
        assert result["score"] == 1
        assert result["tier"] == "medium"

    def test_mixed_signals_sum_correctly(self) -> None:
        # high=3 + medium=2 + opportunity=1 = 6 => critical
        signals = [
            {"urgency": "high"},
            {"urgency": "medium"},
            {"urgency": "opportunity"},
        ]
        result = _compute_urgency(signals)
        assert result["score"] == 6
        assert result["tier"] == "critical"
        assert result["signal_count"] == 3

    def test_unknown_urgency_counts_as_zero(self) -> None:
        signals = [{"urgency": "unknown_value"}]
        result = _compute_urgency(signals)
        assert result["score"] == 0
        assert result["tier"] == "low"

    def test_signal_count_matches_input_length(self) -> None:
        signals = [{"urgency": "high"}, {"urgency": "low"}, {"urgency": "medium"}]
        result = _compute_urgency(signals)
        assert result["signal_count"] == 3


# ---------------------------------------------------------------------------
# TestSectorMatch
# ---------------------------------------------------------------------------


class TestSectorMatch:
    """Tests for _score_sector_fit()."""

    def _body(self, **kwargs) -> SectorMatchBody:
        return SectorMatchBody(company_name="Test Co", **kwargs)

    def test_sector_hint_adds_forty_points(self) -> None:
        body = self._body(sector_hint="technology")
        results = _score_sector_fit(body)
        tech = next(r for r in results if r["sector_id"] == "technology")
        # 40 (hint) + 5 (tier_1 bonus) = 45
        assert tech["fit_score"] >= 40

    def test_sector_hint_technology_ranks_first(self) -> None:
        body = self._body(sector_hint="technology")
        results = _score_sector_fit(body)
        assert results[0]["sector_id"] == "technology"

    def test_has_zatca_issue_adds_fifteen_to_all(self) -> None:
        body_base = self._body()
        body_zatca = self._body(has_zatca_issue=True)
        base_results = {r["sector_id"]: r["fit_score"] for r in _score_sector_fit(body_base)}
        zatca_results = {r["sector_id"]: r["fit_score"] for r in _score_sector_fit(body_zatca)}
        for sid in base_results:
            assert zatca_results[sid] == base_results[sid] + 15

    def test_zatca_issue_reason_appears_in_results(self) -> None:
        body = self._body(has_zatca_issue=True)
        results = _score_sector_fit(body)
        for r in results:
            assert "ZATCA pain match" in r["fit_reasons"]["en"]

    def test_employee_count_in_range_adds_twenty(self) -> None:
        # technology ICP: 50-500 — use count=100
        body_no_emp = self._body(sector_hint="technology")
        body_with_emp = self._body(sector_hint="technology", employee_count=100)
        no_emp_results = {r["sector_id"]: r["fit_score"] for r in _score_sector_fit(body_no_emp)}
        with_emp_results = {r["sector_id"]: r["fit_score"] for r in _score_sector_fit(body_with_emp)}
        assert with_emp_results["technology"] == no_emp_results["technology"] + 20

    def test_employee_count_out_of_range_no_bonus(self) -> None:
        # technology ICP: 50-500 — use count=1 (below range)
        body = self._body(sector_hint="technology", employee_count=1)
        results = {r["sector_id"]: r["fit_score"] for r in _score_sector_fit(body)}
        body_no_emp = self._body(sector_hint="technology")
        no_emp = {r["sector_id"]: r["fit_score"] for r in _score_sector_fit(body_no_emp)}
        assert results["technology"] == no_emp["technology"]

    def test_tier1_priority_adds_five_points(self) -> None:
        # manufacturing is tier_2, technology is tier_1 — no other signals
        body = self._body()
        results = {r["sector_id"]: r["fit_score"] for r in _score_sector_fit(body)}
        assert results["technology"] == 5
        assert results["manufacturing"] == 0

    def test_returns_all_sectors(self) -> None:
        body = self._body()
        results = _score_sector_fit(body)
        assert len(results) == 10

    def test_sorted_descending_by_score(self) -> None:
        body = self._body(sector_hint="technology", has_zatca_issue=True)
        results = _score_sector_fit(body)
        scores = [r["fit_score"] for r in results]
        assert scores == sorted(scores, reverse=True)

    def test_each_result_has_required_keys(self) -> None:
        body = self._body()
        results = _score_sector_fit(body)
        required = {
            "sector_id",
            "sector_name",
            "fit_score",
            "fit_reasons",
            "avg_deal_size_sar",
            "typical_cycle_days",
        }
        for r in results:
            for key in required:
                assert key in r


# ---------------------------------------------------------------------------
# TestOfferRecommendation
# ---------------------------------------------------------------------------


class TestOfferRecommendation:
    """Tests for _recommend_offer()."""

    def _body(self, **kwargs) -> SectorMatchBody:
        return SectorMatchBody(company_name="Test Co", **kwargs)

    def _top_match(self, avg_deal_size_sar: int) -> dict:
        return {
            "sector_id": "technology",
            "avg_deal_size_sar": avg_deal_size_sar,
            "fit_score": 50,
            "fit_reasons": {"ar": [], "en": []},
            "typical_cycle_days": 18,
            "sector_name": {"ar": "تقنية", "en": "Technology"},
        }

    def test_zatca_pain_returns_sprint_499(self) -> None:
        body = self._body(has_zatca_issue=True)
        top = self._top_match(10_000)
        result = _recommend_offer(body, top)
        assert result["price_sar"] == 499
        assert "Sprint" in result["offer_en"]

    def test_pdpl_pain_returns_sprint_499(self) -> None:
        body = self._body(has_pdpl_concern=True)
        top = self._top_match(8_000)
        result = _recommend_offer(body, top)
        assert result["price_sar"] == 499
        assert "Sprint" in result["offer_en"]

    def test_high_deal_size_returns_managed_ops(self) -> None:
        body = self._body()
        top = self._top_match(12_000)
        result = _recommend_offer(body, top)
        assert result["price_sar"] == 2999
        assert "Managed" in result["offer_en"]

    def test_deal_size_below_12k_no_pain_returns_free_diagnostic_sprint(self) -> None:
        body = self._body()
        top = self._top_match(5_000)
        result = _recommend_offer(body, top)
        assert result["price_sar"] == 499
        assert "Diagnostic" in result["offer_en"] or "Sprint" in result["offer_en"]

    def test_no_top_match_returns_free_diagnostic(self) -> None:
        body = self._body()
        result = _recommend_offer(body, None)
        assert result["price_sar"] == 0
        assert "Diagnostic" in result["offer_en"]

    def test_zatca_pain_takes_precedence_over_high_deal_size(self) -> None:
        # has_zatca_issue should give Sprint even when deal_size >= 12k
        body = self._body(has_zatca_issue=True)
        top = self._top_match(15_000)
        result = _recommend_offer(body, top)
        assert result["price_sar"] == 499

    def test_result_has_bilingual_offer_labels(self) -> None:
        body = self._body()
        top = self._top_match(5_000)
        result = _recommend_offer(body, top)
        assert "offer_ar" in result
        assert "offer_en" in result
        assert result["offer_ar"]
        assert result["offer_en"]


# ---------------------------------------------------------------------------
# TestSectorAPIIntegration
# ---------------------------------------------------------------------------


class TestSectorAPIIntegration:
    """End-to-end integration tests via TestClient."""

    def test_list_sectors_status_200(self) -> None:
        response = client.get("/api/v1/sectors/")
        assert response.status_code == 200

    def test_sector_deep_brief_technology_200(self) -> None:
        response = client.get("/api/v1/sectors/technology")
        assert response.status_code == 200

    def test_sector_deep_brief_financial_services_200(self) -> None:
        response = client.get("/api/v1/sectors/financial_services")
        assert response.status_code == 200

    def test_sector_signals_technology_200(self) -> None:
        response = client.get("/api/v1/sectors/technology/signals")
        assert response.status_code == 200

    def test_sector_signals_governance_decision(self) -> None:
        response = client.get("/api/v1/sectors/healthcare/signals")
        data = response.json()
        assert data["governance_decision"] == "ALLOW_WITH_REVIEW"

    def test_match_endpoint_with_zatca_issue(self) -> None:
        payload = {
            "company_name": "Al Noor Tech",
            "has_zatca_issue": True,
        }
        response = client.post("/api/v1/sectors/match", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["governance_decision"] == "ALLOW_WITH_REVIEW"
        assert data["recommended_entry_offer"]["price_sar"] == 499

    def test_match_endpoint_returns_top_match(self) -> None:
        payload = {
            "company_name": "Riyadh Systems",
            "sector_hint": "technology",
        }
        response = client.post("/api/v1/sectors/match", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["top_match"]["sector_id"] == "technology"

    def test_match_endpoint_returns_three_or_fewer_matches(self) -> None:
        payload = {"company_name": "Generic Corp"}
        response = client.post("/api/v1/sectors/match", json=payload)
        data = response.json()
        assert len(data["all_matches"]) <= 3

    def test_match_endpoint_company_name_echoed(self) -> None:
        payload = {"company_name": "My Company"}
        response = client.post("/api/v1/sectors/match", json=payload)
        data = response.json()
        assert data["company"] == "My Company"

    def test_match_endpoint_with_employee_count(self) -> None:
        payload = {
            "company_name": "Mid-Size Co",
            "sector_hint": "technology",
            "employee_count": 150,
        }
        response = client.post("/api/v1/sectors/match", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["top_match"]["sector_id"] == "technology"

    def test_match_endpoint_extra_fields_rejected(self) -> None:
        payload = {
            "company_name": "Corp",
            "nonexistent_field": "value",
        }
        response = client.post("/api/v1/sectors/match", json=payload)
        assert response.status_code == 422

    def test_match_endpoint_empty_company_name_rejected(self) -> None:
        payload = {"company_name": ""}
        response = client.post("/api/v1/sectors/match", json=payload)
        assert response.status_code == 422

    def test_signals_unknown_sector_404(self) -> None:
        response = client.get("/api/v1/sectors/not_a_real_sector/signals")
        assert response.status_code == 404

    def test_all_sector_deep_briefs_return_200(self) -> None:
        for sector_id in SECTORS:
            response = client.get(f"/api/v1/sectors/{sector_id}")
            assert response.status_code == 200, (
                f"Expected 200 for sector '{sector_id}', got {response.status_code}"
            )

    def test_all_sector_signal_endpoints_return_200(self) -> None:
        for sector_id in SECTORS:
            response = client.get(f"/api/v1/sectors/{sector_id}/signals")
            assert response.status_code == 200, (
                f"Expected 200 for signals on '{sector_id}', got {response.status_code}"
            )
