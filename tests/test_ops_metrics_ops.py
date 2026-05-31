"""Tests for the ops_metrics_ops API router.

Covers: demo data integrity, snapshot, pulse, weekly-summary, benchmarks,
flag-issue, health computation, governance decision presence, and helper
function correctness.
"""

from __future__ import annotations

import os
import sys
import types

import pytest

os.environ.setdefault("ADMIN_API_KEY", "test-admin-key")
os.environ.setdefault("ADMIN_API_KEYS", "test-admin-key")

# ---------------------------------------------------------------------------
# Stub the security module before any router import to avoid jose/crypto issues
# ---------------------------------------------------------------------------
_mock_security = types.ModuleType("api.security.api_key")
_mock_security.require_admin_key = lambda: None
sys.modules.setdefault("api.security.api_key", _mock_security)
if "api.security" not in sys.modules:
    sys.modules["api.security"] = types.ModuleType("api.security")

from api.routers.ops_metrics_ops import (  # noqa: E402
    VALID_ISSUE_TYPES,
    VALID_PRIORITIES,
    _FLAGGED_ISSUES,
    _OPS_SNAPSHOT,
    _build_alerts,
    _compute_health,
    _issue_type_label,
    _now_iso,
    _priority_label,
    router,
)
from fastapi import FastAPI  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

app = FastAPI()
app.include_router(router)
client = TestClient(app, headers={"X-Admin-API-Key": "test-admin-key"})


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture(autouse=True)
def _clear_flagged_issues():
    """Clear the in-memory flagged issues store after each test."""
    yield
    _FLAGGED_ISSUES.clear()


# ===========================================================================
# 1. Demo data integrity
# ===========================================================================


class TestOpsSnapshotData:
    # Revenue fields
    def test_mrr_sar_present(self):
        assert "mrr_sar" in _OPS_SNAPSHOT

    def test_arr_sar_present(self):
        assert "arr_sar" in _OPS_SNAPSHOT

    def test_mrr_growth_pct_present(self):
        assert "mrr_growth_pct" in _OPS_SNAPSHOT

    def test_nrr_pct_present(self):
        assert "nrr_pct" in _OPS_SNAPSHOT

    # Client fields
    def test_active_clients_present(self):
        assert "active_clients" in _OPS_SNAPSHOT

    def test_at_risk_clients_present(self):
        assert "at_risk_clients" in _OPS_SNAPSHOT

    def test_avg_health_score_present(self):
        assert "avg_health_score" in _OPS_SNAPSHOT

    def test_avg_proof_score_present(self):
        assert "avg_proof_score" in _OPS_SNAPSHOT

    # Pipeline fields
    def test_pipeline_deals_present(self):
        assert "pipeline_deals" in _OPS_SNAPSHOT

    def test_pipeline_value_sar_present(self):
        assert "pipeline_value_sar" in _OPS_SNAPSHOT

    def test_deals_closing_30d_present(self):
        assert "deals_closing_30d" in _OPS_SNAPSHOT

    # Operations fields
    def test_active_onboardings_present(self):
        assert "active_onboardings" in _OPS_SNAPSHOT

    def test_pending_approvals_present(self):
        assert "pending_approvals" in _OPS_SNAPSHOT

    def test_open_invoices_present(self):
        assert "open_invoices" in _OPS_SNAPSHOT

    def test_overdue_invoices_present(self):
        assert "overdue_invoices" in _OPS_SNAPSHOT

    # Proof pack fields
    def test_proof_packs_delivered_30d_present(self):
        assert "proof_packs_delivered_30d" in _OPS_SNAPSHOT

    def test_proof_packs_pending_delivery_present(self):
        assert "proof_packs_pending_delivery" in _OPS_SNAPSHOT

    # Team fields
    def test_active_team_members_present(self):
        assert "active_team_members" in _OPS_SNAPSHOT

    def test_open_roles_present(self):
        assert "open_roles" in _OPS_SNAPSHOT

    # Compliance fields
    def test_zatca_compliance_rate_pct_present(self):
        assert "zatca_compliance_rate_pct" in _OPS_SNAPSHOT

    def test_pdpl_readiness_score_present(self):
        assert "pdpl_readiness_score" in _OPS_SNAPSHOT

    # Value assertions — all numeric values must be positive
    def test_mrr_sar_positive(self):
        assert _OPS_SNAPSHOT["mrr_sar"] > 0

    def test_arr_sar_positive(self):
        assert _OPS_SNAPSHOT["arr_sar"] > 0

    def test_active_clients_positive(self):
        assert _OPS_SNAPSHOT["active_clients"] > 0

    def test_pipeline_value_positive(self):
        assert _OPS_SNAPSHOT["pipeline_value_sar"] > 0

    def test_zatca_compliance_rate_positive(self):
        assert _OPS_SNAPSHOT["zatca_compliance_rate_pct"] > 0

    def test_total_field_count(self):
        # 4 revenue + 4 client + 3 pipeline + 4 operations + 2 proof_packs
        # + 2 team + 2 compliance = 21 fields
        assert len(_OPS_SNAPSHOT) == 21


