"""Tests for /api/v1/zatca — ZATCA Compliance Operations router.

Covers:
  - Demo data integrity (8 invoices, field presence, VAT accuracy)
  - Pure helper functions (status counts, compliance rate, averages, VAT sums)
  - GET /api/v1/zatca-ops/invoices (list, filters, governance)
  - GET /api/v1/zatca-ops/invoices/pending (status filter, counts)
  - GET /api/v1/zatca-ops/invoices/{invoice_id} (detail, 404)
  - POST /api/v1/zatca-ops/invoices/{invoice_id}/submit (state machine, 409, 404)
  - POST /api/v1/zatca-ops/invoices/{invoice_id}/resubmit (state machine, 409, 404)
  - GET /api/v1/zatca-ops/compliance-dashboard (metrics, structure)
  - GET /api/v1/zatca-ops/vat-summary (VAT breakdown, structure)
  - Governance gates (ALLOW_WITH_REVIEW vs APPROVAL_FIRST)
  - PDPL: no fake claims, no guaranteed outcomes in responses
"""

from __future__ import annotations

import copy
import os
import sys
import types

import pytest

os.environ.setdefault("ADMIN_API_KEY", "test-admin-key")
os.environ.setdefault("ADMIN_API_KEYS", "test-admin-key")

# ---------------------------------------------------------------------------
# Stub the security module only if the real one can't be imported.
# Using setdefault unconditionally contaminates the whole pytest session
# in CI (where jose/cryptography work) and breaks auth tests in other files.
# ---------------------------------------------------------------------------
if "api.security.api_key" not in sys.modules:
    try:
        import importlib
        importlib.import_module("api.security.api_key")
    except BaseException:
        _mock_security = types.ModuleType("api.security.api_key")
        _mock_security.require_admin_key = lambda: None
        sys.modules["api.security.api_key"] = _mock_security
        if "api.security" not in sys.modules:
            sys.modules["api.security"] = types.ModuleType("api.security")

from api.routers.zatca_compliance_ops import (  # noqa: E402
    ZATCA_INVOICES,
    _ALL_INVOICE_TYPES,
    _ALL_STATUSES,
    _ACTIVE_STATUSES,
    _PENDING_STATUSES,
    _build_vat_type_counts,
    _compute_avg_score,
    _compute_compliance_rate,
    _now_iso,
    _status_counts,
    _sum_positive_revenue,
    _sum_positive_vat,
    router,
)
from fastapi import FastAPI  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

app = FastAPI()
app.include_router(router)
client = TestClient(app, headers={"X-Admin-API-Key": "test-admin-key"})


# ===========================================================================
# 1. Demo data integrity
# ===========================================================================


class TestDemoDataIntegrity:
    def test_eight_invoices_exist(self) -> None:
        assert len(ZATCA_INVOICES) == 8

    def test_invoice_ids_ztv001_to_ztv008(self) -> None:
        expected = {f"ZTV-{i:03d}" for i in range(1, 9)}
        assert set(ZATCA_INVOICES.keys()) == expected

    def test_all_invoices_have_id_field(self) -> None:
        for key, inv in ZATCA_INVOICES.items():
            assert inv["id"] == key

    def test_all_invoices_have_required_fields(self) -> None:
        required = {
            "id", "invoice_number", "seller_vat", "buyer_name",
            "invoice_date", "supply_date", "subtotal_sar", "vat_rate",
            "vat_amount_sar", "total_sar", "invoice_type", "zatca_status",
            "compliance_score",
        }
        for inv in ZATCA_INVOICES.values():
            for field in required:
                assert field in inv, f"Missing '{field}' in {inv['id']}"

    def test_all_statuses_are_valid(self) -> None:
        for inv in ZATCA_INVOICES.values():
            assert inv["zatca_status"] in _ALL_STATUSES, (
                f"{inv['id']} has invalid status: {inv['zatca_status']}"
            )

    def test_all_invoice_types_are_valid(self) -> None:
        for inv in ZATCA_INVOICES.values():
            assert inv["invoice_type"] in _ALL_INVOICE_TYPES, (
                f"{inv['id']} has invalid type: {inv['invoice_type']}"
            )

    def test_draft_invoices_exist(self) -> None:
        drafts = [inv for inv in ZATCA_INVOICES.values() if inv["zatca_status"] == "draft"]
        assert len(drafts) == 2

    def test_signed_invoice_exists(self) -> None:
        signed = [inv for inv in ZATCA_INVOICES.values() if inv["zatca_status"] == "signed"]
        assert len(signed) == 1

    def test_reported_invoices_exist(self) -> None:
        reported = [inv for inv in ZATCA_INVOICES.values() if inv["zatca_status"] == "reported"]
        assert len(reported) == 2

    def test_cleared_invoices_exist(self) -> None:
        cleared = [inv for inv in ZATCA_INVOICES.values() if inv["zatca_status"] == "cleared"]
        assert len(cleared) == 2

    def test_rejected_invoice_exists(self) -> None:
        rejected = [inv for inv in ZATCA_INVOICES.values() if inv["zatca_status"] == "rejected"]
        assert len(rejected) == 1

    def test_vat_rate_is_15_percent_for_all(self) -> None:
        for inv in ZATCA_INVOICES.values():
            assert inv["vat_rate"] == 0.15

    def test_vat_amount_equals_subtotal_times_rate_for_positive(self) -> None:
        for inv in ZATCA_INVOICES.values():
            if inv["subtotal_sar"] > 0:
                expected = round(abs(inv["subtotal_sar"]) * 0.15, 2)
                actual = round(abs(inv["vat_amount_sar"]), 2)
                assert abs(actual - expected) < 0.02, (
                    f"{inv['id']}: vat {actual} != expected {expected}"
                )

    def test_total_sar_equals_subtotal_plus_vat_for_positive(self) -> None:
        for inv in ZATCA_INVOICES.values():
            if inv["subtotal_sar"] > 0:
                expected = round(inv["subtotal_sar"] + inv["vat_amount_sar"], 2)
                assert abs(inv["total_sar"] - expected) < 0.02, (
                    f"{inv['id']}: total mismatch"
                )

    def test_compliance_scores_in_valid_range(self) -> None:
        for inv in ZATCA_INVOICES.values():
            assert 0 <= inv["compliance_score"] <= 100, (
                f"{inv['id']} has score {inv['compliance_score']} out of range"
            )

    def test_cleared_invoices_have_clearance_id(self) -> None:
        for inv in ZATCA_INVOICES.values():
            if inv["zatca_status"] == "cleared":
                assert inv["clearance_id"] is not None, (
                    f"{inv['id']} is cleared but has no clearance_id"
                )

    def test_draft_invoices_have_no_xml_hash(self) -> None:
        for inv in ZATCA_INVOICES.values():
            if inv["zatca_status"] == "draft":
                assert inv.get("xml_hash") is None, (
                    f"{inv['id']} is draft but has xml_hash"
                )

    def test_credit_note_has_negative_amounts(self) -> None:
        cn = ZATCA_INVOICES["ZTV-005"]
        assert cn["invoice_type"] == "credit_note"
        assert cn["subtotal_sar"] < 0
        assert cn["vat_amount_sar"] < 0
        assert cn["total_sar"] < 0

    def test_rejected_invoice_has_rejection_reason(self) -> None:
        rejected = next(
            inv for inv in ZATCA_INVOICES.values()
            if inv["zatca_status"] == "rejected"
        )
        assert "rejection_reason" in rejected
        assert rejected["rejection_reason"]

    def test_seller_vat_consistent(self) -> None:
        seller_vats = {inv["seller_vat"] for inv in ZATCA_INVOICES.values()}
        assert len(seller_vats) == 1
        assert "300012345600003" in seller_vats

    def test_simplified_invoice_has_no_buyer_vat(self) -> None:
        simplified = [
            inv for inv in ZATCA_INVOICES.values()
            if inv["invoice_type"] == "simplified"
        ]
        assert len(simplified) >= 1
        for inv in simplified:
            assert inv.get("buyer_vat") is None

    def test_all_invoice_dates_in_may_2026(self) -> None:
        for inv in ZATCA_INVOICES.values():
            assert inv["invoice_date"].startswith("2026-05"), (
                f"{inv['id']} date {inv['invoice_date']} is not in May 2026"
            )

    def test_all_subtotals_are_nonzero(self) -> None:
        for inv in ZATCA_INVOICES.values():
            assert inv["subtotal_sar"] != 0.0


