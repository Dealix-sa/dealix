"""Tests for the canonical Action Queue contracts.

Covers:
  - Deterministic ID generation and idempotency
  - Priority scoring formula
  - Autonomy level and approval enforcement
  - External effect safety gates
  - Status transition state machine
  - Retry budget enforcement
  - Fail-closed on invalid inputs
  - Builder convenience
"""
from __future__ import annotations

from datetime import UTC, datetime

import pytest

from dealix.company_intelligence.action_contracts import (
    ActionStatus,
    ActionType,
    AutonomyLevel,
    CanonicalAction,
    build_action,
    compute_priority_score,
    is_valid_transition,
    transition_action,
    valid_transitions_from,
)

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


def _action(**overrides: object) -> CanonicalAction:
    """Build a minimal valid action, overriding any fields."""
    defaults: dict[str, object] = dict(
        tenant_id="tenant-a",
        idempotency_key="idem-1",
        action_type=ActionType.RESEARCH,
        department="market_intelligence",
        autonomy_level=AutonomyLevel.L1_ANALYZE,
    )
    defaults.update(overrides)
    return build_action(**defaults)


# ---------------------------------------------------------------------------
# Deterministic identity
# ---------------------------------------------------------------------------


class TestDeterministicIdentity:
    def test_same_inputs_produce_same_id(self) -> None:
        a = _action()
        b = _action()
        assert a.action_id == b.action_id

    def test_different_idempotency_key_produces_different_id(self) -> None:
        a = _action(idempotency_key="idem-1")
        b = _action(idempotency_key="idem-2")
        assert a.action_id != b.action_id

    def test_different_tenant_produces_different_id(self) -> None:
        a = _action(tenant_id="tenant-a")
        b = _action(tenant_id="tenant-b")
        assert a.action_id != b.action_id

    def test_different_action_type_produces_different_id(self) -> None:
        a = _action(action_type=ActionType.RESEARCH)
        b = _action(action_type=ActionType.QUALIFY)
        assert a.action_id != b.action_id

    def test_different_department_produces_different_id(self) -> None:
        a = _action(department="sales")
        b = _action(department="engineering")
        assert a.action_id != b.action_id

    def test_action_id_format(self) -> None:
        a = _action()
        assert a.action_id.startswith("action_")
        assert len(a.action_id) == 7 + 16  # "action_" + 16 hex chars

    def test_whitespace_in_idempotency_key_is_stripped(self) -> None:
        a = _action(idempotency_key="  idem-1  ")
        b = _action(idempotency_key="idem-1")
        assert a.action_id == b.action_id


# ---------------------------------------------------------------------------
# Priority scoring
# ---------------------------------------------------------------------------


class TestPriorityScoring:
    def test_formula_basic(self) -> None:
        # (0.8 * 0.9 * 1.0 * 0.7) / (0.3 * 0.2) = 0.504 / 0.06 = 8.4
        score = compute_priority_score(
            impact=0.8, urgency=0.9, confidence=1.0,
            reversibility=0.7, effort=0.3, risk=0.2,
        )
        assert abs(score - 8.4) < 0.001

    def test_zero_effort_uses_minimum(self) -> None:
        score = compute_priority_score(
            impact=0.5, urgency=0.5, confidence=0.5,
            reversibility=0.5, effort=0.0, risk=0.5,
        )
        # (0.5^4) / (0.01 * 0.5) = 0.0625 / 0.005 = 12.5
        assert abs(score - 12.5) < 0.001

    def test_zero_risk_uses_minimum(self) -> None:
        score = compute_priority_score(
            impact=0.5, urgency=0.5, confidence=0.5,
            reversibility=0.5, effort=0.5, risk=0.0,
        )
        # (0.5^4) / (0.5 * 0.01) = 0.0625 / 0.005 = 12.5
        assert abs(score - 12.5) < 0.001

    def test_all_ones(self) -> None:
        score = compute_priority_score(
            impact=1.0, urgency=1.0, confidence=1.0,
            reversibility=1.0, effort=1.0, risk=1.0,
        )
        assert score == 1.0

    def test_builder_computes_score_automatically(self) -> None:
        a = _action(impact=0.8, urgency=0.9, confidence=1.0,
                     reversibility=0.7, effort=0.3, risk=0.2)
        expected = compute_priority_score(
            impact=0.8, urgency=0.9, confidence=1.0,
            reversibility=0.7, effort=0.3, risk=0.2,
        )
        assert a.priority_score == expected

    def test_out_of_range_input_rejected(self) -> None:
        with pytest.raises(ValueError, match="impact"):
            compute_priority_score(
                impact=1.5, urgency=0.5, confidence=0.5,
                reversibility=0.5, effort=0.5, risk=0.5,
            )
        with pytest.raises(ValueError, match="risk"):
            compute_priority_score(
                impact=0.5, urgency=0.5, confidence=0.5,
                reversibility=0.5, effort=0.5, risk=-0.1,
            )

    def test_mismatched_priority_score_rejected(self) -> None:
        """Constructing directly with wrong priority_score fails."""
        a = _action()
        data = a.model_dump()
        data["priority_score"] = 999.0
        with pytest.raises(ValueError, match="priority_score"):
            CanonicalAction(**data)


