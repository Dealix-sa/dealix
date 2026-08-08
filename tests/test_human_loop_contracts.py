"""Tests for HumanLoopPolicy contracts — autonomy, escalation, and safety."""
from __future__ import annotations

import pytest

from dealix.company_intelligence.action_contracts import AutonomyLevel, RiskLevel
from dealix.company_intelligence.human_loop_contracts import (
    CanonicalHumanLoopPolicy,
    EscalationRule,
    EscalationTrigger,
    HumanLoopMode,
    HumanLoopPolicyStatus,
    TimeoutAction,
    build_human_loop_policy,
    is_valid_policy_transition,
    requires_human_approval,
    transition_policy,
    valid_policy_transitions_from,
)

# ---------------------------------------------------------------------------
# Builder
# ---------------------------------------------------------------------------


class TestBuildHumanLoopPolicy:
    """build_human_loop_policy produces a valid, deterministic policy."""

    def test_default_policy(self) -> None:
        policy = build_human_loop_policy(
            tenant_id="t1",
            name="Default Policy",
            source_id="src1",
        )
        assert policy.tenant_id == "t1"
        assert policy.name == "Default Policy"
        assert policy.mode == HumanLoopMode.SMART_APPROVAL
        assert policy.default_autonomy_level == AutonomyLevel.L2_DRAFT
        assert policy.never_auto_external is True
        assert policy.status == HumanLoopPolicyStatus.DRAFT
        assert policy.policy_id.startswith("hlpolicy_")

    def test_deterministic_id(self) -> None:
        p1 = build_human_loop_policy(
            tenant_id="t1", name="Policy A", source_id="src1"
        )
        p2 = build_human_loop_policy(
            tenant_id="t1", name="Policy A", source_id="src2"
        )
        assert p1.policy_id == p2.policy_id

    def test_different_names_different_ids(self) -> None:
        p1 = build_human_loop_policy(
            tenant_id="t1", name="Policy A", source_id="src1"
        )
        p2 = build_human_loop_policy(
            tenant_id="t1", name="Policy B", source_id="src1"
        )
        assert p1.policy_id != p2.policy_id

    def test_full_approval_mode(self) -> None:
        policy = build_human_loop_policy(
            tenant_id="t1",
            name="Full Approval",
            source_id="src1",
            mode=HumanLoopMode.FULL_APPROVAL,
            default_autonomy_level=AutonomyLevel.L0_OBSERVE,
        )
        assert policy.mode == HumanLoopMode.FULL_APPROVAL
        assert policy.default_autonomy_level == AutonomyLevel.L0_OBSERVE

    def test_with_escalation_rules(self) -> None:
        rules = (
            EscalationRule(
                trigger=EscalationTrigger.LOW_CONFIDENCE,
                threshold=0.3,
                description="Escalate when confidence < 30%",
            ),
            EscalationRule(
                trigger=EscalationTrigger.FIRST_CONTACT,
                threshold=1.0,
                description="Always escalate first contact",
            ),
            EscalationRule(
                trigger=EscalationTrigger.HIGH_VALUE,
                threshold=0.8,
                description="Escalate high-value deals",
            ),
        )
        policy = build_human_loop_policy(
            tenant_id="t1",
            name="Escalation Policy",
            source_id="src1",
            escalation_rules=rules,
        )
        assert len(policy.escalation_rules) == 3

    def test_with_action_type_overrides(self) -> None:
        policy = build_human_loop_policy(
            tenant_id="t1",
            name="Override Policy",
            source_id="src1",
            action_type_overrides=(
                ("research", AutonomyLevel.L1_ANALYZE.value),
                ("send_external", AutonomyLevel.L5_SENSITIVE_EXECUTE.value),
            ),
        )
        assert len(policy.action_type_overrides) == 2

    def test_with_notification_channels(self) -> None:
        policy = build_human_loop_policy(
            tenant_id="t1",
            name="Notified Policy",
            source_id="src1",
            notification_channels=("email", "whatsapp_draft", "dashboard"),
        )
        assert len(policy.notification_channels) == 3

    def test_timeout_configuration(self) -> None:
        policy = build_human_loop_policy(
            tenant_id="t1",
            name="Timeout Policy",
            source_id="src1",
            response_timeout_minutes=120,
            timeout_action=TimeoutAction.ESCALATE,
        )
        assert policy.response_timeout_minutes == 120
        assert policy.timeout_action == TimeoutAction.ESCALATE