# ===========================================================================
# 2. Helper — _now_iso
# ===========================================================================


class TestNowIso:
    def test_returns_string(self):
        assert isinstance(_now_iso(), str)

    def test_contains_t_separator(self):
        assert "T" in _now_iso()

    def test_ends_with_utc_offset(self):
        result = _now_iso()
        assert "+00:00" in result or result.endswith("Z")

    def test_two_calls_differ_or_same_second(self):
        # Just confirm it doesn't throw
        a = _now_iso()
        b = _now_iso()
        assert isinstance(a, str) and isinstance(b, str)


# ===========================================================================
# 3. Helper — _compute_health
# ===========================================================================


class TestComputeHealth:
    def test_returns_tuple(self):
        result = _compute_health(_OPS_SNAPSHOT)
        assert isinstance(result, tuple) and len(result) == 2

    def test_score_is_float(self):
        score, _ = _compute_health(_OPS_SNAPSHOT)
        assert isinstance(score, float)

    def test_band_is_string(self):
        _, band = _compute_health(_OPS_SNAPSHOT)
        assert isinstance(band, str)

    def test_score_0_to_100(self):
        score, _ = _compute_health(_OPS_SNAPSHOT)
        assert 0.0 <= score <= 100.0

    def test_green_band_at_75_plus(self):
        snap = dict(_OPS_SNAPSHOT)
        snap["mrr_growth_pct"] = 10.0
        snap["avg_health_score"] = 90
        snap["proof_packs_delivered_30d"] = 8
        snap["pending_approvals"] = 1
        snap["zatca_compliance_rate_pct"] = 100
        snap["pdpl_readiness_score"] = 100
        score, band = _compute_health(snap)
        assert score >= 75.0
        assert band == "green"

    def test_red_band_below_50(self):
        snap = dict(_OPS_SNAPSHOT)
        snap["mrr_growth_pct"] = -5.0
        snap["avg_health_score"] = 20
        snap["proof_packs_delivered_30d"] = 1
        snap["pending_approvals"] = 10
        snap["zatca_compliance_rate_pct"] = 40
        snap["pdpl_readiness_score"] = 40
        score, band = _compute_health(snap)
        assert score < 50.0
        assert band == "red"

    def test_amber_band_between_50_and_74(self):
        snap = dict(_OPS_SNAPSHOT)
        snap["mrr_growth_pct"] = 1.0        # revenue_health = 70
        snap["avg_health_score"] = 55       # client_health = 55
        snap["proof_packs_delivered_30d"] = 2  # delivery_health = 65
        snap["pending_approvals"] = 2
        snap["zatca_compliance_rate_pct"] = 60
        snap["pdpl_readiness_score"] = 60
        score, band = _compute_health(snap)
        assert 50.0 <= score < 75.0
        assert band == "amber"

    def test_revenue_health_100_when_growth_ge_5(self):
        snap = dict(_OPS_SNAPSHOT)
        snap["mrr_growth_pct"] = 5.0
        score_5, _ = _compute_health(snap)
        snap["mrr_growth_pct"] = 10.0
        score_10, _ = _compute_health(snap)
        # Both should contribute 100 * 0.30 to the revenue component
        assert score_5 == score_10

    def test_revenue_health_70_when_growth_zero(self):
        snap = dict(_OPS_SNAPSHOT)
        snap["mrr_growth_pct"] = 0.0
        score_zero, _ = _compute_health(snap)
        snap["mrr_growth_pct"] = 3.0
        score_three, _ = _compute_health(snap)
        assert score_zero == score_three

    def test_revenue_health_40_when_growth_negative(self):
        snap_neg = dict(_OPS_SNAPSHOT)
        snap_neg["mrr_growth_pct"] = -1.0
        snap_zero = dict(_OPS_SNAPSHOT)
        snap_zero["mrr_growth_pct"] = 0.0
        score_neg, _ = _compute_health(snap_neg)
        score_zero, _ = _compute_health(snap_zero)
        assert score_neg < score_zero

    def test_delivery_health_90_when_delivered_gt_3_and_approvals_le_3(self):
        snap = dict(_OPS_SNAPSHOT)
        snap["proof_packs_delivered_30d"] = 4
        snap["pending_approvals"] = 3
        score_high, _ = _compute_health(snap)
        snap["proof_packs_delivered_30d"] = 1
        score_low, _ = _compute_health(snap)
        assert score_high > score_low

    def test_score_clamped_to_100(self):
        snap = {k: 999 for k in _OPS_SNAPSHOT}
        snap["mrr_growth_pct"] = 100
        snap["avg_health_score"] = 100
        snap["proof_packs_delivered_30d"] = 100
        snap["pending_approvals"] = 0
        snap["zatca_compliance_rate_pct"] = 100
        snap["pdpl_readiness_score"] = 100
        score, _ = _compute_health(snap)
        assert score <= 100.0


