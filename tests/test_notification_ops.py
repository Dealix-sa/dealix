"""Tests for the notification_ops API router.

Covers: data integrity, list endpoint, unread summary, mark-read,
mark-all-read, create, delete, governance decisions, and helper functions.
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
# Stub the security module before any router import to avoid jose/crypto issues
# ---------------------------------------------------------------------------
_mock_security = types.ModuleType("api.security.api_key")
_mock_security.require_admin_key = lambda: None
sys.modules.setdefault("api.security.api_key", _mock_security)
if "api.security" not in sys.modules:
    sys.modules["api.security"] = types.ModuleType("api.security")

from api.routers.notification_ops import (  # noqa: E402
    VALID_PRIORITIES,
    VALID_TYPES,
    _NOTIFICATIONS,
    _now_iso,
    _notification_or_404,
    _priority_order,
    _sorted_notifications,
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

_ORIGINAL_NOTIFICATIONS: list = []


@pytest.fixture(autouse=True)
def _restore_notifications():
    """Restore the in-memory notification list after each test."""
    original = copy.deepcopy(_NOTIFICATIONS)
    yield
    _NOTIFICATIONS.clear()
    _NOTIFICATIONS.extend(original)


# ===========================================================================
# Unit tests — _now_iso
# ===========================================================================


class TestNowIso:
    def test_returns_string(self):
        assert isinstance(_now_iso(), str)

    def test_contains_t_separator(self):
        assert "T" in _now_iso()

    def test_ends_with_utc_offset(self):
        result = _now_iso()
        assert "+00:00" in result or result.endswith("Z")

    def test_non_empty(self):
        assert len(_now_iso()) > 0


# ===========================================================================
# Unit tests — _priority_order
# ===========================================================================


class TestPriorityOrder:
    def test_high_is_zero(self):
        assert _priority_order("high") == 0

    def test_medium_is_one(self):
        assert _priority_order("medium") == 1

    def test_low_is_two(self):
        assert _priority_order("low") == 2

    def test_unknown_returns_99(self):
        assert _priority_order("unknown") == 99

    def test_returns_int(self):
        assert isinstance(_priority_order("high"), int)

    def test_high_sorts_before_medium(self):
        assert _priority_order("high") < _priority_order("medium")

    def test_medium_sorts_before_low(self):
        assert _priority_order("medium") < _priority_order("low")


# ===========================================================================
# Unit tests — _notification_or_404
# ===========================================================================


class TestNotificationOr404:
    def test_valid_id_returns_record(self):
        record = _notification_or_404("NTF-001")
        assert record["notification_id"] == "NTF-001"

    def test_unknown_id_raises_404(self):
        from fastapi import HTTPException

        with pytest.raises(HTTPException) as exc_info:
            _notification_or_404("NTF-999")
        assert exc_info.value.status_code == 404

    def test_404_detail_has_ar_and_en(self):
        from fastapi import HTTPException

        with pytest.raises(HTTPException) as exc_info:
            _notification_or_404("NTF-BOGUS")
        detail = exc_info.value.detail
        assert "ar" in detail
        assert "en" in detail

    def test_returns_dict(self):
        record = _notification_or_404("NTF-002")
        assert isinstance(record, dict)


# ===========================================================================
# Unit tests — _sorted_notifications
# ===========================================================================


class TestSortedNotifications:
    def test_returns_list(self):
        result = _sorted_notifications(list(_NOTIFICATIONS))
        assert isinstance(result, list)

    def test_high_priority_before_low(self):
        records = [
            {"priority": "low", "created_at": "2026-01-01T00:00:00+00:00"},
            {"priority": "high", "created_at": "2026-01-01T00:00:00+00:00"},
        ]
        result = _sorted_notifications(records)
        assert result[0]["priority"] == "high"

    def test_same_priority_sorted_by_created_at(self):
        records = [
            {"priority": "high", "created_at": "2026-01-02T00:00:00+00:00"},
            {"priority": "high", "created_at": "2026-01-01T00:00:00+00:00"},
        ]
        result = _sorted_notifications(records)
        assert result[0]["created_at"] == "2026-01-01T00:00:00+00:00"

    def test_does_not_mutate_input(self):
        original = list(_NOTIFICATIONS)
        _ = _sorted_notifications(list(_NOTIFICATIONS))
        assert _NOTIFICATIONS == original


# ===========================================================================
# Data integrity tests
# ===========================================================================


class TestDataIntegrity:
    def test_exactly_ten_notifications(self):
        assert len(_NOTIFICATIONS) == 10

    def test_notification_ids_ntf_001_to_010(self):
        ids = {n["notification_id"] for n in _NOTIFICATIONS}
        expected = {f"NTF-{i:03d}" for i in range(1, 11)}
        assert ids == expected

    def test_three_unread_approval_required(self):
        count = sum(
            1 for n in _NOTIFICATIONS
            if n["type"] == "approval_required" and not n["read"]
        )
        assert count == 3

    def test_two_unread_churn_signal(self):
        count = sum(
            1 for n in _NOTIFICATIONS
            if n["type"] == "churn_signal" and not n["read"]
        )
        assert count == 2

    def test_two_read_renewal_reminder(self):
        count = sum(
            1 for n in _NOTIFICATIONS
            if n["type"] == "renewal_reminder" and n["read"]
        )
        assert count == 2

    def test_two_unread_health_alert(self):
        count = sum(
            1 for n in _NOTIFICATIONS
            if n["type"] == "health_alert" and not n["read"]
        )
        assert count == 2

    def test_one_read_proof_pack_ready(self):
        count = sum(
            1 for n in _NOTIFICATIONS
            if n["type"] == "proof_pack_ready" and n["read"]
        )
        assert count == 1

    def test_unread_count_is_seven(self):
        unread = sum(1 for n in _NOTIFICATIONS if not n["read"])
        assert unread == 7

    def test_all_types_are_valid(self):
        for n in _NOTIFICATIONS:
            assert n["type"] in VALID_TYPES

    def test_all_priorities_are_valid(self):
        for n in _NOTIFICATIONS:
            assert n["priority"] in VALID_PRIORITIES

    def test_each_notification_has_required_fields(self):
        required = {
            "notification_id", "type", "priority",
            "title_ar", "title_en", "body_ar", "body_en",
            "read", "created_at", "read_at", "requires_action",
        }
        for n in _NOTIFICATIONS:
            assert required.issubset(n.keys()), f"Missing fields in {n['notification_id']}"

    def test_read_notifications_have_read_at(self):
        for n in _NOTIFICATIONS:
            if n["read"]:
                assert n["read_at"] is not None

    def test_unread_notifications_have_null_read_at(self):
        for n in _NOTIFICATIONS:
            if not n["read"]:
                assert n["read_at"] is None

    def test_title_ar_non_empty(self):
        for n in _NOTIFICATIONS:
            assert len(n["title_ar"]) >= 3

    def test_title_en_non_empty(self):
        for n in _NOTIFICATIONS:
            assert len(n["title_en"]) >= 3

    def test_body_ar_non_empty(self):
        for n in _NOTIFICATIONS:
            assert len(n["body_ar"]) >= 5

    def test_body_en_non_empty(self):
        for n in _NOTIFICATIONS:
            assert len(n["body_en"]) >= 5


# ===========================================================================
# GET / — list notifications
# ===========================================================================


class TestListNotifications:
    def test_returns_200(self):
        resp = client.get("/api/v1/notifications/")
        assert resp.status_code == 200

    def test_governance_decision_present(self):
        resp = client.get("/api/v1/notifications/")
        assert "governance_decision" in resp.json()

    def test_governance_is_allow_with_review(self):
        resp = client.get("/api/v1/notifications/")
        assert resp.json()["governance_decision"] == "ALLOW_WITH_REVIEW"

    def test_total_count_is_ten(self):
        resp = client.get("/api/v1/notifications/")
        assert resp.json()["total_count"] == 10

    def test_unread_count_field_present(self):
        resp = client.get("/api/v1/notifications/")
        assert "unread_count" in resp.json()

    def test_unread_count_is_seven(self):
        resp = client.get("/api/v1/notifications/")
        assert resp.json()["unread_count"] == 7

    def test_requires_action_count_field_present(self):
        resp = client.get("/api/v1/notifications/")
        assert "requires_action_count" in resp.json()

    def test_notifications_field_is_list(self):
        resp = client.get("/api/v1/notifications/")
        assert isinstance(resp.json()["notifications"], list)

    def test_filter_unread_only_returns_only_unread(self):
        resp = client.get("/api/v1/notifications/?unread_only=true")
        data = resp.json()
        for n in data["notifications"]:
            assert n["read"] is False

    def test_filter_unread_only_count(self):
        resp = client.get("/api/v1/notifications/?unread_only=true")
        data = resp.json()
        assert len(data["notifications"]) == 7

    def test_filter_by_type_churn_signal(self):
        resp = client.get("/api/v1/notifications/?type=churn_signal")
        data = resp.json()
        for n in data["notifications"]:
            assert n["type"] == "churn_signal"

    def test_filter_by_type_returns_correct_count(self):
        resp = client.get("/api/v1/notifications/?type=renewal_reminder")
        data = resp.json()
        assert len(data["notifications"]) == 2

    def test_filter_unknown_type_returns_empty_list(self):
        resp = client.get("/api/v1/notifications/?type=nonexistent_type")
        data = resp.json()
        assert data["notifications"] == []

    def test_generated_at_present(self):
        resp = client.get("/api/v1/notifications/")
        assert "generated_at" in resp.json()

    def test_high_priority_appears_before_low_in_sorted_results(self):
        resp = client.get("/api/v1/notifications/")
        notifications = resp.json()["notifications"]
        priorities = [n["priority"] for n in notifications]
        high_indices = [i for i, p in enumerate(priorities) if p == "high"]
        low_indices = [i for i, p in enumerate(priorities) if p == "low"]
        if high_indices and low_indices:
            assert min(high_indices) < max(low_indices)


# ===========================================================================
# GET /unread-summary
# ===========================================================================


class TestUnreadSummary:
    def test_returns_200(self):
        resp = client.get("/api/v1/notifications/unread-summary")
        assert resp.status_code == 200

    def test_governance_decision_present(self):
        resp = client.get("/api/v1/notifications/unread-summary")
        assert "governance_decision" in resp.json()

    def test_governance_is_allow_with_review(self):
        resp = client.get("/api/v1/notifications/unread-summary")
        assert resp.json()["governance_decision"] == "ALLOW_WITH_REVIEW"

    def test_unread_count_field_present(self):
        resp = client.get("/api/v1/notifications/unread-summary")
        assert "unread_count" in resp.json()

    def test_unread_count_correct(self):
        resp = client.get("/api/v1/notifications/unread-summary")
        assert resp.json()["unread_count"] == 7

    def test_high_priority_unread_field_present(self):
        resp = client.get("/api/v1/notifications/unread-summary")
        assert "high_priority_unread" in resp.json()

    def test_requires_action_count_field_present(self):
        resp = client.get("/api/v1/notifications/unread-summary")
        assert "requires_action_count" in resp.json()

    def test_top_3_unread_field_present(self):
        resp = client.get("/api/v1/notifications/unread-summary")
        assert "top_3_unread" in resp.json()

    def test_top_3_unread_at_most_3_items(self):
        resp = client.get("/api/v1/notifications/unread-summary")
        assert len(resp.json()["top_3_unread"]) <= 3

    def test_top_3_unread_are_all_unread(self):
        resp = client.get("/api/v1/notifications/unread-summary")
        for n in resp.json()["top_3_unread"]:
            assert n["read"] is False

    def test_generated_at_present(self):
        resp = client.get("/api/v1/notifications/unread-summary")
        assert "generated_at" in resp.json()


# ===========================================================================
# POST /{notification_id}/mark-read
# ===========================================================================


class TestMarkNotificationRead:
    def test_returns_200_for_unread(self):
        resp = client.post("/api/v1/notifications/NTF-001/mark-read")
        assert resp.status_code == 200

    def test_governance_decision_present(self):
        resp = client.post("/api/v1/notifications/NTF-001/mark-read")
        assert "governance_decision" in resp.json()

    def test_governance_is_allow_with_review(self):
        resp = client.post("/api/v1/notifications/NTF-001/mark-read")
        assert resp.json()["governance_decision"] == "ALLOW_WITH_REVIEW"

    def test_read_field_is_true_after_mark(self):
        resp = client.post("/api/v1/notifications/NTF-001/mark-read")
        assert resp.json()["read"] is True

    def test_read_at_is_set(self):
        resp = client.post("/api/v1/notifications/NTF-001/mark-read")
        assert resp.json()["read_at"] is not None

    def test_notification_id_in_response(self):
        resp = client.post("/api/v1/notifications/NTF-001/mark-read")
        assert resp.json()["notification_id"] == "NTF-001"

    def test_404_for_unknown_id(self):
        resp = client.post("/api/v1/notifications/NTF-999/mark-read")
        assert resp.status_code == 404

    def test_409_if_already_read(self):
        # NTF-006 is already read in the demo data
        resp = client.post("/api/v1/notifications/NTF-006/mark-read")
        assert resp.status_code == 409

    def test_409_detail_has_ar_and_en(self):
        resp = client.post("/api/v1/notifications/NTF-006/mark-read")
        detail = resp.json()["detail"]
        assert "ar" in detail
        assert "en" in detail

    def test_mark_read_reflects_in_list(self):
        client.post("/api/v1/notifications/NTF-001/mark-read")
        list_resp = client.get("/api/v1/notifications/?type=approval_required")
        notifications = list_resp.json()["notifications"]
        ntf_001 = next(n for n in notifications if n["notification_id"] == "NTF-001")
        assert ntf_001["read"] is True


# ===========================================================================
# POST /mark-all-read
# ===========================================================================


class TestMarkAllRead:
    def test_returns_200(self):
        resp = client.post("/api/v1/notifications/mark-all-read")
        assert resp.status_code == 200

    def test_governance_decision_present(self):
        resp = client.post("/api/v1/notifications/mark-all-read")
        assert "governance_decision" in resp.json()

    def test_governance_is_allow_with_review(self):
        resp = client.post("/api/v1/notifications/mark-all-read")
        assert resp.json()["governance_decision"] == "ALLOW_WITH_REVIEW"

    def test_marked_count_field_present(self):
        resp = client.post("/api/v1/notifications/mark-all-read")
        assert "marked_count" in resp.json()

    def test_marked_count_equals_unread_before_call(self):
        unread_before = sum(1 for n in _NOTIFICATIONS if not n["read"])
        resp = client.post("/api/v1/notifications/mark-all-read")
        assert resp.json()["marked_count"] == unread_before

    def test_all_read_is_true_after_call(self):
        resp = client.post("/api/v1/notifications/mark-all-read")
        assert resp.json()["all_read"] is True

    def test_all_read_field_present(self):
        resp = client.post("/api/v1/notifications/mark-all-read")
        assert "all_read" in resp.json()

    def test_unread_count_zero_after_mark_all(self):
        client.post("/api/v1/notifications/mark-all-read")
        list_resp = client.get("/api/v1/notifications/")
        assert list_resp.json()["unread_count"] == 0

    def test_second_call_marks_zero(self):
        client.post("/api/v1/notifications/mark-all-read")
        resp2 = client.post("/api/v1/notifications/mark-all-read")
        assert resp2.json()["marked_count"] == 0

    def test_generated_at_present(self):
        resp = client.post("/api/v1/notifications/mark-all-read")
        assert "generated_at" in resp.json()


# ===========================================================================
# POST /create
# ===========================================================================


class TestCreateNotification:
    _valid_payload = {
        "type": "health_alert",
        "priority": "high",
        "title_ar": "تنبيه صحة جديد",
        "title_en": "New Health Alert",
        "body_ar": "درجة صحة العميل انخفضت بشكل حاد",
        "body_en": "Client health score dropped sharply",
        "client_id": "ARC-003",
        "requires_action": False,
    }

    def test_returns_200(self):
        resp = client.post("/api/v1/notifications/create", json=self._valid_payload)
        assert resp.status_code == 200

    def test_governance_decision_present(self):
        resp = client.post("/api/v1/notifications/create", json=self._valid_payload)
        assert "governance_decision" in resp.json()

    def test_non_approval_required_gets_allow_with_review(self):
        resp = client.post("/api/v1/notifications/create", json=self._valid_payload)
        assert resp.json()["governance_decision"] == "ALLOW_WITH_REVIEW"

    def test_approval_required_type_gets_approval_first(self):
        payload = {**self._valid_payload, "type": "approval_required", "requires_action": True}
        resp = client.post("/api/v1/notifications/create", json=payload)
        assert resp.json()["governance_decision"] == "APPROVAL_FIRST"

    def test_churn_signal_gets_allow_with_review(self):
        payload = {**self._valid_payload, "type": "churn_signal"}
        resp = client.post("/api/v1/notifications/create", json=payload)
        assert resp.json()["governance_decision"] == "ALLOW_WITH_REVIEW"

    def test_notification_field_present(self):
        resp = client.post("/api/v1/notifications/create", json=self._valid_payload)
        assert "notification" in resp.json()

    def test_created_notification_has_id(self):
        resp = client.post("/api/v1/notifications/create", json=self._valid_payload)
        assert "notification_id" in resp.json()["notification"]

    def test_created_notification_is_unread(self):
        resp = client.post("/api/v1/notifications/create", json=self._valid_payload)
        assert resp.json()["notification"]["read"] is False

    def test_created_notification_read_at_is_null(self):
        resp = client.post("/api/v1/notifications/create", json=self._valid_payload)
        assert resp.json()["notification"]["read_at"] is None

    def test_created_notification_appears_in_list(self):
        resp = client.post("/api/v1/notifications/create", json=self._valid_payload)
        new_id = resp.json()["notification"]["notification_id"]
        list_resp = client.get("/api/v1/notifications/")
        ids = [n["notification_id"] for n in list_resp.json()["notifications"]]
        assert new_id in ids

    def test_invalid_type_returns_422(self):
        payload = {**self._valid_payload, "type": "not_a_real_type"}
        resp = client.post("/api/v1/notifications/create", json=payload)
        assert resp.status_code == 422

    def test_invalid_priority_returns_422(self):
        payload = {**self._valid_payload, "priority": "urgent"}
        resp = client.post("/api/v1/notifications/create", json=payload)
        assert resp.status_code == 422

    def test_title_ar_too_short_returns_422(self):
        payload = {**self._valid_payload, "title_ar": "ab"}
        resp = client.post("/api/v1/notifications/create", json=payload)
        assert resp.status_code == 422

    def test_body_en_too_short_returns_422(self):
        payload = {**self._valid_payload, "body_en": "ok"}
        resp = client.post("/api/v1/notifications/create", json=payload)
        assert resp.status_code == 422

    def test_all_seven_valid_types_accepted(self):
        for notification_type in VALID_TYPES:
            payload = {**self._valid_payload, "type": notification_type}
            resp = client.post("/api/v1/notifications/create", json=payload)
            assert resp.status_code == 200, f"Type '{notification_type}' should be accepted"

    def test_client_id_nullable(self):
        payload = {**self._valid_payload, "client_id": None}
        resp = client.post("/api/v1/notifications/create", json=payload)
        assert resp.status_code == 200
        assert resp.json()["notification"]["client_id"] is None

    def test_generated_at_present(self):
        resp = client.post("/api/v1/notifications/create", json=self._valid_payload)
        assert "generated_at" in resp.json()


# ===========================================================================
# DELETE /{notification_id}
# ===========================================================================


class TestDeleteNotification:
    def test_returns_200_for_existing_non_approval_required(self):
        # NTF-008 is a health_alert (not approval_required)
        resp = client.delete("/api/v1/notifications/NTF-008")
        assert resp.status_code == 200

    def test_governance_decision_present(self):
        resp = client.delete("/api/v1/notifications/NTF-008")
        assert "governance_decision" in resp.json()

    def test_governance_is_approval_first(self):
        resp = client.delete("/api/v1/notifications/NTF-008")
        assert resp.json()["governance_decision"] == "APPROVAL_FIRST"

    def test_deleted_field_is_true(self):
        resp = client.delete("/api/v1/notifications/NTF-008")
        assert resp.json()["deleted"] is True

    def test_notification_id_in_response(self):
        resp = client.delete("/api/v1/notifications/NTF-008")
        assert resp.json()["notification_id"] == "NTF-008"

    def test_message_ar_present(self):
        resp = client.delete("/api/v1/notifications/NTF-008")
        assert "message_ar" in resp.json()

    def test_message_en_present(self):
        resp = client.delete("/api/v1/notifications/NTF-008")
        assert "message_en" in resp.json()

    def test_404_for_unknown_id(self):
        resp = client.delete("/api/v1/notifications/NTF-999")
        assert resp.status_code == 404

    def test_404_detail_has_ar_and_en(self):
        resp = client.delete("/api/v1/notifications/NTF-999")
        detail = resp.json()["detail"]
        assert "ar" in detail
        assert "en" in detail

    def test_400_for_unactioned_approval_required(self):
        # NTF-001 is approval_required with requires_action=True
        resp = client.delete("/api/v1/notifications/NTF-001")
        assert resp.status_code == 400

    def test_400_detail_has_ar_and_en(self):
        resp = client.delete("/api/v1/notifications/NTF-001")
        detail = resp.json()["detail"]
        assert "ar" in detail
        assert "en" in detail

    def test_400_detail_has_doctrine_note(self):
        resp = client.delete("/api/v1/notifications/NTF-001")
        detail = resp.json()["detail"]
        assert "doctrine_note" in detail

    def test_deleted_notification_not_in_list(self):
        client.delete("/api/v1/notifications/NTF-008")
        list_resp = client.get("/api/v1/notifications/")
        ids = [n["notification_id"] for n in list_resp.json()["notifications"]]
        assert "NTF-008" not in ids

    def test_can_delete_read_renewal_reminder(self):
        # NTF-006 is renewal_reminder, read=True, requires_action=False
        resp = client.delete("/api/v1/notifications/NTF-006")
        assert resp.status_code == 200

    def test_can_delete_read_proof_pack_ready(self):
        # NTF-010 is proof_pack_ready, read=True, requires_action=False
        resp = client.delete("/api/v1/notifications/NTF-010")
        assert resp.status_code == 200

    def test_generated_at_present(self):
        resp = client.delete("/api/v1/notifications/NTF-009")
        assert "generated_at" in resp.json()


# ===========================================================================
# Valid types and priorities constants
# ===========================================================================


class TestValidTypesAndPriorities:
    def test_valid_types_is_frozenset(self):
        assert isinstance(VALID_TYPES, frozenset)

    def test_valid_types_contains_seven_values(self):
        assert len(VALID_TYPES) == 7

    def test_health_alert_in_valid_types(self):
        assert "health_alert" in VALID_TYPES

    def test_renewal_reminder_in_valid_types(self):
        assert "renewal_reminder" in VALID_TYPES

    def test_invoice_overdue_in_valid_types(self):
        assert "invoice_overdue" in VALID_TYPES

    def test_proof_pack_ready_in_valid_types(self):
        assert "proof_pack_ready" in VALID_TYPES

    def test_churn_signal_in_valid_types(self):
        assert "churn_signal" in VALID_TYPES

    def test_approval_required_in_valid_types(self):
        assert "approval_required" in VALID_TYPES

    def test_expansion_opportunity_in_valid_types(self):
        assert "expansion_opportunity" in VALID_TYPES

    def test_valid_priorities_is_frozenset(self):
        assert isinstance(VALID_PRIORITIES, frozenset)

    def test_valid_priorities_contains_three_values(self):
        assert len(VALID_PRIORITIES) == 3

    def test_high_in_valid_priorities(self):
        assert "high" in VALID_PRIORITIES

    def test_medium_in_valid_priorities(self):
        assert "medium" in VALID_PRIORITIES

    def test_low_in_valid_priorities(self):
        assert "low" in VALID_PRIORITIES