# ===========================================================================
# 2. Pure helper: _now_iso
# ===========================================================================


class TestNowIso:
    def test_returns_string(self) -> None:
        assert isinstance(_now_iso(), str)

    def test_contains_t_separator(self) -> None:
        assert "T" in _now_iso()

    def test_contains_timezone_info(self) -> None:
        result = _now_iso()
        assert "+" in result or result.endswith("Z") or "+00:00" in result

    def test_non_empty(self) -> None:
        assert len(_now_iso()) > 0


# ===========================================================================
# 3. Pure helper: _status_counts
# ===========================================================================


class TestStatusCounts:
    def test_returns_dict(self) -> None:
        invoices = list(ZATCA_INVOICES.values())
        result = _status_counts(invoices)
        assert isinstance(result, dict)

    def test_sums_to_total(self) -> None:
        invoices = list(ZATCA_INVOICES.values())
        result = _status_counts(invoices)
        assert sum(result.values()) == len(invoices)

    def test_counts_draft_correctly(self) -> None:
        invoices = list(ZATCA_INVOICES.values())
        result = _status_counts(invoices)
        expected = sum(1 for inv in invoices if inv["zatca_status"] == "draft")
        assert result.get("draft", 0) == expected

    def test_counts_cleared_correctly(self) -> None:
        invoices = list(ZATCA_INVOICES.values())
        result = _status_counts(invoices)
        expected = sum(1 for inv in invoices if inv["zatca_status"] == "cleared")
        assert result.get("cleared", 0) == expected

    def test_empty_input_returns_empty_dict(self) -> None:
        assert _status_counts([]) == {}

    def test_single_invoice(self) -> None:
        single = [{"zatca_status": "draft"}]
        assert _status_counts(single) == {"draft": 1}

    def test_multiple_same_status(self) -> None:
        invoices = [{"zatca_status": "draft"}, {"zatca_status": "draft"}]
        assert _status_counts(invoices) == {"draft": 2}


# ===========================================================================
# 4. Pure helper: _compute_compliance_rate
# ===========================================================================


class TestComputeComplianceRate:
    def test_returns_float(self) -> None:
        invoices = list(ZATCA_INVOICES.values())
        result = _compute_compliance_rate(invoices)
        assert isinstance(result, float)

    def test_in_valid_range(self) -> None:
        invoices = list(ZATCA_INVOICES.values())
        result = _compute_compliance_rate(invoices)
        assert 0.0 <= result <= 1.0

    def test_empty_list_returns_zero(self) -> None:
        assert _compute_compliance_rate([]) == 0.0

    def test_all_cleared_returns_one(self) -> None:
        invoices = [
            {"invoice_type": "standard", "zatca_status": "cleared"},
            {"invoice_type": "standard", "zatca_status": "cleared"},
        ]
        assert _compute_compliance_rate(invoices) == 1.0

    def test_all_draft_returns_zero(self) -> None:
        invoices = [
            {"invoice_type": "standard", "zatca_status": "draft"},
            {"invoice_type": "standard", "zatca_status": "draft"},
        ]
        assert _compute_compliance_rate(invoices) == 0.0

    def test_credit_notes_excluded_from_denominator(self) -> None:
        invoices = [
            {"invoice_type": "standard", "zatca_status": "cleared"},
            {"invoice_type": "credit_note", "zatca_status": "cleared"},
        ]
        # Only 1 taxable invoice, 1 active => 1.0
        assert _compute_compliance_rate(invoices) == 1.0

    def test_debit_notes_excluded_from_denominator(self) -> None:
        invoices = [
            {"invoice_type": "standard", "zatca_status": "draft"},
            {"invoice_type": "debit_note", "zatca_status": "cleared"},
        ]
        # Only 1 taxable invoice, 0 active => 0.0
        assert _compute_compliance_rate(invoices) == 0.0

    def test_only_credit_notes_returns_zero(self) -> None:
        invoices = [{"invoice_type": "credit_note", "zatca_status": "cleared"}]
        assert _compute_compliance_rate(invoices) == 0.0

    def test_reported_counts_as_active(self) -> None:
        invoices = [
            {"invoice_type": "standard", "zatca_status": "reported"},
        ]
        assert _compute_compliance_rate(invoices) == 1.0


# ===========================================================================
# 5. Pure helper: _compute_avg_score
# ===========================================================================


class TestComputeAvgScore:
    def test_returns_float(self) -> None:
        invoices = list(ZATCA_INVOICES.values())
        assert isinstance(_compute_avg_score(invoices), float)

    def test_empty_list_returns_zero(self) -> None:
        assert _compute_avg_score([]) == 0.0

    def test_single_invoice(self) -> None:
        invoices = [{"compliance_score": 80}]
        assert _compute_avg_score(invoices) == 80.0

    def test_average_two_invoices(self) -> None:
        invoices = [{"compliance_score": 60}, {"compliance_score": 100}]
        assert _compute_avg_score(invoices) == 80.0

    def test_demo_data_avg_in_valid_range(self) -> None:
        invoices = list(ZATCA_INVOICES.values())
        avg = _compute_avg_score(invoices)
        assert 0.0 <= avg <= 100.0

    def test_all_perfect_scores(self) -> None:
        invoices = [{"compliance_score": 100}, {"compliance_score": 100}]
        assert _compute_avg_score(invoices) == 100.0