# ===========================================================================
# 4. Snapshot endpoint
# ===========================================================================


class TestSnapshotEndpoint:
    def test_returns_200(self):
        resp = client.get("/api/v1/ops-metrics/snapshot")
        assert resp.status_code == 200

    def test_governance_decision_present(self):
        resp = client.get("/api/v1/ops-metrics/snapshot")
        assert "governance_decision" in resp.json()

    def test_governance_is_allow_with_review(self):
        resp = client.get("/api/v1/ops-metrics/snapshot")
        assert resp.json()["governance_decision"] == "ALLOW_WITH_REVIEW"

    def test_overall_health_score_present(self):
        resp = client.get("/api/v1/ops-metrics/snapshot")
        assert "overall_health_score" in resp.json()

    def test_overall_health_score_in_range(self):
        score = client.get("/api/v1/ops-metrics/snapshot").json()["overall_health_score"]
        assert 0.0 <= score <= 100.0

    def test_health_band_valid(self):
        band = client.get("/api/v1/ops-metrics/snapshot").json()["health_band"]
        assert band in ("green", "amber", "red")

    def test_kpis_key_present(self):
        assert "kpis" in client.get("/api/v1/ops-metrics/snapshot").json()

    def test_kpis_contains_mrr(self):
        kpis = client.get("/api/v1/ops-metrics/snapshot").json()["kpis"]
        assert "mrr_sar" in kpis

    def test_generated_at_present(self):
        assert "generated_at" in client.get("/api/v1/ops-metrics/snapshot").json()

    def test_generated_at_is_iso_string(self):
        generated_at = client.get("/api/v1/ops-metrics/snapshot").json()["generated_at"]
        assert "T" in generated_at


# ===========================================================================
# 5. Pulse endpoint
# ===========================================================================


class TestPulseEndpoint:
    def test_returns_200(self):
        resp = client.get("/api/v1/ops-metrics/pulse")
        assert resp.status_code == 200

    def test_governance_decision_present(self):
        assert "governance_decision" in client.get("/api/v1/ops-metrics/pulse").json()

    def test_governance_is_allow_with_review(self):
        assert client.get("/api/v1/ops-metrics/pulse").json()["governance_decision"] == "ALLOW_WITH_REVIEW"

    def test_overall_health_score_present(self):
        assert "overall_health_score" in client.get("/api/v1/ops-metrics/pulse").json()

    def test_health_score_in_range(self):
        score = client.get("/api/v1/ops-metrics/pulse").json()["overall_health_score"]
        assert 0.0 <= score <= 100.0

    def test_health_band_valid(self):
        band = client.get("/api/v1/ops-metrics/pulse").json()["health_band"]
        assert band in ("green", "amber", "red")

    def test_top_alerts_present(self):
        assert "top_alerts" in client.get("/api/v1/ops-metrics/pulse").json()

    def test_top_alerts_is_list(self):
        alerts = client.get("/api/v1/ops-metrics/pulse").json()["top_alerts"]
        assert isinstance(alerts, list)

    def test_top_alerts_max_3(self):
        alerts = client.get("/api/v1/ops-metrics/pulse").json()["top_alerts"]
        assert len(alerts) <= 3

    def test_generated_at_present(self):
        assert "generated_at" in client.get("/api/v1/ops-metrics/pulse").json()


# ===========================================================================
# 6. _build_alerts helper
# ===========================================================================


