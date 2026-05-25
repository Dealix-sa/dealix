"""An agent cannot delegate a capability it does not itself hold."""

from __future__ import annotations

from dealix.hermes.agent_comms.delegation_policy import Agent, can_delegate, delegate


def test_cannot_delegate_outside_capabilities() -> None:
    coordinator = Agent(agent_id="agent.coordinator", capabilities=frozenset({"plan"}))
    worker = Agent(agent_id="agent.worker", capabilities=frozenset({"plan", "send_email"}))
    assert can_delegate(coordinator, "send_email") is False
    result = delegate(coordinator, worker, "send_email")
    assert result.allowed is False
    assert "coordinator" in result.reason
