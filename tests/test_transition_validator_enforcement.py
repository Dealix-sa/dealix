"""Regression tests: transition helpers re-run Pydantic model validators.

These tests verify the fix for the model_copy(update=...) bypass identified
in PR #1041 review. In Pydantic v2, model_copy(update=...) does NOT re-run
model validators, so transition helpers must use model_validate() instead.

Each test constructs a scenario where the old model_copy approach would have
silently produced an invalid object, and asserts that the fixed transition
helper now correctly raises ValueError.
"""
from __future__ import annotations

from datetime import UTC, datetime, timezone

import pytest

from dealix.company_intelligence.action_contracts import (
    ActionStatus,
    ActionType,
    AutonomyLevel,
    RiskLevel,
    build_action,
    transition_action,
)
from dealix.company_intelligence.execution_contracts import (
    CanonicalApproval,
    CanonicalApprovalStatus,
    CanonicalOpportunity,
    DraftChannel,
    DraftStatus,
    LawfulContactBasis,
    OpportunityStage,
    build_draft,
    transition_approval,
    transition_draft,
    transition_opportunity,
)
from dealix.company_intelligence.proposal_contracts import (
    ProposalStatus,
    build_proposal,
    transition_proposal,
)
from dealix.company_intelligence.tenant_contracts import (
    TenantStatus,
    build_tenant,
    transition_tenant,
)


# ---------------------------------------------------------------------------
# Action: retry exhaustion bypass
# ---------------------------------------------------------------------------


class TestActionRetryExhaustion:
    """Transition FAILED → QUEUED increments retry_count.

    The model_validator rejects retry_count > max_retries. With
    model_copy(update=...) this invariant was silently bypassed.
    """

    def test_retry_within_limit_succeeds(self) -> None:
        action = build_action(
            tenant_id="t1",
            idempotency_key="k1",
            action_type=ActionType.RESEARCH,
            department="sales",
            autonomy_level=AutonomyLevel.L0_OBSERVE,
            max_retries=2,
        )
        # QUEUED → IN_PROGRESS → FAILED → QUEUED (retry 1)
        action = transition_action(action, to_status=ActionStatus.IN_PROGRESS)
        action = transition_action(action, to_status=ActionStatus.FAILED)
        action = transition_action(action, to_status=ActionStatus.QUEUED)
        assert action.retry_count == 1

    def test_retry_exhaustion_raises(self) -> None:
        action = build_action(
            tenant_id="t1",
            idempotency_key="k1",
            action_type=ActionType.RESEARCH,
            department="sales",
            autonomy_level=AutonomyLevel.L0_OBSERVE,
            max_retries=1,
        )
        # First cycle: QUEUED → IN_PROGRESS → FAILED → QUEUED (retry_count=1)
        action = transition_action(action, to_status=ActionStatus.IN_PROGRESS)
        action = transition_action(action, to_status=ActionStatus.FAILED)
        action = transition_action(action, to_status=ActionStatus.QUEUED)
        assert action.retry_count == 1

        # Second cycle: QUEUED → IN_PROGRESS → FAILED
        action = transition_action(action, to_status=ActionStatus.IN_PROGRESS)
        action = transition_action(action, to_status=ActionStatus.FAILED)

        # retry_count would become 2 > max_retries=1 → must raise
        with pytest.raises(ValueError, match="retry_count exceeds max_retries"):
            transition_action(action, to_status=ActionStatus.QUEUED)

    def test_zero_retries_rejects_first_retry(self) -> None:
        action = build_action(
            tenant_id="t1",
            idempotency_key="k2",
            action_type=ActionType.INTERNAL_UPDATE,
            department="ops",
            autonomy_level=AutonomyLevel.L1_ANALYZE,
            max_retries=0,
        )
        action = transition_action(action, to_status=ActionStatus.IN_PROGRESS)
        action = transition_action(action, to_status=ActionStatus.FAILED)

        with pytest.raises(ValueError, match="retry_count exceeds max_retries"):
            transition_action(action, to_status=ActionStatus.QUEUED)


# ---------------------------------------------------------------------------
# Action: deterministic ID is preserved across transitions
# ---------------------------------------------------------------------------


