"""Smoke tests across the domain modules."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pytest

from dealix.hermes.customer.health_score import CustomerHealthScorer
from dealix.hermes.customer.value_report import ValueReportBuilder
from dealix.hermes.intelligence.market_radar import MarketRadar, MarketSignalKind
from dealix.hermes.marketplace.listings import ListingKind, Marketplace
from dealix.hermes.money.cash_scout import CashScout
from dealix.hermes.money.pricing import PriceBand, PricingPolicy
from dealix.hermes.money.proposal_factory import ProposalFactory
from dealix.hermes.partners.fit_score import PartnerFitInputs, PartnerFitScorer
from dealix.hermes.partners.revenue_share import RevenueShareLedger
from dealix.hermes.partners.scout import PartnerScout, PartnerType
from dealix.hermes.products.flagship import FLAGSHIP_OFFERS
from dealix.hermes.products.offer_builder import OfferBuilder, OfferLifecycleStatus
from dealix.hermes.training.workshop_builder import WorkshopBuilder
from dealix.hermes.ventures.vertical_launcher import VerticalLauncher
from dealix.hermes.api.capabilities import CapabilityGateway, Exposure
from dealix.hermes.core.schemas import Opportunity, Signal


# ---------------------------------------------------------------------------
# Money
# ---------------------------------------------------------------------------


def test_cash_scout_ranks_higher_revenue_first():
    a = Signal.make(source="x", domain="money", summary="A",
                    payload={"cash": {"expected_revenue_sar": 200_000, "days_to_cash": 7, "win_probability": 0.7}})
    b = Signal.make(source="x", domain="money", summary="B",
                    payload={"cash": {"expected_revenue_sar": 5_000, "days_to_cash": 60, "win_probability": 0.2}})
    scout = CashScout()
    ranked = scout.rank([a, b])
    assert ranked[0][0] is a


def test_proposal_requires_all_fields():
    f = ProposalFactory()
    opp = Opportunity.make(signal_id="sig_x", domain="money", title="x")
    with pytest.raises(ValueError):
        f.draft(opp, buyer="", deliverables=[], price_sar=0, timeline_weeks=2, metric="")
    p = f.draft(opp, buyer="CTO Acme", deliverables=["pilot"], price_sar=14_900,
                timeline_weeks=2, metric="meetings")
    assert p.status == "draft"


def test_pricing_policy_requires_sovereign():
    pol = PricingPolicy()
    with pytest.raises(PermissionError):
        pol.set_band(PriceBand(name="pilot", min_sar=1, max_sar=100, list_sar=50), by="agent")
    pol.set_band(PriceBand(name="pilot", min_sar=10_000, max_sar=20_000, list_sar=14_900), by="sami")
    assert pol.validate("pilot", 14_900)


# ---------------------------------------------------------------------------
# Products
# ---------------------------------------------------------------------------


def test_offer_builder_readiness():
    b = OfferBuilder()
    with pytest.raises(ValueError):
        b.draft(buyer="", pain="", promise="", deliverables=[], price_sar=0,
                timeline_weeks=2, metric="", upsell="", trust_risks=[])
    o = b.draft(
        buyer="CTO Acme",
        pain="No pipeline",
        promise="30 leads",
        deliverables=["leads"],
        price_sar=14_900,
        timeline_weeks=2,
        metric="meetings",
        upsell="retainer",
        trust_risks=["data scope"],
    )
    assert o.status == OfferLifecycleStatus.DRAFT


def test_flagship_offers_are_valid():
    b = OfferBuilder()
    for spec in FLAGSHIP_OFFERS:
        o = b.draft(
            buyer=spec.buyer,
            pain=spec.pain,
            promise=spec.promise,
            deliverables=list(spec.deliverables),
            price_sar=spec.price_sar,
            timeline_weeks=spec.timeline_weeks,
            metric=spec.metric,
            upsell=spec.upsell,
            trust_risks=list(spec.trust_risks),
        )
        assert o.id


# ---------------------------------------------------------------------------
# Partners
# ---------------------------------------------------------------------------


def test_partner_fit_scorer_clips_inputs():
    s = PartnerFitScorer()
    total, _ = s.compute(PartnerFitInputs(
        client_base=2.0, sales_capability=1.0, delivery_capability=1.0,
        trust_level=1.0, sector_fit=1.0, risk_level=0.0,
    ))
    assert 0.0 <= total <= 1.0


def test_partner_revenue_share_total():
    p = PartnerScout().add(name="X", type=PartnerType.REFERRAL, sector="fintech", contact="x@y")
    ledger = RevenueShareLedger()
    ledger.record(partner_id=p.id, deal_ref="d1", gross_sar=100_000, share_pct=20.0)
    ledger.record(partner_id=p.id, deal_ref="d2", gross_sar=50_000, share_pct=10.0)
    assert ledger.total_for(p.id) == 100_000 * 0.2 + 50_000 * 0.1


# ---------------------------------------------------------------------------
# Intelligence
# ---------------------------------------------------------------------------


def test_market_radar_requires_known_intent():
    r = MarketRadar()
    with pytest.raises(ValueError):
        r.emit(kind=MarketSignalKind.TREND, summary="x", intent="unknown")
    sig = r.emit(kind=MarketSignalKind.TENDER, summary="x", intent="lead_list")
    assert sig.payload["intent"] == "lead_list"


# ---------------------------------------------------------------------------
# Training
# ---------------------------------------------------------------------------


def test_workshop_requires_upsell():
    w = WorkshopBuilder()
    with pytest.raises(ValueError):
        w.build(name="x", audience="founders", duration_hours=4,
                modules=["m"], upsell_offer_id="", price_sar=2000)
    ok = w.build(name="x", audience="founders", duration_hours=4,
                 modules=["m"], upsell_offer_id="off_x", price_sar=2000)
    assert ok.upsell_offer_id == "off_x"


# ---------------------------------------------------------------------------
# Customer
# ---------------------------------------------------------------------------


def test_customer_health_components_sum_to_score():
    h = CustomerHealthScorer().compute(usage=0.8, outcomes=0.7, communication=0.6, value=0.9)
    assert 0.0 <= h.score <= 1.0
    assert h.renewal_risk in {"low", "medium", "high"}


def test_value_report_silent_customers():
    b = ValueReportBuilder()
    b.issue(customer_id="acme",
            period_end=datetime.now(timezone.utc),
            wins=["x"], metrics={}, next_actions=["y"])
    silent = b.silent_customers(active_customers=["acme", "globex"], window=timedelta(seconds=0))
    # 'globex' has no report at all, so it's silent. 'acme' just issued; with 0 window, also silent.
    assert "globex" in silent


# ---------------------------------------------------------------------------
# Ventures
# ---------------------------------------------------------------------------


def test_vertical_requires_50_targets():
    v = VerticalLauncher()
    with pytest.raises(ValueError):
        v.launch(
            name="fintech", buyer="b", pain="p", offer_id="o", first_targets=["a"],
            pilot_metric="m", scale_rule="s", kill_rule="k", trust_requirements=["r"],
        )
    targets = [f"t{i}" for i in range(50)]
    vrt = v.launch(
        name="fintech", buyer="b", pain="p", offer_id="o", first_targets=targets,
        pilot_metric="m", scale_rule="s", kill_rule="k", trust_requirements=["r"],
    )
    assert vrt.active


# ---------------------------------------------------------------------------
# API + Marketplace
# ---------------------------------------------------------------------------


def test_public_capability_requires_all_gates_and_sovereign():
    gw = CapabilityGateway()
    cap = gw.register(id="trust_check", name="Trust Check API")
    for g in [
        "authentication", "rate_limits", "billing", "audit", "abuse_prevention",
        "terms", "monitoring", "kill_switch", "developer_docs", "sovereign_approval",
    ]:
        cap.declare_gate(g)
    # Missing closure → refused.
    with pytest.raises(ValueError):
        gw.graduate(cap.id, to=Exposure.PUBLIC, by="sami")
    for g in list(cap.gates.keys()):
        cap.close_gate(g)
    # Wrong approver still refused.
    with pytest.raises(PermissionError):
        gw.graduate(cap.id, to=Exposure.PUBLIC, by="agent")
    gw.graduate(cap.id, to=Exposure.PUBLIC, by="sami")
    assert cap.exposure == Exposure.PUBLIC


def test_marketplace_only_sovereign_publishes():
    m = Marketplace()
    l = m.draft(title="Agent Template", kind=ListingKind.AGENT_TEMPLATE)
    m.quality_review(l.id); m.trust_review(l.id); m.set_price(l.id, price_sar=2000)
    with pytest.raises(PermissionError):
        m.publish(l.id, by="agent")
    m.publish(l.id, by="sami")
