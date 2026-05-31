"""Tests for the Proof Pack Operations API — verifiable client result packs.

Covers: data integrity, list/filter, pending delivery, detail, generate,
submit-for-review, approve, deliver, metrics library, doctrine compliance.
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

from api.routers.proof_pack_ops import (  # noqa: E402
    _PACKS,
    _VALID_CHANNELS,
    _VALID_PACK_TYPES,
    _VALID_STATUSES,
    _compute_proof_score,
    _days_since,
    _now_iso,
    router,
)
from fastapi import FastAPI  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

app = FastAPI()
app.include_router(router)
client = TestClient(app, headers={"X-Admin-API-Key": "test-admin-key"})


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _delivered_packs() -> list[dict]:
    return [p for p in _PACKS if p["status"] == "delivered"]


def _approved_packs() -> list[dict]:
    return [p for p in _PACKS if p["status"] == "approved" and p["delivered_at"] is None]


def _draft_packs() -> list[dict]:
    return [p for p in _PACKS if p["status"] == "draft"]


def _review_packs() -> list[dict]:
    return [p for p in _PACKS if p["status"] == "review"]


# ---------------------------------------------------------------------------
# Helper function unit tests
# ---------------------------------------------------------------------------


class TestNowIso:
    def test_returns_string(self):
        result = _now_iso()
        assert isinstance(result, str)

    def test_contains_t_separator(self):
        result = _now_iso()
        assert "T" in result

    def test_has_timezone_offset(self):
        result = _now_iso()
        assert "+" in result or "Z" in result


class TestDaysSince:
    def test_recent_date_returns_small_number(self):
        result = _days_since("2026-05-30T00:00:00+00:00")
        assert isinstance(result, int)
        assert result >= 0

    def test_old_date_returns_large_number(self):
        result = _days_since("2025-01-01T00:00:00+00:00")
        assert result > 100

    def test_invalid_date_returns_zero(self):
        result = _days_since("not-a-date")
        assert result == 0

    def test_returns_non_negative(self):
        result = _days_since("2030-01-01T00:00:00+00:00")
        assert result == 0


class TestComputeProofScore:
    def test_empty_metrics_returns_zero(self):
        assert _compute_proof_score([]) == 0

    def test_all_verified_high_improvement(self):
        metrics = [
            {"verified": True, "improvement_pct": 80.0},
            {"verified": True, "improvement_pct": 100.0},
        ]
        score = _compute_proof_score(metrics)
        assert 0 <= score <= 100

    def test_no_verified_returns_zero(self):
        metrics = [
            {"verified": False, "improvement_pct": 80.0},
            {"verified": False, "improvement_pct": 100.0},
        ]
        assert _compute_proof_score(metrics) == 0

    def test_half_verified(self):
        metrics = [
            {"verified": True, "improvement_pct": 100.0},
            {"verified": False, "improvement_pct": 100.0},
        ]
        score = _compute_proof_score(metrics)
        assert 0 < score <= 50

    def test_score_capped_at_100(self):
        metrics = [{"verified": True, "improvement_pct": 500.0}]
        score = _compute_proof_score(metrics)
        assert score <= 100

    def test_score_not_negative(self):
        metrics = [{"verified": True, "improvement_pct": -50.0}]
        score = _compute_proof_score(metrics)
        assert score >= 0

    def test_returns_int(self):
        metrics = [{"verified": True, "improvement_pct": 60.0}]
        assert isinstance(_compute_proof_score(metrics), int)


# ---------------------------------------------------------------------------
# Data Integrity
# ---------------------------------------------------------------------------


class TestDemoDataIntegrity:
    def test_eight_packs_exist(self):
        assert len(_PACKS) == 8

    def test_all_pack_ids_unique(self):
        ids = [p["pack_id"] for p in _PACKS]
        assert len(ids) == len(set(ids))

    def test_pack_ids_use_pp_prefix(self):
        for p in _PACKS:
            assert p["pack_id"].startswith("PP-")

    def test_all_have_required_fields(self):
        required = {
            "pack_id", "client_id", "company_ar", "company_en",
            "status", "pack_type", "generated_at", "metrics", "proof_score",
        }
        for p in _PACKS:
            for f in required:
                assert f in p, f"Missing field {f!r} in {p['pack_id']}"

    def test_all_statuses_valid(self):
        for p in _PACKS:
            assert p["status"] in _VALID_STATUSES, f"Invalid status in {p['pack_id']}"

    def test_all_pack_types_valid(self):
        for p in _PACKS:
            assert p["pack_type"] in _VALID_PACK_TYPES, f"Invalid pack_type in {p['pack_id']}"

    def test_at_least_three_delivered(self):
        assert len(_delivered_packs()) >= 3

    def test_at_least_two_approved(self):
        assert len(_approved_packs()) >= 2

    def test_at_least_two_draft(self):
        assert len(_draft_packs()) >= 2

    def test_at_least_one_review(self):
        assert len(_review_packs()) >= 1

    def test_proof_score_in_range(self):
        for p in _PACKS:
            assert 0 <= p["proof_score"] <= 100, f"proof_score out of range in {p['pack_id']}"

    def test_metrics_have_all_fields(self):
        required_metric_fields = {
            "metric_name_ar", "metric_name_en",
            "baseline_value", "current_value", "unit", "improvement_pct", "verified",
        }
        for p in _PACKS:
            for m in p["metrics"]:
                for f in required_metric_fields:
                    assert f in m, f"Missing metric field {f!r} in {p['pack_id']}"

    def test_verified_field_is_bool(self):
        for p in _PACKS:
            for m in p["metrics"]:
                assert isinstance(m["verified"], bool)

    def test_delivered_packs_have_delivered_at(self):
        for p in _delivered_packs():
            assert p["delivered_at"] is not None

    def test_approved_packs_have_no_delivered_at(self):
        for p in _approved_packs():
            assert p["delivered_at"] is None

    def test_approved_packs_have_approved_by(self):
        for p in _approved_packs():
            assert p["approved_by"] is not None

    def test_bilingual_company_names(self):
        for p in _PACKS:
            assert p["company_ar"]
            assert p["company_en"]

    def test_delivered_packs_have_delivery_channel(self):
        for p in _delivered_packs():
            assert p["delivery_channel"] in _VALID_CHANNELS

    def test_review_pack_has_reviewer_notes(self):
        for p in _review_packs():
            assert p.get("reviewer_notes") is not None

    def test_all_metrics_have_arabic_names(self):
        for p in _PACKS:
            for m in p["metrics"]:
                assert m["metric_name_ar"]

    def test_all_metrics_have_english_names(self):
        for p in _PACKS:
            for m in p["metrics"]:
                assert m["metric_name_en"]


# ---------------------------------------------------------------------------
# GET / — list endpoint
# ---------------------------------------------------------------------------


class TestListProofPacks:
    def test_returns_200(self):
        assert client.get("/api/v1/proof-packs/").status_code == 200

    def test_governance_decision_allow_with_review(self):
        data = client.get("/api/v1/proof-packs/").json()
        assert data["governance_decision"] == "ALLOW_WITH_REVIEW"

    def test_has_packs_list(self):
        data = client.get("/api/v1/proof-packs/").json()
        assert "packs" in data

    def test_has_summary(self):
        data = client.get("/api/v1/proof-packs/").json()
        assert "summary" in data

    def test_summary_total_packs(self):
        data = client.get("/api/v1/proof-packs/").json()
        assert data["summary"]["total_packs"] == 8

    def test_summary_delivered_count(self):
        data = client.get("/api/v1/proof-packs/").json()
        assert data["summary"]["delivered_count"] >= 3

    def test_summary_pending_delivery_count(self):
        data = client.get("/api/v1/proof-packs/").json()
        assert data["summary"]["pending_delivery_count"] >= 2

    def test_summary_avg_proof_score(self):
        data = client.get("/api/v1/proof-packs/").json()
        assert 0 <= data["summary"]["avg_proof_score"] <= 100

    def test_summary_total_clients_with_packs(self):
        data = client.get("/api/v1/proof-packs/").json()
        assert data["summary"]["total_clients_with_packs"] >= 1

    def test_has_generated_at(self):
        data = client.get("/api/v1/proof-packs/").json()
        assert "generated_at" in data

    def test_filter_by_status_delivered(self):
        data = client.get("/api/v1/proof-packs/?status=delivered").json()
        for p in data["packs"]:
            assert p["status"] == "delivered"

    def test_filter_by_status_draft(self):
        data = client.get("/api/v1/proof-packs/?status=draft").json()
        for p in data["packs"]:
            assert p["status"] == "draft"

    def test_filter_by_status_approved(self):
        data = client.get("/api/v1/proof-packs/?status=approved").json()
        for p in data["packs"]:
            assert p["status"] == "approved"

    def test_filter_unknown_status_returns_empty(self):
        data = client.get("/api/v1/proof-packs/?status=nonexistent").json()
        assert data["packs"] == []

    def test_sorted_by_generated_at_descending(self):
        data = client.get("/api/v1/proof-packs/").json()
        dates = [p["generated_at"] for p in data["packs"]]
        assert dates == sorted(dates, reverse=True)

    def test_filter_count_accurate(self):
        data_delivered = client.get("/api/v1/proof-packs/?status=delivered").json()
        delivered_packs = [p for p in _PACKS if p["status"] == "delivered"]
        assert len(data_delivered["packs"]) == len(delivered_packs)


# ---------------------------------------------------------------------------
# GET /pending-delivery
# ---------------------------------------------------------------------------


class TestPendingDelivery:
    def test_returns_200(self):
        assert client.get("/api/v1/proof-packs/pending-delivery").status_code == 200

    def test_governance_decision_allow_with_review(self):
        data = client.get("/api/v1/proof-packs/pending-delivery").json()
        assert data["governance_decision"] == "ALLOW_WITH_REVIEW"

    def test_only_approved_undelivered_packs(self):
        data = client.get("/api/v1/proof-packs/pending-delivery").json()
        for p in data["packs"]:
            assert p["status"] == "approved"
            assert p["delivered_at"] is None

    def test_pending_count_accurate(self):
        data = client.get("/api/v1/proof-packs/pending-delivery").json()
        assert data["pending_count"] == len(data["packs"])

    def test_has_days_since_approval(self):
        data = client.get("/api/v1/proof-packs/pending-delivery").json()
        for p in data["packs"]:
            assert "days_since_approval" in p
            assert isinstance(p["days_since_approval"], int)
            assert p["days_since_approval"] >= 0

    def test_has_bilingual_action(self):
        data = client.get("/api/v1/proof-packs/pending-delivery").json()
        assert "action_ar" in data
        assert "action_en" in data

    def test_action_ar_is_arabic_text(self):
        data = client.get("/api/v1/proof-packs/pending-delivery").json()
        assert data["action_ar"]
        assert len(data["action_ar"]) > 5

    def test_action_en_is_english_text(self):
        data = client.get("/api/v1/proof-packs/pending-delivery").json()
        assert data["action_en"]
        assert len(data["action_en"]) > 5

    def test_has_generated_at(self):
        data = client.get("/api/v1/proof-packs/pending-delivery").json()
        assert "generated_at" in data

    def test_no_delivered_packs_in_pending(self):
        data = client.get("/api/v1/proof-packs/pending-delivery").json()
        pack_ids = {p["pack_id"] for p in data["packs"]}
        for p in _delivered_packs():
            assert p["pack_id"] not in pack_ids

    def test_no_draft_packs_in_pending(self):
        data = client.get("/api/v1/proof-packs/pending-delivery").json()
        pack_ids = {p["pack_id"] for p in data["packs"]}
        for p in _draft_packs():
            assert p["pack_id"] not in pack_ids


# ---------------------------------------------------------------------------
# GET /{pack_id}
# ---------------------------------------------------------------------------


class TestGetProofPackDetail:
    def test_returns_200_for_valid_id(self):
        assert client.get("/api/v1/proof-packs/PP-001").status_code == 200

    def test_returns_404_for_unknown_id(self):
        assert client.get("/api/v1/proof-packs/PP-UNKNOWN").status_code == 404

    def test_governance_decision_allow_with_review(self):
        data = client.get("/api/v1/proof-packs/PP-001").json()
        assert data["governance_decision"] == "ALLOW_WITH_REVIEW"

    def test_pack_id_matches(self):
        data = client.get("/api/v1/proof-packs/PP-001").json()
        assert data["pack_id"] == "PP-001"

    def test_has_metrics(self):
        data = client.get("/api/v1/proof-packs/PP-001").json()
        assert "metrics" in data
        assert len(data["metrics"]) > 0

    def test_has_proof_score(self):
        data = client.get("/api/v1/proof-packs/PP-001").json()
        assert "proof_score" in data
        assert 0 <= data["proof_score"] <= 100

    def test_has_status(self):
        data = client.get("/api/v1/proof-packs/PP-001").json()
        assert "status" in data

    def test_has_pack_type(self):
        data = client.get("/api/v1/proof-packs/PP-001").json()
        assert "pack_type" in data

    def test_has_company_ar(self):
        data = client.get("/api/v1/proof-packs/PP-001").json()
        assert "company_ar" in data

    def test_has_company_en(self):
        data = client.get("/api/v1/proof-packs/PP-001").json()
        assert "company_en" in data

    def test_has_generated_at(self):
        data = client.get("/api/v1/proof-packs/PP-001").json()
        assert "generated_at" in data

    def test_review_pack_detail(self):
        data = client.get("/api/v1/proof-packs/PP-008").json()
        assert data["status"] == "review"

    def test_approved_pack_has_approved_by(self):
        data = client.get("/api/v1/proof-packs/PP-004").json()
        assert data["approved_by"] is not None


# ---------------------------------------------------------------------------
# POST /generate
# ---------------------------------------------------------------------------


class TestGeneratePack:
    def _valid_body(self, **kwargs) -> dict:
        base = {
            "client_id": "CLT-TEST",
            "company_ar": "شركة الاختبار",
            "company_en": "Test Company",
            "pack_type": "sprint_result",
            "sprint_id": "SPR-TEST",
            "initial_metrics": [
                {
                    "metric_name_ar": "درجة جودة البيانات",
                    "metric_name_en": "Data Quality Score",
                    "baseline_value": 40.0,
                    "current_value": 80.0,
                    "unit": "score",
                    "verified": True,
                }
            ],
        }
        base.update(kwargs)
        return base

    def test_returns_200(self):
        r = client.post("/api/v1/proof-packs/generate", json=self._valid_body())
        assert r.status_code == 200

    def test_governance_decision_approval_first(self):
        r = client.post("/api/v1/proof-packs/generate", json=self._valid_body())
        assert r.json()["governance_decision"] == "APPROVAL_FIRST"

    def test_status_is_draft(self):
        r = client.post("/api/v1/proof-packs/generate", json=self._valid_body())
        assert r.json()["pack"]["status"] == "draft"

    def test_pack_id_assigned(self):
        r = client.post("/api/v1/proof-packs/generate", json=self._valid_body())
        pack_id = r.json()["pack"]["pack_id"]
        assert pack_id.startswith("PP-")

    def test_improvement_pct_computed(self):
        r = client.post("/api/v1/proof-packs/generate", json=self._valid_body())
        metric = r.json()["pack"]["metrics"][0]
        assert "improvement_pct" in metric
        assert metric["improvement_pct"] == 100.0

    def test_proof_score_auto_computed(self):
        r = client.post("/api/v1/proof-packs/generate", json=self._valid_body())
        score = r.json()["pack"]["proof_score"]
        assert isinstance(score, int)
        assert 0 <= score <= 100

    def test_verified_metric_affects_score(self):
        body_verified = self._valid_body()
        body_unverified = self._valid_body()
        body_unverified["initial_metrics"][0]["verified"] = False
        r1 = client.post("/api/v1/proof-packs/generate", json=body_verified)
        r2 = client.post("/api/v1/proof-packs/generate", json=body_unverified)
        assert r1.json()["pack"]["proof_score"] >= r2.json()["pack"]["proof_score"]

    def test_invalid_pack_type_returns_422(self):
        r = client.post("/api/v1/proof-packs/generate", json=self._valid_body(pack_type="bad_type"))
        assert r.status_code == 422

    def test_no_metrics_gives_zero_proof_score(self):
        body = self._valid_body()
        body["initial_metrics"] = []
        r = client.post("/api/v1/proof-packs/generate", json=body)
        assert r.json()["pack"]["proof_score"] == 0

    def test_delivered_at_is_null(self):
        r = client.post("/api/v1/proof-packs/generate", json=self._valid_body())
        assert r.json()["pack"]["delivered_at"] is None

    def test_has_bilingual_message(self):
        r = client.post("/api/v1/proof-packs/generate", json=self._valid_body())
        data = r.json()
        assert "message_ar" in data
        assert "message_en" in data

    def test_monthly_ops_pack_type_accepted(self):
        r = client.post("/api/v1/proof-packs/generate", json=self._valid_body(pack_type="monthly_ops"))
        assert r.status_code == 200

    def test_annual_review_pack_type_accepted(self):
        r = client.post("/api/v1/proof-packs/generate", json=self._valid_body(pack_type="annual_review"))
        assert r.status_code == 200

    def test_zatca_compliance_pack_type_accepted(self):
        r = client.post("/api/v1/proof-packs/generate", json=self._valid_body(pack_type="zatca_compliance"))
        assert r.status_code == 200

    def test_zero_baseline_improvement_computed(self):
        body = self._valid_body()
        body["initial_metrics"][0]["baseline_value"] = 0.0
        body["initial_metrics"][0]["current_value"] = 50.0
        r = client.post("/api/v1/proof-packs/generate", json=body)
        metric = r.json()["pack"]["metrics"][0]
        assert metric["improvement_pct"] == 100.0

    def test_negative_baseline_improvement_computed(self):
        body = self._valid_body()
        body["initial_metrics"][0]["baseline_value"] = 100.0
        body["initial_metrics"][0]["current_value"] = 50.0
        r = client.post("/api/v1/proof-packs/generate", json=body)
        metric = r.json()["pack"]["metrics"][0]
        assert metric["improvement_pct"] == -50.0

    def test_new_pack_retrievable_by_id(self):
        r = client.post("/api/v1/proof-packs/generate", json=self._valid_body())
        pack_id = r.json()["pack"]["pack_id"]
        r2 = client.get(f"/api/v1/proof-packs/{pack_id}")
        assert r2.status_code == 200
        assert r2.json()["pack_id"] == pack_id


# ---------------------------------------------------------------------------
# POST /{pack_id}/submit-for-review
# ---------------------------------------------------------------------------


class TestSubmitForReview:
    def _get_draft_id(self) -> str:
        drafts = _draft_packs()
        assert drafts, "No draft packs available"
        return drafts[0]["pack_id"]

    def test_returns_200_for_draft(self):
        pack_id = self._get_draft_id()
        r = client.post(
            f"/api/v1/proof-packs/{pack_id}/submit-for-review",
            json={"notes": "Ready for founder sign-off review"},
        )
        assert r.status_code == 200

    def test_governance_decision_approval_first(self):
        pack_id = self._get_draft_id()
        r = client.post(
            f"/api/v1/proof-packs/{pack_id}/submit-for-review",
            json={"notes": "Requesting founder review now"},
        )
        if r.status_code == 200:
            assert r.json()["governance_decision"] == "APPROVAL_FIRST"

    def test_status_changes_to_review(self):
        body = {
            "client_id": "CLT-SR", "company_ar": "شركة ب", "company_en": "Company B",
            "pack_type": "sprint_result", "initial_metrics": [],
        }
        gen_r = client.post("/api/v1/proof-packs/generate", json=body)
        pack_id = gen_r.json()["pack"]["pack_id"]
        client.post(
            f"/api/v1/proof-packs/{pack_id}/submit-for-review",
            json={"notes": "All metrics validated and ready"},
        )
        detail = client.get(f"/api/v1/proof-packs/{pack_id}").json()
        assert detail["status"] == "review"

    def test_400_for_non_draft(self):
        r = client.post(
            "/api/v1/proof-packs/PP-001/submit-for-review",
            json={"notes": "Should fail — already delivered"},
        )
        assert r.status_code == 400

    def test_400_for_approved_pack(self):
        r = client.post(
            "/api/v1/proof-packs/PP-004/submit-for-review",
            json={"notes": "Should fail — already approved"},
        )
        assert r.status_code == 400

    def test_400_for_review_pack(self):
        r = client.post(
            "/api/v1/proof-packs/PP-008/submit-for-review",
            json={"notes": "Should fail — already in review"},
        )
        assert r.status_code == 400

    def test_404_for_unknown_pack(self):
        r = client.post(
            "/api/v1/proof-packs/PP-UNKNOWN/submit-for-review",
            json={"notes": "Should return 404"},
        )
        assert r.status_code == 404

    def test_notes_too_short_returns_422(self):
        pack_id = self._get_draft_id()
        r = client.post(
            f"/api/v1/proof-packs/{pack_id}/submit-for-review",
            json={"notes": "No"},
        )
        assert r.status_code == 422

    def test_response_contains_notes(self):
        body = {
            "client_id": "CLT-SR2", "company_ar": "شركة ج", "company_en": "Company C",
            "pack_type": "monthly_ops", "initial_metrics": [],
        }
        gen_r = client.post("/api/v1/proof-packs/generate", json=body)
        pack_id = gen_r.json()["pack"]["pack_id"]
        r = client.post(
            f"/api/v1/proof-packs/{pack_id}/submit-for-review",
            json={"notes": "Metrics have been verified by data team"},
        )
        assert r.json()["reviewer_notes"] == "Metrics have been verified by data team"


# ---------------------------------------------------------------------------
# POST /{pack_id}/approve
# ---------------------------------------------------------------------------


class TestApprovePack:
    def _get_review_id(self) -> str:
        reviews = _review_packs()
        assert reviews, "No review packs available"
        return reviews[0]["pack_id"]

    def test_returns_200_for_review_pack(self):
        body = {
            "client_id": "CLT-APR", "company_ar": "شركة د", "company_en": "Company D",
            "pack_type": "zatca_compliance", "initial_metrics": [],
        }
        gen_r = client.post("/api/v1/proof-packs/generate", json=body)
        pack_id = gen_r.json()["pack"]["pack_id"]
        client.post(
            f"/api/v1/proof-packs/{pack_id}/submit-for-review",
            json={"notes": "Ready for founder approval sign-off"},
        )
        r = client.post(
            f"/api/v1/proof-packs/{pack_id}/approve",
            json={"approved_by": "Bassam Al-Assiri"},
        )
        assert r.status_code == 200

    def test_governance_decision_approval_first(self):
        body = {
            "client_id": "CLT-APR2", "company_ar": "شركة ه", "company_en": "Company E",
            "pack_type": "sprint_result", "initial_metrics": [],
        }
        gen_r = client.post("/api/v1/proof-packs/generate", json=body)
        pack_id = gen_r.json()["pack"]["pack_id"]
        client.post(
            f"/api/v1/proof-packs/{pack_id}/submit-for-review",
            json={"notes": "All checks completed and ready"},
        )
        r = client.post(
            f"/api/v1/proof-packs/{pack_id}/approve",
            json={"approved_by": "Bassam Al-Assiri"},
        )
        assert r.json()["governance_decision"] == "APPROVAL_FIRST"

    def test_approved_by_recorded(self):
        body = {
            "client_id": "CLT-APR3", "company_ar": "شركة و", "company_en": "Company F",
            "pack_type": "annual_review", "initial_metrics": [],
        }
        gen_r = client.post("/api/v1/proof-packs/generate", json=body)
        pack_id = gen_r.json()["pack"]["pack_id"]
        client.post(
            f"/api/v1/proof-packs/{pack_id}/submit-for-review",
            json={"notes": "Annual review completed with all departments"},
        )
        r = client.post(
            f"/api/v1/proof-packs/{pack_id}/approve",
            json={"approved_by": "Founder Name"},
        )
        assert r.json()["approved_by"] == "Founder Name"

    def test_400_for_draft_pack(self):
        pack_id = _draft_packs()[0]["pack_id"]
        r = client.post(
            f"/api/v1/proof-packs/{pack_id}/approve",
            json={"approved_by": "Founder"},
        )
        assert r.status_code == 400

    def test_400_for_delivered_pack(self):
        r = client.post(
            "/api/v1/proof-packs/PP-001/approve",
            json={"approved_by": "Founder"},
        )
        assert r.status_code == 400

    def test_404_for_unknown_pack(self):
        r = client.post(
            "/api/v1/proof-packs/PP-UNKNOWN/approve",
            json={"approved_by": "Founder"},
        )
        assert r.status_code == 404

    def test_approved_by_too_short_returns_422(self):
        pack_id = _review_packs()[0]["pack_id"] if _review_packs() else "PP-008"
        r = client.post(
            f"/api/v1/proof-packs/{pack_id}/approve",
            json={"approved_by": "AB"},
        )
        assert r.status_code == 422

    def test_status_changes_to_approved(self):
        body = {
            "client_id": "CLT-APR4", "company_ar": "شركة ز", "company_en": "Company G",
            "pack_type": "sprint_result", "initial_metrics": [],
        }
        gen_r = client.post("/api/v1/proof-packs/generate", json=body)
        pack_id = gen_r.json()["pack"]["pack_id"]
        client.post(
            f"/api/v1/proof-packs/{pack_id}/submit-for-review",
            json={"notes": "Ready for founder review and approval"},
        )
        client.post(
            f"/api/v1/proof-packs/{pack_id}/approve",
            json={"approved_by": "Founder"},
        )
        detail = client.get(f"/api/v1/proof-packs/{pack_id}").json()
        assert detail["status"] == "approved"


# ---------------------------------------------------------------------------
# POST /{pack_id}/deliver
# ---------------------------------------------------------------------------


class TestDeliverPack:
    def _get_approved_id(self) -> str:
        approved = _approved_packs()
        assert approved, "No approved packs available"
        return approved[0]["pack_id"]

    def _make_approved_pack(self) -> str:
        body = {
            "client_id": "CLT-DLV", "company_ar": "شركة ح", "company_en": "Company H",
            "pack_type": "sprint_result", "initial_metrics": [],
        }
        gen_r = client.post("/api/v1/proof-packs/generate", json=body)
        pack_id = gen_r.json()["pack"]["pack_id"]
        client.post(
            f"/api/v1/proof-packs/{pack_id}/submit-for-review",
            json={"notes": "Ready for delivery via email channel"},
        )
        client.post(
            f"/api/v1/proof-packs/{pack_id}/approve",
            json={"approved_by": "Founder"},
        )
        return pack_id

    def test_returns_200_for_approved_pack(self):
        pack_id = self._make_approved_pack()
        r = client.post(
            f"/api/v1/proof-packs/{pack_id}/deliver",
            json={"delivery_channel": "email"},
        )
        assert r.status_code == 200

    def test_governance_decision_approval_first(self):
        pack_id = self._make_approved_pack()
        r = client.post(
            f"/api/v1/proof-packs/{pack_id}/deliver",
            json={"delivery_channel": "email"},
        )
        assert r.json()["governance_decision"] == "APPROVAL_FIRST"

    def test_status_changes_to_delivered(self):
        pack_id = self._make_approved_pack()
        client.post(
            f"/api/v1/proof-packs/{pack_id}/deliver",
            json={"delivery_channel": "in_person"},
        )
        detail = client.get(f"/api/v1/proof-packs/{pack_id}").json()
        assert detail["status"] == "delivered"

    def test_delivered_at_set(self):
        pack_id = self._make_approved_pack()
        r = client.post(
            f"/api/v1/proof-packs/{pack_id}/deliver",
            json={"delivery_channel": "email"},
        )
        assert r.json()["delivered_at"] is not None

    def test_delivery_channel_recorded(self):
        pack_id = self._make_approved_pack()
        r = client.post(
            f"/api/v1/proof-packs/{pack_id}/deliver",
            json={"delivery_channel": "in_person"},
        )
        assert r.json()["delivery_channel"] == "in_person"

    def test_400_for_draft_pack(self):
        pack_id = _draft_packs()[0]["pack_id"]
        r = client.post(
            f"/api/v1/proof-packs/{pack_id}/deliver",
            json={"delivery_channel": "email"},
        )
        assert r.status_code == 400

    def test_400_for_already_delivered(self):
        r = client.post(
            "/api/v1/proof-packs/PP-001/deliver",
            json={"delivery_channel": "email"},
        )
        assert r.status_code == 400

    def test_400_for_review_pack(self):
        r = client.post(
            "/api/v1/proof-packs/PP-008/deliver",
            json={"delivery_channel": "email"},
        )
        assert r.status_code == 400

    def test_404_for_unknown_pack(self):
        r = client.post(
            "/api/v1/proof-packs/PP-UNKNOWN/deliver",
            json={"delivery_channel": "email"},
        )
        assert r.status_code == 404

    def test_invalid_channel_returns_422(self):
        pack_id = self._make_approved_pack()
        r = client.post(
            f"/api/v1/proof-packs/{pack_id}/deliver",
            json={"delivery_channel": "telegram"},
        )
        assert r.status_code == 422

    def test_email_channel_no_consent_note(self):
        pack_id = self._make_approved_pack()
        r = client.post(
            f"/api/v1/proof-packs/{pack_id}/deliver",
            json={"delivery_channel": "email"},
        )
        data = r.json()
        assert "whatsapp_note_ar" not in data
        assert "whatsapp_note_en" not in data

    def test_in_person_channel_no_consent_note(self):
        pack_id = self._make_approved_pack()
        r = client.post(
            f"/api/v1/proof-packs/{pack_id}/deliver",
            json={"delivery_channel": "in_person"},
        )
        data = r.json()
        assert "whatsapp_note_ar" not in data
        assert "whatsapp_note_en" not in data

    def test_has_bilingual_message(self):
        pack_id = self._make_approved_pack()
        r = client.post(
            f"/api/v1/proof-packs/{pack_id}/deliver",
            json={"delivery_channel": "email"},
        )
        data = r.json()
        assert "message_ar" in data
        assert "message_en" in data


# ---------------------------------------------------------------------------
# Doctrine: WhatsApp delivery requires consent note
# ---------------------------------------------------------------------------


class TestDoctrineWhatsAppConsent:
    def _make_approved_pack(self) -> str:
        body = {
            "client_id": "CLT-WA", "company_ar": "شركة ط", "company_en": "Company I",
            "pack_type": "sprint_result", "initial_metrics": [],
        }
        gen_r = client.post("/api/v1/proof-packs/generate", json=body)
        pack_id = gen_r.json()["pack"]["pack_id"]
        client.post(
            f"/api/v1/proof-packs/{pack_id}/submit-for-review",
            json={"notes": "Metrics approved and ready for WhatsApp delivery"},
        )
        client.post(
            f"/api/v1/proof-packs/{pack_id}/approve",
            json={"approved_by": "Founder"},
        )
        return pack_id

    def test_whatsapp_delivery_has_consent_note_ar(self):
        pack_id = self._make_approved_pack()
        r = client.post(
            f"/api/v1/proof-packs/{pack_id}/deliver",
            json={"delivery_channel": "whatsapp"},
        )
        assert r.status_code == 200
        assert "whatsapp_note_ar" in r.json()

    def test_whatsapp_delivery_has_consent_note_en(self):
        pack_id = self._make_approved_pack()
        r = client.post(
            f"/api/v1/proof-packs/{pack_id}/deliver",
            json={"delivery_channel": "whatsapp"},
        )
        assert r.status_code == 200
        assert "whatsapp_note_en" in r.json()

    def test_whatsapp_consent_note_ar_content(self):
        pack_id = self._make_approved_pack()
        r = client.post(
            f"/api/v1/proof-packs/{pack_id}/deliver",
            json={"delivery_channel": "whatsapp"},
        )
        note_ar = r.json()["whatsapp_note_ar"]
        assert "موافقة" in note_ar or "واتساب" in note_ar

    def test_whatsapp_consent_note_en_content(self):
        pack_id = self._make_approved_pack()
        r = client.post(
            f"/api/v1/proof-packs/{pack_id}/deliver",
            json={"delivery_channel": "whatsapp"},
        )
        note_en = r.json()["whatsapp_note_en"]
        assert "consent" in note_en.lower() or "whatsapp" in note_en.lower()

    def test_whatsapp_delivery_still_requires_approval_first(self):
        pack_id = self._make_approved_pack()
        r = client.post(
            f"/api/v1/proof-packs/{pack_id}/deliver",
            json={"delivery_channel": "whatsapp"},
        )
        assert r.json()["governance_decision"] == "APPROVAL_FIRST"


# ---------------------------------------------------------------------------
# GET /metrics-library
# ---------------------------------------------------------------------------


class TestMetricsLibrary:
    def test_returns_200(self):
        assert client.get("/api/v1/proof-packs/metrics-library").status_code == 200

    def test_governance_decision_allow_with_review(self):
        data = client.get("/api/v1/proof-packs/metrics-library").json()
        assert data["governance_decision"] == "ALLOW_WITH_REVIEW"

    def test_has_metrics_dict(self):
        data = client.get("/api/v1/proof-packs/metrics-library").json()
        assert "metrics" in data
        assert isinstance(data["metrics"], dict)

    def test_has_total_unique_metrics(self):
        data = client.get("/api/v1/proof-packs/metrics-library").json()
        assert "total_unique_metrics" in data
        assert data["total_unique_metrics"] >= 1

    def test_metric_count_is_positive(self):
        data = client.get("/api/v1/proof-packs/metrics-library").json()
        for name, count in data["metrics"].items():
            assert count >= 1, f"Metric {name!r} has zero count"

    def test_known_metric_appears(self):
        data = client.get("/api/v1/proof-packs/metrics-library").json()
        assert "Data Quality Score" in data["metrics"]

    def test_zatca_metric_appears(self):
        data = client.get("/api/v1/proof-packs/metrics-library").json()
        assert "ZATCA Compliance Rate" in data["metrics"]

    def test_count_matches_dict_size(self):
        data = client.get("/api/v1/proof-packs/metrics-library").json()
        assert data["total_unique_metrics"] == len(data["metrics"])

    def test_has_generated_at(self):
        data = client.get("/api/v1/proof-packs/metrics-library").json()
        assert "generated_at" in data

    def test_returns_dict_not_list(self):
        data = client.get("/api/v1/proof-packs/metrics-library").json()
        assert isinstance(data["metrics"], dict)