class TestBuildAlerts:
    def test_returns_list(self):
        assert isinstance(_build_alerts(_OPS_SNAPSHOT), list)

    def test_max_3_alerts(self):
        assert len(_build_alerts(_OPS_SNAPSHOT)) <= 3

    def test_overdue_invoice_alert_type(self):
        snap = dict(_OPS_SNAPSHOT)
        snap["overdue_invoices"] = 3
        snap["at_risk_clients"] = 0
        snap["pending_approvals"] = 0
        alerts = _build_alerts(snap)
        assert any(a["type"] == "overdue_invoices" for a in alerts)

    def test_at_risk_clients_alert_type(self):
        snap = dict(_OPS_SNAPSHOT)
        snap["overdue_invoices"] = 0
        snap["at_risk_clients"] = 2
        snap["pending_approvals"] = 0
        alerts = _build_alerts(snap)
        assert any(a["type"] == "at_risk_clients" for a in alerts)

    def test_pending_approvals_alert_type(self):
        snap = dict(_OPS_SNAPSHOT)
        snap["overdue_invoices"] = 0
        snap["at_risk_clients"] = 0
        snap["pending_approvals"] = 1
        alerts = _build_alerts(snap)
        assert any(a["type"] == "pending_approvals" for a in alerts)

    def test_no_alerts_when_zero(self):
        snap = dict(_OPS_SNAPSHOT)
        snap["overdue_invoices"] = 0
        snap["at_risk_clients"] = 0
        snap["pending_approvals"] = 0
        assert _build_alerts(snap) == []

    def test_each_alert_has_bilingual_messages(self):
        for alert in _build_alerts(_OPS_SNAPSHOT):
            assert "message_ar" in alert
            assert "message_en" in alert

    def test_each_alert_has_severity(self):
        for alert in _build_alerts(_OPS_SNAPSHOT):
            assert "severity" in alert


# ===========================================================================
# 7. Weekly summary endpoint
# ===========================================================================


class TestWeeklySummaryEndpoint:
    def test_returns_200(self):
        resp = client.get("/api/v1/ops-metrics/weekly-summary")
        assert resp.status_code == 200

    def test_governance_decision_present(self):
        assert "governance_decision" in client.get("/api/v1/ops-metrics/weekly-summary").json()

    def test_governance_is_allow_with_review(self):
        assert client.get("/api/v1/ops-metrics/weekly-summary").json()["governance_decision"] == "ALLOW_WITH_REVIEW"

    def test_week_label_present(self):
        assert "week_label" in client.get("/api/v1/ops-metrics/weekly-summary").json()

    def test_week_label_starts_with_week_of(self):
        label = client.get("/api/v1/ops-metrics/weekly-summary").json()["week_label"]
        assert label.startswith("Week of ")

    def test_key_wins_present(self):
        assert "key_wins" in client.get("/api/v1/ops-metrics/weekly-summary").json()

    def test_key_wins_is_list(self):
        assert isinstance(client.get("/api/v1/ops-metrics/weekly-summary").json()["key_wins"], list)

    def test_key_wins_count_3(self):
        assert len(client.get("/api/v1/ops-metrics/weekly-summary").json()["key_wins"]) == 3

    def test_key_wins_bilingual(self):
        wins = client.get("/api/v1/ops-metrics/weekly-summary").json()["key_wins"]
        for win in wins:
            assert "win_ar" in win
            assert "win_en" in win

    def test_focus_areas_present(self):
        assert "focus_areas" in client.get("/api/v1/ops-metrics/weekly-summary").json()

    def test_focus_areas_is_list(self):
        assert isinstance(client.get("/api/v1/ops-metrics/weekly-summary").json()["focus_areas"], list)

    def test_focus_areas_count_3(self):
        assert len(client.get("/api/v1/ops-metrics/weekly-summary").json()["focus_areas"]) == 3

    def test_focus_areas_bilingual(self):
        areas = client.get("/api/v1/ops-metrics/weekly-summary").json()["focus_areas"]
        for area in areas:
            assert "area_ar" in area
            assert "area_en" in area

    def test_kpi_highlights_present(self):
        assert "kpi_highlights" in client.get("/api/v1/ops-metrics/weekly-summary").json()

    def test_kpi_highlights_count_5(self):
        assert len(client.get("/api/v1/ops-metrics/weekly-summary").json()["kpi_highlights"]) == 5

    def test_action_items_present(self):
        assert "action_items" in client.get("/api/v1/ops-metrics/weekly-summary").json()

    def test_action_items_is_list(self):
        assert isinstance(client.get("/api/v1/ops-metrics/weekly-summary").json()["action_items"], list)

    def test_action_items_count_3(self):
        assert len(client.get("/api/v1/ops-metrics/weekly-summary").json()["action_items"]) == 3

    def test_action_items_have_approval_first(self):
        items = client.get("/api/v1/ops-metrics/weekly-summary").json()["action_items"]
        for item in items:
            assert item["governance_decision"] == "APPROVAL_FIRST"

    def test_generated_at_present(self):
        assert "generated_at" in client.get("/api/v1/ops-metrics/weekly-summary").json()