# ===========================================================================
# 6. Pure helper: _sum_positive_vat
# ===========================================================================


class TestSumPositiveVat:
    def test_returns_float(self) -> None:
        invoices = list(ZATCA_INVOICES.values())
        assert isinstance(_sum_positive_vat(invoices), float)

    def test_empty_list_returns_zero(self) -> None:
        assert _sum_positive_vat([]) == 0.0

    def test_excludes_negative_vat(self) -> None:
        invoices = [
            {"zatca_status": "cleared", "vat_amount_sar": -100.0},
        ]
        assert _sum_positive_vat(invoices) == 0.0

    def test_excludes_non_active_status(self) -> None:
        invoices = [
            {"zatca_status": "draft", "vat_amount_sar": 500.0},
        ]
        assert _sum_positive_vat(invoices) == 0.0

    def test_includes_reported(self) -> None:
        invoices = [
            {"zatca_status": "reported", "vat_amount_sar": 300.0},
        ]
        assert _sum_positive_vat(invoices) == 300.0

    def test_includes_cleared(self) -> None:
        invoices = [
            {"zatca_status": "cleared", "vat_amount_sar": 400.0},
        ]
        assert _sum_positive_vat(invoices) == 400.0

    def test_demo_data_positive(self) -> None:
        invoices = list(ZATCA_INVOICES.values())
        result = _sum_positive_vat(invoices)
        assert result > 0.0


# ===========================================================================
# 7. Pure helper: _sum_positive_revenue
# ===========================================================================


class TestSumPositiveRevenue:
    def test_returns_float(self) -> None:
        invoices = list(ZATCA_INVOICES.values())
        assert isinstance(_sum_positive_revenue(invoices), float)

    def test_empty_list_returns_zero(self) -> None:
        assert _sum_positive_revenue([]) == 0.0

    def test_excludes_negative_total(self) -> None:
        invoices = [{"zatca_status": "cleared", "total_sar": -500.0}]
        assert _sum_positive_revenue(invoices) == 0.0

    def test_excludes_non_active(self) -> None:
        invoices = [{"zatca_status": "draft", "total_sar": 1000.0}]
        assert _sum_positive_revenue(invoices) == 0.0

    def test_includes_positive_active(self) -> None:
        invoices = [{"zatca_status": "cleared", "total_sar": 1000.0}]
        assert _sum_positive_revenue(invoices) == 1000.0

    def test_demo_data_positive(self) -> None:
        invoices = list(ZATCA_INVOICES.values())
        result = _sum_positive_revenue(invoices)
        assert result > 0.0


# ===========================================================================
# 8. Pure helper: _build_vat_type_counts
# ===========================================================================


class TestBuildVatTypeCounts:
    def test_returns_dict(self) -> None:
        invoices = list(ZATCA_INVOICES.values())
        result = _build_vat_type_counts(invoices)
        assert isinstance(result, dict)

    def test_has_all_invoice_type_keys(self) -> None:
        invoices = list(ZATCA_INVOICES.values())
        result = _build_vat_type_counts(invoices)
        for t in _ALL_INVOICE_TYPES:
            assert t in result

    def test_total_matches_invoice_count(self) -> None:
        invoices = list(ZATCA_INVOICES.values())
        result = _build_vat_type_counts(invoices)
        assert sum(result.values()) == len(invoices)

    def test_standard_count_correct(self) -> None:
        invoices = list(ZATCA_INVOICES.values())
        result = _build_vat_type_counts(invoices)
        expected = sum(1 for inv in invoices if inv["invoice_type"] == "standard")
        assert result["standard"] == expected

    def test_credit_note_count_one(self) -> None:
        invoices = list(ZATCA_INVOICES.values())
        result = _build_vat_type_counts(invoices)
        assert result["credit_note"] == 1

    def test_debit_note_count_zero(self) -> None:
        invoices = list(ZATCA_INVOICES.values())
        result = _build_vat_type_counts(invoices)
        assert result["debit_note"] == 0

    def test_empty_list_all_zeros(self) -> None:
        result = _build_vat_type_counts([])
        for count in result.values():
            assert count == 0


# ===========================================================================
# 9. GET /api/v1/zatca-ops/invoices — list all invoices
# ===========================================================================


