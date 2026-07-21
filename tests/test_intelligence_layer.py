"""Tests for the Dealix Intelligence Layer."""

from datetime import datetime, timedelta

from intelligence import (
    Deal,
    EvidenceItem,
    EvidenceSynthesizer,
    EvidenceType,
    IntelligenceRouter,
    RevenueIntelligenceEngine,
    SaudiCompanyProfile,
    SaudiMarketIntelligence,
    TaskType,
    Urgency,
)


def test_router_reasoning_selects_sonnet():
    router = IntelligenceRouter()
    decision = router.route(TaskType.REASONING, Urgency.NORMAL)
    assert decision.provider == "anthropic"
    assert decision.model == "claude-3-5-sonnet"
    assert decision.force_json is False


def test_router_realtime_selects_fast_model():
    router = IntelligenceRouter()
    decision = router.route(TaskType.CLASSIFICATION, Urgency.REALTIME)
    assert decision.provider == "openai"
    assert decision.model == "gpt-4o-mini"


def test_router_saudi_context_prefers_anthropic():
    router = IntelligenceRouter()
    decision = router.route(TaskType.EXTRACTION, Urgency.FAST, requires_saudi_context=True)
    assert decision.provider == "anthropic"


def test_saudi_market_intelligence_scores_profile():
    engine = SaudiMarketIntelligence()
    profile = SaudiCompanyProfile(
        company_name="Najm Tech",
        sector="software",
        city="Riyadh",
        employees_estimate=45,
        website="https://najmtech.sa",
    )
    score = engine.score_icp(profile)
    assert score.score >= 80
    assert any("high-growth" in r for r in score.reasons)


def test_revenue_intelligence_empty_pipeline():
    engine = RevenueIntelligenceEngine()
    engine.load_deals([])
    result = engine.analyze()
    assert result.pipeline_health == 0.0
    assert "No active deals" in result.recommended_actions[0]


def test_revenue_intelligence_detects_risk():
    engine = RevenueIntelligenceEngine()
    stale = datetime.utcnow() - timedelta(days=20)
    engine.load_deals([
        Deal(
            deal_id="d1",
            company_name="Stale Co",
            stage="proposal_sent",
            value_sar=10000,
            created_at=stale,
            last_activity_at=stale,
            activities_count=1,
        ),
    ])
    result = engine.analyze()
    assert result.revenue_at_risk_sar > 0
    assert any("at risk" in a for a in result.recommended_actions)


def test_evidence_synthesizer_go_decision():
    synth = EvidenceSynthesizer()
    now = datetime.utcnow()
    synth.add(EvidenceItem("e1", EvidenceType.METRIC, "Revenue uplift", "+30%", "pilot", now, verified=True))
    synth.add(EvidenceItem("e2", EvidenceType.TESTIMONIAL, "CEO quote", "Great ROI", "client", now, verified=True))
    synth.add(EvidenceItem("e3", EvidenceType.DELIVERABLE, "Report", "CEO brief", "team", now, verified=True))
    synth.add(EvidenceItem("e4", EvidenceType.AUDIT_LOG, "Audit", "Approved", "system", now, verified=True))
    pack = synth.synthesize("Should we offer the pilot to similar prospects?")
    assert pack.decision_type.value == "go"
    assert pack.confidence >= 0.8


def test_evidence_synthesizer_defer_without_evidence():
    synth = EvidenceSynthesizer()
    pack = synth.synthesize("Should we enter a new sector?")
    assert pack.decision_type.value == "defer"
    assert len(pack.gaps) > 0
