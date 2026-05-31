"""Tests for the Competitor Intelligence API router.

Covers: landscape, individual competitor detail, battlecards,
compare endpoint (POST), and win/loss patterns.
All competitor names are fictional.
"""

from __future__ import annotations

import os
import sys
import types

os.environ.setdefault("ADMIN_API_KEY", "test-admin-key")
os.environ.setdefault("ADMIN_API_KEYS", "test-admin-key")

_mock_security = types.ModuleType("api.security.api_key")
_mock_security.require_admin_key = lambda: None
sys.modules.setdefault("api.security.api_key", _mock_security)
if "api.security" not in sys.modules:
    sys.modules["api.security"] = types.ModuleType("api.security")

from api.routers.competitor_intel import (  # noqa: E402
    _BATTLECARDS,
    _COMPETITORS,
    _DEALIX_ADVANTAGES,
    _WIN_LOSS_PATTERNS,
    _build_positioning,
    _compute_win_score,
    router,
)
from fastapi import FastAPI  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

app = FastAPI()
app.include_router(router)
client = TestClient(app, headers={"X-Admin-API-Key": "test-admin-key"})

_VALID_IDS = [
    "alpha_revenue",
    "nexus_ops",
    "dataflow_arabia",
    "riyadh_tech",
    "jadara_saas",
]


# ---------------------------------------------------------------------------
# Unit: internal helpers
# ---------------------------------------------------------------------------


class TestBuildPositioning:
    def test_returns_competitor_key(self) -> None:
        result = _build_positioning("alpha_revenue")
        assert "competitor" in result

    def test_returns_dealix_advantages(self) -> None:
        result = _build_positioning("alpha_revenue")
        assert "dealix_advantages" in result
        assert len(result["dealix_advantages"]) >= 1

    def test_summary_bilingual(self) -> None:
        result = _build_positioning("nexus_ops")
        assert "summary_en" in result
        assert "summary_ar" in result
        assert len(result["summary_en"]) > 10
        assert len(result["summary_ar"]) > 10

    def test_competitor_has_weaknesses(self) -> None:
        result = _build_positioning("jadara_saas")
        comp = result["competitor"]
        assert "weaknesses_en" in comp
        assert len(comp["weaknesses_en"]) >= 3


class TestComputeWinScore:
    def test_returns_integer_in_0_to_100(self) -> None:
        score = _compute_win_score(["ZATCA compliance", "Arabic UI"], "alpha_revenue")
        assert isinstance(score, int)
        assert 0 <= score <= 100

    def test_empty_features_returns_base(self) -> None:
        score = _compute_win_score([], "nexus_ops")
        assert isinstance(score, int)
        assert 0 <= score <= 100

    def test_relevant_features_increase_score(self) -> None:
        base = _compute_win_score([], "alpha_revenue")
        high = _compute_win_score(
            ["Arabic", "ZATCA", "PDPL", "governance", "proof"],
            "alpha_revenue",
        )
        assert high >= base

    def test_score_never_exceeds_100(self) -> None:
        score = _compute_win_score(
            ["Arabic", "ZATCA", "PDPL", "governance", "proof pack", "compliance", "AI"],
            "riyadh_tech",
        )
        assert score <= 100

    def test_all_competitor_ids_accepted(self) -> None:
        for cid in _VALID_IDS:
            score = _compute_win_score(["governance"], cid)
            assert 0 <= score <= 100


# ---------------------------------------------------------------------------
# Unit: data integrity
# ---------------------------------------------------------------------------