# ===========================================================================
# 8. Benchmarks endpoint
# ===========================================================================


class TestBenchmarksEndpoint:
    def test_returns_200(self):
        resp = client.get("/api/v1/ops-metrics/benchmarks")
        assert resp.status_code == 200

    def test_governance_decision_present(self):
        assert "governance_decision" in client.get("/api/v1/ops-metrics/benchmarks").json()

    def test_governance_is_allow_with_review(self):
        assert client.get("/api/v1/ops-metrics/benchmarks").json()["governance_decision"] == "ALLOW_WITH_REVIEW"

    def test_benchmarks_key_present(self):
        assert "benchmarks" in client.get("/api/v1/ops-metrics/benchmarks").json()

    def test_benchmarks_count_8(self):
        benchmarks = client.get("/api/v1/ops-metrics/benchmarks").json()["benchmarks"]
        assert len(benchmarks) == 8

    def test_each_benchmark_has_metric_name_ar(self):
        for b in client.get("/api/v1/ops-metrics/benchmarks").json()["benchmarks"]:
            assert "metric_name_ar" in b

    def test_each_benchmark_has_metric_name_en(self):
        for b in client.get("/api/v1/ops-metrics/benchmarks").json()["benchmarks"]:
            assert "metric_name_en" in b

    def test_each_benchmark_has_current_value(self):
        for b in client.get("/api/v1/ops-metrics/benchmarks").json()["benchmarks"]:
            assert "current_value" in b

    def test_each_benchmark_has_target_value(self):
        for b in client.get("/api/v1/ops-metrics/benchmarks").json()["benchmarks"]:
            assert "target_value" in b

    def test_each_benchmark_has_unit(self):
        for b in client.get("/api/v1/ops-metrics/benchmarks").json()["benchmarks"]:
            assert "unit" in b

    def test_each_benchmark_has_valid_status(self):
        valid_statuses = {"on_track", "needs_attention", "critical"}
        for b in client.get("/api/v1/ops-metrics/benchmarks").json()["benchmarks"]:
            assert b["status"] in valid_statuses, f"Invalid status: {b['status']}"

    def test_each_benchmark_has_gap(self):
        for b in client.get("/api/v1/ops-metrics/benchmarks").json()["benchmarks"]:
            assert "gap" in b

    def test_mrr_benchmark_present(self):
        benchmarks = client.get("/api/v1/ops-metrics/benchmarks").json()["benchmarks"]
        mrr_names = [b["metric_name_en"] for b in benchmarks]
        assert "MRR" in mrr_names

    def test_nrr_benchmark_present(self):
        benchmarks = client.get("/api/v1/ops-metrics/benchmarks").json()["benchmarks"]
        assert any(b["metric_name_en"] == "NRR" for b in benchmarks)

    def test_generated_at_present(self):
        assert "generated_at" in client.get("/api/v1/ops-metrics/benchmarks").json()


# ===========================================================================
# 9. Flag-issue endpoint
# ===========================================================================


