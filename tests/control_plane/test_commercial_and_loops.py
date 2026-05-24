"""Money / Offer / Asset / Loops / Readiness gates (sections 66–75)."""

from __future__ import annotations

import pytest

from dealix.control_plane.approval_center import (
    ApprovalCenter,
    ApprovalDecision,
    SovereigntyLevel,
)
from dealix.control_plane.asset_library import AssetLibrary, AssetType
from dealix.control_plane.identity_access import Identity, IdentityKind
from dealix.control_plane.intelligence_graph import (
    EdgeKind,
    IntelligenceGraph,
    NodeKind,
)
from dealix.control_plane.marketplace import MarketplaceReadiness
from dealix.control_plane.money_command import MoneyCommand
from dealix.control_plane.offer_system import OfferState, OfferSystem
from dealix.control_plane.partner_loop import PartnerRiskKind, PartnerValueLoop
from dealix.control_plane.public_api import PublicAPIReadiness
from dealix.control_plane.scale_kill_board import (
    KillReason,
    ScaleKillBoard,
    ScaleScore,
)
from dealix.control_plane.venture_loop import VentureValueLoop


def test_money_command_weighs_pipeline() -> None:
    money = MoneyCommand()
    deal = money.open_deal(
        target="Agency X",
        offer="Agency White-label Kit",
        deal_value_sar=20_000,
        floor_price_sar=5_000,
        target_price_sar=15_000,
        pain="Needs AI offer for clients",
        workspace_id="ws_internal_dealix",
        next_step="Send proposal",
        close_probability=0.5,
    )
    assert deal.expected_revenue_sar == 10_000
    snapshot = money.snapshot()
    assert snapshot.pipeline_sar == 20_000
    assert snapshot.probability_weighted_revenue_sar == 10_000


def test_offer_cannot_go_active_when_incomplete() -> None:
    offers = OfferSystem()
    offer = offers.draft(name="Revenue Hunter Pilot")
    with pytest.raises(ValueError):
        offers.transition(offer.offer_id, target=OfferState.INTERNAL_REVIEW)


def test_offer_full_lifecycle() -> None:
    offers = OfferSystem()
    offer = offers.draft(
        name="Revenue Hunter Pilot",
        buyer="agency_founder",
        pain="no inbound pipeline",
        promise="20 qualified replies / month",
        deliverables=["outreach_kit", "trust_pack"],
        price_sar=15_000,
        metric="qualified_replies",
        upsell="Founder OS",
        trust_risks=["overclaim"],
    )
    offers.transition(offer.offer_id, target=OfferState.INTERNAL_REVIEW)
    offers.transition(offer.offer_id, target=OfferState.PILOT_READY)
    offers.transition(offer.offer_id, target=OfferState.ACTIVE)
    offers.record_metric_event(offer.offer_id, field="messages_sent", delta=10)
    assert offers.get(offer.offer_id).metrics.messages_sent == 10


def test_asset_library_marks_productizable() -> None:
    library = AssetLibrary()
    asset = library.create(
        name="Agency proposal v1",
        type=AssetType.PROPOSAL_TEMPLATE,
        workspace_id="ws_internal_dealix",
        owner_identity_id="sami",
    )
    library.reuse(asset.asset_id, revenue_sar=20_000)
    library.reuse(asset.asset_id, revenue_sar=15_000)
    library.link_offer(asset.asset_id, offer_id="of_xyz")
    assert library.get(asset.asset_id).commercializable is True
    assert library.get(asset.asset_id).score.reuse_count == 2