# ---------------------------------------------------------------------------
# Safety invariants — NON-NEGOTIABLE
# ---------------------------------------------------------------------------


class TestHumanLoopSafetyInvariants:
    """Model validator enforces human loop safety rules."""

    def test_never_auto_external_must_be_true(self) -> None:
        """never_auto_external=False must raise — this is non-negotiable."""
        with pytest.raises(
            ValueError,
            match="external actions always require human approval",
        ):
            CanonicalHumanLoopPolicy(
                tenant_id="t1",
                policy_id="hlpolicy_fake",
                name="Unsafe",
                never_auto_external=False,  # ← must fail
                evidence_refs=("ev1",),
                source_id="src1",
            )

    def test_default_autonomy_cannot_exceed_l3(self) -> None:
        """L4+ autonomy would imply external auto-execution."""
        with pytest.raises(
            ValueError,
            match="cannot exceed L3_INTERNAL_EXECUTE",
        ):
            build_human_loop_policy(
                tenant_id="t1",
                name="Too Autonomous",
                source_id="src1",
                default_autonomy_level=AutonomyLevel.L4_CONTROLLED_EXECUTE,
            )

    def test_l5_autonomy_also_rejected(self) -> None:
        with pytest.raises(ValueError, match="cannot exceed L3"):
            build_human_loop_policy(
                tenant_id="t1",
                name="Way Too Autonomous",
                source_id="src1",
                default_autonomy_level=AutonomyLevel.L5_SENSITIVE_EXECUTE,
            )

    def test_no_evidence_raises(self) -> None:
        with pytest.raises(ValueError, match="at least one evidence reference"):
            build_human_loop_policy(
                tenant_id="t1",
                name="No Evidence",
                source_id="src1",
                evidence_refs=(),
            )

    def test_invalid_action_override_level_raises(self) -> None:
        with pytest.raises(ValueError, match="invalid autonomy level"):
            build_human_loop_policy(
                tenant_id="t1",
                name="Bad Override",
                source_id="src1",
                action_type_overrides=(("research", 99),),
            )

    def test_frozen_model(self) -> None:
        policy = build_human_loop_policy(
            tenant_id="t1", name="Frozen", source_id="src1"
        )
        with pytest.raises(Exception):
            policy.never_auto_external = False  # type: ignore[misc]


# ---------------------------------------------------------------------------
# requires_human_approval decision function
# ---------------------------------------------------------------------------


