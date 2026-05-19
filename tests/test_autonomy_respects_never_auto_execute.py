"""Guard: NEVER_AUTO_EXECUTE actions can never be auto-approved.

Constitution Art. V.3 — any action in ``NEVER_AUTO_EXECUTE`` requires
executive approval irrespective of other signals. This test proves the
founder-rule auto-approval path honours that even against a deliberately
permissive wildcard rule and a mislabelled ``risk_level="low"``.
"""
from __future__ import annotations

import os
from pathlib import Path
from unittest.mock import patch

import pytest

from auto_client_acquisition.approval_center.founder_rules import FounderRuleEngine
from auto_client_acquisition.approval_center.founder_rules_integration import (
    try_auto_approve_via_founder_rule,
)
from auto_client_acquisition.approval_center.schemas import (
    ApprovalRequest,
    ApprovalStatus,
)
from dealix.classifications import NEVER_AUTO_EXECUTE


@pytest.fixture
def wildcard_engine(tmp_path: Path):
    """An engine with a maximally-permissive signed rule: any email
    action, any customer, any content, zero confidence floor."""
    rules_p = tmp_path / "active_rules.jsonl"
    audit_p = tmp_path / "rule_match_audit.jsonl"
    with patch.dict(os.environ, {"DEALIX_FOUNDER_RULES_SECRET": "test-secret-12345"}):
        engine = FounderRuleEngine(rules_path=rules_p, audit_path=audit_p)
        rule = engine.create_rule(
            name="auto-approve everything on email",
            channel="email",
            customer_handle="*",
            action_type="*",
            max_risk_level="low",
            min_confidence=0.0,
        )
        engine.append_rule(rule)
        yield engine


def _request(action_type: str) -> ApprovalRequest:
    """A request the wildcard rule WOULD match if the action were allowed:
    email channel, low risk, awaiting approval."""
    return ApprovalRequest(
        object_type="lead",
        object_id="lead:acme-real-estate-001",
        action_type=action_type,
        action_mode="approval_required",
        channel="email",
        risk_level="low",
    )


def test_wildcard_rule_auto_approves_an_ordinary_action(
    wildcard_engine: FounderRuleEngine,
) -> None:
    """Positive control — the wildcard rule genuinely auto-approves a
    non-NEVER_AUTO_EXECUTE action, so the negative tests below isolate
    the NEVER_AUTO_EXECUTE block as the cause of refusal."""
    req = _request("draft_email")
    result = try_auto_approve_via_founder_rule(req, engine=wildcard_engine)
    assert ApprovalStatus(result.status) == ApprovalStatus.APPROVED


@pytest.mark.parametrize("action_type", sorted(NEVER_AUTO_EXECUTE))
def test_never_auto_execute_action_is_not_auto_approved(
    wildcard_engine: FounderRuleEngine, action_type: str
) -> None:
    """Every NEVER_AUTO_EXECUTE action stays PENDING even when a
    permissive wildcard rule and a low risk label would otherwise match."""
    req = _request(action_type)
    result = try_auto_approve_via_founder_rule(req, engine=wildcard_engine)
    assert ApprovalStatus(result.status) == ApprovalStatus.PENDING
    assert result.action_mode == "approval_required"


@pytest.mark.parametrize("action_type", sorted(NEVER_AUTO_EXECUTE))
def test_engine_match_returns_none_for_never_auto_execute(
    wildcard_engine: FounderRuleEngine, action_type: str
) -> None:
    """The rule engine itself refuses to match a NEVER_AUTO_EXECUTE
    action — defence in depth below the integration layer."""
    req = _request(action_type)
    assert wildcard_engine.match(req, confidence=1.0) is None
