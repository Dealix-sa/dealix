from dealix.commercial_intelligence import EvidenceLevel, SourcePolicyStatus
from dealix.commercial_persuasion import (
    BuyerDecisionContext,
    BuyerRole,
    EvidenceUse,
    PersuasionEvidence,
    build_buyer_decision_plan,
    classify_evidence,
)
from dealix.launch_os.proposal_engine import build_proposal


def _evidence(
    *,
    claim: str = "The customer confirmed missed follow-ups in the current workflow.",
    signal_type: str = "verified_operating_problem",
    level: EvidenceLevel = EvidenceLevel.L3_FIRST_PARTY,
    consent_ref: str | None = None,
    policy: SourcePolicyStatus = SourcePolicyStatus.APPROVED,
    stale: bool = False,
) -> PersuasionEvidence:
    return PersuasionEvidence(
        claim=claim,
        signal_type=signal_type,
        evidence_ref="evidence://discovery/1",
        evidence_level=level,
        confidence=85,
        source_policy_status=policy,
        publication_consent_ref=consent_ref,
        stale=stale,
    )


def _context(**overrides: object) -> BuyerDecisionContext:
    values: dict[str, object] = {
        "opportunity_id": "opp_1",
        "account_name": "شركة اختبار",
        "opportunity_title": "متابعات غير موثقة",
        "offer_id": "revenue_proof_sprint",
        "objective": "توحيد رؤية المتابعة والقرار",
        "metric": "verified_next_action_rate",
        "proof_target": "قياس خط الأساس والتحسن خلال التجربة",
        "evidence_level": EvidenceLevel.L3_FIRST_PARTY,
        "opportunity_score": 72,
        "evidence": (_evidence(),),
        "relationship_permission_state": "consented",
    }
    values.update(overrides)
    return BuyerDecisionContext(**values)  # type: ignore[arg-type]


def test_public_signal_becomes_discovery_question_not_customer_fact() -> None:
    item = _evidence(level=EvidenceLevel.L2_PUBLIC_SIGNAL)

    assert classify_evidence(item) is EvidenceUse.DISCOVERY_ONLY
    plan = build_buyer_decision_plan(
        _context(evidence=(item,), evidence_level=EvidenceLevel.L2_PUBLIC_SIGNAL)
    )
    assert "first_party_customer_validation_required" in plan.blockers
    assert plan.truth_map[0]["disposition"] == "discovery_only"
    assert plan.external_action_allowed is False


def test_measured_dealix_outcome_needs_publication_consent() -> None:
    internal = _evidence(
        signal_type="dealix_measured_outcome",
        level=EvidenceLevel.L5_MEASURED_OUTCOME,
    )
    publishable = _evidence(
        signal_type="dealix_measured_outcome",
        level=EvidenceLevel.L5_MEASURED_OUTCOME,
        consent_ref="consent://case-study/1",
    )

    assert classify_evidence(internal) is EvidenceUse.INTERNAL_OUTCOME
    assert classify_evidence(publishable) is EvidenceUse.PUBLISHABLE_PROOF


def test_guarantee_language_is_never_promoted_as_proof() -> None:
    item = _evidence(
        claim="نضمن مضاعفة المبيعات",
        signal_type="dealix_measured_outcome",
        level=EvidenceLevel.L5_MEASURED_OUTCOME,
        consent_ref="consent://unsafe",
    )

    assert classify_evidence(item) is EvidenceUse.BLOCKED


def test_stale_or_research_only_evidence_requires_revalidation() -> None:
    stale = _evidence(stale=True)
    restricted = _evidence(policy=SourcePolicyStatus.RESEARCH_ONLY)

    assert classify_evidence(stale) is EvidenceUse.DISCOVERY_ONLY
    assert classify_evidence(restricted) is EvidenceUse.DISCOVERY_ONLY


def test_plan_maps_distinct_buyer_questions_and_hides_price() -> None:
    plan = build_buyer_decision_plan(_context())
    roles = {row["role"]: row for row in plan.buying_committee}

    assert (
        roles[BuyerRole.FINANCE.value]["decision_question_ar"]
        != roles[BuyerRole.TECHNOLOGY_DATA.value]["decision_question_ar"]
    )
    assert (
        roles[BuyerRole.ECONOMIC_BUYER.value]["proof_required"]
        != roles[BuyerRole.CHAMPION_END_USER.value]["proof_required"]
    )
    assert plan.price_included is False
    assert plan.offer_architecture["price_sar"] is None
    assert "launch_offer_and_price_not_founder_approved" in plan.blockers


def test_objections_create_specific_proof_and_red_lines() -> None:
    plan = build_buyer_decision_plan(
        _context(
            known_objections=(
                "عندي Odoo ليش أحتاجكم؟",
                "اضمن زيادة المبيعات",
                "أعطني خصم 30%",
                "كيف تدخلون على بياناتنا؟",
            ),
            requested_discount_pct=30,
        )
    )
    categories = {row["category"]: row for row in plan.objection_responses}

    assert set(categories) == {"existing_stack", "guarantee", "price", "security_data"}
    assert categories["guarantee"]["red_line"] == "no_revenue_roi_or_sales_guarantee"
    assert categories["price"]["approval_required"] is True
    assert plan.negotiation["external_commitment_made"] is False
    assert any(row["id"] == "approve_commercial_exception" for row in plan.approval_queue)


def test_research_only_relationship_blocks_external_action() -> None:
    plan = build_buyer_decision_plan(_context(relationship_permission_state="research_only"))

    assert "relationship_permission_not_verified" in plan.blockers
    assert plan.external_action_allowed is False
    assert plan.external_commitment_made is False


def test_legacy_proposal_catalog_does_not_emit_fake_proof_or_unapproved_price() -> None:
    pack = build_proposal(
        {"account_id": "account-1", "account_name": "شركة اختبار"},
        "REVENUE_LEAK_AUDIT",
        {},
    )

    assert pack.proof_references == []
    assert pack.investment_sar == 0
    assert pack.pricing_status == "draft_only"
    assert pack.approval_required is True
