"""Tests for Company and Contact state machine transitions.

Covers:
  - Company pipeline: discovered → researched → qualified → active
  - Company recovery: churned/parked → discovered
  - Company parked from any non-terminal state
  - Contact pipeline: identified → verified → engaged
  - Contact recovery: inactive → verified
  - Contact opt-out terminal enforcement
  - Frozen immutability of originals after transition
"""
from __future__ import annotations

import pytest

from dealix.company_intelligence.graph_contracts import (
    CompanyStatus,
    ContactStatus,
    build_company,
    build_contact,
    is_valid_company_transition,
    is_valid_contact_transition,
    transition_company,
    transition_contact,
    valid_company_transitions_from,
    valid_contact_transitions_from,
)


def _company(**overrides: object):
    defaults = dict(
        tenant_id="tenant-a",
        deduplication_key="key-1",
        name="Test Company",
        source_id="source-1",
    )
    defaults.update(overrides)
    return build_company(**defaults)


def _contact(**overrides: object):
    defaults = dict(
        tenant_id="tenant-a",
        deduplication_key="key-1",
        company_id="company_abc123",
        source_id="source-1",
    )
    defaults.update(overrides)
    return build_contact(**defaults)


# ---------------------------------------------------------------------------
# Company pipeline
# ---------------------------------------------------------------------------


class TestCompanyPipeline:
    def test_discovered_to_researched(self) -> None:
        c = _company(status=CompanyStatus.DISCOVERED)
        t = transition_company(c, to_status=CompanyStatus.RESEARCHED)
        assert t.status == CompanyStatus.RESEARCHED

    def test_researched_to_qualified(self) -> None:
        c = _company(status=CompanyStatus.RESEARCHED)
        t = transition_company(c, to_status=CompanyStatus.QUALIFIED)
        assert t.status == CompanyStatus.QUALIFIED

    def test_qualified_to_active(self) -> None:
        c = _company(status=CompanyStatus.QUALIFIED)
        t = transition_company(c, to_status=CompanyStatus.ACTIVE)
        assert t.status == CompanyStatus.ACTIVE

    def test_full_pipeline_traversal(self) -> None:
        c = _company(status=CompanyStatus.DISCOVERED)
        for next_status in [
            CompanyStatus.RESEARCHED,
            CompanyStatus.QUALIFIED,
            CompanyStatus.ACTIVE,
        ]:
            c = transition_company(c, to_status=next_status)
        assert c.status == CompanyStatus.ACTIVE


class TestCompanyParked:
    @pytest.mark.parametrize("status", [
        CompanyStatus.DISCOVERED,
        CompanyStatus.RESEARCHED,
        CompanyStatus.QUALIFIED,
        CompanyStatus.ACTIVE,
    ])
    def test_can_park_from_any_active_stage(self, status: CompanyStatus) -> None:
        c = _company(status=status)
        t = transition_company(c, to_status=CompanyStatus.PARKED)
        assert t.status == CompanyStatus.PARKED


class TestCompanyRecovery:
    def test_churned_to_discovered(self) -> None:
        c = _company(status=CompanyStatus.CHURNED)
        t = transition_company(c, to_status=CompanyStatus.DISCOVERED)
        assert t.status == CompanyStatus.DISCOVERED

    def test_parked_to_discovered(self) -> None:
        c = _company(status=CompanyStatus.PARKED)
        t = transition_company(c, to_status=CompanyStatus.DISCOVERED)
        assert t.status == CompanyStatus.DISCOVERED


class TestCompanyInvalidTransitions:
    def test_discovered_cannot_jump_to_active(self) -> None:
        c = _company(status=CompanyStatus.DISCOVERED)
        with pytest.raises(ValueError, match="invalid company transition"):
            transition_company(c, to_status=CompanyStatus.ACTIVE)

    def test_churned_cannot_jump_to_active(self) -> None:
        c = _company(status=CompanyStatus.CHURNED)
        with pytest.raises(ValueError, match="invalid company transition"):
            transition_company(c, to_status=CompanyStatus.ACTIVE)

    def test_is_valid_transition_check(self) -> None:
        assert is_valid_company_transition(
            CompanyStatus.DISCOVERED, CompanyStatus.RESEARCHED
        )
        assert not is_valid_company_transition(
            CompanyStatus.DISCOVERED, CompanyStatus.ACTIVE
        )

    def test_valid_transitions_from(self) -> None:
        transitions = valid_company_transitions_from(CompanyStatus.ACTIVE)
        assert CompanyStatus.CHURNED in transitions
        assert CompanyStatus.PARKED in transitions


