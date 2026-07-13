from dealix.commercial_command_center import build_command_center
from dealix.commercial_universe import (
    DepartmentObjective,
    PermissionState,
    RelationshipType,
    CommercialAccount,
    create_approval_envelope,
)


def make_account(account_id: str, department: DepartmentObjective, permission: PermissionState, urgency: int) -> CommercialAccount:
    return CommercialAccount(
        tenant_id="tenant_demo",
        account_id=account_id,
        company_name=account_id,
        department=department,
        relationship=RelationshipType.PROSPECT,
        permission=permission,
        strategic_fit=90,
        urgency=urgency,
        value_exchange="diagnostic",
        source_ref=f"internal:{account_id}",
    )


def test_command_center_ranks_pending_accounts_and_counts_departments() -> None:
    first = make_account("acct_a", DepartmentObjective.SALES, PermissionState.WARM, 80)
    second = make_account("acct_b", DepartmentObjective.PARTNERSHIPS, PermissionState.REFERRAL, 95)
    blocked = make_account("acct_c", DepartmentObjective.SALES, PermissionState.RESEARCH_ONLY, 100)
    envelopes = [
        create_approval_envelope(first, action="follow_up_task", channel="internal", proof_target="follow_up"),
        create_approval_envelope(second, action="partner_intro", channel="internal", proof_target="intro"),
        create_approval_envelope(blocked, action="draft_email", channel="email", proof_target="research"),
    ]

    snapshot = build_command_center([first, second, blocked], envelopes)

    assert snapshot.tenant_id == "tenant_demo"
    assert snapshot.account_count == 3
    assert snapshot.pending_approval_count == 2
    assert snapshot.blocked_count == 1
    assert snapshot.department_counts == {"partnerships": 1, "sales": 2}
    assert snapshot.priority_account_ids == ("acct_b", "acct_a")
    assert snapshot.priority_actions == ("partner_intro", "follow_up_task")


def test_command_center_rejects_mixed_tenants() -> None:
    account = make_account("acct_a", DepartmentObjective.SALES, PermissionState.WARM, 50)
    envelope = create_approval_envelope(
        account, action="follow_up_task", channel="internal", proof_target="follow_up"
    )
    try:
        build_command_center([account], [type(envelope)(
            tenant_id="other_tenant",
            account_id=envelope.account_id,
            department=envelope.department,
            relationship=envelope.relationship,
            action=envelope.action,
            channel=envelope.channel,
            rationale=envelope.rationale,
            proof_target=envelope.proof_target,
            status=envelope.status,
        )])
    except ValueError as exc:
        assert "tenant" in str(exc)
    else:
        raise AssertionError("mixed tenants must be rejected")
