"""Tests for engine #5 — onboarding triggered by a paid webhook."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from auto_client_acquisition.payment_ops.moyasar_harness import MoyasarWebhookEvent
from auto_client_acquisition.payment_ops.onboarding_on_payment import (
    OnboardingArtifacts,
    OnboardingError,
    onboard_on_payment,
)


def _paid_event(**kwargs) -> MoyasarWebhookEvent:
    base: dict = {
        "type": "payment_paid",
        "payment_id": "p_test_abc",
        "status": "paid",
        "amount_halalas": 49900,
        "currency": "SAR",
        "metadata": {"engagement_id": "ENG-001"},
    }
    base.update(kwargs)
    return MoyasarWebhookEvent(**base)


def test_onboard_creates_all_four_artifacts(tmp_path: Path) -> None:
    artifacts = onboard_on_payment(
        event=_paid_event(),
        engagement_root=tmp_path,
        customer_name="TestCo",
    )
    assert isinstance(artifacts, OnboardingArtifacts)
    assert artifacts.engagement_dir.exists()
    assert artifacts.manifest_path.exists()
    assert artifacts.receipt_path.exists()
    assert artifacts.welcome_draft_path.exists()
    assert artifacts.approval_gate_path.exists()


def test_manifest_contains_correct_fields(tmp_path: Path) -> None:
    artifacts = onboard_on_payment(
        event=_paid_event(),
        engagement_root=tmp_path,
        customer_name="TestCo",
    )
    data = json.loads(artifacts.manifest_path.read_text(encoding="utf-8"))
    assert data["customer_name"] == "TestCo"
    assert data["payment_id"] == "p_test_abc"
    assert data["amount_sar"] == 499.0
    assert data["approval_required_for_external_send"] is True
    assert "estimated_outcomes_not_guaranteed" in data["doctrine_notes"]


def test_welcome_draft_is_bilingual_and_draft_only(tmp_path: Path) -> None:
    artifacts = onboard_on_payment(
        event=_paid_event(),
        engagement_root=tmp_path,
        customer_name="TestCo",
    )
    body = artifacts.welcome_draft_path.read_text(encoding="utf-8")
    assert "## القسم العربي" in body
    assert "## English Section" in body
    assert "DRAFT" in body
    assert "not guaranteed" in body
    assert "ليست نتائج مضمونة" in body


def test_approval_gate_marks_draft_only(tmp_path: Path) -> None:
    artifacts = onboard_on_payment(
        event=_paid_event(),
        engagement_root=tmp_path,
        customer_name="TestCo",
    )
    gate = json.loads(artifacts.approval_gate_path.read_text(encoding="utf-8"))
    assert gate["state"] == "draft_only"
    assert gate["requires_approval_before_send"] is True


def test_receipt_marks_zatca_stub_not_real_invoice(tmp_path: Path) -> None:
    artifacts = onboard_on_payment(
        event=_paid_event(),
        engagement_root=tmp_path,
        customer_name="TestCo",
    )
    body = artifacts.receipt_path.read_text(encoding="utf-8")
    assert "stub structure, not a registered ZATCA e-invoice" in body
    assert "499.00 SAR" in body


def test_non_paid_event_raises(tmp_path: Path) -> None:
    event = _paid_event(type="payment_failed", status="failed")
    with pytest.raises(OnboardingError, match="not a paid event"):
        onboard_on_payment(
            event=event,
            engagement_root=tmp_path,
            customer_name="TestCo",
        )


def test_blank_customer_name_raises(tmp_path: Path) -> None:
    with pytest.raises(OnboardingError, match="customer_name"):
        onboard_on_payment(
            event=_paid_event(),
            engagement_root=tmp_path,
            customer_name="   ",
        )


def test_zero_amount_raises(tmp_path: Path) -> None:
    event = _paid_event(amount_halalas=0)
    with pytest.raises(OnboardingError, match="non-positive"):
        onboard_on_payment(
            event=event,
            engagement_root=tmp_path,
            customer_name="TestCo",
        )


def test_engagement_id_from_metadata_is_sanitized(tmp_path: Path) -> None:
    event = _paid_event(metadata={"engagement_id": "ENG/../bad name 001"})
    artifacts = onboard_on_payment(
        event=event,
        engagement_root=tmp_path,
        customer_name="TestCo",
    )
    # only [A-Za-z0-9_-] survive; truncated to 64
    assert all(c.isalnum() or c in ("-", "_") for c in artifacts.engagement_id)


def test_engagement_id_falls_back_to_payment_id(tmp_path: Path) -> None:
    event = _paid_event(metadata={})
    artifacts = onboard_on_payment(
        event=event,
        engagement_root=tmp_path,
        customer_name="TestCo",
    )
    assert artifacts.engagement_id.startswith("ENG-")
    assert "p_test_abc"[:16] in artifacts.engagement_id


def test_re_onboarding_is_idempotent_on_engagement_id(tmp_path: Path) -> None:
    event = _paid_event()
    first = onboard_on_payment(
        event=event, engagement_root=tmp_path, customer_name="TestCo"
    )
    second = onboard_on_payment(
        event=event, engagement_root=tmp_path, customer_name="TestCo"
    )
    assert first.engagement_id == second.engagement_id
    assert first.engagement_dir == second.engagement_dir


def test_to_dict_is_serializable(tmp_path: Path) -> None:
    artifacts = onboard_on_payment(
        event=_paid_event(),
        engagement_root=tmp_path,
        customer_name="TestCo",
    )
    payload = artifacts.to_dict()
    assert payload["customer_name"] == "TestCo"
    assert payload["amount_sar"] == 499.0
    json.dumps(payload)  # must be JSON-serializable
