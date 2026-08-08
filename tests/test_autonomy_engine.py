"""Tests for the Autonomy & Approval Engine.

Covers action evaluation, auto-approval logic, escalation, risk
classification, and the non-negotiable external-action safety invariant.
"""
from __future__ import annotations

import pytest

from dealix.company_intelligence.action_contracts import (
    ActionType,
    AutonomyLevel,
    RiskLevel,
    build_action,
)
from dealix.company_intelligence.autonomy_engine import (
    ActionEvaluation,
    AutonomyDecisionType,
    EscalationReason,
    can_auto_execute,
    classify_risk,
    evaluate_action,
)
from dealix.company_intelligence.human_loop_contracts import (
    EscalationRule,
    EscalationTrigger,
    HumanLoopMode,
    build_human_loop_policy,
)

TENANT = "tenant_test_autonomy"
SOURCE = "test_source"


def _make_action(**overrides):
    defaults = {
        "tenant_id": TENANT,
        "idempotency_key": "test_action_001",
        "action_type": ActionType.INTERNAL_UPDATE,
        "department": "operations",
        "autonomy_level": AutonomyLevel.L2_DRAFT,
        "risk_level": RiskLevel.LOW,
        "approval_required": True,
        "external_effect": False,
    }
    defaults.update(overrides)
    return build_action(**defaults)


def _make_policy(**overrides):
    defaults = {
        "tenant_id": TENANT,
        "name": "default_policy",
        "source_id": SOURCE,
        "mode": HumanLoopMode.SMART_APPROVAL,
        "auto_approve_internal": True,
    }
    defaults.update(overrides)
    return build_human_loop_policy(**defaults)


# -----------------------------------------------------------------------
# Action evaluation basics
# -----------------------------------------------------------------------


class TestActionEvaluation:
    def test_evaluate_internal_low_risk(self):
        action = _make_action()
        policy = _make_policy()
        evaluation = evaluate_action(action, policy, source_id=SOURCE)
        assert isinstance(evaluation, ActionEvaluation)
        assert evaluation.tenant_id == TENANT
        assert evaluation.action_id == action.action_id
        assert evaluation.policy_id == policy.policy_id
        assert evaluation.decision == AutonomyDecisionType.AUTO_APPROVE

    def test_deterministic_id(self):
        action = _make_action()
        policy = _make_policy()
        e1 = evaluate_action(action, policy, source_id=SOURCE)
        e2 = evaluate_action(action, policy, source_id=SOURCE)
        assert e1.evaluation_id == e2.evaluation_id
        assert e1.evaluation_id.startswith("autoeval_")

    def test_reasoning_populated(self):
        action = _make_action()
        policy = _make_policy()
        evaluation = evaluate_action(action, policy, source_id=SOURCE)
        assert evaluation.reasoning != ""
        assert "auto-approved" in evaluation.reasoning


# -----------------------------------------------------------------------
# External action safety — NON-NEGOTIABLE
# -----------------------------------------------------------------------


class TestExternalActionSafety:
    def test_external_never_auto_approved(self):
        """External actions ALWAYS need human approval."""
        action = _make_action(
            idempotency_key="external_001",
            action_type=ActionType.SEND_EXTERNAL,
            autonomy_level=AutonomyLevel.L4_CONTROLLED_EXECUTE,
            external_effect=True,
        )
        # Even the most permissive policy cannot auto-approve
        policy = _make_policy(mode=HumanLoopMode.AUTONOMOUS)
        evaluation = evaluate_action(action, policy, source_id=SOURCE)
        assert evaluation.decision != AutonomyDecisionType.AUTO_APPROVE
        assert evaluation.is_external is True
        assert EscalationReason.EXTERNAL_ACTION in evaluation.escalation_reasons

    def test_external_with_high_risk_escalates(self):
        action = _make_action(
            idempotency_key="ext_high_risk",
            action_type=ActionType.SEND_EXTERNAL,
            autonomy_level=AutonomyLevel.L4_CONTROLLED_EXECUTE,
            external_effect=True,
            risk_level=RiskLevel.HIGH,
        )
        policy = _make_policy()
        evaluation = evaluate_action(action, policy, source_id=SOURCE)
        assert evaluation.decision == AutonomyDecisionType.ESCALATE

    def test_cannot_construct_external_auto_approve(self):
        """Model validator prevents external + auto_approve."""
        action = _make_action()
        policy = _make_policy()
        evaluation = evaluate_action(action, policy, source_id=SOURCE)

        with pytest.raises(ValueError, match="external.*cannot be auto-approved"):
            ActionEvaluation(
                tenant_id=TENANT,
                evaluation_id=evaluation.evaluation_id,
                action_id=action.action_id,
                action_type=ActionType.SEND_EXTERNAL,
                policy_id=policy.policy_id,
                decision=AutonomyDecisionType.AUTO_APPROVE,
                autonomy_level_required=AutonomyLevel.L4_CONTROLLED_EXECUTE,
                autonomy_level_granted=AutonomyLevel.L4_CONTROLLED_EXECUTE,
                is_external=True,
                reasoning="test",
                policy_mode=HumanLoopMode.AUTONOMOUS,
                source_id=SOURCE,
            )


