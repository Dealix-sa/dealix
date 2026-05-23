"""ActionRouter routes decisions to the right destination."""
from __future__ import annotations

from control_plane.action_router import ActionRouter
from control_plane.decision_engine import Decision


def test_auto_decision_routes_to_workflow():
    d = Decision(label="Add 10 qualified leads this week", rationale="x", approval_class="auto")
    routed = ActionRouter().route(d)
    assert routed.destination == "workflow"
    assert routed.handler.startswith("dealix.workflows.")


def test_founder_decision_routes_to_queue():
    d = Decision(label="Send proposal to acme", rationale="x", approval_class="founder")
    routed = ActionRouter().route(d)
    assert routed.destination == "approval_queue"


def test_blocked_phrase_overrides_class():
    d = Decision(label="auto_send_external_outbound campaign", rationale="x", approval_class="auto")
    routed = ActionRouter().route(d)
    assert routed.destination == "blocked"