class TestCompanyImmutability:
    def test_original_unchanged_after_transition(self) -> None:
        c = _company(status=CompanyStatus.DISCOVERED)
        t = transition_company(c, to_status=CompanyStatus.RESEARCHED)
        assert c.status == CompanyStatus.DISCOVERED
        assert t.status == CompanyStatus.RESEARCHED
        assert c.company_id == t.company_id


# ---------------------------------------------------------------------------
# Contact pipeline
# ---------------------------------------------------------------------------


class TestContactPipeline:
    def test_identified_to_verified(self) -> None:
        c = _contact(status=ContactStatus.IDENTIFIED)
        t = transition_contact(c, to_status=ContactStatus.VERIFIED)
        assert t.status == ContactStatus.VERIFIED

    def test_verified_to_engaged(self) -> None:
        c = _contact(status=ContactStatus.VERIFIED)
        t = transition_contact(c, to_status=ContactStatus.ENGAGED)
        assert t.status == ContactStatus.ENGAGED

    def test_full_pipeline_traversal(self) -> None:
        c = _contact(status=ContactStatus.IDENTIFIED)
        c = transition_contact(c, to_status=ContactStatus.VERIFIED)
        c = transition_contact(c, to_status=ContactStatus.ENGAGED)
        assert c.status == ContactStatus.ENGAGED


class TestContactOptOut:
    @pytest.mark.parametrize("status", [
        ContactStatus.IDENTIFIED,
        ContactStatus.VERIFIED,
        ContactStatus.ENGAGED,
        ContactStatus.INACTIVE,
    ])
    def test_can_opt_out_from_any_non_terminal(self, status: ContactStatus) -> None:
        c = _contact(status=status)
        t = transition_contact(c, to_status=ContactStatus.OPTED_OUT)
        assert t.status == ContactStatus.OPTED_OUT

    def test_opted_out_is_terminal(self) -> None:
        assert valid_contact_transitions_from(ContactStatus.OPTED_OUT) == frozenset()

    def test_opted_out_transition_rejected(self) -> None:
        c = _contact(status=ContactStatus.OPTED_OUT)
        with pytest.raises(ValueError, match="invalid contact transition"):
            transition_contact(c, to_status=ContactStatus.IDENTIFIED)


class TestContactRecovery:
    def test_inactive_to_verified(self) -> None:
        c = _contact(status=ContactStatus.INACTIVE)
        t = transition_contact(c, to_status=ContactStatus.VERIFIED)
        assert t.status == ContactStatus.VERIFIED


class TestContactInvalidTransitions:
    def test_identified_cannot_jump_to_engaged(self) -> None:
        c = _contact(status=ContactStatus.IDENTIFIED)
        with pytest.raises(ValueError, match="invalid contact transition"):
            transition_contact(c, to_status=ContactStatus.ENGAGED)

    def test_engaged_cannot_jump_to_identified(self) -> None:
        c = _contact(status=ContactStatus.ENGAGED)
        with pytest.raises(ValueError, match="invalid contact transition"):
            transition_contact(c, to_status=ContactStatus.IDENTIFIED)

    def test_is_valid_transition_check(self) -> None:
        assert is_valid_contact_transition(
            ContactStatus.IDENTIFIED, ContactStatus.VERIFIED
        )
        assert not is_valid_contact_transition(
            ContactStatus.IDENTIFIED, ContactStatus.ENGAGED
        )


class TestContactImmutability:
    def test_original_unchanged_after_transition(self) -> None:
        c = _contact(status=ContactStatus.IDENTIFIED)
        t = transition_contact(c, to_status=ContactStatus.VERIFIED)
        assert c.status == ContactStatus.IDENTIFIED
        assert t.status == ContactStatus.VERIFIED
        assert c.contact_id == t.contact_id