class TestListZatcaInvoices:
    def test_returns_200(self) -> None:
        r = client.get("/api/v1/zatca-ops/invoices")
        assert r.status_code == 200

    def test_governance_decision_present(self) -> None:
        r = client.get("/api/v1/zatca-ops/invoices")
        assert "governance_decision" in r.json()

    def test_governance_decision_is_allow_with_review(self) -> None:
        r = client.get("/api/v1/zatca-ops/invoices")
        assert r.json()["governance_decision"] == "ALLOW_WITH_REVIEW"

    def test_total_field_present(self) -> None:
        r = client.get("/api/v1/zatca-ops/invoices")
        assert "total" in r.json()

    def test_total_is_8_unfiltered(self) -> None:
        r = client.get("/api/v1/zatca-ops/invoices")
        assert r.json()["total"] == 8

    def test_invoices_list_present(self) -> None:
        r = client.get("/api/v1/zatca-ops/invoices")
        assert "invoices" in r.json()
        assert isinstance(r.json()["invoices"], list)

    def test_invoices_count_matches_total(self) -> None:
        r = client.get("/api/v1/zatca-ops/invoices")
        data = r.json()
        assert len(data["invoices"]) == data["total"]

    def test_generated_at_present(self) -> None:
        r = client.get("/api/v1/zatca-ops/invoices")
        assert "generated_at" in r.json()

    def test_filters_applied_field_present(self) -> None:
        r = client.get("/api/v1/zatca-ops/invoices")
        assert "filters_applied" in r.json()

    def test_filter_by_status_draft(self) -> None:
        r = client.get("/api/v1/zatca-ops/invoices?status=draft")
        assert r.status_code == 200
        data = r.json()
        for inv in data["invoices"]:
            assert inv["zatca_status"] == "draft"

    def test_filter_by_status_cleared(self) -> None:
        r = client.get("/api/v1/zatca-ops/invoices?status=cleared")
        assert r.status_code == 200
        for inv in r.json()["invoices"]:
            assert inv["zatca_status"] == "cleared"

    def test_filter_by_status_reported(self) -> None:
        r = client.get("/api/v1/zatca-ops/invoices?status=reported")
        assert r.status_code == 200
        for inv in r.json()["invoices"]:
            assert inv["zatca_status"] == "reported"

    def test_filter_by_status_rejected(self) -> None:
        r = client.get("/api/v1/zatca-ops/invoices?status=rejected")
        assert r.status_code == 200
        data = r.json()
        assert data["total"] == 1

    def test_filter_by_invalid_status_422(self) -> None:
        r = client.get("/api/v1/zatca-ops/invoices?status=unknown_status")
        assert r.status_code == 422

    def test_filter_by_invoice_type_standard(self) -> None:
        r = client.get("/api/v1/zatca-ops/invoices?invoice_type=standard")
        assert r.status_code == 200
        for inv in r.json()["invoices"]:
            assert inv["invoice_type"] == "standard"

    def test_filter_by_invoice_type_simplified(self) -> None:
        r = client.get("/api/v1/zatca-ops/invoices?invoice_type=simplified")
        assert r.status_code == 200
        for inv in r.json()["invoices"]:
            assert inv["invoice_type"] == "simplified"

    def test_filter_by_invoice_type_credit_note(self) -> None:
        r = client.get("/api/v1/zatca-ops/invoices?invoice_type=credit_note")
        assert r.status_code == 200
        data = r.json()
        assert data["total"] == 1

    def test_filter_by_invalid_type_422(self) -> None:
        r = client.get("/api/v1/zatca-ops/invoices?invoice_type=invalid_type")
        assert r.status_code == 422

    def test_combined_filter_status_and_type(self) -> None:
        r = client.get("/api/v1/zatca-ops/invoices?status=cleared&invoice_type=standard")
        assert r.status_code == 200
        for inv in r.json()["invoices"]:
            assert inv["zatca_status"] == "cleared"
            assert inv["invoice_type"] == "standard"

    def test_invoices_sorted_by_date_descending(self) -> None:
        r = client.get("/api/v1/zatca-ops/invoices")
        dates = [inv["invoice_date"] for inv in r.json()["invoices"]]
        assert dates == sorted(dates, reverse=True)

    def test_filters_applied_reflects_query(self) -> None:
        r = client.get("/api/v1/zatca-ops/invoices?status=draft")
        filters = r.json()["filters_applied"]
        assert filters["status"] == "draft"

    def test_no_filters_applied_none_values(self) -> None:
        r = client.get("/api/v1/zatca-ops/invoices")
        filters = r.json()["filters_applied"]
        assert filters["status"] is None
        assert filters["invoice_type"] is None


# ===========================================================================
# 10. GET /api/v1/zatca-ops/invoices/pending — pending invoices
# ===========================================================================


class TestListPendingZatcaInvoices:
    def test_returns_200(self) -> None:
        r = client.get("/api/v1/zatca-ops/invoices/pending")
        assert r.status_code == 200

    def test_governance_decision_present(self) -> None:
        r = client.get("/api/v1/zatca-ops/invoices/pending")
        assert "governance_decision" in r.json()

    def test_governance_decision_is_allow_with_review(self) -> None:
        r = client.get("/api/v1/zatca-ops/invoices/pending")
        assert r.json()["governance_decision"] == "ALLOW_WITH_REVIEW"

    def test_total_field_present(self) -> None:
        r = client.get("/api/v1/zatca-ops/invoices/pending")
        assert "total" in r.json()

    def test_only_pending_statuses_returned(self) -> None:
        r = client.get("/api/v1/zatca-ops/invoices/pending")
        for inv in r.json()["invoices"]:
            assert inv["zatca_status"] in _PENDING_STATUSES

    def test_total_is_4(self) -> None:
        # draft: 2, signed: 1, rejected: 1 = 4 pending
        r = client.get("/api/v1/zatca-ops/invoices/pending")
        assert r.json()["total"] == 4

    def test_by_status_field_present(self) -> None:
        r = client.get("/api/v1/zatca-ops/invoices/pending")
        assert "by_status" in r.json()
        assert isinstance(r.json()["by_status"], dict)

    def test_by_status_counts_sum_to_total(self) -> None:
        r = client.get("/api/v1/zatca-ops/invoices/pending")
        data = r.json()
        assert sum(data["by_status"].values()) == data["total"]

    def test_action_ar_present(self) -> None:
        r = client.get("/api/v1/zatca-ops/invoices/pending")
        assert "action_ar" in r.json()
        assert len(r.json()["action_ar"]) > 0

    def test_action_en_present(self) -> None:
        r = client.get("/api/v1/zatca-ops/invoices/pending")
        assert "action_en" in r.json()
        assert len(r.json()["action_en"]) > 0

    def test_invoices_list_present(self) -> None:
        r = client.get("/api/v1/zatca-ops/invoices/pending")
        assert "invoices" in r.json()
        assert isinstance(r.json()["invoices"], list)

    def test_invoices_count_matches_total(self) -> None:
        r = client.get("/api/v1/zatca-ops/invoices/pending")
        data = r.json()
        assert len(data["invoices"]) == data["total"]

    def test_generated_at_present(self) -> None:
        r = client.get("/api/v1/zatca-ops/invoices/pending")
        assert "generated_at" in r.json()

    def test_draft_count_in_by_status(self) -> None:
        r = client.get("/api/v1/zatca-ops/invoices/pending")
        assert r.json()["by_status"].get("draft", 0) == 2

    def test_rejected_count_in_by_status(self) -> None:
        r = client.get("/api/v1/zatca-ops/invoices/pending")
        assert r.json()["by_status"].get("rejected", 0) == 1


# ===========================================================================
# 11. GET /api/v1/zatca-ops/invoices/{invoice_id} — invoice detail
# ===========================================================================


