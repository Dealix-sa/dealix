from datetime import UTC, datetime, timedelta

from dealix.commercial_intelligence import (
    CommercialSignal,
    EvidenceLevel,
    GovernedSource,
    OpportunityInputs,
    SourceKind,
    SourcePolicyStatus,
    highest_evidence_level,
    score_opportunity,
    score_source,
    source_scorecard,
)

NOW = datetime(2026, 7, 15, tzinfo=UTC)


def _source(
    *,
    tenant_id: str = "tenant-a",
    source_id: str = "source-a",
    policy: SourcePolicyStatus = SourcePolicyStatus.APPROVED,
) -> GovernedSource:
    return GovernedSource(
        tenant_id=tenant_id,
        source_id=source_id,
        name="Authorized source",
        kind=SourceKind.CRM,
        policy_status=policy,
        allowed_use="tenant_authorized_revenue_operations",
        authority_score=90,
        verifiability_score=90,
        freshness_days=30,
        retention_days=365,
        terms_reviewed_at=NOW,
    )


def _signal(
    *,
    signal_id: str,
    source_id: str = "source-a",
    tenant_id: str = "tenant-a",
    evidence_level: EvidenceLevel = EvidenceLevel.L3_FIRST_PARTY,
    expires_at: datetime | None = None,
) -> CommercialSignal:
    return CommercialSignal(
        tenant_id=tenant_id,
        signal_id=signal_id,
        account_id="account-a",
        source_id=source_id,
        signal_type="verified_operating_problem",
        claim="The buyer confirmed a measurable operating delay.",
        evidence_ref=f"evidence://{signal_id}",
        observed_at=NOW - timedelta(days=1),
        confidence=85,
        evidence_level=evidence_level,
        expires_at=expires_at,
    )


def test_blocked_source_always_scores_zero() -> None:
    assert score_source(_source(policy=SourcePolicyStatus.BLOCKED), now=NOW) == 0


def test_public_signal_caps_an_otherwise_strong_opportunity() -> None:
    result = score_opportunity(
        OpportunityInputs(
            strategic_fit=100,
            problem_evidence=100,
            urgency=100,
            relationship_strength=100,
            commercial_value=100,
            evidence_level=EvidenceLevel.L2_PUBLIC_SIGNAL,
            source_score=100,
            signal_count=3,
        )
    )

    assert result.uncapped_score == 100
    assert result.score == 60
    assert result.evidence_cap == 60
    assert "client_validation_required" in result.blockers
    assert result.external_action_allowed is False


def test_no_signal_forces_research_score_and_blocker() -> None:
    result = score_opportunity(
        OpportunityInputs(
            strategic_fit=100,
            problem_evidence=100,
            urgency=100,
            relationship_strength=100,
            commercial_value=100,
            evidence_level=EvidenceLevel.L5_MEASURED_OUTCOME,
            source_score=100,
            signal_count=0,
        )
    )

    assert result.score == 20
    assert result.confidence_band == "low"
    assert "no_evidence_signal" in result.blockers


def test_scorecard_is_tenant_and_source_scoped_and_marks_stale_evidence() -> None:
    source = _source()
    included = _signal(signal_id="included", expires_at=NOW - timedelta(seconds=1))
    wrong_tenant = _signal(signal_id="wrong-tenant", tenant_id="tenant-b")
    wrong_source = _signal(signal_id="wrong-source", source_id="source-b")

    card = source_scorecard(
        source,
        [included, wrong_tenant, wrong_source],
        now=NOW,
    )

    assert card["signals"] == 1
    assert card["stale_signals"] == 1
    assert card["average_signal_confidence"] == 85
    assert card["external_action_allowed"] is False


def test_highest_evidence_level_uses_strongest_linked_signal() -> None:
    signals = [
        _signal(signal_id="public", evidence_level=EvidenceLevel.L2_PUBLIC_SIGNAL),
        _signal(signal_id="verified", evidence_level=EvidenceLevel.L4_VERIFIED),
    ]

    assert highest_evidence_level(signals) is EvidenceLevel.L4_VERIFIED
