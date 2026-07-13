from auto_client_acquisition.approval_center.schemas import ApprovalStatus as QueueStatus
from dealix.commercial_universe import (
    DepartmentObjective,
    PermissionState,
    RelationshipType,
    create_approval_envelope,
    CommercialAccount,
)
from dealix.commercial_universe_approval import to_approval_request


def account(permission: PermissionState, relationship: RelationshipType) -> CommercialAccount:
    return CommercialAccount(
        tenant_id="tenant_demo",
        account_id="acct_demo",
        company_name="Demo Co",
        department=DepartmentObjective.PARTNERSHIPS,
        relationship=relationship,
        permission=permission,
        strategic_fit=90,
        urgency=80,
        value_exchange="implementation exchange",
        source_ref="internal:demo",
    )


def test_permitted_account_maps_to_pending_canonical_partner_action() -> None:
    record = account(PermissionState.WARM, RelationshipType.STRATEGIC_PARTNER)
    envelope = create_approval_envelope(
        record,
        action="prepare strategic conversation",
        channel="email",
        proof_target="approved_partner_brief",
    )

    request = to_approval_request(record, envelope)

    assert request.status is QueueStatus.PENDING
    assert request.action_mode == "approval_required"
    assert request.action_type == "partner_intro"
    assert request.object_type == "commercial_account"
    assert request.object_id == "acct_demo"
    assert request.customer_id == "tenant_demo"
    assert request.proof_target == "approved_partner_brief"
    assert request.audit_ref == "commercial-universe:tenant_demo:internal:demo"


def test_blocked_research_account_is_terminal_in_canonical_queue() -> None:
    record = account(PermissionState.RESEARCH_ONLY, RelationshipType.PROSPECT)
    envelope = create_approval_envelope(
        record,
        action="draft_email",
        channel="email",
        proof_target="research_note",
    )

    request = to_approval_request(record, envelope)

    assert request.status is QueueStatus.BLOCKED
    assert request.action_mode == "blocked"
    assert request.action_type == "draft_email"


def test_explicit_canonical_action_is_preserved() -> None:
    record = account(PermissionState.REFERRAL, RelationshipType.PROSPECT)
    envelope = create_approval_envelope(
        record,
        action="prepare_diagnostic",
        channel="internal",
        proof_target="diagnostic_draft",
    )

    request = to_approval_request(record, envelope)

    assert request.action_type == "prepare_diagnostic"


def test_scope_mismatch_is_rejected() -> None:
    record = account(PermissionState.WARM, RelationshipType.PROSPECT)
    envelope = create_approval_envelope(
        record,
        action="follow_up_task",
        channel="internal",
        proof_target="follow_up_task",
    )
    mismatched = type(envelope)(
        tenant_id="other_tenant",
        account_id=envelope.account_id,
        department=envelope.department,
        relationship=envelope.relationship,
        action=envelope.action,
        channel=envelope.channel,
        rationale=envelope.rationale,
        proof_target=envelope.proof_target,
        status=envelope.status,
    )

    try:
        to_approval_request(record, mismatched)
    except ValueError as exc:
        assert "scope" in str(exc)
    else:
        raise AssertionError("scope mismatch must be rejected")