class TestFlagIssueEndpoint:
    def _valid_body(self, **overrides) -> dict:
        base = {
            "issue_type": "revenue",
            "description": "MRR growth has stalled this month.",
            "priority": "high",
        }
        base.update(overrides)
        return base

    def test_returns_200_on_valid(self):
        resp = client.post("/api/v1/ops-metrics/flag-issue", json=self._valid_body())
        assert resp.status_code == 200

    def test_governance_is_approval_first(self):
        resp = client.post("/api/v1/ops-metrics/flag-issue", json=self._valid_body())
        assert resp.json()["governance_decision"] == "APPROVAL_FIRST"

    def test_response_has_issue_id(self):
        resp = client.post("/api/v1/ops-metrics/flag-issue", json=self._valid_body())
        assert "issue_id" in resp.json()

    def test_issue_id_starts_with_issue(self):
        resp = client.post("/api/v1/ops-metrics/flag-issue", json=self._valid_body())
        assert resp.json()["issue_id"].startswith("ISSUE-")

    def test_response_has_acknowledgement_ar(self):
        resp = client.post("/api/v1/ops-metrics/flag-issue", json=self._valid_body())
        assert "acknowledgement_ar" in resp.json()

    def test_response_has_acknowledgement_en(self):
        resp = client.post("/api/v1/ops-metrics/flag-issue", json=self._valid_body())
        assert "acknowledgement_en" in resp.json()

    def test_invalid_issue_type_returns_422(self):
        resp = client.post("/api/v1/ops-metrics/flag-issue", json=self._valid_body(issue_type="invalid_type"))
        assert resp.status_code == 422

    def test_short_description_returns_422(self):
        resp = client.post("/api/v1/ops-metrics/flag-issue", json=self._valid_body(description="Too short"))
        assert resp.status_code == 422

    def test_invalid_priority_returns_422(self):
        resp = client.post("/api/v1/ops-metrics/flag-issue", json=self._valid_body(priority="urgent"))
        assert resp.status_code == 422

    def test_all_valid_issue_types_accepted(self):
        for issue_type in VALID_ISSUE_TYPES:
            resp = client.post("/api/v1/ops-metrics/flag-issue", json=self._valid_body(issue_type=issue_type))
            assert resp.status_code == 200, f"Expected 200 for issue_type={issue_type}, got {resp.status_code}"

    def test_all_valid_priorities_accepted(self):
        for priority in VALID_PRIORITIES:
            resp = client.post("/api/v1/ops-metrics/flag-issue", json=self._valid_body(priority=priority))
            assert resp.status_code == 200, f"Expected 200 for priority={priority}, got {resp.status_code}"

    def test_issue_type_label_ar_present(self):
        resp = client.post("/api/v1/ops-metrics/flag-issue", json=self._valid_body())
        assert "issue_type_label_ar" in resp.json()

    def test_issue_type_label_en_present(self):
        resp = client.post("/api/v1/ops-metrics/flag-issue", json=self._valid_body())
        assert "issue_type_label_en" in resp.json()

    def test_priority_label_ar_present(self):
        resp = client.post("/api/v1/ops-metrics/flag-issue", json=self._valid_body())
        assert "priority_label_ar" in resp.json()

    def test_priority_label_en_present(self):
        resp = client.post("/api/v1/ops-metrics/flag-issue", json=self._valid_body())
        assert "priority_label_en" in resp.json()

    def test_status_is_flagged_pending_review(self):
        resp = client.post("/api/v1/ops-metrics/flag-issue", json=self._valid_body())
        assert resp.json()["status"] == "issue_flagged_pending_review"

    def test_issue_stored_in_memory(self):
        assert len(_FLAGGED_ISSUES) == 0
        client.post("/api/v1/ops-metrics/flag-issue", json=self._valid_body())
        assert len(_FLAGGED_ISSUES) == 1

    def test_generated_at_in_response(self):
        resp = client.post("/api/v1/ops-metrics/flag-issue", json=self._valid_body())
        assert "generated_at" in resp.json()


# ===========================================================================
# 10. Helper — _issue_type_label
# ===========================================================================


class TestIssueTypeLabel:
    def test_revenue_label(self):
        ar, en = _issue_type_label("revenue")
        assert en == "Revenue"

    def test_client_label(self):
        ar, en = _issue_type_label("client")
        assert en == "Client"

    def test_delivery_label(self):
        ar, en = _issue_type_label("delivery")
        assert en == "Delivery"

    def test_compliance_label(self):
        ar, en = _issue_type_label("compliance")
        assert en == "Compliance"

    def test_team_label(self):
        ar, en = _issue_type_label("team")
        assert en == "Team"

    def test_other_label(self):
        ar, en = _issue_type_label("other")
        assert en == "Other"

    def test_returns_tuple(self):
        result = _issue_type_label("revenue")
        assert isinstance(result, tuple) and len(result) == 2


# ===========================================================================
# 11. Helper — _priority_label
# ===========================================================================


class TestPriorityLabel:
    def test_high_label(self):
        ar, en = _priority_label("high")
        assert en == "High"

    def test_medium_label(self):
        ar, en = _priority_label("medium")
        assert en == "Medium"

    def test_low_label(self):
        ar, en = _priority_label("low")
        assert en == "Low"

    def test_returns_tuple(self):
        result = _priority_label("high")
        assert isinstance(result, tuple) and len(result) == 2