def test_intelligence_graph_finds_best_offer() -> None:
    graph = IntelligenceGraph()
    sector = graph.add_node(kind=NodeKind.SECTOR, label="agencies")
    offer_hot = graph.add_node(kind=NodeKind.OFFER, label="Agency Kit")
    offer_cold = graph.add_node(kind=NodeKind.OFFER, label="Cold Offer")
    outcome = graph.add_node(kind=NodeKind.OUTCOME, label="20k SAR")
    graph.add_edge(
        kind=EdgeKind.PROPOSAL_LED_TO_OUTCOME,
        src=offer_hot.node_id,
        dst=outcome.node_id,
        payload={"revenue_sar": 20_000},
    )
    graph.add_edge(
        kind=EdgeKind.PROPOSAL_LED_TO_OUTCOME,
        src=offer_cold.node_id,
        dst=outcome.node_id,
        payload={"revenue_sar": 0},
    )
    # revenue is summed on the destination node — best_offer asks per offer
    # using `revenue_for` which sums incoming weights/payloads
    # Add explicit revenue edges into each offer
    revenue_in = graph.add_node(kind=NodeKind.OPPORTUNITY, label="opp_hot")
    graph.add_edge(
        kind=EdgeKind.OPPORTUNITY_USED_OFFER,
        src=revenue_in.node_id,
        dst=offer_hot.node_id,
        payload={"revenue_sar": 30_000},
    )
    assert graph.best_offer().node_id == offer_hot.node_id


def test_scale_kill_board_classifies() -> None:
    board = ScaleKillBoard()
    board.record(
        entity_id="offer_a",
        entity_kind="offer",
        label="High flyer",
        score=ScaleScore(
            revenue_score=0.9,
            repeatability_score=0.9,
            margin_score=0.9,
            data_moat_score=0.9,
            partner_score=0.9,
            trust_score=0.9,
            delivery_score=0.9,
        ),
    )
    board.record(
        entity_id="offer_b",
        entity_kind="offer",
        label="Drag",
        score=ScaleScore(),
        kill_reasons=[KillReason.NO_DEMAND, KillReason.LOW_MARGIN],
    )
    assert board.verdict("offer_a") == "scale"
    assert board.verdict("offer_b") == "kill"


def test_partner_loop_trust_check_requires_all_clear() -> None:
    loop = PartnerValueLoop()
    partner = loop.scout(name="Agency Acme", workspace_id="ws_partner_acme")
    loop.add_risk_check(
        partner.partner_id,
        risk_kind=PartnerRiskKind.DELIVERY,
        severity="medium",
        note="needs ramp-up",
        cleared=False,
    )
    assert loop.trust_check_clear(partner.partner_id) is False
    loop.add_risk_check(
        partner.partner_id,
        risk_kind=PartnerRiskKind.BRAND,
        severity="low",
        note="ok",
        cleared=True,
    )
    assert loop.trust_check_clear(partner.partner_id) is False
    partner.risks[0].cleared = True
    assert loop.trust_check_clear(partner.partner_id) is True


def test_venture_loop_blocks_scale_without_prereqs() -> None:
    loop = VentureValueLoop()
    venture = loop.signal(sector="real_estate", workspace_id="ws_venture_real_estate")
    with pytest.raises(ValueError):
        loop.scale(venture.venture_id)
    loop.set_pain_map(venture.venture_id, pains=["lead chaos", "no follow-up"])
    loop.attach_offer(venture.venture_id, offer_id="of_re_pilot")
    loop.add_targets(venture.venture_id, targets=[f"target_{i}" for i in range(50)])
    loop.record_reply(venture.venture_id, reply="Acme RE replied")
    loop.record_outcome(venture.venture_id, outcome="signed pilot")
    scaled = loop.scale(venture.venture_id)
    assert scaled.stage.value == "scale"


def test_public_api_and_marketplace_require_s4_launch() -> None:
    centre = ApprovalCenter()
    api = PublicAPIReadiness()
    with pytest.raises(PermissionError):
        api.launch(approval_center=centre)
    for check in list(api.checks.keys()):
        api.mark(check, value=True)
    card = centre.request(
        requested_by="sami",
        action_type="launch_public_api",
        sovereignty_level=SovereigntyLevel.S4_LAUNCH_GATE,
        risk_level="high",
        summary="launch public API",
    )
    sami = Identity(identity_id="sami", kind=IdentityKind.SAMI, display_name="Sami")
    centre.approve(approval_id=card.approval_id, actor=sami)
    api.s4_approval_id = card.approval_id
    api.launch(approval_center=centre)
    assert api.launched is True

    market = MarketplaceReadiness()
    with pytest.raises(PermissionError):
        market.launch(approval_center=centre)