# ---------------------------------------------------------------------------
# Autonomy and approval enforcement
# ---------------------------------------------------------------------------


class TestAutonomyAndApproval:
    def test_l5_requires_approval(self) -> None:
        with pytest.raises(ValueError, match="L5 sensitive"):
            build_action(
                tenant_id="tenant-a",
                idempotency_key="idem-1",
                action_type=ActionType.INTERNAL_UPDATE,
                department="executive",
                autonomy_level=AutonomyLevel.L5_SENSITIVE_EXECUTE,
                approval_required=False,
                external_effect=False,
            )

    def test_external_effect_requires_approval(self) -> None:
        with pytest.raises(ValueError, match="external effects require approval"):
            build_action(
                tenant_id="tenant-a",
                idempotency_key="idem-1",
                action_type=ActionType.SEND_EXTERNAL,
                department="sales",
                autonomy_level=AutonomyLevel.L4_CONTROLLED_EXECUTE,
                approval_required=False,
                external_effect=True,
            )

    def test_external_effect_requires_l4_minimum(self) -> None:
        with pytest.raises(ValueError, match="external effects require autonomy level L4"):
            build_action(
                tenant_id="tenant-a",
                idempotency_key="idem-1",
                action_type=ActionType.SEND_EXTERNAL,
                department="sales",
                autonomy_level=AutonomyLevel.L2_DRAFT,
                external_effect=True,
            )

    def test_internal_action_at_l1_allowed(self) -> None:
        a = build_action(
            tenant_id="tenant-a",
            idempotency_key="idem-1",
            action_type=ActionType.RESEARCH,
            department="market_intelligence",
            autonomy_level=AutonomyLevel.L1_ANALYZE,
            approval_required=True,
            external_effect=False,
        )
        assert a.external_effect is False

    def test_l4_with_external_effect_and_approval_allowed(self) -> None:
        a = build_action(
            tenant_id="tenant-a",
            idempotency_key="idem-ext",
            action_type=ActionType.SEND_EXTERNAL,
            department="sales",
            autonomy_level=AutonomyLevel.L4_CONTROLLED_EXECUTE,
            approval_required=True,
            external_effect=True,
        )
        assert a.external_effect is True
        assert a.approval_required is True


# ---------------------------------------------------------------------------
# Status transitions
# ---------------------------------------------------------------------------


