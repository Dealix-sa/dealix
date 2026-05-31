"""Tests for partners, assets, and graphs."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

from dealix.hermes.assets import (
    Asset,
    AssetKind,
    commercialization_candidates,
    grade_asset,
    propose_product_from_asset,
    record_reuse,
    register_asset,
)
from dealix.hermes.graphs import (
    AssetGraph,
    OpportunityGraph,
    OutcomeGraph,
    PartnerGraph,
    RevenueGraph,
    RiskGraph,
    SectorGraph,
)
from dealix.hermes.graphs.asset_graph import AssetEdge
from dealix.hermes.graphs.opportunity_graph import OpportunityNode
from dealix.hermes.graphs.outcome_graph import OutcomeNode
from dealix.hermes.graphs.partner_graph import PartnerEdge
from dealix.hermes.graphs.revenue_graph import RevenueNode
from dealix.hermes.graphs.risk_graph import RiskEvent
from dealix.hermes.partners.program import (
    APPROVED_CLAIMS,
    PARTNER_TIERS,
    PartnerTier,
    calculate_share,
    review_partner,
)
from dealix.hermes.partners.program.partner_claims import is_claim_approved


def test_approved_claim_present():
    assert any(c.approved for c in APPROVED_CLAIMS)


def test_forbidden_claim_blocked():
    assert not is_claim_approved("Dealix guarantees sales")


def test_revenue_share_under_minimum_returns_zero():
    share = calculate_share(tier=PartnerTier.WHITE_LABEL, verified_revenue_sar=5_000)
    assert share == 0.0


def test_revenue_share_normal_case():
    spec = PARTNER_TIERS[PartnerTier.REFERRAL]
    share = calculate_share(tier=PartnerTier.REFERRAL, verified_revenue_sar=50_000)
    assert share == round(50_000 * spec.revenue_share_pct, 2)


def test_partner_performance_drop_decision():
    perf = review_partner(
        partner_id="p1", period="2026Q1",
        verified_revenue_sar=1_000, incidents=10, customer_csat=0.3,
        minimum_verified_revenue_sar=25_000,
    )
    assert perf.decision == "drop"


def test_asset_register_grade_reuse_commercialize():
    asset = register_asset(Asset(
        asset_id="a1",
        kind=AssetKind.PROPOSAL_TEMPLATE,
        title="Enterprise governance proposal",
        owner="sami",
        created_at=datetime.now(UTC) - timedelta(days=30),
    ))
    for _ in range(4):
        record_reuse("a1", verified_revenue_influence_sar=25_000)
    grade_asset(asset)
    assert asset.quality_grade in ("A", "B", "C", "D")
    candidates = commercialization_candidates(min_reuse=3, min_revenue_sar=10_000)
    assert asset in candidates
    pkg = propose_product_from_asset(asset)
    assert pkg.required_approval.value == "S2_SAMI_APPROVAL"


def test_revenue_graph_top_offer():
    g = RevenueGraph()
    g.add(RevenueNode("d1", "ai_trust_kit", "bfsi", "geo", 60_000))
    g.add(RevenueNode("d2", "ai_trust_kit", "telco", "partner", 40_000))
    g.add(RevenueNode("d3", "revenue_hunter_pilot", "telco", "outbound", 25_000))
    assert g.top_offer() == "ai_trust_kit"


def test_opportunity_graph_win_rate():
    g = OpportunityGraph()
    g.add(OpportunityNode("o1", "ai_trust_kit", "bfsi", "geo", 30_000, "won"))
    g.add(OpportunityNode("o2", "ai_trust_kit", "bfsi", "geo", 30_000, "lost"))
    assert g.win_rate("ai_trust_kit") == 0.5


def test_outcome_graph_value_by_agent():
    g = OutcomeGraph()
    g.add(OutcomeNode("r1", "draft_commercial_proposal", "proposal_factory", True, 15_000))
    g.add(OutcomeNode("r2", "score_leads", "revenue_hunter", True, 5_000))
    by_agent = g.value_by_agent()
    assert by_agent["proposal_factory"] == 15_000


def test_partner_graph_revenue_and_incidents():
    g = PartnerGraph()
    g.add(PartnerEdge("acme", "d1", 50_000, incidents=0))
    g.add(PartnerEdge("acme", "d2", 30_000, incidents=2))
    assert g.revenue()["acme"] == 80_000
    assert g.incident_rate()["acme"] == 1.0


def test_asset_graph_revenue_attribution():
    g = AssetGraph()
    g.add(AssetEdge("evidence_pack", "d1", 20_000))
    g.add(AssetEdge("evidence_pack", "d2", 10_000))
    assert g.revenue_by_asset()["evidence_pack"] == 30_000


def test_risk_graph_top_categories():
    g = RiskGraph()
    g.add(RiskEvent("r1", "overclaim", "high"))
    g.add(RiskEvent("r2", "overclaim", "medium"))
    g.add(RiskEvent("r3", "pdpl_scope", "low"))
    top = g.top_categories(2)
    assert top[0][0] == "overclaim"


def test_sector_graph_ranking():
    g = SectorGraph()
    g.add_revenue("bfsi", 80_000)
    g.add_revenue("telco", 30_000)
    ranked = g.ranked_by_revenue()
    assert ranked[0].sector == "bfsi"
