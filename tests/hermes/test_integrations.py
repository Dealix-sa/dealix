"""Hermes ↔ approval_center + capital_ledger integration bridges.

These tests exercise the inference + decision logic without touching the
heavy approval_store / capital_ledger modules (which are imported lazily
inside the bridges; absence is a no-op).
"""
from __future__ import annotations

from dealix.hermes.audit import HermesAuditRecord
from dealix.hermes.governance_gate import Decision, GovernanceDecision
from dealix.hermes.integrations import (
    _infer_asset_type,
    bridge_to_approval_center,
    bridge_to_capital_ledger,
    daily_cost_budget_usd,
)


def _record(customer_id: str = "cust_123", sub_agent: str = "dealix-delivery") -> HermesAuditRecord:
    return HermesAuditRecord(
        run_id="hermes_test_001",
        agent_id="hermes",
        task_class="delivery",
        customer_id=customer_id,
        intent_summary="produce a proof pack for ACME",
        governance_decision={"decision": "approved"},
        sub_agent=sub_agent,
        provider="openrouter",
        model_id="deepseek/deepseek-chat",
    )


def test_infer_asset_type_matches_known_phrases() -> None:
    assert _infer_asset_type("draft a scoring rule for warm-list") == "scoring_rule"
    assert _infer_asset_type("Use the standard draft template") == "draft_template"
    assert _infer_asset_type("ASSEMBLE THE PROOF PACK") == "proof_example"
    assert _infer_asset_type("sector report for FinTech") == "sector_insight"
    assert _infer_asset_type("hello world") is None


def test_capital_bridge_skipped_for_internal_runs() -> None:
    record = _record(customer_id="dealix_internal")
    decision = GovernanceDecision(decision=Decision.APPROVED.value, reason="ok")
    result = bridge_to_capital_ledger(
        record,
        decision,
        intent="build a proof pack",
        deliverable_text="proof pack with 14 sections",
    )
    assert result is None


def test_capital_bridge_skipped_on_refusal() -> None:
    record = _record(customer_id="cust_abc")
    decision = GovernanceDecision(decision=Decision.REJECTED.value, reason="blocked")
    result = bridge_to_capital_ledger(
        record,
        decision,
        intent="something",
        deliverable_text="proof pack",
    )
    assert result is None


def test_capital_bridge_skipped_without_asset_signal() -> None:
    record = _record(customer_id="cust_abc")
    decision = GovernanceDecision(decision=Decision.APPROVED.value, reason="ok")
    # Generic intent — no asset taxonomy keyword.
    result = bridge_to_capital_ledger(
        record,
        decision,
        intent="hello",
        deliverable_text="just a chat",
    )
    assert result is None


def test_approval_bridge_skipped_for_non_approval_decision() -> None:
    record = _record(customer_id="cust_abc")
    decision = GovernanceDecision(decision=Decision.APPROVED.value, reason="ok")
    assert bridge_to_approval_center(record, decision, intent="anything") is None


def test_approval_bridge_skipped_without_customer() -> None:
    record = _record(customer_id="")
    decision = GovernanceDecision(
        decision=Decision.NEEDS_APPROVAL.value,
        reason="external send",
        requires_channel_approval="email",
    )
    assert bridge_to_approval_center(record, decision, intent="send email") is None


def test_daily_budget_defaults_to_zero(monkeypatch) -> None:
    monkeypatch.delenv("HERMES_DAILY_BUDGET_USD", raising=False)
    assert daily_cost_budget_usd() == 0.0


def test_daily_budget_respects_env(monkeypatch) -> None:
    monkeypatch.setenv("HERMES_DAILY_BUDGET_USD", "12.5")
    assert daily_cost_budget_usd() == 12.5


def test_daily_budget_handles_bad_value(monkeypatch) -> None:
    monkeypatch.setenv("HERMES_DAILY_BUDGET_USD", "not-a-number")
    assert daily_cost_budget_usd() == 0.0