class TestGetZatcaInvoice:
    def test_returns_200_for_valid_id(self) -> None:
        r = client.get("/api/v1/zatca-ops/invoices/ZTV-001")
        assert r.status_code == 200

    def test_returns_404_for_unknown_id(self) -> None:
        r = client.get("/api/v1/zatca-ops/invoices/ZTV-999")
        assert r.status_code == 404

    def test_governance_decision_present(self) -> None:
        r = client.get("/api/v1/zatca-ops/invoices/ZTV-001")
        assert r.json()["governance_decision"] == "ALLOW_WITH_REVIEW"

    def test_generated_at_present(self) -> None:
        r = client.get("/api/v1/zatca-ops/invoices/ZTV-001")
        assert "generated_at" in r.json()

    def test_invoice_id_returned(self) -> None:
        r = client.get("/api/v1/zatca-ops/invoices/ZTV-001")
        assert r.json()["id"] == "ZTV-001"

    def test_invoice_number_present(self) -> None:
        r = client.get("/api/v1/zatca-ops/invoices/ZTV-001")
        assert "invoice_number" in r.json()

    def test_vat_amount_present(self) -> None:
        r = client.get("/api/v1/zatca-ops/invoices/ZTV-001")
        assert "vat_amount_sar" in r.json()

    def test_total_sar_present(self) -> None:
        r = client.get("/api/v1/zatca-ops/invoices/ZTV-001")
        assert "total_sar" in r.json()

    def test_zatca_status_present(self) -> None:
        r = client.get("/api/v1/zatca-ops/invoices/ZTV-001")
        assert "zatca_status" in r.json()

    def test_compliance_score_present(self) -> None:
        r = client.get("/api/v1/zatca-ops/invoices/ZTV-001")
        assert "compliance_score" in r.json()

    def test_case_insensitive_lookup(self) -> None:
        r = client.get("/api/v1/zatca-ops/invoices/ztv-001")
        assert r.status_code == 200

    def test_get_ztv002(self) -> None:
        r = client.get("/api/v1/zatca-ops/invoices/ZTV-002")
        assert r.status_code == 200
        assert r.json()["id"] == "ZTV-002"

    def test_get_ztv003_simplified(self) -> None:
        r = client.get("/api/v1/zatca-ops/invoices/ZTV-003")
        assert r.status_code == 200
        assert r.json()["invoice_type"] == "simplified"

    def test_get_ztv005_credit_note(self) -> None:
        r = client.get("/api/v1/zatca-ops/invoices/ZTV-005")
        assert r.status_code == 200
        assert r.json()["invoice_type"] == "credit_note"

    def test_get_ztv006_rejected_has_rejection_reason(self) -> None:
        r = client.get("/api/v1/zatca-ops/invoices/ZTV-006")
        assert r.status_code == 200
        assert "rejection_reason" in r.json()

    def test_404_error_contains_invoice_id(self) -> None:
        r = client.get("/api/v1/zatca-ops/invoices/ZTV-999")
        assert r.status_code == 404
        detail = r.json().get("detail", {})
        assert "ZTV-999" in str(detail)


# ===========================================================================
# 12. POST /api/v1/zatca-ops/invoices/{invoice_id}/submit
# ===========================================================================


class TestSubmitZatcaInvoice:
    # Use a fresh copy of ZATCA_INVOICES for each state-mutating test by
    # resetting the status field after the test.

    _submit_body = {"reason": "Finance manager approved for ZATCA submission"}

    def test_submit_draft_returns_200(self) -> None:
        # ZTV-004 and ZTV-008 are drafts; use ZTV-004
        original_status = ZATCA_INVOICES["ZTV-004"]["zatca_status"]
        ZATCA_INVOICES["ZTV-004"]["zatca_status"] = "draft"
        r = client.post("/api/v1/zatca-ops/invoices/ZTV-004/submit", json=self._submit_body)
        # Restore
        ZATCA_INVOICES["ZTV-004"]["zatca_status"] = original_status
        assert r.status_code == 200

    def test_submit_governance_approval_first(self) -> None:
        ZATCA_INVOICES["ZTV-008"]["zatca_status"] = "draft"
        r = client.post("/api/v1/zatca-ops/invoices/ZTV-008/submit", json=self._submit_body)
        ZATCA_INVOICES["ZTV-008"]["zatca_status"] = "draft"
        assert r.json()["governance_decision"] == "APPROVAL_FIRST"

    def test_submit_transitions_to_signed(self) -> None:
        ZATCA_INVOICES["ZTV-004"]["zatca_status"] = "draft"
        r = client.post("/api/v1/zatca-ops/invoices/ZTV-004/submit", json=self._submit_body)
        assert r.json()["new_status"] == "signed"
        # Status is now signed; reset for isolation
        ZATCA_INVOICES["ZTV-004"]["zatca_status"] = "draft"

    def test_submit_mutates_invoice_status(self) -> None:
        ZATCA_INVOICES["ZTV-004"]["zatca_status"] = "draft"
        client.post("/api/v1/zatca-ops/invoices/ZTV-004/submit", json=self._submit_body)
        assert ZATCA_INVOICES["ZTV-004"]["zatca_status"] == "signed"
        ZATCA_INVOICES["ZTV-004"]["zatca_status"] = "draft"

    def test_submit_previous_status_is_draft(self) -> None:
        ZATCA_INVOICES["ZTV-008"]["zatca_status"] = "draft"
        r = client.post("/api/v1/zatca-ops/invoices/ZTV-008/submit", json=self._submit_body)
        assert r.json()["previous_status"] == "draft"
        ZATCA_INVOICES["ZTV-008"]["zatca_status"] = "draft"

    def test_submit_reason_returned(self) -> None:
        ZATCA_INVOICES["ZTV-004"]["zatca_status"] = "draft"
        reason = "Approved by CFO on 2026-05-31"
        r = client.post(
            "/api/v1/zatca-ops/invoices/ZTV-004/submit",
            json={"reason": reason},
        )
        assert r.json()["reason"] == reason
        ZATCA_INVOICES["ZTV-004"]["zatca_status"] = "draft"

    def test_submit_invoice_number_returned(self) -> None:
        ZATCA_INVOICES["ZTV-004"]["zatca_status"] = "draft"
        r = client.post("/api/v1/zatca-ops/invoices/ZTV-004/submit", json=self._submit_body)
        assert "invoice_number" in r.json()
        ZATCA_INVOICES["ZTV-004"]["zatca_status"] = "draft"

    def test_submit_message_ar_present(self) -> None:
        ZATCA_INVOICES["ZTV-008"]["zatca_status"] = "draft"
        r = client.post("/api/v1/zatca-ops/invoices/ZTV-008/submit", json=self._submit_body)
        assert "message_ar" in r.json()
        ZATCA_INVOICES["ZTV-008"]["zatca_status"] = "draft"

    def test_submit_message_en_present(self) -> None:
        ZATCA_INVOICES["ZTV-004"]["zatca_status"] = "draft"
        r = client.post("/api/v1/zatca-ops/invoices/ZTV-004/submit", json=self._submit_body)
        assert "message_en" in r.json()
        ZATCA_INVOICES["ZTV-004"]["zatca_status"] = "draft"

    def test_submit_already_cleared_returns_409(self) -> None:
        r = client.post(
            "/api/v1/zatca-ops/invoices/ZTV-002/submit",
            json=self._submit_body,
        )
        assert r.status_code == 409

    def test_submit_already_reported_returns_409(self) -> None:
        r = client.post(
            "/api/v1/zatca-ops/invoices/ZTV-001/submit",
            json=self._submit_body,
        )
        assert r.status_code == 409

    def test_submit_rejected_returns_409(self) -> None:
        r = client.post(
            "/api/v1/zatca-ops/invoices/ZTV-006/submit",
            json=self._submit_body,
        )
        assert r.status_code == 409

    def test_submit_already_signed_returns_409(self) -> None:
        r = client.post(
            "/api/v1/zatca-ops/invoices/ZTV-007/submit",
            json=self._submit_body,
        )
        assert r.status_code == 409

    def test_submit_unknown_id_returns_404(self) -> None:
        r = client.post(
            "/api/v1/zatca-ops/invoices/ZTV-999/submit",
            json=self._submit_body,
        )
        assert r.status_code == 404

    def test_submit_short_reason_422(self) -> None:
        ZATCA_INVOICES["ZTV-004"]["zatca_status"] = "draft"
        r = client.post(
            "/api/v1/zatca-ops/invoices/ZTV-004/submit",
            json={"reason": "Hi"},
        )
        ZATCA_INVOICES["ZTV-004"]["zatca_status"] = "draft"
        assert r.status_code == 422

    def test_submit_generated_at_present(self) -> None:
        ZATCA_INVOICES["ZTV-008"]["zatca_status"] = "draft"
        r = client.post("/api/v1/zatca-ops/invoices/ZTV-008/submit", json=self._submit_body)
        assert "generated_at" in r.json()
        ZATCA_INVOICES["ZTV-008"]["zatca_status"] = "draft"

    def test_submit_updates_xml_hash(self) -> None:
        ZATCA_INVOICES["ZTV-004"]["zatca_status"] = "draft"
        ZATCA_INVOICES["ZTV-004"]["xml_hash"] = None
        client.post("/api/v1/zatca-ops/invoices/ZTV-004/submit", json=self._submit_body)
        assert ZATCA_INVOICES["ZTV-004"]["xml_hash"] is not None
        ZATCA_INVOICES["ZTV-004"]["zatca_status"] = "draft"
        ZATCA_INVOICES["ZTV-004"]["xml_hash"] = None

    def test_submit_updates_qr_code(self) -> None:
        ZATCA_INVOICES["ZTV-008"]["zatca_status"] = "draft"
        ZATCA_INVOICES["ZTV-008"]["qr_code_b64"] = None
        client.post("/api/v1/zatca-ops/invoices/ZTV-008/submit", json=self._submit_body)
        assert ZATCA_INVOICES["ZTV-008"]["qr_code_b64"] is not None
        ZATCA_INVOICES["ZTV-008"]["zatca_status"] = "draft"
        ZATCA_INVOICES["ZTV-008"]["qr_code_b64"] = None