class TestCompetitorDataIntegrity:
    def test_five_competitors_defined(self) -> None:
        assert len(_COMPETITORS) == 5

    def test_all_ids_present(self) -> None:
        for cid in _VALID_IDS:
            assert cid in _COMPETITORS

    def test_each_competitor_has_bilingual_name(self) -> None:
        for comp in _COMPETITORS.values():
            assert "name" in comp and comp["name"]
            assert "name_ar" in comp and comp["name_ar"]

    def test_each_competitor_has_strengths_and_weaknesses(self) -> None:
        for comp in _COMPETITORS.values():
            assert len(comp["strengths_en"]) >= 1
            assert len(comp["strengths_ar"]) >= 1
            assert len(comp["weaknesses_en"]) >= 1
            assert len(comp["weaknesses_ar"]) >= 1

    def test_pricing_range_has_min_and_max(self) -> None:
        for comp in _COMPETITORS.values():
            rng = comp["pricing_sar_range"]
            assert rng["min"] > 0
            assert rng["max"] >= rng["min"]


class TestDealixAdvantagesIntegrity:
    def test_at_least_six_advantages(self) -> None:
        assert len(_DEALIX_ADVANTAGES) >= 6

    def test_each_advantage_bilingual(self) -> None:
        for adv in _DEALIX_ADVANTAGES:
            assert "en" in adv and adv["en"]
            assert "ar" in adv and adv["ar"]

    def test_governance_layer_advantage_present(self) -> None:
        ids = [a["id"] for a in _DEALIX_ADVANTAGES]
        assert "governance_layer" in ids


# ---------------------------------------------------------------------------
# TestLandscapeEndpoint
# ---------------------------------------------------------------------------


class TestLandscapeEndpoint:
    def test_returns_200(self) -> None:
        r = client.get("/api/v1/competitor-intel/landscape")
        assert r.status_code == 200

    def test_governance_decision_present(self) -> None:
        data = client.get("/api/v1/competitor-intel/landscape").json()
        assert data["governance_decision"] == "ALLOW_WITH_REVIEW"

    def test_five_competitors_in_response(self) -> None:
        data = client.get("/api/v1/competitor-intel/landscape").json()
        assert data["total_competitors"] == 5
        assert len(data["competitors"]) == 5

    def test_each_competitor_has_strengths(self) -> None:
        data = client.get("/api/v1/competitor-intel/landscape").json()
        for comp in data["competitors"]:
            assert "strengths_en" in comp
            assert len(comp["strengths_en"]) >= 1

    def test_each_competitor_has_weaknesses(self) -> None:
        data = client.get("/api/v1/competitor-intel/landscape").json()
        for comp in data["competitors"]:
            assert "weaknesses_en" in comp
            assert len(comp["weaknesses_en"]) >= 1

    def test_bilingual_competitor_names(self) -> None:
        data = client.get("/api/v1/competitor-intel/landscape").json()
        for comp in data["competitors"]:
            assert "name" in comp and comp["name"]
            assert "name_ar" in comp and comp["name_ar"]

    def test_dealix_advantages_in_landscape(self) -> None:
        data = client.get("/api/v1/competitor-intel/landscape").json()
        assert "dealix_advantages" in data
        assert len(data["dealix_advantages"]) >= 6

    def test_all_valid_ids_present(self) -> None:
        data = client.get("/api/v1/competitor-intel/landscape").json()
        ids = [c["id"] for c in data["competitors"]]
        for cid in _VALID_IDS:
            assert cid in ids

    def test_each_competitor_has_positioning(self) -> None:
        data = client.get("/api/v1/competitor-intel/landscape").json()
        for comp in data["competitors"]:
            assert "dealix_positioning" in comp


# ---------------------------------------------------------------------------
# TestCompetitorDetailEndpoint
# ---------------------------------------------------------------------------