class TestActionIdIntegrity:
    """Transitions must preserve the deterministic action_id.

    model_validate re-checks the ID matches the canonical payload.
    """

    def test_id_stable_across_transitions(self) -> None:
        action = build_action(
            tenant_id="t1",
            idempotency_key="k1",
            action_type=ActionType.QUALIFY,
            department="sales",
            autonomy_level=AutonomyLevel.L2_DRAFT,
        )
        original_id = action.action_id
        action = transition_action(action, to_status=ActionStatus.IN_PROGRESS)
        assert action.action_id == original_id
        action = transition_action(action, to_status=ActionStatus.COMPLETED)
        assert action.action_id == original_id


# ---------------------------------------------------------------------------
# Proposal: sent_at invariants
# ---------------------------------------------------------------------------


class TestProposalSentAtInvariants:
    """Proposal model_validator enforces:
    - SENT proposals must have sent_at
    - DRAFT proposals must not have sent_at
    - sent_at must be timezone-aware

    With model_copy(update=...) these were silently bypassed.
    """

    def test_transition_to_sent_without_sent_at_raises(self) -> None:
        proposal = build_proposal(
            tenant_id="t1",
            opportunity_id="opp1",
            offer_id="off1",
            approval_id="apr1",
            source_id="src1",
        )
        # DRAFT → PENDING_REVIEW → APPROVED
        proposal = transition_proposal(proposal, to_status=ProposalStatus.PENDING_REVIEW)
        proposal = transition_proposal(proposal, to_status=ProposalStatus.APPROVED)

        # APPROVED → SENT without sent_at → must raise
        with pytest.raises(ValueError, match="sent proposals must have a sent_at"):
            transition_proposal(proposal, to_status=ProposalStatus.SENT)

    def test_transition_to_sent_with_sent_at_succeeds(self) -> None:
        proposal = build_proposal(
            tenant_id="t1",
            opportunity_id="opp1",
            offer_id="off1",
            approval_id="apr1",
            source_id="src1",
        )
        proposal = transition_proposal(proposal, to_status=ProposalStatus.PENDING_REVIEW)
        proposal = transition_proposal(proposal, to_status=ProposalStatus.APPROVED)

        now = datetime.now(UTC)
        sent = transition_proposal(
            proposal,
            to_status=ProposalStatus.SENT,
            sent_at=now,
        )
        assert sent.status == ProposalStatus.SENT
        assert sent.sent_at == now

    def test_transition_to_sent_with_naive_datetime_raises(self) -> None:
        proposal = build_proposal(
            tenant_id="t1",
            opportunity_id="opp2",
            offer_id="off2",
            approval_id="apr2",
            source_id="src2",
        )
        proposal = transition_proposal(proposal, to_status=ProposalStatus.PENDING_REVIEW)
        proposal = transition_proposal(proposal, to_status=ProposalStatus.APPROVED)

        # naive datetime → must raise
        with pytest.raises(ValueError, match="sent_at must be timezone-aware"):
            transition_proposal(
                proposal,
                to_status=ProposalStatus.SENT,
                sent_at=datetime(2026, 1, 1, 12, 0, 0),  # no tzinfo
            )


# ---------------------------------------------------------------------------
# Tenant: suspended_at invariants
# ---------------------------------------------------------------------------


class TestTenantSuspendedAtInvariants:
    """Tenant model_validator enforces:
    - suspended_at must be timezone-aware if set
    - SUSPENDED tenants must have suspended_at
    - ACTIVE tenants must not have suspended_at

    With model_copy(update=...) a naive datetime for suspended_at
    would have silently produced an invalid object.
    """

    def test_suspend_auto_sets_timestamp(self) -> None:
        tenant = build_tenant(handle="acme", name="Acme", source_id="src1")
        suspended = transition_tenant(tenant, to_status=TenantStatus.SUSPENDED)
        assert suspended.status == TenantStatus.SUSPENDED
        assert suspended.suspended_at is not None
        assert suspended.suspended_at.tzinfo is not None

    def test_reactivate_clears_suspended_at(self) -> None:
        tenant = build_tenant(handle="acme", name="Acme", source_id="src1")
        suspended = transition_tenant(tenant, to_status=TenantStatus.SUSPENDED)
        reactivated = transition_tenant(suspended, to_status=TenantStatus.ACTIVE)
        assert reactivated.status == TenantStatus.ACTIVE
        assert reactivated.suspended_at is None

    def test_suspend_with_naive_datetime_raises(self) -> None:
        tenant = build_tenant(handle="acme", name="Acme", source_id="src1")

        with pytest.raises(ValueError, match="suspended_at must be timezone-aware"):
            transition_tenant(
                tenant,
                to_status=TenantStatus.SUSPENDED,
                suspended_at=datetime(2026, 6, 1, 12, 0, 0),  # no tzinfo
            )

    def test_suspend_with_aware_datetime_succeeds(self) -> None:
        tenant = build_tenant(handle="acme", name="Acme", source_id="src1")
        ts = datetime(2026, 6, 1, 12, 0, 0, tzinfo=UTC)
        suspended = transition_tenant(
            tenant,
            to_status=TenantStatus.SUSPENDED,
            suspended_at=ts,
        )
        assert suspended.suspended_at == ts