class TestRequiresHumanApproval:
    """The central decision function enforces safety consistently."""

    def test_external_always_requires_approval(self) -> None:
        """External actions ALWAYS require approval, even in AUTONOMOUS mode."""
        policy = build_human_loop_policy(
            tenant_id="t1",
            name="Autonomous",
            source_id="src1",
            mode=HumanLoopMode.AUTONOMOUS,
            auto_approve_internal=True,
        )
        assert requires_human_approval(
            policy,
            action_type="send_email",
            risk_level=RiskLevel.LOW,
            confidence=0.99,
            is_external=True,
        )

    def test_full_approval_always_requires(self) -> None:
        policy = build_human_loop_policy(
            tenant_id="t1",
            name="Full",
            source_id="src1",
            mode=HumanLoopMode.FULL_APPROVAL,
        )
        assert requires_human_approval(
            policy,
            action_type="research",
            risk_level=RiskLevel.LOW,
            confidence=0.99,
            is_external=False,
        )

    def test_smart_approval_with_auto_internal(self) -> None:
        policy = build_human_loop_policy(
            tenant_id="t1",
            name="Smart Auto",
            source_id="src1",
            mode=HumanLoopMode.SMART_APPROVAL,
            auto_approve_internal=True,
        )
        # Internal low-risk → no approval needed
        assert not requires_human_approval(
            policy,
            action_type="research",
            risk_level=RiskLevel.LOW,
            confidence=0.8,
            is_external=False,
        )

    def test_smart_approval_without_auto_internal(self) -> None:
        policy = build_human_loop_policy(
            tenant_id="t1",
            name="Smart Manual",
            source_id="src1",
            mode=HumanLoopMode.SMART_APPROVAL,
            auto_approve_internal=False,
        )
        # Without auto_approve_internal → always needs approval
        assert requires_human_approval(
            policy,
            action_type="research",
            risk_level=RiskLevel.LOW,
            confidence=0.8,
            is_external=False,
        )

    def test_notify_and_proceed_internal(self) -> None:
        policy = build_human_loop_policy(
            tenant_id="t1",
            name="Notify",
            source_id="src1",
            mode=HumanLoopMode.NOTIFY_AND_PROCEED,
        )
        assert not requires_human_approval(
            policy,
            action_type="research",
            risk_level=RiskLevel.LOW,
            confidence=0.8,
            is_external=False,
        )

    def test_notify_and_proceed_external(self) -> None:
        """Even NOTIFY mode requires approval for external actions."""
        policy = build_human_loop_policy(
            tenant_id="t1",
            name="Notify",
            source_id="src1",
            mode=HumanLoopMode.NOTIFY_AND_PROCEED,
        )
        assert requires_human_approval(
            policy,
            action_type="send_external",
            risk_level=RiskLevel.LOW,
            confidence=0.99,
            is_external=True,
        )

    def test_autonomous_internal(self) -> None:
        policy = build_human_loop_policy(
            tenant_id="t1",
            name="Auto",
            source_id="src1",
            mode=HumanLoopMode.AUTONOMOUS,
        )
        assert not requires_human_approval(
            policy,
            action_type="internal_update",
            risk_level=RiskLevel.LOW,
            confidence=0.9,
            is_external=False,
        )

    def test_high_risk_triggers_approval(self) -> None:
        policy = build_human_loop_policy(
            tenant_id="t1",
            name="Risk Aware",
            source_id="src1",
            mode=HumanLoopMode.AUTONOMOUS,
            max_autonomous_risk=RiskLevel.LOW,
        )
        # MEDIUM risk exceeds LOW threshold → needs approval
        assert requires_human_approval(
            policy,
            action_type="qualify",
            risk_level=RiskLevel.MEDIUM,
            confidence=0.9,
            is_external=False,
        )

    def test_low_confidence_escalation(self) -> None:
        policy = build_human_loop_policy(
            tenant_id="t1",
            name="Confidence Watch",
            source_id="src1",
            mode=HumanLoopMode.AUTONOMOUS,
            escalation_rules=(
                EscalationRule(
                    trigger=EscalationTrigger.LOW_CONFIDENCE,
                    threshold=0.5,
                ),
            ),
        )
        # Confidence 0.3 < threshold 0.5 → escalate
        assert requires_human_approval(
            policy,
            action_type="research",
            risk_level=RiskLevel.LOW,
            confidence=0.3,
            is_external=False,
        )
        # Confidence 0.7 > threshold 0.5 → no escalation
        assert not requires_human_approval(
            policy,
            action_type="research",
            risk_level=RiskLevel.LOW,
            confidence=0.7,
            is_external=False,
        )

    def test_first_contact_escalation(self) -> None:
        policy = build_human_loop_policy(
            tenant_id="t1",
            name="First Contact Policy",
            source_id="src1",
            mode=HumanLoopMode.AUTONOMOUS,
            escalation_rules=(
                EscalationRule(
                    trigger=EscalationTrigger.FIRST_CONTACT,
                    threshold=1.0,
                ),
            ),
        )
        # First contact → escalate
        assert requires_human_approval(
            policy,
            action_type="outreach",
            risk_level=RiskLevel.LOW,
            confidence=0.9,
            is_external=False,
            is_first_contact=True,
        )
        # Not first contact → no escalation
        assert not requires_human_approval(
            policy,
            action_type="outreach",
            risk_level=RiskLevel.LOW,
            confidence=0.9,
            is_external=False,
            is_first_contact=False,
        )


