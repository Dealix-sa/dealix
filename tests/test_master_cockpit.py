"""Tests for the Master Cockpit API — founder intelligence aggregator.

Covers: pulse, kpis, alerts, approvals, revenue-summary, compliance-overview.
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

from api.routers.master_cockpit import router  # noqa: E402
from fastapi import FastAPI  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

app = FastAPI()
app.include_router(router)
client = TestClient(app, headers={"X-Admin-API-Key": "test-admin-key"})


class TestPulseEndpoint:
    def test_returns_200(self):
        assert client.get("/api/v1/cockpit/pulse").status_code == 200

    def test_governance_decision(self):
        data = client.get("/api/v1/cockpit/pulse").json()
        assert data["governance_decision"] == "ALLOW_WITH_REVIEW"

    def test_has_portfolio_block(self):
        data = client.get("/api/v1/cockpit/pulse").json()
        assert "portfolio" in data
        assert "total_clients" in data["portfolio"]
        assert "mrr_sar" in data["portfolio"]

    def test_has_revenue_block(self):
        data = client.get("/api/v1/cockpit/pulse").json()
        assert "revenue" in data
        assert "mrr_sar" in data["revenue"]
        assert "arr_sar" in data["revenue"]

    def test_has_pipeline_block(self):
        data = client.get("/api/v1/cockpit/pulse").json()
        assert "pipeline" in data
        assert "total_deals" in data["pipeline"]

    def test_has_compliance_block(self):
        data = client.get("/api/v1/cockpit/pulse").json()
        assert "compliance" in data
        assert "clients_zatca_compliant" in data["compliance"]

    def test_alerts_block_structure(self):
        data = client.get("/api/v1/cockpit/pulse").json()
        alerts = data["alerts"]
        assert "total" in alerts
        assert "critical" in alerts
        assert "items" in alerts

    def test_alerts_sorted_critical_first(self):
        data = client.get("/api/v1/cockpit/pulse").json()
        items = data["alerts"]["items"]
        if len(items) > 1:
            order = {"critical": 0, "high": 1, "medium": 2}
            severities = [order.get(a["severity"], 9) for a in items]
            assert severities == sorted(severities)

    def test_pending_approvals_block(self):
        data = client.get("/api/v1/cockpit/pulse").json()
        approvals = data["pending_approvals"]
        assert "total" in approvals
        assert "items" in approvals

    def test_top_growth_signals_present(self):
        data = client.get("/api/v1/cockpit/pulse").json()
        assert "top_growth_signals" in data
        assert len(data["top_growth_signals"]) >= 1

    def test_has_bilingual_status(self):
        data = client.get("/api/v1/cockpit/pulse").json()
        assert "overall_status_ar" in data
        assert "overall_status_en" in data

    def test_has_disclaimer(self):
        data = client.get("/api/v1/cockpit/pulse").json()
        assert "disclaimer_ar" in data
        assert "disclaimer_en" in data


class TestKPIsEndpoint:
    def test_returns_200(self):
        assert client.get("/api/v1/cockpit/kpis").status_code == 200

    def test_governance_decision(self):
        data = client.get("/api/v1/cockpit/kpis").json()
        assert data["governance_decision"] == "ALLOW_WITH_REVIEW"

    def test_has_6_kpis(self):
        data = client.get("/api/v1/cockpit/kpis").json()
        assert data["kpi_count"] == 6
        assert len(data["kpis"]) == 6

    def test_each_kpi_has_required_fields(self):
        data = client.get("/api/v1/cockpit/kpis").json()
        for kpi in data["kpis"]:
            assert "name_ar" in kpi
            assert "name_en" in kpi
            assert "value" in kpi
            assert "trend" in kpi
            assert "target" in kpi

    def test_has_on_track_count(self):
        data = client.get("/api/v1/cockpit/kpis").json()
        assert "on_track_count" in data
        assert data["on_track_count"] >= 0

    def test_has_bilingual_summary(self):
        data = client.get("/api/v1/cockpit/kpis").json()
        assert "summary_ar" in data
        assert "summary_en" in data

    def test_mrr_kpi_present(self):
        data = client.get("/api/v1/cockpit/kpis").json()
        names_en = [k["name_en"] for k in data["kpis"]]
        assert any("MRR" in n or "Revenue" in n for n in names_en)


class TestAlertsEndpoint:
    def test_returns_200(self):
        assert client.get("/api/v1/cockpit/alerts").status_code == 200

    def test_governance_decision(self):
        data = client.get("/api/v1/cockpit/alerts").json()
        assert data["governance_decision"] == "ALLOW_WITH_REVIEW"

    def test_alert_count_matches_list(self):
        data = client.get("/api/v1/cockpit/alerts").json()
        assert data["alert_count"] == len(data["alerts"])

    def test_each_alert_has_bilingual_issue(self):
        data = client.get("/api/v1/cockpit/alerts").json()
        for alert in data["alerts"]:
            assert "issue_ar" in alert
            assert "issue_en" in alert

    def test_each_alert_has_action(self):
        data = client.get("/api/v1/cockpit/alerts").json()
        for alert in data["alerts"]:
            assert "action_ar" in alert
            assert "action_en" in alert

    def test_sorted_critical_first(self):
        data = client.get("/api/v1/cockpit/alerts").json()
        order = {"critical": 0, "high": 1, "medium": 2}
        sev = [order.get(a["severity"], 9) for a in data["alerts"]]
        assert sev == sorted(sev)

    def test_has_critical_and_high_counts(self):
        data = client.get("/api/v1/cockpit/alerts").json()
        assert "critical_count" in data
        assert "high_count" in data


class TestApprovalsEndpoint:
    def test_returns_200(self):
        assert client.get("/api/v1/cockpit/approvals").status_code == 200

    def test_governance_decision_is_approval_first(self):
        data = client.get("/api/v1/cockpit/approvals").json()
        assert data["governance_decision"] == "APPROVAL_FIRST"

    def test_has_approvals_list(self):
        data = client.get("/api/v1/cockpit/approvals").json()
        assert "approvals" in data
        assert len(data["approvals"]) >= 1

    def test_each_approval_has_type(self):
        data = client.get("/api/v1/cockpit/approvals").json()
        for approval in data["approvals"]:
            assert "type" in approval
            assert "type_ar" in approval

    def test_each_approval_has_value_sar(self):
        data = client.get("/api/v1/cockpit/approvals").json()
        for approval in data["approvals"]:
            assert "value_sar" in approval
            assert approval["value_sar"] > 0

    def test_note_mentions_approval_first(self):
        data = client.get("/api/v1/cockpit/approvals").json()
        assert "APPROVAL_FIRST" in data.get("note_en", "") or \
               "APPROVAL_FIRST" in data.get("note_ar", "")


class TestRevenueSummaryEndpoint:
    def test_returns_200(self):
        assert client.get("/api/v1/cockpit/revenue-summary").status_code == 200

    def test_governance_decision(self):
        data = client.get("/api/v1/cockpit/revenue-summary").json()
        assert data["governance_decision"] == "ALLOW_WITH_REVIEW"

    def test_has_mrr_and_arr(self):
        data = client.get("/api/v1/cockpit/revenue-summary").json()
        assert "mrr_sar" in data
        assert "arr_sar" in data
        assert data["arr_sar"] == data["mrr_sar"] * 12

    def test_has_nrr(self):
        data = client.get("/api/v1/cockpit/revenue-summary").json()
        assert "nrr_pct" in data
        assert data["nrr_pct"] > 0

    def test_pct_to_target_in_range(self):
        data = client.get("/api/v1/cockpit/revenue-summary").json()
        assert 0 <= data["pct_to_target"] <= 200

    def test_has_disclaimer(self):
        data = client.get("/api/v1/cockpit/revenue-summary").json()
        assert "disclaimer_ar" in data
        assert "disclaimer_en" in data

    def test_target_mrr_positive(self):
        data = client.get("/api/v1/cockpit/revenue-summary").json()
        assert data["target_mrr_sar"] > 0


class TestComplianceOverviewEndpoint:
    def test_returns_200(self):
        assert client.get("/api/v1/cockpit/compliance-overview").status_code == 200

    def test_governance_decision(self):
        data = client.get("/api/v1/cockpit/compliance-overview").json()
        assert data["governance_decision"] == "ALLOW_WITH_REVIEW"

    def test_has_zatca_block(self):
        data = client.get("/api/v1/cockpit/compliance-overview").json()
        zatca = data["zatca"]
        assert "compliant_clients" in zatca
        assert "at_risk_clients" in zatca
        assert "avg_score" in zatca
        assert "next_deadline" in zatca

    def test_has_pdpl_block(self):
        data = client.get("/api/v1/cockpit/compliance-overview").json()
        pdpl = data["pdpl"]
        assert "aligned_clients" in pdpl
        assert "at_risk_clients" in pdpl
        assert "avg_score" in pdpl

    def test_compliance_rates_in_range(self):
        data = client.get("/api/v1/cockpit/compliance-overview").json()
        assert 0 <= data["zatca"]["compliance_rate_pct"] <= 100
        assert 0 <= data["pdpl"]["alignment_rate_pct"] <= 100

    def test_has_disclaimer(self):
        data = client.get("/api/v1/cockpit/compliance-overview").json()
        assert "disclaimer_ar" in data
        assert "disclaimer_en" in data
