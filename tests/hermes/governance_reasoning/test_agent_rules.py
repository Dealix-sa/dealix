"""Agent rules enforce capability scope and autonomy ceiling."""

from __future__ import annotations

from dealix.hermes.governance_reasoning.agent_rules import AgentCapabilities, clear, evaluate, register_agent


def test_agent_rules_enforce_capability_and_autonomy() -> None:
    clear()
    register_agent(AgentCapabilities(agent_id="agent.sales", capabilities=frozenset({"draft_proposal"}), max_autonomy_level=1))
    assert evaluate("agent.sales", "draft_proposal", required_autonomy=1).allowed is True
    assert evaluate("agent.sales", "send_email", required_autonomy=1).allowed is False
    assert evaluate("agent.sales", "draft_proposal", required_autonomy=2).allowed is False