# ===========================================================================
# 13. POST /api/v1/zatca-ops/invoices/{invoice_id}/resubmit
# ===========================================================================


class TestResubmitZatcaInvoice:
    _resubmit_body = {
        "reason": "Corrected supply_date_format per ZATCA specification",
        "corrections": ["Fixed supply_date format to ISO-8601", "Updated XML schema version"],
    }

    def test_resubmit_rejected_returns_200(self) -> None:
        original_status = ZATCA_INVOICES["ZTV-006"]["zatca_status"]
        ZATCA_INVOICES["ZTV-006"]["zatca_status"] = "rejected"
        r = client.post(
            "/api/v1/zatca-ops/invoices/ZTV-006/resubmit",
            json=self._resubmit_body,
        )
        ZATCA_INVOICES["ZTV-006"]["zatca_status"] = original_status
        assert r.status_code == 200

    def test_resubmit_governance_approval_first(self) -> None:
        ZATCA_INVOICES["ZTV-006"]["zatca_status"] = "rejected"
        r = client.post(
            "/api/v1/zatca-ops/invoices/ZTV-006/resubmit",
            json=self._resubmit_body,
        )
        ZATCA_INVOICES["ZTV-006"]["zatca_status"] = "rejected"
        assert r.json()["governance_decision"] == "APPROVAL_FIRST"

    def test_resubmit_transitions_to_signed(self) -> None:
        ZATCA_INVOICES["ZTV-006"]["zatca_status"] = "rejected"
        r = client.post(
            "/api/v1/zatca-ops/invoices/ZTV-006/resubmit",
            json=self._resubmit_body,
        )
        assert r.json()["new_status"] == "signed"
        ZATCA_INVOICES["ZTV-006"]["zatca_status"] = "rejected"

    def test_resubmit_mutates_invoice_status(self) -> None:
        ZATCA_INVOICES["ZTV-006"]["zatca_status"] = "rejected"
        client.post(
            "/api/v1/zatca-ops/invoices/ZTV-006/resubmit",
            json=self._resubmit_body,
        )
        assert ZATCA_INVOICES["ZTV-006"]["zatca_status"] == "signed"
        ZATCA_INVOICES["ZTV-006"]["zatca_status"] = "rejected"

    def test_resubmit_previous_status_is_rejected(self) -> None:
        ZATCA_INVOICES["ZTV-006"]["zatca_status"] = "rejected"
        r = client.post(
            "/api/v1/zatca-ops/invoices/ZTV-006/resubmit",
            json=self._resubmit_body,
        )
        assert r.json()["previous_status"] == "rejected"
        ZATCA_INVOICES["ZTV-006"]["zatca_status"] = "rejected"

    def test_resubmit_corrections_returned(self) -> None:
        ZATCA_INVOICES["ZTV-006"]["zatca_status"] = "rejected"
        r = client.post(
            "/api/v1/zatca-ops/invoices/ZTV-006/resubmit",
            json=self._resubmit_body,
        )
        assert r.json()["corrections_applied"] == self._resubmit_body["corrections"]
        ZATCA_INVOICES["ZTV-006"]["zatca_status"] = "rejected"

    def test_resubmit_reason_returned(self) -> None:
        ZATCA_INVOICES["ZTV-006"]["zatca_status"] = "rejected"
        r = client.post(
            "/api/v1/zatca-ops/invoices/ZTV-006/resubmit",
            json=self._resubmit_body,
        )
        assert r.json()["reason"] == self._resubmit_body["reason"]
        ZATCA_INVOICES["ZTV-006"]["zatca_status"] = "rejected"

    def test_resubmit_message_ar_present(self) -> None:
        ZATCA_INVOICES["ZTV-006"]["zatca_status"] = "rejected"
        r = client.post(
            "/api/v1/zatca-ops/invoices/ZTV-006/resubmit",
            json=self._resubmit_body,
        )
        assert "message_ar" in r.json()
        ZATCA_INVOICES["ZTV-006"]["zatca_status"] = "rejected"

    def test_resubmit_message_en_present(self) -> None:
        ZATCA_INVOICES["ZTV-006"]["zatca_status"] = "rejected"
        r = client.post(
            "/api/v1/zatca-ops/invoices/ZTV-006/resubmit",
            json=self._resubmit_body,
        )
        assert "message_en" in r.json()
        ZATCA_INVOICES["ZTV-006"]["zatca_status"] = "rejected"

    def test_resubmit_removes_rejection_reason(self) -> None:
        ZATCA_INVOICES["ZTV-006"]["zatca_status"] = "rejected"
        ZATCA_INVOICES["ZTV-006"]["rejection_reason"] = "Some error"
        client.post(
            "/api/v1/zatca-ops/invoices/ZTV-006/resubmit",
            json=self._resubmit_body,
        )
        assert "rejection_reason" not in ZATCA_INVOICES["ZTV-006"]
        ZATCA_INVOICES["ZTV-006"]["zatca_status"] = "rejected"
        ZATCA_INVOICES["ZTV-006"]["rejection_reason"] = "Missing mandatory field: supply_date_format"

    def test_resubmit_draft_returns_409(self) -> None:
        r = client.post(
            "/api/v1/zatca-ops/invoices/ZTV-004/resubmit",
            json=self._resubmit_body,
        )
        assert r.status_code == 409

    def test_resubmit_cleared_returns_409(self) -> None:
        r = client.post(
            "/api/v1/zatca-ops/invoices/ZTV-002/resubmit",
            json=self._resubmit_body,
        )
        assert r.status_code == 409

    def test_resubmit_reported_returns_409(self) -> None:
        r = client.post(
            "/api/v1/zatca-ops/invoices/ZTV-001/resubmit",
            json=self._resubmit_body,
        )
        assert r.status_code == 409

    def test_resubmit_signed_returns_409(self) -> None:
        r = client.post(
            "/api/v1/zatca-ops/invoices/ZTV-007/resubmit",
            json=self._resubmit_body,
        )
        assert r.status_code == 409

    def test_resubmit_unknown_id_returns_404(self) -> None:
        r = client.post(
            "/api/v1/zatca-ops/invoices/ZTV-999/resubmit",
            json=self._resubmit_body,
        )
        assert r.status_code == 404

    def test_resubmit_short_reason_422(self) -> None:
        ZATCA_INVOICES["ZTV-006"]["zatca_status"] = "rejected"
        r = client.post(
            "/api/v1/zatca-ops/invoices/ZTV-006/resubmit",
            json={"reason": "No"},
        )
        ZATCA_INVOICES["ZTV-006"]["zatca_status"] = "rejected"
        assert r.status_code == 422

    def test_resubmit_empty_corrections_allowed(self) -> None:
        ZATCA_INVOICES["ZTV-006"]["zatca_status"] = "rejected"
        r = client.post(
            "/api/v1/zatca-ops/invoices/ZTV-006/resubmit",
            json={"reason": "Corrected all mandatory fields", "corrections": []},
        )
        ZATCA_INVOICES["ZTV-006"]["zatca_status"] = "rejected"
        assert r.status_code == 200

    def test_resubmit_generated_at_present(self) -> None:
        ZATCA_INVOICES["ZTV-006"]["zatca_status"] = "rejected"
        r = client.post(
            "/api/v1/zatca-ops/invoices/ZTV-006/resubmit",
            json=self._resubmit_body,
        )
        assert "generated_at" in r.json()
        ZATCA_INVOICES["ZTV-006"]["zatca_status"] = "rejected"


