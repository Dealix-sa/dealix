"""Regression tests for the tenant commercial universe core."""

from __future__ import annotations

import pytest

from dealix.commercial_universe import (
    ApprovalStatus,
    DepartmentObjective,
    PermissionState,
    RelationshipType,
    classify_account,
    create_approval_envelope,
    score_account,
)


def account(**overrides: object) -> dict[str, object]:
    payload: dict[str, object] = {
        "tenant_id": "tenant-a",
        "account_id": "account-1",
        "company_name": "Riyadh Operations Co.",
        "department": "partnerships",
        "relationship": "strategic_partner",
        "permission": "warm",
        "strategic_fit": 90,
        "urgency": 70,
        "value_exchange": "Revenue command pilot in exchange for qualified introductions.",
        "source_ref": "manual-approved:brief-001",
    }
    payload.update(overrides)
    return payload


def test_permitted_relationship_creates_approval_only_envelope() -> None:
    item = classify_account(account())

    envelope = create_approval_envelope(
        item,
        action="prepare partnership proposal",
        channel="email",
        proof_target="approved meeting request or written counterparty response",
    )

    assert item.department is DepartmentObjective.PARTNERSHIPS
    assert item.relationship is RelationshipType.STRATEGIC_PARTNER
    assert envelope.status is ApprovalStatus.REQUIRED
    assert envelope.external_action_allowed is False
    assert envelope.tenant_id == "tenant-a"


def test_research_only_relationship_is_blocked_even_with_high_score() -> None:
    item = classify_account(account(permission="research_only", strategic_fit=100, urgency=100))

    envelope = create_approval_envelope(
        item,
        action="prepare discovery questions",
        channel="email",
        proof_target="internal research note",
    )

    assert score_account(item) == 100
    assert envelope.status is ApprovalStatus.BLOCKED
    assert envelope.external_action_allowed is False


def test_tenant_and_taxonomy_are_required() -> None:
    with pytest.raises(ValueError, match="tenant_id"):
        classify_account(account(tenant_id=""))
    with pytest.raises(ValueError, match="invalid commercial account"):
        classify_account(account(department="not-a-department"))


def test_service_exchange_and_market_access_are_first_class() -> None:
    service = classify_account(
        account(
            account_id="account-service",
            department="service_exchange",
            relationship="service_exchange",
            permission="referral",
        )
    )
    access = classify_account(
        account(
            account_id="account-access",
            department="market_access",
            relationship="implementation_partner",
            permission="approved",
        )
    )

    assert service.department is DepartmentObjective.SERVICE_EXCHANGE
    assert service.relationship is RelationshipType.SERVICE_EXCHANGE
    assert access.department is DepartmentObjective.MARKET_ACCESS
    assert access.permission is PermissionState.APPROVED


def test_invalid_scores_are_rejected() -> None:
    with pytest.raises(ValueError, match="strategic_fit"):
        classify_account(account(strategic_fit=101))
    with pytest.raises(ValueError, match="urgency"):
        classify_account(account(urgency=-1))