# ---------------------------------------------------------------------------
# Approval: execution_allowed invariants
# ---------------------------------------------------------------------------


class TestApprovalExecutionInvariants:
    """Approval model_validator enforces that execution_allowed=True
    requires status=GRANTED.

    With model_copy(update=...) a transition to REJECTED would have
    kept execution_allowed=True unchecked.
    """

    def test_approval_transition_preserves_safety(self) -> None:
        approval = CanonicalApproval(
            tenant_id="t1",
            approval_id="appr-1",
            action_id="act1",
            object_type="draft",
            object_id="draft-1",
            action_type="send_email",
            proof_target="approved outcome",
        )
        assert approval.status == CanonicalApprovalStatus.PENDING
        assert not approval.execution_allowed

        granted = transition_approval(
            approval,
            to_status=CanonicalApprovalStatus.GRANTED,
        )
        assert granted.status == CanonicalApprovalStatus.GRANTED
        assert granted.decision_at is not None

    def test_approval_rejection_succeeds(self) -> None:
        approval = CanonicalApproval(
            tenant_id="t1",
            approval_id="appr-1",
            action_id="act1",
            object_type="draft",
            object_id="draft-1",
            action_type="send_email",
            proof_target="approved outcome",
        )
        rejected = transition_approval(
            approval,
            to_status=CanonicalApprovalStatus.REJECTED,
        )
        assert rejected.status == CanonicalApprovalStatus.REJECTED
        assert not rejected.execution_allowed


# ---------------------------------------------------------------------------
# Draft: channel safety invariants survive transitions
# ---------------------------------------------------------------------------


class TestDraftSafetyInvariants:
    """Draft model_validator enforces:
    - execution_allowed must be False
    - approval_required must be True
    - WhatsApp and LinkedIn channel restrictions

    Transitions must not bypass these.
    """

    def test_draft_transitions_preserve_safety_flags(self) -> None:
        draft = build_draft(
            tenant_id="t1",
            action_id="act1",
            opportunity_id="opp1",
            channel=DraftChannel.EMAIL,
            content="Test draft content",
            lawful_contact_basis=LawfulContactBasis.EXISTING_RELATIONSHIP,
            source_evidence=["evidence-abc"],
        )
        assert not draft.execution_allowed
        assert draft.approval_required

        # GENERATED → PENDING_APPROVAL
        pending = transition_draft(draft, to_status=DraftStatus.PENDING_APPROVAL)
        assert not pending.execution_allowed
        assert pending.approval_required

        # PENDING_APPROVAL → APPROVED
        approved = transition_draft(pending, to_status=DraftStatus.APPROVED)
        assert not approved.execution_allowed
        assert approved.approval_required


# ---------------------------------------------------------------------------
# Opportunity: external_action_allowed invariant
# ---------------------------------------------------------------------------


class TestOpportunitySafetyInvariants:
    """Opportunity model_validator enforces external_action_allowed=False.

    Transitions must re-validate this invariant.
    """

    def test_opportunity_transition_preserves_external_block(self) -> None:
        opp = CanonicalOpportunity(
            tenant_id="t1",
            opportunity_id="opp-1",
            company_id="comp1",
            company_name="TestCo",
            offer_id="off1",
            stage=OpportunityStage.RESEARCH,
            score=50,
            next_action="qualify",
            proof_target="initial assessment",
        )
        assert not opp.external_action_allowed

        qualified = transition_opportunity(opp, to_stage=OpportunityStage.QUALIFY)
        assert not qualified.external_action_allowed

        approved = transition_opportunity(qualified, to_stage=OpportunityStage.APPROVAL)
        assert not approved.external_action_allowed


# ---------------------------------------------------------------------------
# Deterministic IDs survive round-trip through model_validate
# ---------------------------------------------------------------------------