# ===========================================================================
# 14. GET /api/v1/zatca-ops/compliance-dashboard
# ===========================================================================


class TestComplianceDashboard:
    def test_returns_200(self) -> None:
        r = client.get("/api/v1/zatca-ops/compliance-dashboard")
        assert r.status_code == 200

    def test_governance_decision_present(self) -> None:
        r = client.get("/api/v1/zatca-ops/compliance-dashboard")
        assert "governance_decision" in r.json()

    def test_governance_decision_is_allow_with_review(self) -> None:
        r = client.get("/api/v1/zatca-ops/compliance-dashboard")
        assert r.json()["governance_decision"] == "ALLOW_WITH_REVIEW"

    def test_total_invoices_is_8(self) -> None:
        r = client.get("/api/v1/zatca-ops/compliance-dashboard")
        assert r.json()["total_invoices"] == 8

    def test_by_status_field_present(self) -> None:
        r = client.get("/api/v1/zatca-ops/compliance-dashboard")
        assert "by_status" in r.json()
        assert isinstance(r.json()["by_status"], dict)

    def test_by_status_sums_to_total(self) -> None:
        r = client.get("/api/v1/zatca-ops/compliance-dashboard")
        data = r.json()
        assert sum(data["by_status"].values()) == data["total_invoices"]

    def test_by_status_has_draft_2(self) -> None:
        r = client.get("/api/v1/zatca-ops/compliance-dashboard")
        assert r.json()["by_status"].get("draft", 0) == 2

    def test_by_status_has_cleared_2(self) -> None:
        r = client.get("/api/v1/zatca-ops/compliance-dashboard")
        assert r.json()["by_status"].get("cleared", 0) == 2

    def test_by_status_has_reported_2(self) -> None:
        r = client.get("/api/v1/zatca-ops/compliance-dashboard")
        assert r.json()["by_status"].get("reported", 0) == 2

    def test_by_status_has_signed_1(self) -> None:
        r = client.get("/api/v1/zatca-ops/compliance-dashboard")
        assert r.json()["by_status"].get("signed", 0) == 1

    def test_by_status_has_rejected_1(self) -> None:
        r = client.get("/api/v1/zatca-ops/compliance-dashboard")
        assert r.json()["by_status"].get("rejected", 0) == 1

    def test_compliance_rate_present(self) -> None:
        r = client.get("/api/v1/zatca-ops/compliance-dashboard")
        assert "compliance_rate" in r.json()

    def test_compliance_rate_in_valid_range(self) -> None:
        r = client.get("/api/v1/zatca-ops/compliance-dashboard")
        rate = r.json()["compliance_rate"]
        assert 0.0 <= rate <= 1.0

    def test_avg_compliance_score_present(self) -> None:
        r = client.get("/api/v1/zatca-ops/compliance-dashboard")
        assert "avg_compliance_score" in r.json()

    def test_avg_compliance_score_in_range(self) -> None:
        r = client.get("/api/v1/zatca-ops/compliance-dashboard")
        score = r.json()["avg_compliance_score"]
        assert 0.0 <= score <= 100.0

    def test_total_vat_collected_sar_present(self) -> None:
        r = client.get("/api/v1/zatca-ops/compliance-dashboard")
        assert "total_vat_collected_sar" in r.json()

    def test_total_vat_collected_sar_positive(self) -> None:
        r = client.get("/api/v1/zatca-ops/compliance-dashboard")
        assert r.json()["total_vat_collected_sar"] > 0

    def test_total_revenue_sar_present(self) -> None:
        r = client.get("/api/v1/zatca-ops/compliance-dashboard")
        assert "total_revenue_sar" in r.json()

    def test_total_revenue_sar_positive(self) -> None:
        r = client.get("/api/v1/zatca-ops/compliance-dashboard")
        assert r.json()["total_revenue_sar"] > 0

    def test_pending_clearance_count_is_1(self) -> None:
        r = client.get("/api/v1/zatca-ops/compliance-dashboard")
        assert r.json()["pending_clearance_count"] == 1

    def test_rejected_count_is_1(self) -> None:
        r = client.get("/api/v1/zatca-ops/compliance-dashboard")
        assert r.json()["rejected_count"] == 1

    def test_phase2_active_is_true(self) -> None:
        r = client.get("/api/v1/zatca-ops/compliance-dashboard")
        assert r.json()["phase2_active"] is True

    def test_seller_vat_present(self) -> None:
        r = client.get("/api/v1/zatca-ops/compliance-dashboard")
        assert r.json()["seller_vat"] == "300012345600003"

    def test_report_month_present(self) -> None:
        r = client.get("/api/v1/zatca-ops/compliance-dashboard")
        assert "report_month" in r.json()
        assert len(r.json()["report_month"]) == 7  # "YYYY-MM"

    def test_generated_at_present(self) -> None:
        r = client.get("/api/v1/zatca-ops/compliance-dashboard")
        assert "generated_at" in r.json()

    def test_no_guaranteed_outcome_language(self) -> None:
        r = client.get("/api/v1/zatca-ops/compliance-dashboard")
        body_str = str(r.json()).lower()
        for phrase in ("guarantee", "guaranteed", "نضمن", "ضمان"):
            assert phrase not in body_str, f"Found forbidden phrase '{phrase}' in dashboard response"