# -----------------------------------------------------------------------
# Policy modes
# -----------------------------------------------------------------------


class TestPolicyModes:
    def test_full_approval_queues_everything(self):
        action = _make_action(idempotency_key="full_001")
        policy = _make_policy(
            name="full_approval_policy",
            mode=HumanLoopMode.FULL_APPROVAL,
        )
        evaluation = evaluate_action(action, policy, source_id=SOURCE)
        assert evaluation.decision == AutonomyDecisionType.QUEUE_FOR_APPROVAL

    def test_smart_approval_auto_approves_internal(self):
        action = _make_action(idempotency_key="smart_001")
        policy = _make_policy(
            name="smart_policy",
            mode=HumanLoopMode.SMART_APPROVAL,
            auto_approve_internal=True,
        )
        evaluation = evaluate_action(action, policy, source_id=SOURCE)
        assert evaluation.decision == AutonomyDecisionType.AUTO_APPROVE

    def test_smart_approval_without_auto_queues(self):
        action = _make_action(idempotency_key="smart_002")
        policy = _make_policy(
            name="smart_strict",
            mode=HumanLoopMode.SMART_APPROVAL,
            auto_approve_internal=False,
        )
        evaluation = evaluate_action(action, policy, source_id=SOURCE)
        assert evaluation.decision == AutonomyDecisionType.QUEUE_FOR_APPROVAL

    def test_notify_and_proceed_auto_approves_internal(self):
        action = _make_action(idempotency_key="notify_001")
        policy = _make_policy(
            name="notify_policy",
            mode=HumanLoopMode.NOTIFY_AND_PROCEED,
        )
        evaluation = evaluate_action(action, policy, source_id=SOURCE)
        assert evaluation.decision == AutonomyDecisionType.AUTO_APPROVE

    def test_autonomous_auto_approves_internal(self):
        action = _make_action(idempotency_key="auto_001")
        policy = _make_policy(
            name="autonomous_policy",
            mode=HumanLoopMode.AUTONOMOUS,
        )
        evaluation = evaluate_action(action, policy, source_id=SOURCE)
        assert evaluation.decision == AutonomyDecisionType.AUTO_APPROVE


# -----------------------------------------------------------------------
# Risk-based escalation
# -----------------------------------------------------------------------


class TestRiskEscalation:
    def test_high_risk_escalates(self):
        action = _make_action(
            idempotency_key="high_risk_001",
            risk_level=RiskLevel.HIGH,
        )
        policy = _make_policy()
        evaluation = evaluate_action(action, policy, source_id=SOURCE)
        assert evaluation.decision == AutonomyDecisionType.ESCALATE
        assert EscalationReason.HIGH_RISK in evaluation.escalation_reasons

    def test_critical_risk_escalates(self):
        action = _make_action(
            idempotency_key="critical_001",
            risk_level=RiskLevel.CRITICAL,
        )
        policy = _make_policy()
        evaluation = evaluate_action(action, policy, source_id=SOURCE)
        assert evaluation.decision == AutonomyDecisionType.ESCALATE

    def test_cannot_auto_approve_high_risk(self):
        """Model validator prevents high risk auto-approve."""
        action = _make_action()
        policy = _make_policy()
        evaluation = evaluate_action(action, policy, source_id=SOURCE)

        with pytest.raises(ValueError, match="high/critical.*cannot be auto"):
            ActionEvaluation(
                tenant_id=TENANT,
                evaluation_id=evaluation.evaluation_id,
                action_id=action.action_id,
                action_type=ActionType.INTERNAL_UPDATE,
                policy_id=policy.policy_id,
                decision=AutonomyDecisionType.AUTO_APPROVE,
                autonomy_level_required=AutonomyLevel.L2_DRAFT,
                autonomy_level_granted=AutonomyLevel.L2_DRAFT,
                risk_level=RiskLevel.HIGH,
                reasoning="test",
                policy_mode=HumanLoopMode.AUTONOMOUS,
                source_id=SOURCE,
            )


# -----------------------------------------------------------------------
# Escalation rules
# -----------------------------------------------------------------------