class TestStatusTransitions:
    def test_queued_to_in_progress(self) -> None:
        a = _action()
        assert a.status == ActionStatus.QUEUED
        b = transition_action(a, to_status=ActionStatus.IN_PROGRESS)
        assert b.status == ActionStatus.IN_PROGRESS
        assert a.status == ActionStatus.QUEUED  # original unchanged

    def test_in_progress_to_completed(self) -> None:
        a = _action()
        b = transition_action(a, to_status=ActionStatus.IN_PROGRESS)
        c = transition_action(b, to_status=ActionStatus.COMPLETED)
        assert c.status == ActionStatus.COMPLETED

    def test_completed_is_terminal(self) -> None:
        a = _action()
        b = transition_action(a, to_status=ActionStatus.IN_PROGRESS)
        c = transition_action(b, to_status=ActionStatus.COMPLETED)
        with pytest.raises(ValueError, match="invalid transition"):
            transition_action(c, to_status=ActionStatus.QUEUED)

    def test_cancelled_is_terminal(self) -> None:
        a = _action()
        b = transition_action(a, to_status=ActionStatus.CANCELLED)
        with pytest.raises(ValueError, match="invalid transition"):
            transition_action(b, to_status=ActionStatus.QUEUED)

    def test_expired_is_terminal(self) -> None:
        a = _action()
        b = transition_action(a, to_status=ActionStatus.EXPIRED)
        with pytest.raises(ValueError, match="invalid transition"):
            transition_action(b, to_status=ActionStatus.QUEUED)

    def test_failed_can_retry_to_queued(self) -> None:
        a = build_action(
            tenant_id="tenant-a",
            idempotency_key="idem-retry",
            action_type=ActionType.SYSTEM_TASK,
            department="engineering",
            autonomy_level=AutonomyLevel.L3_INTERNAL_EXECUTE,
            max_retries=2,
        )
        b = transition_action(a, to_status=ActionStatus.IN_PROGRESS)
        c = transition_action(b, to_status=ActionStatus.FAILED)
        d = transition_action(c, to_status=ActionStatus.QUEUED)
        assert d.status == ActionStatus.QUEUED
        assert d.retry_count == 1

    def test_retry_count_increments_on_failed_to_queued(self) -> None:
        a = build_action(
            tenant_id="tenant-a",
            idempotency_key="idem-retry-2",
            action_type=ActionType.SYSTEM_TASK,
            department="engineering",
            autonomy_level=AutonomyLevel.L3_INTERNAL_EXECUTE,
            max_retries=3,
        )
        b = transition_action(a, to_status=ActionStatus.IN_PROGRESS)
        c = transition_action(b, to_status=ActionStatus.FAILED)
        d = transition_action(c, to_status=ActionStatus.QUEUED)
        assert d.retry_count == 1
        e = transition_action(d, to_status=ActionStatus.IN_PROGRESS)
        f = transition_action(e, to_status=ActionStatus.FAILED)
        g = transition_action(f, to_status=ActionStatus.QUEUED)
        assert g.retry_count == 2

    def test_approval_flow(self) -> None:
        a = _action()
        b = transition_action(a, to_status=ActionStatus.IN_PROGRESS)
        c = transition_action(b, to_status=ActionStatus.AWAITING_APPROVAL)
        d = transition_action(c, to_status=ActionStatus.APPROVED)
        e = transition_action(d, to_status=ActionStatus.IN_PROGRESS)
        f = transition_action(e, to_status=ActionStatus.COMPLETED)
        assert f.status == ActionStatus.COMPLETED

    def test_invalid_transition_rejected(self) -> None:
        a = _action()
        with pytest.raises(ValueError, match="invalid transition"):
            transition_action(a, to_status=ActionStatus.COMPLETED)

    def test_valid_transitions_from_queued(self) -> None:
        allowed = valid_transitions_from(ActionStatus.QUEUED)
        assert ActionStatus.IN_PROGRESS in allowed
        assert ActionStatus.BLOCKED in allowed
        assert ActionStatus.CANCELLED in allowed
        assert ActionStatus.COMPLETED not in allowed

    def test_is_valid_transition_helper(self) -> None:
        assert is_valid_transition(ActionStatus.QUEUED, ActionStatus.IN_PROGRESS) is True
        assert is_valid_transition(ActionStatus.QUEUED, ActionStatus.COMPLETED) is False


# ---------------------------------------------------------------------------
# Retry budget
# ---------------------------------------------------------------------------


class TestRetryBudget:
    def test_retry_count_cannot_exceed_max(self) -> None:
        a = _action()
        data = a.model_dump()
        data["retry_count"] = 10
        data["max_retries"] = 3
        with pytest.raises(ValueError, match="retry_count exceeds max_retries"):
            CanonicalAction(**data)

    def test_max_retries_capped_at_five(self) -> None:
        with pytest.raises(ValueError):
            build_action(
                tenant_id="tenant-a",
                idempotency_key="idem-1",
                action_type=ActionType.SYSTEM_TASK,
                department="engineering",
                autonomy_level=AutonomyLevel.L3_INTERNAL_EXECUTE,
                max_retries=10,
            )


