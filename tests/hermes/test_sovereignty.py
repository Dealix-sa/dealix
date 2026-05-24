"""Sovereignty S0..S5 enforcement."""

from __future__ import annotations

import pytest

from dealix.hermes.kernel import HermesKernel
from dealix.hermes.sovereignty.approval_rules import ApprovalRules
from dealix.hermes.sovereignty.capital_allocation import AllocationStatus, CapitalLedger
from dealix.hermes.sovereignty.classifier import SovereigntyClassifier
from dealix.hermes.sovereignty.kill_switch import KillScope, KillSwitch
from dealix.hermes.sovereignty.levels import SovereigntyLevel
from dealix.hermes.sovereignty.sovereign_memory import SovereignMemory


def test_classifier_levels():
    c = SovereigntyClassifier()
    assert c.classify("summarize_lead")[0] == SovereigntyLevel.S0_AUTO_SAFE
    assert c.classify("draft_proposal")[0] == SovereigntyLevel.S1_INTERNAL
    assert c.classify("send_email")[0] == SovereigntyLevel.S2_SAMI_APPROVAL
    assert c.classify("price_quote")[0] == SovereigntyLevel.S3_SOVEREIGN_MEMO
    assert c.classify("publish_marketplace")[0] == SovereigntyLevel.S4_SOVEREIGN_ONLY
    assert c.classify("wire_transfer")[0] == SovereigntyLevel.S5_NEVER_AUTONOMOUS
    # Unknown action defaults to S2.
    assert c.classify("totally_unknown")[0] == SovereigntyLevel.S2_SAMI_APPROVAL


def test_rules_block_s4_s5():
    rules = ApprovalRules()
    v5 = rules.evaluate(action="wire_transfer", level=SovereigntyLevel.S5_NEVER_AUTONOMOUS)
    assert not v5.allowed and not v5.auto
    v4 = rules.evaluate(action="public_api", level=SovereigntyLevel.S4_SOVEREIGN_ONLY)
    assert not v4.allowed
    v3 = rules.evaluate(action="enterprise_contract", level=SovereigntyLevel.S3_SOVEREIGN_MEMO)
    assert v3.allowed and not v3.auto and v3.requires_approver == "sami"
    v2 = rules.evaluate(action="send_email", level=SovereigntyLevel.S2_SAMI_APPROVAL)
    assert v2.allowed and not v2.auto
    v1 = rules.evaluate(action="draft_proposal", level=SovereigntyLevel.S1_INTERNAL)
    assert v1.allowed and v1.auto


def test_kill_switch_overrides_everything():
    sw = KillSwitch()
    rules = ApprovalRules(kill_switch=sw)
    sw.activate(KillScope.GLOBAL, reason="incident")
    v = rules.evaluate(action="draft_proposal", level=SovereigntyLevel.S1_INTERNAL)
    assert not v.allowed
    sw.deactivate(KillScope.GLOBAL)
    v2 = rules.evaluate(action="draft_proposal", level=SovereigntyLevel.S1_INTERNAL)
    assert v2.allowed


def test_capital_allocation_only_sovereign_disburses():
    ledger = CapitalLedger()
    alloc = ledger.propose(bucket="marketing", amount_sar=10_000, proposed_by="market_radar", rationale="seed campaign")
    with pytest.raises(PermissionError):
        ledger.approve(alloc.id, by="market_radar")
    ledger.approve(alloc.id, by="sami")
    assert alloc.status == AllocationStatus.APPROVED
    with pytest.raises(PermissionError):
        ledger.disburse(alloc.id, by="agent")
    ledger.disburse(alloc.id, by="sami")
    assert alloc.status == AllocationStatus.DISBURSED


def test_sovereign_memory_is_write_protected():
    mem = SovereignMemory()
    with pytest.raises(PermissionError):
        mem.write("strategy", "fold the company", author="market_radar")
    mem.write("strategy", "win Q1 with trust kit", author="sami", sensitive=True)
    # Agents read sensitive entries redacted.
    assert mem.read("strategy", agent_id="market_radar") == "[REDACTED]"
    assert mem.read("strategy") == "win Q1 with trust kit"


def test_decision_log_records_blocked_actions():
    k = HermesKernel()
    from dealix.hermes.core.schemas import Decision
    dec = Decision.make(
        opportunity_id="opp_x",
        action="wire_transfer",
        sovereignty_level=SovereigntyLevel.S5_NEVER_AUTONOMOUS,
        rationale="send vendor payment",
    )
    k.decisions.file(dec, domain="money")
    assert dec.status.value == "blocked"
    assert any(e.outcome == "blocked" for e in k.journal.all())