class TestEscalationRules:
    def test_low_confidence_triggers_escalation(self):
        action = _make_action(
            idempotency_key="low_conf_001",
            confidence=0.2,
        )
        policy = _make_policy(
            name="conf_policy",
            escalation_rules=(
                EscalationRule(
                    trigger=EscalationTrigger.LOW_CONFIDENCE,
                    threshold=0.5,
                ),
            ),
        )
        evaluation = evaluate_action(action, policy, source_id=SOURCE)
        assert EscalationReason.LOW_CONFIDENCE in evaluation.escalation_reasons
        assert len(evaluation.triggered_rules) > 0

    def test_first_contact_escalation(self):
        action = _make_action(idempotency_key="first_001")
        policy = _make_policy(
            name="first_contact_policy",
            escalation_rules=(
                EscalationRule(
                    trigger=EscalationTrigger.FIRST_CONTACT,
                    threshold=0.0,
                ),
            ),
        )
        evaluation = evaluate_action(
            action, policy,
            source_id=SOURCE,
            is_first_contact=True,
        )
        assert EscalationReason.FIRST_CONTACT in evaluation.escalation_reasons

    def test_high_value_escalation(self):
        action = _make_action(
            idempotency_key="high_val_001",
            impact=0.9,
        )
        policy = _make_policy(
            name="high_value_policy",
            escalation_rules=(
                EscalationRule(
                    trigger=EscalationTrigger.HIGH_VALUE,
                    threshold=0.8,
                ),
            ),
        )
        evaluation = evaluate_action(action, policy, source_id=SOURCE)
        assert EscalationReason.HIGH_VALUE in evaluation.escalation_reasons


# -----------------------------------------------------------------------
# can_auto_execute shortcut
# -----------------------------------------------------------------------


class TestCanAutoExecute:
    def test_internal_low_risk_can_auto(self):
        action = _make_action()
        policy = _make_policy(
            mode=HumanLoopMode.NOTIFY_AND_PROCEED,
        )
        assert can_auto_execute(action, policy) is True

    def test_external_cannot_auto(self):
        action = _make_action(
            idempotency_key="ext_auto",
            action_type=ActionType.SEND_EXTERNAL,
            autonomy_level=AutonomyLevel.L4_CONTROLLED_EXECUTE,
            external_effect=True,
        )
        policy = _make_policy(mode=HumanLoopMode.AUTONOMOUS)
        assert can_auto_execute(action, policy) is False

    def test_high_risk_cannot_auto(self):
        action = _make_action(
            idempotency_key="risk_auto",
            risk_level=RiskLevel.HIGH,
        )
        policy = _make_policy(mode=HumanLoopMode.AUTONOMOUS)
        assert can_auto_execute(action, policy) is False


# -----------------------------------------------------------------------
# Risk classification
# -----------------------------------------------------------------------


class TestRiskClassification:
    def test_external_send_is_critical(self):
        risk = classify_risk(
            is_external=True,
            autonomy_level=AutonomyLevel.L4_CONTROLLED_EXECUTE,
            action_type=ActionType.SEND_EXTERNAL,
            confidence=0.9,
        )
        assert risk == RiskLevel.CRITICAL

    def test_invoice_is_critical(self):
        risk = classify_risk(
            is_external=True,
            autonomy_level=AutonomyLevel.L4_CONTROLLED_EXECUTE,
            action_type=ActionType.INVOICE_REQUEST,
            confidence=0.9,
        )
        assert risk == RiskLevel.CRITICAL

    def test_external_non_send_is_high(self):
        risk = classify_risk(
            is_external=True,
            autonomy_level=AutonomyLevel.L4_CONTROLLED_EXECUTE,
            action_type=ActionType.RESEARCH,
            confidence=0.9,
        )
        assert risk == RiskLevel.HIGH

    def test_l5_is_high(self):
        risk = classify_risk(
            is_external=False,
            autonomy_level=AutonomyLevel.L5_SENSITIVE_EXECUTE,
            action_type=ActionType.INTERNAL_UPDATE,
            confidence=0.9,
        )
        assert risk == RiskLevel.HIGH

    def test_low_confidence_is_medium(self):
        risk = classify_risk(
            is_external=False,
            autonomy_level=AutonomyLevel.L2_DRAFT,
            action_type=ActionType.RESEARCH,
            confidence=0.2,
        )
        assert risk == RiskLevel.MEDIUM

    def test_internal_low_level_high_confidence_is_low(self):
        risk = classify_risk(
            is_external=False,
            autonomy_level=AutonomyLevel.L2_DRAFT,
            action_type=ActionType.RESEARCH,
            confidence=0.9,
        )
        assert risk == RiskLevel.LOW


# -----------------------------------------------------------------------
# Notification and timeout
# -----------------------------------------------------------------------


class TestNotificationRouting:
    def test_evaluation_captures_policy_timeout(self):
        action = _make_action()
        policy = _make_policy(
            name="timeout_policy",
            response_timeout_minutes=120,
            notification_channels=("whatsapp", "email"),
        )
        evaluation = evaluate_action(action, policy, source_id=SOURCE)
        assert evaluation.approval_timeout_minutes == 120
        assert "whatsapp" in evaluation.notification_channels
        assert "email" in evaluation.notification_channels
