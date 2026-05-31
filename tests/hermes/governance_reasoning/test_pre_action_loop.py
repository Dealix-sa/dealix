"""PAGRL decision blocks PII-to-external and escalates sensitive workflows."""

from __future__ import annotations

from dealix.hermes.governance_reasoning import agent_rules, workflow_rules
from dealix.hermes.governance_reasoning.pre_action_loop import decide


def setup_function() -> None:  # noqa: D401
    workflow_rules.clear()
    agent_rules.clear()
    agent_rules.register_agent(
        agent_rules.AgentCapabilities(
            agent_id="agent.sales",
            capabilities=frozenset({"draft_proposal"}),
            max_autonomy_level=2,
        )
    )


def test_pagrl_blocks_pii_to_external() -> None:
    d = decide(action="draft_proposal", actor="agent.sales", workflow_id="wf_a", context={"pii": True, "target": "external"})
    assert d.decision == "block"


def test_pagrl_escalates_sensitive_context() -> None:
    d = decide(
        action="draft_proposal",
        actor="agent.sales",
        workflow_id="wf_a",
        context={"sensitivity": 4, "magnitude": 1, "irreversibility": 1},
    )
    assert d.decision == "escalate"
    assert d.approval_id is not None