class TestDeterministicIdPreservation:
    """Verify that model_validate({**model_dump, **updates}) preserves
    deterministic IDs. This confirms model_validate is a valid replacement
    for model_copy(update=...) — IDs remain stable because they are
    recomputed from the same identity fields.
    """

    def test_action_id_preserved(self) -> None:
        action = build_action(
            tenant_id="t1",
            idempotency_key="k1",
            action_type=ActionType.RESEARCH,
            department="dept",
            autonomy_level=AutonomyLevel.L0_OBSERVE,
        )
        progressed = transition_action(action, to_status=ActionStatus.IN_PROGRESS)
        assert progressed.action_id == action.action_id

    def test_proposal_id_preserved(self) -> None:
        proposal = build_proposal(
            tenant_id="t1",
            opportunity_id="opp1",
            offer_id="off1",
            approval_id="apr1",
            source_id="src1",
        )
        pending = transition_proposal(
            proposal,
            to_status=ProposalStatus.PENDING_REVIEW,
        )
        assert pending.proposal_id == proposal.proposal_id

    def test_tenant_id_preserved(self) -> None:
        tenant = build_tenant(handle="test-co", name="Test", source_id="src1")
        suspended = transition_tenant(tenant, to_status=TenantStatus.SUSPENDED)
        assert suspended.tenant_id == tenant.tenant_id
        reactivated = transition_tenant(suspended, to_status=TenantStatus.ACTIVE)
        assert reactivated.tenant_id == tenant.tenant_id


# ---------------------------------------------------------------------------
# Full lifecycle round-trips
# ---------------------------------------------------------------------------


class TestFullLifecycleRoundTrips:
    """Exercise complete lifecycle paths through transition helpers.

    These tests ensure model_validate handles repeated transitions
    (each producing a new validated instance) without accumulating errors.
    """

    def test_action_full_success_path(self) -> None:
        action = build_action(
            tenant_id="t1",
            idempotency_key="lc1",
            action_type=ActionType.QUALIFY,
            department="sales",
            autonomy_level=AutonomyLevel.L2_DRAFT,
            max_retries=1,
        )
        assert action.status == ActionStatus.QUEUED
        action = transition_action(action, to_status=ActionStatus.IN_PROGRESS)
        assert action.status == ActionStatus.IN_PROGRESS
        action = transition_action(action, to_status=ActionStatus.COMPLETED)
        assert action.status == ActionStatus.COMPLETED

    def test_action_retry_then_complete(self) -> None:
        action = build_action(
            tenant_id="t1",
            idempotency_key="lc2",
            action_type=ActionType.RESEARCH,
            department="ops",
            autonomy_level=AutonomyLevel.L1_ANALYZE,
            max_retries=1,
        )
        action = transition_action(action, to_status=ActionStatus.IN_PROGRESS)
        action = transition_action(action, to_status=ActionStatus.FAILED)
        action = transition_action(action, to_status=ActionStatus.QUEUED)
        assert action.retry_count == 1
        action = transition_action(action, to_status=ActionStatus.IN_PROGRESS)
        action = transition_action(action, to_status=ActionStatus.COMPLETED)
        assert action.status == ActionStatus.COMPLETED

    def test_proposal_full_lifecycle(self) -> None:
        proposal = build_proposal(
            tenant_id="t1",
            opportunity_id="opp1",
            offer_id="off1",
            approval_id="apr1",
            source_id="src1",
        )
        proposal = transition_proposal(proposal, to_status=ProposalStatus.PENDING_REVIEW)
        proposal = transition_proposal(proposal, to_status=ProposalStatus.APPROVED)
        proposal = transition_proposal(
            proposal,
            to_status=ProposalStatus.SENT,
            sent_at=datetime.now(UTC),
        )
        proposal = transition_proposal(proposal, to_status=ProposalStatus.ACCEPTED)
        assert proposal.status == ProposalStatus.ACCEPTED

    def test_tenant_suspend_and_reactivate(self) -> None:
        tenant = build_tenant(handle="round-trip", name="RT", source_id="src1")
        tenant = transition_tenant(tenant, to_status=TenantStatus.SUSPENDED)
        assert tenant.suspended_at is not None
        tenant = transition_tenant(tenant, to_status=TenantStatus.ACTIVE)
        assert tenant.suspended_at is None
        tenant = transition_tenant(tenant, to_status=TenantStatus.CHURNED)
        assert tenant.status == TenantStatus.CHURNED
