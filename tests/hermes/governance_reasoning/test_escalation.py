"""Escalation tickets are appended to a ledger and assigned approval_ids."""

from __future__ import annotations

from dealix.hermes.governance_reasoning.escalation import escalate, list_pending


def test_escalate_creates_ticket_and_appends_to_ledger() -> None:
    ticket = escalate("publish_pricing", actor="agent.marketing", reason="founder-approval", context={"sensitivity": 4})
    assert ticket.approval_id.startswith("esc_")
    pending = list_pending()
    assert any(p.approval_id == ticket.approval_id for p in pending)