# ---------------------------------------------------------------------------
# State machine
# ---------------------------------------------------------------------------


class TestHumanLoopPolicyTransitions:
    """Transition helpers enforce the policy lifecycle."""

    def test_valid_transitions_from_draft(self) -> None:
        valid = valid_policy_transitions_from(HumanLoopPolicyStatus.DRAFT)
        assert HumanLoopPolicyStatus.ACTIVE in valid
        assert HumanLoopPolicyStatus.SUSPENDED in valid

    def test_valid_transitions_from_active(self) -> None:
        valid = valid_policy_transitions_from(HumanLoopPolicyStatus.ACTIVE)
        assert HumanLoopPolicyStatus.UNDER_REVIEW in valid
        assert HumanLoopPolicyStatus.SUSPENDED in valid

    def test_suspended_can_reactivate(self) -> None:
        valid = valid_policy_transitions_from(HumanLoopPolicyStatus.SUSPENDED)
        assert HumanLoopPolicyStatus.ACTIVE in valid

    def test_transition_draft_to_active(self) -> None:
        policy = build_human_loop_policy(
            tenant_id="t1", name="Activate", source_id="src1"
        )
        active = transition_policy(policy, to_status=HumanLoopPolicyStatus.ACTIVE)
        assert active.status == HumanLoopPolicyStatus.ACTIVE
        assert active.policy_id == policy.policy_id

    def test_invalid_transition_raises(self) -> None:
        policy = build_human_loop_policy(
            tenant_id="t1", name="Invalid", source_id="src1"
        )
        with pytest.raises(ValueError, match="invalid human loop policy transition"):
            transition_policy(policy, to_status=HumanLoopPolicyStatus.UNDER_REVIEW)

    def test_full_lifecycle(self) -> None:
        policy = build_human_loop_policy(
            tenant_id="t1", name="Lifecycle", source_id="src1"
        )
        policy = transition_policy(policy, to_status=HumanLoopPolicyStatus.ACTIVE)
        policy = transition_policy(policy, to_status=HumanLoopPolicyStatus.UNDER_REVIEW)
        policy = transition_policy(policy, to_status=HumanLoopPolicyStatus.ACTIVE)
        policy = transition_policy(policy, to_status=HumanLoopPolicyStatus.SUSPENDED)
        policy = transition_policy(policy, to_status=HumanLoopPolicyStatus.ACTIVE)
        assert policy.status == HumanLoopPolicyStatus.ACTIVE

    def test_is_valid_transition_helper(self) -> None:
        assert is_valid_policy_transition(
            HumanLoopPolicyStatus.DRAFT, HumanLoopPolicyStatus.ACTIVE
        )
        assert not is_valid_policy_transition(
            HumanLoopPolicyStatus.DRAFT, HumanLoopPolicyStatus.UNDER_REVIEW
        )


# ---------------------------------------------------------------------------
# ID preservation
# ---------------------------------------------------------------------------


class TestPolicyIdPreservation:
    """Deterministic IDs survive model_validate round-trips."""

    def test_id_stable_across_transitions(self) -> None:
        policy = build_human_loop_policy(
            tenant_id="t1", name="Stable", source_id="src1"
        )
        original_id = policy.policy_id
        active = transition_policy(policy, to_status=HumanLoopPolicyStatus.ACTIVE)
        assert active.policy_id == original_id
        suspended = transition_policy(active, to_status=HumanLoopPolicyStatus.SUSPENDED)
        assert suspended.policy_id == original_id
        reactivated = transition_policy(
            suspended, to_status=HumanLoopPolicyStatus.ACTIVE
        )
        assert reactivated.policy_id == original_id
