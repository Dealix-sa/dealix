"""Quality contract tests — every output must carry its required fields."""

from __future__ import annotations

import pytest

from dealix.hermes.core.schemas import (
    OpportunityType,
    SignalType,
    SovereigntyLevel,
)
from dealix.hermes.core.signals import SignalStore
from dealix.hermes.intelligence.market_radar import MarketRadar
from dealix.hermes.money.proposal_factory import ProposalFactory
from dealix.hermes.partners.fit_score import PartnerFitScorer
from dealix.hermes.products.offer_builder import OfferBuildError, OfferBuilder
from dealix.hermes.products.offer_library import default_offers


def test_offer_has_canonical_fields():
    for offer in default_offers():
        for field in (
            "offer",
            "buyer",
            "pain",
            "promise",
            "deliverables",
            "price_range_sar",
            "outcome_metric",
        ):
            assert offer.get(field), f"offer missing {field}"
        assert offer["deliverables"], "deliverables cannot be empty"


def test_offer_builder_rejects_missing_fields():
    with pytest.raises(OfferBuildError):
        OfferBuilder().build(
            offer="X",
            buyer="",
            pain="p",
            promise="pr",
            deliverables=["a"],
            price_range_sar="1",
            outcome_metric="m",
        )


def test_proposal_carries_buyer_pain_price_deliverables_metric():
    from dealix.hermes.core.opportunities import OpportunityStore

    store = OpportunityStore()
    sig = SignalStore().ingest(
        source="customer",
        signal_type=SignalType.CUSTOMER,
        title="Lead",
    )
    opp = store.evaluate(
        sig,
        opportunity_type=OpportunityType.CUSTOMER,
        estimated_value_sar=10_000,
    )
    offer = default_offers()[0]
    proposal = ProposalFactory().draft(opp, offer=offer)
    for field in ("buyer", "pain", "deliverables", "metric", "price"):
        assert proposal.get(field), f"proposal missing {field}"
    assert proposal["external_send"] is False


def test_partner_has_fit_score_and_action():
    fit = PartnerFitScorer().score(
        partner_name="Agency X",
        partner_type="white_label",
        client_base_score=5,
        sales_capability=4,
        delivery_capability=3,
        trust_level=4,
        sector_fit=5,
        risk_level=2,
    )
    assert fit.fit_score > 0
    assert fit.next_action
    assert fit.produces


def test_market_signal_produces_an_action():
    sig = SignalStore().ingest(
        source="news",
        signal_type=SignalType.MARKET,
        title="Companies adopting AI",
    )
    out = MarketRadar().process(
        sig,
        sector="AI Governance",
        opportunity="Companies need governance",
        recommended_offer="AI Trust Kit",
        target_segments=["education", "healthcare"],
    )
    assert out.produces, "market signal must produce something"


def test_value_report_carries_required_fields():
    from dealix.hermes.customer.value_report import ValueReportBuilder

    report = ValueReportBuilder().build(
        customer_id="cust_001",
        opportunities_count=3,
        messages_drafted=10,
        proposals_count=2,
        outcomes_count=4,
        value_summary="Closed 1 deal worth SAR 9,999",
        next_plan="Run upsell workshop",
        recommendation="Move to AI Governance OS",
        upsell="AI Governance OS",
    )
    for field in ("customer_id", "what_we_delivered", "what_value", "next_plan", "recommendation", "suggested_upsell"):
        assert report.get(field), f"value report missing {field}"
    assert report["external_send"] is False


def test_sovereignty_classify_for_high_value_opportunity():
    from dealix.hermes.core.opportunities import OpportunityStore

    sig = SignalStore().ingest(
        source="sami",
        signal_type=SignalType.CUSTOMER,
        title="Big enterprise deal",
    )
    opp = OpportunityStore().evaluate(sig, estimated_value_sar=50_000)
    assert opp.sovereignty_level == SovereigntyLevel.S2_SAMI_APPROVAL.value
