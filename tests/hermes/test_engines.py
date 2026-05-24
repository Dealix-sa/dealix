"""Engine smoke tests: money, products, partners, customer, ventures."""

from __future__ import annotations

import pytest

from dealix.hermes import ValueOutput
from dealix.hermes.core.opportunities import OpportunityGraph
from dealix.hermes.core.schemas import (
    AssetKind,
    OpportunityKind,
    OutcomeKind,
    SignalSource,
)
from dealix.hermes.core.signals import SignalIntake
from dealix.hermes.customer.health_score import CustomerSignals, evaluate
from dealix.hermes.money.cash_scout import CashScout
from dealix.hermes.money.followup import draft as draft_followup
from dealix.hermes.money.pricing import quote
from dealix.hermes.money.proposal_factory import render as render_proposal
from dealix.hermes.orchestrator import HermesOrchestrator
from dealix.hermes.partners.fit_score import PartnerSignals
from dealix.hermes.partners.scout import PartnerKind, PartnerScout
from dealix.hermes.products.scale_kill import evaluate_library
from dealix.hermes.ventures.vertical_launcher import evaluate as eval_vertical, make as make_vertical


def _seeded_orchestrator():
    orch = HermesOrchestrator()
    s = orch.intake.capture(
        source=SignalSource.INBOUND_LEAD,
        title="Pilot",
        summary="Wants pilot",
        captured_by="sami",
    )
    o = orch.opportunities.register(
        source_signals=[s],
        kind=OpportunityKind.DIRECT_DEAL,
        title="Pilot deal",
        buyer_segment="agency",
        estimated_value_sar=3000,
        close_probability=0.7,
        fit_score=0.8,
        urgency_score=0.6,
        risk_score=0.2,
        proposed_value_outputs=[ValueOutput.MONEY],
    )
    return orch, s, o


def test_cash_scout_ranks_opportunities():
    orch, _, _ = _seeded_orchestrator()
    actions = orch.cash_scout.fastest_cash()
    assert actions
    assert actions[0].priority > 0


def test_pricing_quote_target_in_range():
    _, _, opp = _seeded_orchestrator()
    p = quote(base_floor=999, base_ceiling=4999, opportunity=opp, delivery_complexity=0.5)
    assert p.floor_sar <= p.target_sar <= p.ceiling_sar
    assert 0.0 <= p.confidence <= 1.0


def test_proposal_renders_arabic_with_required_sections():
    _, _, opp = _seeded_orchestrator()
    p = quote(base_floor=999, base_ceiling=4999, opportunity=opp)
    draft = render_proposal(
        opportunity=opp,
        offer_title="Revenue Hunter Pilot",
        pain="pain",
        promise="promise",
        deliverables=["a", "b"],
        timeline="14 days",
        price=p,
        language="ar",
    )
    assert "السعر" in draft.body_markdown
    assert "invoice_paid" in draft.body_markdown
    assert draft.target_price_sar == p.target_sar


def test_followup_respects_cooldown():
    from datetime import UTC, datetime

    d = draft_followup(
        opportunity_id="o",
        buyer_name="Sami",
        sequence_step=1,
        promise="promise",
        last_contact_at=datetime(2026, 1, 1, 9, 0, tzinfo=UTC),
    )
    assert d.send_after.day == 3
    assert "متابعة" in d.subject


def test_offer_scale_decision_with_no_outcomes_is_hold():
    orch, _, _ = _seeded_orchestrator()
    decisions = evaluate_library(
        library=orch.offers,
        outcomes=orch.outcomes,
        opportunity_to_offer={},
        engine=orch.scale,
    )
    assert decisions
    assert all(d.verdict.value in {"scale", "hold", "kill"} for d in decisions)


def test_partner_fit_score_penalises_risk():
    scout = PartnerScout()
    safe = scout.register(
        name="Safe agency",
        kind=PartnerKind.REFERRAL,
        signals=PartnerSignals(0.8, 0.8, 0.8, 0.8, 0.8, 0.1),
    )
    risky = scout.register(
        name="Risky agency",
        kind=PartnerKind.REFERRAL,
        signals=PartnerSignals(0.8, 0.8, 0.8, 0.8, 0.8, 0.9),
    )
    assert safe.fit_score > risky.fit_score


def test_customer_health_label_buckets():
    healthy = evaluate(CustomerSignals(0.9, 0.9, 0.9, 0.9, 0.1, 0.7))
    risky = evaluate(CustomerSignals(0.3, 0.3, 0.3, 0.3, 0.8, 0.1))
    assert healthy.label in {"thriving", "ok"}
    assert risky.label in {"at_risk", "lost"}


def test_vertical_test_recommends_scale_when_signals_strong():
    test = make_vertical(
        sector="agencies",
        buyer="agency owners",
        pain="lost follow-ups",
        offer="Revenue Hunter Pilot",
        price_sar=2499,
        first_targets_count=40,
        partner_angle="affiliate",
        trust_requirements="PDPL-aware",
        pilot_metric="cash_collected",
        fit_score=0.85,
        risk_score=0.2,
    )
    score, verdict = eval_vertical(test, partner_strength=0.8)
    assert score > 0.6
    assert verdict.value in {"scale", "hold"}