class TestCompetitorDetailEndpoint:
    def test_returns_200_for_all_valid_ids(self) -> None:
        for cid in _VALID_IDS:
            r = client.get(f"/api/v1/competitor-intel/{cid}")
            assert r.status_code == 200, f"Expected 200 for {cid}, got {r.status_code}"

    def test_returns_404_for_unknown_id(self) -> None:
        r = client.get("/api/v1/competitor-intel/unknown_competitor_xyz")
        assert r.status_code == 404

    def test_governance_decision_present(self) -> None:
        data = client.get("/api/v1/competitor-intel/alpha_revenue").json()
        assert data["governance_decision"] == "ALLOW_WITH_REVIEW"

    def test_detail_has_battlecard(self) -> None:
        data = client.get("/api/v1/competitor-intel/alpha_revenue").json()
        assert "battlecard" in data
        assert data["battlecard"]

    def test_detail_has_win_loss(self) -> None:
        data = client.get("/api/v1/competitor-intel/nexus_ops").json()
        assert "win_loss" in data
        assert data["win_loss"]

    def test_detail_has_positioning(self) -> None:
        data = client.get("/api/v1/competitor-intel/riyadh_tech").json()
        assert "positioning" in data

    def test_detail_competitor_has_bilingual_name(self) -> None:
        data = client.get("/api/v1/competitor-intel/jadara_saas").json()
        comp = data["competitor"]
        assert comp["name"]
        assert comp["name_ar"]

    def test_404_detail_contains_available_ids(self) -> None:
        r = client.get("/api/v1/competitor-intel/bad_id")
        body = r.json()
        assert "available" in body["detail"].lower() or body["detail"]


# ---------------------------------------------------------------------------
# TestBattlecardsEndpoint
# ---------------------------------------------------------------------------


class TestBattlecardsEndpoint:
    def test_returns_200(self) -> None:
        r = client.get("/api/v1/competitor-intel/battlecards")
        assert r.status_code == 200

    def test_governance_decision_present(self) -> None:
        data = client.get("/api/v1/competitor-intel/battlecards").json()
        assert data["governance_decision"] == "ALLOW_WITH_REVIEW"

    def test_five_battlecards_returned(self) -> None:
        data = client.get("/api/v1/competitor-intel/battlecards").json()
        assert data["total_battlecards"] == 5
        assert len(data["battlecards"]) == 5

    def test_each_battlecard_has_objections(self) -> None:
        data = client.get("/api/v1/competitor-intel/battlecards").json()
        for card in data["battlecards"]:
            assert "objections" in card
            assert len(card["objections"]) >= 3

    def test_each_objection_bilingual(self) -> None:
        data = client.get("/api/v1/competitor-intel/battlecards").json()
        for card in data["battlecards"]:
            for obj in card["objections"]:
                assert "objection_en" in obj and obj["objection_en"]
                assert "objection_ar" in obj and obj["objection_ar"]
                assert "response_en" in obj and obj["response_en"]
                assert "response_ar" in obj and obj["response_ar"]

    def test_each_card_has_win_conditions(self) -> None:
        data = client.get("/api/v1/competitor-intel/battlecards").json()
        for card in data["battlecards"]:
            assert "win_conditions_en" in card
            assert len(card["win_conditions_en"]) >= 1

    def test_battlecard_competitor_names_bilingual(self) -> None:
        data = client.get("/api/v1/competitor-intel/battlecards").json()
        for card in data["battlecards"]:
            assert "competitor_name" in card and card["competitor_name"]
            assert "competitor_name_ar" in card and card["competitor_name_ar"]


# ---------------------------------------------------------------------------
# TestCompareEndpoint
# ---------------------------------------------------------------------------


