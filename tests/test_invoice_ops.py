"""Tests for the Invoice Operations API router.

Covers: data integrity, list endpoint, overdue endpoint, detail endpoint,
create invoice, issue invoice, mark paid, ZATCA compliance, VAT accuracy,
governance gates, 404 handling, and state machine validation.
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

from api.routers.invoice_ops import (  # noqa: E402
    _INVOICES,
    _INVOICE_COUNTER,
    _build_vat_breakdown,
    _compute_vat,
    _days_overdue,
    _enrich_invoice,
    _now_iso,
    _today_str,
    router,
)
from fastapi import FastAPI  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

app = FastAPI()
app.include_router(router)
client = TestClient(app, headers={"X-Admin-API-Key": "test-admin-key"})


# ---------------------------------------------------------------------------
# Helper: valid line item for create tests
# ---------------------------------------------------------------------------

_VALID_LINE_ITEM = {
    "description_ar": "خدمة استشارية",
    "description_en": "Consulting Service",
    "quantity": 1,
    "unit_price_sar": 1000.0,
}

_VALID_CREATE_BODY = {
    "client_id": "CLT-TEST",
    "company_ar": "شركة الاختبار",
    "company_en": "Test Company",
    "line_items": [_VALID_LINE_ITEM],
    "invoice_type": "standard",
    "due_days": 30,
}


# ===========================================================================
# Data Integrity
# ===========================================================================


class TestDemoDataIntegrity:
    def test_ten_invoices_exist(self):
        assert len(_INVOICES) == 10

    def test_invoice_ids_range_001_to_010(self):
        expected = {f"INV-{i:03d}" for i in range(1, 11)}
        assert set(_INVOICES.keys()) == expected

    def test_all_have_invoice_id(self):
        for inv_id, inv in _INVOICES.items():
            assert inv["invoice_id"] == inv_id

    def test_all_have_required_fields(self):
        required = {
            "invoice_id", "client_id", "company_ar", "company_en",
            "invoice_number", "issue_date", "due_date", "amount_sar",
            "vat_15_sar", "total_with_vat_sar", "state", "payment_method",
            "paid_at", "zatca_status", "invoice_type", "line_items",
        }
        for inv in _INVOICES.values():
            for field in required:
                assert field in inv, f"Missing field '{field}' in {inv['invoice_id']}"

    def test_all_states_valid(self):
        valid = {"draft", "issued", "paid", "overdue", "cancelled"}
        for inv in _INVOICES.values():
            assert inv["state"] in valid, f"{inv['invoice_id']} has invalid state {inv['state']}"

    def test_draft_invoices_exist(self):
        drafts = [inv for inv in _INVOICES.values() if inv["state"] == "draft"]
        assert len(drafts) >= 1

    def test_issued_invoices_exist(self):
        issued = [inv for inv in _INVOICES.values() if inv["state"] == "issued"]
        assert len(issued) >= 1

    def test_paid_invoices_exist(self):
        paid = [inv for inv in _INVOICES.values() if inv["state"] == "paid"]
        assert len(paid) >= 1

    def test_overdue_invoices_exist(self):
        overdue = [inv for inv in _INVOICES.values() if inv["state"] == "overdue"]
        assert len(overdue) >= 1

    def test_cancelled_invoice_exists(self):
        cancelled = [inv for inv in _INVOICES.values() if inv["state"] == "cancelled"]
        assert len(cancelled) >= 1

    def test_zatca_compliant_invoices_exist(self):
        compliant = [
            inv for inv in _INVOICES.values()
            if inv["zatca_status"] in {"reported", "cleared"}
        ]
        assert len(compliant) >= 1

    def test_non_zatca_invoices_exist(self):
        non_zatca = [
            inv for inv in _INVOICES.values()
            if inv["zatca_status"] is None
        ]
        assert len(non_zatca) >= 1

    def test_both_invoice_types_present(self):
        types_present = {inv["invoice_type"] for inv in _INVOICES.values()}
        assert "standard" in types_present
        assert "simplified" in types_present

    def test_vat_15_percent_correct_for_all_invoices(self):
        for inv in _INVOICES.values():
            expected_vat = round(inv["amount_sar"] * 0.15, 2)
            assert abs(inv["vat_15_sar"] - expected_vat) < 0.02, (
                f"{inv['invoice_id']}: vat_15_sar {inv['vat_15_sar']} != {expected_vat}"
            )

    def test_total_with_vat_equals_amount_plus_vat(self):
        for inv in _INVOICES.values():
            expected = round(inv["amount_sar"] + inv["vat_15_sar"], 2)
            assert abs(inv["total_with_vat_sar"] - expected) < 0.02, (
                f"{inv['invoice_id']}: total_with_vat_sar mismatch"
            )

    def test_line_items_non_empty(self):
        for inv in _INVOICES.values():
            assert len(inv["line_items"]) >= 1, f"{inv['invoice_id']} has no line items"

    def test_line_items_have_required_fields(self):
        required = {
            "description_ar", "description_en", "quantity",
            "unit_price_sar", "line_total_sar",
        }
        for inv in _INVOICES.values():
            for item in inv["line_items"]:
                for field in required:
                    assert field in item, (
                        f"{inv['invoice_id']} line item missing '{field}'"
                    )

    def test_paid_invoices_have_paid_at(self):
        for inv in _INVOICES.values():
            if inv["state"] == "paid":
                assert inv["paid_at"] is not None, f"{inv['invoice_id']} paid but no paid_at"

    def test_unpaid_invoices_have_no_paid_at(self):
        for inv in _INVOICES.values():
            if inv["state"] in {"draft", "issued", "overdue"}:
                assert inv["paid_at"] is None

    def test_amounts_are_positive(self):
        for inv in _INVOICES.values():
            assert inv["amount_sar"] > 0
            assert inv["vat_15_sar"] > 0
            assert inv["total_with_vat_sar"] > 0


# ===========================================================================
# Pure helpers
# ===========================================================================


class TestHelpers:
    def test_compute_vat_basic(self):
        assert _compute_vat(1000.0) == 150.0

    def test_compute_vat_zero(self):
        assert _compute_vat(0.0) == 0.0

    def test_compute_vat_rounding(self):
        # 333.33 * 0.15 = 49.9995 → 50.00
        result = _compute_vat(333.33)
        assert isinstance(result, float)
        assert result == round(333.33 * 0.15, 2)

    def test_compute_vat_large_amount(self):
        assert _compute_vat(100000.0) == 15000.0

    def test_days_overdue_past_date(self):
        result = _days_overdue("2020-01-01")
        assert result > 0

    def test_days_overdue_future_date(self):
        result = _days_overdue("2099-12-31")
        assert result == 0

    def test_days_overdue_invalid_date(self):
        result = _days_overdue("not-a-date")
        assert result == 0

    def test_today_str_format(self):
        today = _today_str()
        parts = today.split("-")
        assert len(parts) == 3
        assert len(parts[0]) == 4  # year

    def test_now_iso_format(self):
        now = _now_iso()
        assert "T" in now

    def test_build_vat_breakdown_structure(self):
        inv = _INVOICES["INV-001"]
        breakdown = _build_vat_breakdown(inv)
        assert "subtotal_sar" in breakdown
        assert "vat_rate_pct" in breakdown
        assert "vat_amount_sar" in breakdown
        assert "total_with_vat_sar" in breakdown
        assert breakdown["vat_rate_pct"] == 15.0

    def test_build_vat_breakdown_values(self):
        inv = _INVOICES["INV-001"]
        breakdown = _build_vat_breakdown(inv)
        assert breakdown["subtotal_sar"] == inv["amount_sar"]
        assert breakdown["vat_amount_sar"] == inv["vat_15_sar"]
        assert breakdown["total_with_vat_sar"] == inv["total_with_vat_sar"]

    def test_enrich_invoice_adds_days_overdue_for_overdue(self):
        overdue_inv = next(inv for inv in _INVOICES.values() if inv["state"] == "overdue")
        enriched = _enrich_invoice(overdue_inv)
        assert "days_overdue" in enriched
        assert enriched["days_overdue"] >= 0

    def test_enrich_invoice_no_days_overdue_for_paid(self):
        paid_inv = next(inv for inv in _INVOICES.values() if inv["state"] == "paid")
        enriched = _enrich_invoice(paid_inv)
        assert "days_overdue" not in enriched


# ===========================================================================
# GET / — list all invoices
# ===========================================================================


class TestListInvoices:
    def test_returns_200(self):
        r = client.get("/api/v1/invoices/")
        assert r.status_code == 200

    def test_governance_decision_present(self):
        r = client.get("/api/v1/invoices/")
        assert r.json()["governance_decision"] == "ALLOW_WITH_REVIEW"

    def test_summary_present(self):
        r = client.get("/api/v1/invoices/")
        data = r.json()
        assert "summary" in data

    def test_summary_total_invoices(self):
        r = client.get("/api/v1/invoices/")
        summary = r.json()["summary"]
        assert summary["total_invoices"] == 10

    def test_summary_has_outstanding(self):
        r = client.get("/api/v1/invoices/")
        summary = r.json()["summary"]
        assert "total_outstanding_sar" in summary

    def test_summary_has_total_paid(self):
        r = client.get("/api/v1/invoices/")
        summary = r.json()["summary"]
        assert "total_paid_sar" in summary

    def test_summary_has_overdue_count(self):
        r = client.get("/api/v1/invoices/")
        summary = r.json()["summary"]
        assert "overdue_count" in summary

    def test_summary_has_zatca_compliance_rate(self):
        r = client.get("/api/v1/invoices/")
        summary = r.json()["summary"]
        assert "zatca_compliance_rate" in summary

    def test_invoices_list_present(self):
        r = client.get("/api/v1/invoices/")
        assert "invoices" in r.json()

    def test_invoices_list_count_matches(self):
        r = client.get("/api/v1/invoices/")
        data = r.json()
        assert len(data["invoices"]) == data["summary"]["total_invoices"]

    def test_invoices_sorted_by_issue_date_descending(self):
        r = client.get("/api/v1/invoices/")
        invoices = r.json()["invoices"]
        dates = [inv["issue_date"] for inv in invoices]
        assert dates == sorted(dates, reverse=True)

    def test_overdue_count_accurate(self):
        r = client.get("/api/v1/invoices/")
        overdue_count = r.json()["summary"]["overdue_count"]
        expected = sum(1 for inv in _INVOICES.values() if inv["state"] == "overdue")
        assert overdue_count == expected

    def test_zatca_compliance_rate_is_percentage(self):
        r = client.get("/api/v1/invoices/")
        rate = r.json()["summary"]["zatca_compliance_rate"]
        assert 0 <= rate <= 100

    def test_generated_at_present(self):
        r = client.get("/api/v1/invoices/")
        assert "generated_at" in r.json()

    def test_total_paid_sar_positive(self):
        r = client.get("/api/v1/invoices/")
        assert r.json()["summary"]["total_paid_sar"] > 0


# ===========================================================================
# GET /overdue
# ===========================================================================


class TestOverdueInvoices:
    def test_returns_200(self):
        r = client.get("/api/v1/invoices/overdue")
        assert r.status_code == 200

    def test_governance_decision_present(self):
        r = client.get("/api/v1/invoices/overdue")
        assert r.json()["governance_decision"] == "ALLOW_WITH_REVIEW"

    def test_only_overdue_returned(self):
        r = client.get("/api/v1/invoices/overdue")
        for inv in r.json()["invoices"]:
            assert inv["state"] == "overdue"

    def test_overdue_count_matches_list(self):
        r = client.get("/api/v1/invoices/overdue")
        data = r.json()
        assert data["overdue_count"] == len(data["invoices"])

    def test_days_overdue_computed(self):
        r = client.get("/api/v1/invoices/overdue")
        for inv in r.json()["invoices"]:
            assert "days_overdue" in inv
            assert inv["days_overdue"] >= 0

    def test_total_overdue_sar_present(self):
        r = client.get("/api/v1/invoices/overdue")
        assert "total_overdue_sar" in r.json()

    def test_oldest_overdue_days_present(self):
        r = client.get("/api/v1/invoices/overdue")
        assert "oldest_overdue_days" in r.json()

    def test_oldest_overdue_days_non_negative(self):
        r = client.get("/api/v1/invoices/overdue")
        assert r.json()["oldest_overdue_days"] >= 0

    def test_action_ar_present(self):
        r = client.get("/api/v1/invoices/overdue")
        assert "action_ar" in r.json()
        assert len(r.json()["action_ar"]) > 0

    def test_action_en_present(self):
        r = client.get("/api/v1/invoices/overdue")
        assert "action_en" in r.json()
        assert len(r.json()["action_en"]) > 0

    def test_total_overdue_sar_correct(self):
        r = client.get("/api/v1/invoices/overdue")
        data = r.json()
        expected = sum(
            inv["total_with_vat_sar"]
            for inv in _INVOICES.values()
            if inv["state"] == "overdue"
        )
        assert abs(data["total_overdue_sar"] - expected) < 0.01


# ===========================================================================
# GET /{invoice_id} — invoice detail
# ===========================================================================


class TestInvoiceDetail:
    def test_returns_200_for_valid_id(self):
        r = client.get("/api/v1/invoices/INV-001")
        assert r.status_code == 200

    def test_returns_404_for_unknown_id(self):
        r = client.get("/api/v1/invoices/INV-999")
        assert r.status_code == 404

    def test_governance_decision_present(self):
        r = client.get("/api/v1/invoices/INV-001")
        assert r.json()["governance_decision"] == "ALLOW_WITH_REVIEW"

    def test_vat_breakdown_present(self):
        r = client.get("/api/v1/invoices/INV-001")
        assert "vat_breakdown" in r.json()

    def test_vat_breakdown_has_rate(self):
        r = client.get("/api/v1/invoices/INV-001")
        assert r.json()["vat_breakdown"]["vat_rate_pct"] == 15.0

    def test_vat_breakdown_subtotal_matches(self):
        r = client.get("/api/v1/invoices/INV-001")
        data = r.json()
        assert data["vat_breakdown"]["subtotal_sar"] == data["amount_sar"]

    def test_all_invoice_fields_present(self):
        r = client.get("/api/v1/invoices/INV-001")
        data = r.json()
        for field in [
            "invoice_id", "client_id", "company_ar", "company_en",
            "invoice_number", "issue_date", "due_date", "amount_sar",
            "vat_15_sar", "total_with_vat_sar", "state", "invoice_type",
            "line_items",
        ]:
            assert field in data, f"Missing field '{field}' in detail response"

    def test_overdue_invoice_has_days_overdue(self):
        overdue_id = next(
            inv_id for inv_id, inv in _INVOICES.items()
            if inv["state"] == "overdue"
        )
        r = client.get(f"/api/v1/invoices/{overdue_id}")
        assert "days_overdue" in r.json()

    def test_paid_invoice_has_paid_at(self):
        paid_id = next(
            inv_id for inv_id, inv in _INVOICES.items()
            if inv["state"] == "paid"
        )
        r = client.get(f"/api/v1/invoices/{paid_id}")
        assert r.json()["paid_at"] is not None

    def test_case_insensitive_id_lookup(self):
        r = client.get("/api/v1/invoices/inv-001")
        assert r.status_code == 200

    def test_generated_at_present(self):
        r = client.get("/api/v1/invoices/INV-002")
        assert "generated_at" in r.json()

    def test_line_items_present_in_detail(self):
        r = client.get("/api/v1/invoices/INV-001")
        assert "line_items" in r.json()
        assert len(r.json()["line_items"]) >= 1


# ===========================================================================
# POST / — create invoice
# ===========================================================================


class TestCreateInvoice:
    def test_create_returns_200(self):
        r = client.post("/api/v1/invoices/", json=_VALID_CREATE_BODY)
        assert r.status_code == 200

    def test_create_governance_approval_first(self):
        r = client.post("/api/v1/invoices/", json=_VALID_CREATE_BODY)
        assert r.json()["governance_decision"] == "APPROVAL_FIRST"

    def test_create_returns_invoice(self):
        r = client.post("/api/v1/invoices/", json=_VALID_CREATE_BODY)
        assert "invoice" in r.json()

    def test_create_state_is_draft(self):
        r = client.post("/api/v1/invoices/", json=_VALID_CREATE_BODY)
        assert r.json()["invoice"]["state"] == "draft"

    def test_create_auto_computes_amount(self):
        body = {
            **_VALID_CREATE_BODY,
            "line_items": [
                {
                    "description_ar": "خدمة",
                    "description_en": "Service",
                    "quantity": 2,
                    "unit_price_sar": 500.0,
                }
            ],
        }
        r = client.post("/api/v1/invoices/", json=body)
        assert r.json()["invoice"]["amount_sar"] == 1000.0

    def test_create_auto_computes_vat(self):
        body = {
            **_VALID_CREATE_BODY,
            "line_items": [
                {
                    "description_ar": "خدمة",
                    "description_en": "Service",
                    "quantity": 1,
                    "unit_price_sar": 2000.0,
                }
            ],
        }
        r = client.post("/api/v1/invoices/", json=body)
        invoice = r.json()["invoice"]
        assert invoice["vat_15_sar"] == 300.0

    def test_create_auto_computes_total(self):
        body = {
            **_VALID_CREATE_BODY,
            "line_items": [
                {
                    "description_ar": "خدمة",
                    "description_en": "Service",
                    "quantity": 1,
                    "unit_price_sar": 1000.0,
                }
            ],
        }
        r = client.post("/api/v1/invoices/", json=body)
        invoice = r.json()["invoice"]
        assert abs(invoice["total_with_vat_sar"] - 1150.0) < 0.01

    def test_create_vat_breakdown_present(self):
        r = client.post("/api/v1/invoices/", json=_VALID_CREATE_BODY)
        assert "vat_breakdown" in r.json()

    def test_create_invoice_id_assigned(self):
        r = client.post("/api/v1/invoices/", json=_VALID_CREATE_BODY)
        inv_id = r.json()["invoice"]["invoice_id"]
        assert inv_id.startswith("INV-")

    def test_create_invoice_stored(self):
        r = client.post("/api/v1/invoices/", json=_VALID_CREATE_BODY)
        inv_id = r.json()["invoice"]["invoice_id"]
        assert inv_id in _INVOICES

    def test_create_issue_date_today(self):
        r = client.post("/api/v1/invoices/", json=_VALID_CREATE_BODY)
        assert r.json()["invoice"]["issue_date"] == _today_str()

    def test_create_invalid_invoice_type_422(self):
        body = {**_VALID_CREATE_BODY, "invoice_type": "unknown_type"}
        r = client.post("/api/v1/invoices/", json=body)
        assert r.status_code == 422

    def test_create_empty_line_items_422(self):
        body = {**_VALID_CREATE_BODY, "line_items": []}
        r = client.post("/api/v1/invoices/", json=body)
        assert r.status_code == 422

    def test_create_negative_quantity_422(self):
        body = {
            **_VALID_CREATE_BODY,
            "line_items": [
                {
                    "description_ar": "خدمة",
                    "description_en": "Service",
                    "quantity": -1,
                    "unit_price_sar": 100.0,
                }
            ],
        }
        r = client.post("/api/v1/invoices/", json=body)
        assert r.status_code == 422

    def test_create_zero_unit_price_422(self):
        body = {
            **_VALID_CREATE_BODY,
            "line_items": [
                {
                    "description_ar": "خدمة",
                    "description_en": "Service",
                    "quantity": 1,
                    "unit_price_sar": 0.0,
                }
            ],
        }
        r = client.post("/api/v1/invoices/", json=body)
        assert r.status_code == 422

    def test_create_message_ar_present(self):
        r = client.post("/api/v1/invoices/", json=_VALID_CREATE_BODY)
        assert "message_ar" in r.json()

    def test_create_message_en_present(self):
        r = client.post("/api/v1/invoices/", json=_VALID_CREATE_BODY)
        assert "message_en" in r.json()

    def test_create_due_days_respected(self):
        body = {**_VALID_CREATE_BODY, "due_days": 60}
        r = client.post("/api/v1/invoices/", json=body)
        from datetime import date, timedelta
        expected_due = (date.fromisoformat(_today_str()) + timedelta(days=60)).isoformat()
        assert r.json()["invoice"]["due_date"] == expected_due

    def test_create_total_equals_amount_plus_vat(self):
        r = client.post("/api/v1/invoices/", json=_VALID_CREATE_BODY)
        invoice = r.json()["invoice"]
        expected_total = round(invoice["amount_sar"] + invoice["vat_15_sar"], 2)
        assert abs(invoice["total_with_vat_sar"] - expected_total) < 0.01

    def test_create_due_days_too_large_422(self):
        body = {**_VALID_CREATE_BODY, "due_days": 999}
        r = client.post("/api/v1/invoices/", json=body)
        assert r.status_code == 422

    def test_create_due_days_zero_422(self):
        body = {**_VALID_CREATE_BODY, "due_days": 0}
        r = client.post("/api/v1/invoices/", json=body)
        assert r.status_code == 422

    def test_create_multi_line_items_amount_sum(self):
        body = {
            **_VALID_CREATE_BODY,
            "line_items": [
                {
                    "description_ar": "خدمة أولى",
                    "description_en": "First Service",
                    "quantity": 2,
                    "unit_price_sar": 500.0,
                },
                {
                    "description_ar": "خدمة ثانية",
                    "description_en": "Second Service",
                    "quantity": 3,
                    "unit_price_sar": 200.0,
                },
            ],
        }
        r = client.post("/api/v1/invoices/", json=body)
        # 2*500 + 3*200 = 1600
        assert r.json()["invoice"]["amount_sar"] == 1600.0


# ===========================================================================
# POST /{invoice_id}/issue
# ===========================================================================


class TestIssueInvoice:
    def _get_draft_id(self) -> str:
        """Return a known draft invoice ID, creating one if needed."""
        draft_ids = [
            inv_id for inv_id, inv in _INVOICES.items()
            if inv["state"] == "draft"
        ]
        if draft_ids:
            return draft_ids[0]
        # Create a fresh draft
        r = client.post("/api/v1/invoices/", json=_VALID_CREATE_BODY)
        return r.json()["invoice"]["invoice_id"]

    def test_issue_returns_200(self):
        draft_id = self._get_draft_id()
        r = client.post(
            f"/api/v1/invoices/{draft_id}/issue",
            json={"reason": "Client approved and requested invoice"},
        )
        assert r.status_code == 200

    def test_issue_governance_approval_first(self):
        # Create a fresh draft to avoid state conflicts
        cr = client.post("/api/v1/invoices/", json=_VALID_CREATE_BODY)
        new_id = cr.json()["invoice"]["invoice_id"]
        r = client.post(
            f"/api/v1/invoices/{new_id}/issue",
            json={"reason": "Approved by finance team"},
        )
        assert r.json()["governance_decision"] == "APPROVAL_FIRST"

    def test_issue_new_state_is_issued(self):
        cr = client.post("/api/v1/invoices/", json=_VALID_CREATE_BODY)
        new_id = cr.json()["invoice"]["invoice_id"]
        r = client.post(
            f"/api/v1/invoices/{new_id}/issue",
            json={"reason": "Ready to issue to client"},
        )
        assert r.json()["new_state"] == "issued"

    def test_issue_mutates_invoice_state(self):
        cr = client.post("/api/v1/invoices/", json=_VALID_CREATE_BODY)
        new_id = cr.json()["invoice"]["invoice_id"]
        client.post(
            f"/api/v1/invoices/{new_id}/issue",
            json={"reason": "All checks passed"},
        )
        assert _INVOICES[new_id]["state"] == "issued"

    def test_issue_non_draft_returns_400(self):
        paid_id = next(
            inv_id for inv_id, inv in _INVOICES.items()
            if inv["state"] == "paid"
        )
        r = client.post(
            f"/api/v1/invoices/{paid_id}/issue",
            json={"reason": "Attempting re-issue"},
        )
        assert r.status_code == 400

    def test_issue_unknown_id_returns_404(self):
        r = client.post(
            "/api/v1/invoices/INV-999/issue",
            json={"reason": "Does not exist"},
        )
        assert r.status_code == 404

    def test_issue_short_reason_422(self):
        cr = client.post("/api/v1/invoices/", json=_VALID_CREATE_BODY)
        new_id = cr.json()["invoice"]["invoice_id"]
        r = client.post(
            f"/api/v1/invoices/{new_id}/issue",
            json={"reason": "Hi"},
        )
        assert r.status_code == 422

    def test_issue_reason_returned(self):
        cr = client.post("/api/v1/invoices/", json=_VALID_CREATE_BODY)
        new_id = cr.json()["invoice"]["invoice_id"]
        reason_text = "Finance team approved on review"
        r = client.post(
            f"/api/v1/invoices/{new_id}/issue",
            json={"reason": reason_text},
        )
        assert r.json()["reason"] == reason_text

    def test_issue_message_ar_present(self):
        cr = client.post("/api/v1/invoices/", json=_VALID_CREATE_BODY)
        new_id = cr.json()["invoice"]["invoice_id"]
        r = client.post(
            f"/api/v1/invoices/{new_id}/issue",
            json={"reason": "Approved and ready to send"},
        )
        assert "message_ar" in r.json()

    def test_issue_message_en_present(self):
        cr = client.post("/api/v1/invoices/", json=_VALID_CREATE_BODY)
        new_id = cr.json()["invoice"]["invoice_id"]
        r = client.post(
            f"/api/v1/invoices/{new_id}/issue",
            json={"reason": "Approved and ready to send"},
        )
        assert "message_en" in r.json()

    def test_issue_cancelled_invoice_returns_400(self):
        cancelled_id = next(
            inv_id for inv_id, inv in _INVOICES.items()
            if inv["state"] == "cancelled"
        )
        r = client.post(
            f"/api/v1/invoices/{cancelled_id}/issue",
            json={"reason": "Trying to issue cancelled"},
        )
        assert r.status_code == 400


# ===========================================================================
# POST /{invoice_id}/mark-paid
# ===========================================================================


class TestMarkPaid:
    _MARK_PAID_BODY = {
        "payment_method": "bank_transfer",
        "payment_date": "2026-06-01",
        "notes": "Confirmed via IBAN transfer",
    }

    def _get_issuable_id(self) -> str:
        """Get or create an issued invoice to mark as paid."""
        # Create a fresh draft and issue it
        cr = client.post("/api/v1/invoices/", json=_VALID_CREATE_BODY)
        new_id = cr.json()["invoice"]["invoice_id"]
        client.post(
            f"/api/v1/invoices/{new_id}/issue",
            json={"reason": "Ready for payment test"},
        )
        return new_id

    def test_mark_paid_returns_200(self):
        inv_id = self._get_issuable_id()
        r = client.post(
            f"/api/v1/invoices/{inv_id}/mark-paid",
            json=self._MARK_PAID_BODY,
        )
        assert r.status_code == 200

    def test_mark_paid_governance_approval_first(self):
        inv_id = self._get_issuable_id()
        r = client.post(
            f"/api/v1/invoices/{inv_id}/mark-paid",
            json=self._MARK_PAID_BODY,
        )
        assert r.json()["governance_decision"] == "APPROVAL_FIRST"

    def test_mark_paid_new_state(self):
        inv_id = self._get_issuable_id()
        r = client.post(
            f"/api/v1/invoices/{inv_id}/mark-paid",
            json=self._MARK_PAID_BODY,
        )
        assert r.json()["new_state"] == "paid"

    def test_mark_paid_mutates_state(self):
        inv_id = self._get_issuable_id()
        client.post(
            f"/api/v1/invoices/{inv_id}/mark-paid",
            json=self._MARK_PAID_BODY,
        )
        assert _INVOICES[inv_id]["state"] == "paid"

    def test_mark_paid_stores_payment_method(self):
        inv_id = self._get_issuable_id()
        client.post(
            f"/api/v1/invoices/{inv_id}/mark-paid",
            json=self._MARK_PAID_BODY,
        )
        assert _INVOICES[inv_id]["payment_method"] == "bank_transfer"

    def test_mark_paid_already_paid_returns_400(self):
        paid_id = next(
            inv_id for inv_id, inv in _INVOICES.items()
            if inv["state"] == "paid"
        )
        r = client.post(
            f"/api/v1/invoices/{paid_id}/mark-paid",
            json=self._MARK_PAID_BODY,
        )
        assert r.status_code == 400

    def test_mark_paid_cancelled_returns_400(self):
        cancelled_id = next(
            inv_id for inv_id, inv in _INVOICES.items()
            if inv["state"] == "cancelled"
        )
        r = client.post(
            f"/api/v1/invoices/{cancelled_id}/mark-paid",
            json=self._MARK_PAID_BODY,
        )
        assert r.status_code == 400

    def test_mark_paid_unknown_id_404(self):
        r = client.post(
            "/api/v1/invoices/INV-999/mark-paid",
            json=self._MARK_PAID_BODY,
        )
        assert r.status_code == 404

    def test_mark_paid_payment_method_in_response(self):
        inv_id = self._get_issuable_id()
        r = client.post(
            f"/api/v1/invoices/{inv_id}/mark-paid",
            json=self._MARK_PAID_BODY,
        )
        assert r.json()["payment_method"] == "bank_transfer"

    def test_mark_paid_payment_date_in_response(self):
        inv_id = self._get_issuable_id()
        r = client.post(
            f"/api/v1/invoices/{inv_id}/mark-paid",
            json=self._MARK_PAID_BODY,
        )
        assert r.json()["payment_date"] == "2026-06-01"

    def test_mark_paid_notes_in_response(self):
        inv_id = self._get_issuable_id()
        r = client.post(
            f"/api/v1/invoices/{inv_id}/mark-paid",
            json=self._MARK_PAID_BODY,
        )
        assert r.json()["notes"] == "Confirmed via IBAN transfer"

    def test_mark_paid_notes_optional(self):
        inv_id = self._get_issuable_id()
        body = {"payment_method": "moyasar_card", "payment_date": "2026-06-01"}
        r = client.post(f"/api/v1/invoices/{inv_id}/mark-paid", json=body)
        assert r.status_code == 200
        assert r.json()["notes"] is None

    def test_mark_paid_message_ar_present(self):
        inv_id = self._get_issuable_id()
        r = client.post(
            f"/api/v1/invoices/{inv_id}/mark-paid",
            json=self._MARK_PAID_BODY,
        )
        assert "message_ar" in r.json()

    def test_mark_paid_message_en_present(self):
        inv_id = self._get_issuable_id()
        r = client.post(
            f"/api/v1/invoices/{inv_id}/mark-paid",
            json=self._MARK_PAID_BODY,
        )
        assert "message_en" in r.json()


# ===========================================================================
# GET /zatca-compliance
# ===========================================================================


class TestZatcaCompliance:
    def test_returns_200(self):
        r = client.get("/api/v1/invoices/zatca-compliance")
        assert r.status_code == 200

    def test_governance_decision_present(self):
        r = client.get("/api/v1/invoices/zatca-compliance")
        assert r.json()["governance_decision"] == "ALLOW_WITH_REVIEW"

    def test_total_invoices_present(self):
        r = client.get("/api/v1/invoices/zatca-compliance")
        assert "total_invoices" in r.json()

    def test_compliant_count_present(self):
        r = client.get("/api/v1/invoices/zatca-compliance")
        assert "compliant_count" in r.json()

    def test_non_compliant_present(self):
        r = client.get("/api/v1/invoices/zatca-compliance")
        assert "non_compliant" in r.json()

    def test_compliance_rate_pct_present(self):
        r = client.get("/api/v1/invoices/zatca-compliance")
        assert "compliance_rate_pct" in r.json()

    def test_by_status_breakdown_present(self):
        r = client.get("/api/v1/invoices/zatca-compliance")
        assert "by_status" in r.json()

    def test_action_ar_present(self):
        r = client.get("/api/v1/invoices/zatca-compliance")
        assert "action_ar" in r.json()

    def test_action_en_present(self):
        r = client.get("/api/v1/invoices/zatca-compliance")
        assert "action_en" in r.json()

    def test_compliance_rate_is_percentage(self):
        r = client.get("/api/v1/invoices/zatca-compliance")
        rate = r.json()["compliance_rate_pct"]
        assert 0 <= rate <= 100

    def test_compliant_plus_non_compliant_equals_total(self):
        r = client.get("/api/v1/invoices/zatca-compliance")
        data = r.json()
        assert data["compliant_count"] + data["non_compliant"] == data["total_invoices"]

    def test_by_status_counts_sum_to_total(self):
        r = client.get("/api/v1/invoices/zatca-compliance")
        data = r.json()
        total_from_breakdown = sum(data["by_status"].values())
        assert total_from_breakdown == data["total_invoices"]

    def test_generated_at_present(self):
        r = client.get("/api/v1/invoices/zatca-compliance")
        assert "generated_at" in r.json()

    def test_compliant_count_accurate(self):
        r = client.get("/api/v1/invoices/zatca-compliance")
        expected = sum(
            1 for inv in _INVOICES.values()
            if inv["zatca_status"] in {"reported", "cleared"}
        )
        assert r.json()["compliant_count"] == expected


# ===========================================================================
# VAT precision checks
# ===========================================================================


class TestVatPrecision:
    def test_vat_15_percent_inv001(self):
        inv = _INVOICES["INV-001"]
        assert abs(inv["vat_15_sar"] - inv["amount_sar"] * 0.15) < 0.01

    def test_total_equals_subtotal_plus_vat_inv001(self):
        inv = _INVOICES["INV-001"]
        assert abs(inv["total_with_vat_sar"] - (inv["amount_sar"] + inv["vat_15_sar"])) < 0.01

    def test_vat_15_percent_inv002(self):
        inv = _INVOICES["INV-002"]
        assert abs(inv["vat_15_sar"] - inv["amount_sar"] * 0.15) < 0.01

    def test_total_equals_subtotal_plus_vat_inv002(self):
        inv = _INVOICES["INV-002"]
        assert abs(inv["total_with_vat_sar"] - (inv["amount_sar"] + inv["vat_15_sar"])) < 0.01

    def test_vat_15_percent_inv005(self):
        inv = _INVOICES["INV-005"]
        assert abs(inv["vat_15_sar"] - inv["amount_sar"] * 0.15) < 0.01

    def test_created_invoice_vat_exact(self):
        body = {
            **_VALID_CREATE_BODY,
            "line_items": [
                {
                    "description_ar": "اختبار دقة ضريبة القيمة المضافة",
                    "description_en": "VAT precision test",
                    "quantity": 1,
                    "unit_price_sar": 5000.0,
                }
            ],
        }
        r = client.post("/api/v1/invoices/", json=body)
        invoice = r.json()["invoice"]
        assert invoice["amount_sar"] == 5000.0
        assert invoice["vat_15_sar"] == 750.0
        assert invoice["total_with_vat_sar"] == 5750.0
