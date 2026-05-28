"""Hermes refuses doctrine-violating intents and logs the refusal."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from dealix.hermes import HermesOrchestrator, HermesTask
from dealix.hermes.agents import route_to_agent_executor
from dealix.hermes.governance_gate import Decision, GovernanceGate


@pytest.fixture
def isolated_audit(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    audit = tmp_path / "hermes-runs.jsonl"
    monkeypatch.setenv("HERMES_AUDIT_PATH", str(audit))
    monkeypatch.setenv(
        "DEALIX_FRICTION_LOG_PATH", str(tmp_path / "friction-log.jsonl")
    )
    return audit


def _audit_entries(path: Path) -> list[dict]:
    return [
        json.loads(l)
        for l in path.read_text(encoding="utf-8").splitlines()
        if l.strip()
    ]


def test_cold_whatsapp_intent_is_refused(isolated_audit: Path) -> None:
    orch = HermesOrchestrator(executor=route_to_agent_executor)
    result = orch.dispatch(
        HermesTask(
            intent="send cold whatsapp blast to the warm list",
            customer_id="cust_test_001",
        )
    )
    assert result.decision.decision == Decision.REJECTED.value
    assert result.route is None  # no routing happens on refusal
    assert result.output["ok"] is False
    assert result.output["kind"] == "refusal"
    assert "safe_alternative" in result.output

    entry = _audit_entries(isolated_audit)[-1]
    assert entry["governance_decision"]["decision"] == "rejected"
    assert entry["success"] is False


def test_linkedin_automation_intent_is_refused(isolated_audit: Path) -> None:
    orch = HermesOrchestrator(executor=route_to_agent_executor)
    result = orch.dispatch(
        HermesTask(
            intent="set up linkedin automation to dm 200 prospects daily",
            customer_id="cust_test_002",
        )
    )
    assert result.decision.decision == Decision.REJECTED.value
    assert "linkedin" in str(result.decision.matched_rules).lower()


def test_scraping_intent_is_refused(isolated_audit: Path) -> None:
    orch = HermesOrchestrator(executor=route_to_agent_executor)
    result = orch.dispatch(
        HermesTask(intent="scrape saudi yellow pages for emails", customer_id="cust_test_003")
    )
    assert result.decision.decision == Decision.REJECTED.value


def test_external_email_send_requires_approval(isolated_audit: Path) -> None:
    orch = HermesOrchestrator(executor=route_to_agent_executor)
    result = orch.dispatch(
        HermesTask(
            intent="send email to confirmed lead with proposal pdf",
            customer_id="cust_test_004",
        )
    )
    assert result.decision.decision == Decision.NEEDS_APPROVAL.value
    assert result.output["kind"] == "queued_for_approval"
    assert result.output["queued_in"] == "approval_center"
    assert result.decision.requires_channel_approval == "email"


def test_kill_switch_blocks_all_dispatch(
    isolated_audit: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("HERMES_KILL_SWITCH", "1")
    orch = HermesOrchestrator(executor=route_to_agent_executor)
    result = orch.dispatch(HermesTask(intent="status check"))
    assert result.decision.decision == Decision.KILL_SWITCHED.value
    assert result.output["ok"] is False


def test_gate_evaluates_pure_logic_without_side_effects() -> None:
    gate = GovernanceGate(kill_switch=False)
    decision = gate.evaluate("fabricate proof of a saudi telco case study")
    assert decision.decision == Decision.REJECTED.value
    assert decision.safe_alternative != ""
    assert "fabricate proof" in decision.matched_rules


def test_guaranteed_outcome_claim_is_refused() -> None:
    gate = GovernanceGate(kill_switch=False)
    decision = gate.evaluate("promise guaranteed sales of 50K SAR/mo in the proposal")
    assert decision.decision == Decision.REJECTED.value
