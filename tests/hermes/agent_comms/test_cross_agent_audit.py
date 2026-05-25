"""Agent-to-agent messages are appended to the audit ledger."""

from __future__ import annotations

from dealix.hermes.agent_comms.cross_agent_audit import list_messages, record


def test_record_appends_message_to_ledger() -> None:
    rec = record("agent.sales", "agent.delivery", "handoff", {"deal_id": "d_1"})
    msgs = list_messages()
    assert rec.message_id in {m.message_id for m in msgs}
    assert msgs[-1].intent == "handoff"
