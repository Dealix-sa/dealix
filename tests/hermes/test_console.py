"""Sovereign Console snapshot composition test."""

from __future__ import annotations

from dealix.hermes import ValueOutput
from dealix.hermes.console import render_console
from dealix.hermes.core.schemas import OpportunityKind, SignalSource
from dealix.hermes.orchestrator import HermesOrchestrator
from dealix.hermes.sovereignty import Action, SovereigntyLevel


def test_console_returns_required_top_level_keys():
    orch = HermesOrchestrator()
    snap = render_console(orch)
    assert {"command", "money", "trust", "doctrine_rules_ar"} <= snap.keys()
    assert isinstance(snap["doctrine_rules_ar"], list) and snap["doctrine_rules_ar"]


def test_console_surfaces_pending_approvals_and_top_opportunity():
    orch = HermesOrchestrator()
    s = orch.intake.capture(
        source=SignalSource.FOUNDER_NOTE,
        title="Pilot lead",
        summary="Founder warm intro",
        captured_by="sami",
    )
    orch.opportunities.register(
        source_signals=[s],
        kind=OpportunityKind.DIRECT_DEAL,
        title="Pilot — Agency A",
        buyer_segment="agency",
        estimated_value_sar=4999,
        close_probability=0.7,
        fit_score=0.8,
        urgency_score=0.7,
        risk_score=0.2,
        proposed_value_outputs=[ValueOutput.MONEY],
    )
    # propose an action that requires approval
    orch.propose(
        Action(
            action_type="send_external_message",
            payload={"to": "founder@example.sa"},
            proposed_by="followup_agent",
            sovereignty_level=SovereigntyLevel.S0_AUTONOMOUS,
        )
    )
    snap = render_console(orch)
    assert snap["command"]["top_strategic_opportunity"] is not None
    assert snap["command"]["sovereign_approval_required"], "send_external_message must queue approval"