# ===========================================================================
# 15. GET /api/v1/zatca-ops/vat-summary
# ===========================================================================


class TestVatSummary:
    def test_returns_200(self) -> None:
        r = client.get("/api/v1/zatca-ops/vat-summary")
        assert r.status_code == 200

    def test_governance_decision_present(self) -> None:
        r = client.get("/api/v1/zatca-ops/vat-summary")
        assert "governance_decision" in r.json()

    def test_governance_decision_is_allow_with_review(self) -> None:
        r = client.get("/api/v1/zatca-ops/vat-summary")
        assert r.json()["governance_decision"] == "ALLOW_WITH_REVIEW"

    def test_period_present(self) -> None:
        r = client.get("/api/v1/zatca-ops/vat-summary")
        assert "period" in r.json()

    def test_output_vat_sar_present(self) -> None:
        r = client.get("/api/v1/zatca-ops/vat-summary")
        assert "output_vat_sar" in r.json()

    def test_output_vat_sar_positive(self) -> None:
        r = client.get("/api/v1/zatca-ops/vat-summary")
        assert r.json()["output_vat_sar"] > 0

    def test_input_vat_sar_present(self) -> None:
        r = client.get("/api/v1/zatca-ops/vat-summary")
        assert "input_vat_sar" in r.json()

    def test_input_vat_sar_is_zero(self) -> None:
        r = client.get("/api/v1/zatca-ops/vat-summary")
        assert r.json()["input_vat_sar"] == 0.0

    def test_net_vat_payable_sar_present(self) -> None:
        r = client.get("/api/v1/zatca-ops/vat-summary")
        assert "net_vat_payable_sar" in r.json()

    def test_net_vat_equals_output_minus_input(self) -> None:
        r = client.get("/api/v1/zatca-ops/vat-summary")
        data = r.json()
        expected = round(data["output_vat_sar"] - data["input_vat_sar"], 2)
        assert abs(data["net_vat_payable_sar"] - expected) < 0.01

    def test_standard_invoices_count_present(self) -> None:
        r = client.get("/api/v1/zatca-ops/vat-summary")
        assert "standard_invoices" in r.json()

    def test_standard_invoices_count_correct(self) -> None:
        r = client.get("/api/v1/zatca-ops/vat-summary")
        expected = sum(
            1 for inv in ZATCA_INVOICES.values()
            if inv["invoice_type"] == "standard"
        )
        assert r.json()["standard_invoices"] == expected

    def test_simplified_invoices_count_present(self) -> None:
        r = client.get("/api/v1/zatca-ops/vat-summary")
        assert "simplified_invoices" in r.json()

    def test_simplified_invoices_count_is_1(self) -> None:
        r = client.get("/api/v1/zatca-ops/vat-summary")
        assert r.json()["simplified_invoices"] == 1

    def test_credit_notes_count_present(self) -> None:
        r = client.get("/api/v1/zatca-ops/vat-summary")
        assert "credit_notes" in r.json()

    def test_credit_notes_count_is_1(self) -> None:
        r = client.get("/api/v1/zatca-ops/vat-summary")
        assert r.json()["credit_notes"] == 1

    def test_debit_notes_count_present(self) -> None:
        r = client.get("/api/v1/zatca-ops/vat-summary")
        assert "debit_notes" in r.json()

    def test_debit_notes_count_is_0(self) -> None:
        r = client.get("/api/v1/zatca-ops/vat-summary")
        assert r.json()["debit_notes"] == 0

    def test_vat_rate_present(self) -> None:
        r = client.get("/api/v1/zatca-ops/vat-summary")
        assert "vat_rate" in r.json()

    def test_vat_rate_is_0_15(self) -> None:
        r = client.get("/api/v1/zatca-ops/vat-summary")
        assert r.json()["vat_rate"] == 0.15

    def test_note_present(self) -> None:
        r = client.get("/api/v1/zatca-ops/vat-summary")
        assert "note" in r.json()
        assert r.json()["note"]

    def test_note_mentions_estimates(self) -> None:
        r = client.get("/api/v1/zatca-ops/vat-summary")
        note = r.json()["note"].lower()
        assert "estimate" in note

    def test_note_mentions_zatca_portal(self) -> None:
        r = client.get("/api/v1/zatca-ops/vat-summary")
        assert "ZATCA" in r.json()["note"]

    def test_generated_at_present(self) -> None:
        r = client.get("/api/v1/zatca-ops/vat-summary")
        assert "generated_at" in r.json()

    def test_no_guaranteed_outcome_language(self) -> None:
        r = client.get("/api/v1/zatca-ops/vat-summary")
        body_str = str(r.json()).lower()
        for phrase in ("guarantee", "guaranteed", "نضمن"):
            assert phrase not in body_str, (
                f"Found forbidden phrase '{phrase}' in vat-summary response"
            )
