"""The auto-execute-outbound action class is blocked at the policy layer."""
from __future__ import annotations

from control_plane.action_router import ActionRouter
from control_plane.decision_engine import Decision
from dealix.trust.approval_matrix import ApprovalMatrix
from dealix.trust.autonomy_policy import evaluate as autonomy_evaluate


def test_approval_matrix_blocks_auto_outbound():
    matrix = ApprovalMatrix.from_register()
    assert matrix.is_blocked("auto_send_external_outbound")


def test_autonomy_policy_blocks_send_external():
    decision = autonomy_evaluate("send_external_message")
    assert decision.allowed is False


def test_action_router_blocks_doctrine_violation():
    router = ActionRouter()
    bad_decision = Decision(
        label="auto_send_external_outbound to whole list",
        rationale="should never run",
        approval_class="auto",
    )
    result = router.route(bad_decision)
    assert result.destination == "blocked"


def test_action_router_routes_founder_classes_to_queue():
    router = ActionRouter()
    d = Decision(label="send proposal to acme", rationale="x", approval_class="founder")
    assert router.route(d).destination == "approval_queue"