class TestCompareEndpoint:
    def test_returns_200_with_valid_body(self) -> None:
        r = client.post(
            "/api/v1/competitor-intel/compare",
            json={"our_features": ["ZATCA compliance", "Arabic UI"], "competitor_id": "alpha_revenue"},
        )
        assert r.status_code == 200

    def test_governance_decision_present(self) -> None:
        data = client.post(
            "/api/v1/competitor-intel/compare",
            json={"our_features": ["governance layer"], "competitor_id": "nexus_ops"},
        ).json()
        assert data["governance_decision"] == "ALLOW_WITH_REVIEW"

    def test_win_score_in_0_to_100(self) -> None:
        data = client.post(
            "/api/v1/competitor-intel/compare",
            json={"our_features": ["ZATCA", "PDPL", "Arabic"], "competitor_id": "riyadh_tech"},
        ).json()
        assert "win_score" in data
        assert 0 <= data["win_score"] <= 100

    def test_has_recommended_talking_points(self) -> None:
        data = client.post(
            "/api/v1/competitor-intel/compare",
            json={"our_features": ["governance", "proof pack"], "competitor_id": "jadara_saas"},
        ).json()
        assert "recommended_talking_points" in data
        assert len(data["recommended_talking_points"]) >= 1

    def test_talking_points_bilingual(self) -> None:
        data = client.post(
            "/api/v1/competitor-intel/compare",
            json={"our_features": ["Arabic UI"], "competitor_id": "dataflow_arabia"},
        ).json()
        for tp in data["recommended_talking_points"]:
            assert "en" in tp
            assert "ar" in tp

    def test_comparison_rows_present(self) -> None:
        data = client.post(
            "/api/v1/competitor-intel/compare",
            json={"our_features": ["governance", "ZATCA"], "competitor_id": "alpha_revenue"},
        ).json()
        assert "comparison" in data
        assert len(data["comparison"]) == 2

    def test_404_for_unknown_competitor(self) -> None:
        r = client.post(
            "/api/v1/competitor-intel/compare",
            json={"our_features": ["feature"], "competitor_id": "nonexistent_co"},
        )
        assert r.status_code == 404

    def test_422_for_missing_required_fields(self) -> None:
        r = client.post("/api/v1/competitor-intel/compare", json={})
        assert r.status_code == 422

    def test_win_score_interpretation_present(self) -> None:
        data = client.post(
            "/api/v1/competitor-intel/compare",
            json={"our_features": ["governance"], "competitor_id": "nexus_ops"},
        ).json()
        assert "win_score_interpretation_en" in data
        assert "win_score_interpretation_ar" in data


# ---------------------------------------------------------------------------
# TestWinLossEndpoint
# ---------------------------------------------------------------------------


class TestWinLossEndpoint:
    def test_returns_200(self) -> None:
        r = client.get("/api/v1/competitor-intel/win-loss-patterns")
        assert r.status_code == 200

    def test_governance_decision_present(self) -> None:
        data = client.get("/api/v1/competitor-intel/win-loss-patterns").json()
        assert data["governance_decision"] == "ALLOW_WITH_REVIEW"

    def test_five_patterns_returned(self) -> None:
        data = client.get("/api/v1/competitor-intel/win-loss-patterns").json()
        assert len(data["patterns"]) == 5

    def test_overall_summary_present(self) -> None:
        data = client.get("/api/v1/competitor-intel/win-loss-patterns").json()
        overall = data["overall"]
        assert "total_deals_evaluated" in overall
        assert "total_deals_won" in overall
        assert "overall_win_rate_pct" in overall

    def test_win_rates_are_valid_percentages(self) -> None:
        data = client.get("/api/v1/competitor-intel/win-loss-patterns").json()
        for pattern in data["patterns"]:
            assert 0 <= pattern["win_rate_pct"] <= 100

    def test_each_pattern_bilingual_reasons(self) -> None:
        data = client.get("/api/v1/competitor-intel/win-loss-patterns").json()
        for pattern in data["patterns"]:
            assert "top_win_reason_en" in pattern and pattern["top_win_reason_en"]
            assert "top_win_reason_ar" in pattern and pattern["top_win_reason_ar"]

    def test_each_pattern_has_competitor_name(self) -> None:
        data = client.get("/api/v1/competitor-intel/win-loss-patterns").json()
        for pattern in data["patterns"]:
            assert "competitor_name" in pattern and pattern["competitor_name"]

    def test_summary_bilingual(self) -> None:
        data = client.get("/api/v1/competitor-intel/win-loss-patterns").json()
        assert "summary_en" in data
        assert "summary_ar" in data