# ---------------------------------------------------------------------------
# Extra field protection
# ---------------------------------------------------------------------------


class TestExtraFieldProtection:
    def test_extra_fields_forbidden(self) -> None:
        a = _action()
        data = a.model_dump()
        data["rogue_field"] = "injected"
        with pytest.raises(ValueError):
            CanonicalAction(**data)


# ---------------------------------------------------------------------------
# Builder defaults
# ---------------------------------------------------------------------------


class TestBuilderDefaults:
    def test_default_status_is_queued(self) -> None:
        a = _action()
        assert a.status == ActionStatus.QUEUED

    def test_default_approval_required(self) -> None:
        a = _action()
        assert a.approval_required is True

    def test_default_no_external_effect(self) -> None:
        a = _action()
        assert a.external_effect is False

    def test_all_context_links_optional(self) -> None:
        a = _action()
        assert a.loop_id == ""
        assert a.stage_id == ""
        assert a.opportunity_id == ""
        assert a.trigger == ""
        assert a.objective == ""

    def test_builder_with_full_context(self) -> None:
        a = build_action(
            tenant_id="tenant-a",
            idempotency_key="idem-full",
            action_type=ActionType.PREPARE_PROPOSAL,
            department="sales",
            autonomy_level=AutonomyLevel.L2_DRAFT,
            loop_id="lead_to_cash",
            stage_id="proposal_prepared",
            opportunity_id="opp-1",
            trigger="discovery completed with positive outcome",
            objective="prepare evidence-safe proposal",
            impact=0.9,
            urgency=0.8,
            confidence=0.7,
            reversibility=0.9,
            effort=0.4,
            risk=0.2,
            proof_requirement="proposal reviewed by founder",
            expected_output="CanonicalDraft with proposal content",
            failure_owner="sales_lead",
            due_at=datetime(2026, 8, 10, 12, 0, tzinfo=UTC),
        )
        assert a.loop_id == "lead_to_cash"
        assert a.stage_id == "proposal_prepared"
        assert a.opportunity_id == "opp-1"
        assert a.priority_score > 0


# ---------------------------------------------------------------------------
# Frozen immutability
# ---------------------------------------------------------------------------


class TestFrozenImmutability:
    def test_action_is_frozen(self) -> None:
        a = _action()
        with pytest.raises(Exception):
            a.status = ActionStatus.COMPLETED  # type: ignore[misc]

    def test_transition_returns_new_instance(self) -> None:
        a = _action()
        b = transition_action(a, to_status=ActionStatus.IN_PROGRESS)
        assert a is not b
        assert a.status == ActionStatus.QUEUED
        assert b.status == ActionStatus.IN_PROGRESS


# ---------------------------------------------------------------------------
# Entity ownership registry alignment
# ---------------------------------------------------------------------------


class TestEntityOwnershipAlignment:
    """Verify the contract satisfies the required fields from
    company_intelligence_entity_ownership.json for the Action entity."""

    def test_required_fields_present(self) -> None:
        a = _action()
        # Required: tenant_id, action_type, risk_level, autonomy_level, status, idempotency_key
        assert hasattr(a, "tenant_id") and a.tenant_id
        assert hasattr(a, "action_type") and a.action_type
        assert hasattr(a, "risk_level") and a.risk_level
        assert hasattr(a, "autonomy_level") and isinstance(a.autonomy_level, int)
        assert hasattr(a, "status") and a.status
        assert hasattr(a, "idempotency_key") and a.idempotency_key

    def test_empty_tenant_rejected(self) -> None:
        with pytest.raises(ValueError):
            build_action(
                tenant_id="",
                idempotency_key="idem-1",
                action_type=ActionType.RESEARCH,
                department="sales",
                autonomy_level=AutonomyLevel.L1_ANALYZE,
            )

    def test_empty_idempotency_key_rejected(self) -> None:
        with pytest.raises(ValueError):
            build_action(
                tenant_id="tenant-a",
                idempotency_key="",
                action_type=ActionType.RESEARCH,
                department="sales",
                autonomy_level=AutonomyLevel.L1_ANALYZE,
            )
