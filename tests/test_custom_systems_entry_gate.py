"""Doctrine test — Custom Systems OS entry gate (the coded >=3 paid pilots rule)."""

from __future__ import annotations

from auto_client_acquisition.custom_systems_os.entry_gate import MIN_PAID_PILOTS, check_entry


def test_no_customization_before_3_paid_pilots():
    decision = check_entry(paid_pilots_completed=2, workflow_owner_present=True)
    assert decision.allowed is False
    assert "no_customization_before_3_paid_pilots" in decision.blocked_reasons


def test_entry_allowed_at_three_pilots():
    decision = check_entry(paid_pilots_completed=3, workflow_owner_present=True)
    assert decision.allowed is True
    assert decision.blocked_reasons == ()


def test_workflow_owner_required():
    decision = check_entry(paid_pilots_completed=5, workflow_owner_present=False)
    assert decision.allowed is False
    assert "workflow_owner_missing" in decision.blocked_reasons


def test_delivery_mode_is_founder_assisted():
    decision = check_entry(paid_pilots_completed=3, workflow_owner_present=True)
    assert decision.delivery_mode == "founder_assisted"
    assert decision.disclosure_ar.strip()
    assert decision.disclosure_en.strip()
    assert MIN_PAID_PILOTS == 3


def test_disclosure_has_no_forbidden_guarantee_tokens():
    # The disclosure must never use the banned "guaranteed"/"نضمن" tokens.
    decision = check_entry(paid_pilots_completed=3, workflow_owner_present=True)
    blob = (decision.disclosure_ar + decision.disclosure_en).lower()
    assert "guaranteed" not in blob
    assert "نضمن" not in decision.disclosure_ar
