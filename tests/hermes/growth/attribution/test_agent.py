"""Agent attribution tracks revenue contributed by a specific agent."""

from __future__ import annotations

from dealix.hermes.growth.attribution import _base, agent


def test_agent_attribution() -> None:
    _base.reset()
    agent.attribute("agent.sales", 30_000, evidence_pack_id="ep_1")
    assert agent.total("agent.sales") == 30_000
