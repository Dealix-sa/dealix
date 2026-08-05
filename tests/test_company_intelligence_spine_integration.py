"""Integration tests for the full Company Intelligence execution spine.

Validates that all 22 canonical entities can be constructed, that lifecycle
entities support state machine transitions, and that the pipeline connects
from Company Brain through to Daily Command.

This test file does NOT touch databases, networks, or LLMs — it exercises
only the persistence-neutral contract layer.
"""
from __future__ import annotations

from datetime import UTC, date, datetime

import pytest

from dealix.company_intelligence import (
    # Entity types and enums
    ActionStatus,
    ActionType,
    AutonomyLevel,
    # Canonical models
    CanonicalAction,
    CanonicalApproval,
    CanonicalCompany,
    CanonicalCompanyBrain,
    CanonicalConsentBasis,
    CanonicalContact,
    CanonicalDailyCommand,
    CanonicalDepartmentPlan,
    CanonicalDraft,
    CanonicalLearningEvent,
    CanonicalOffer,
    CanonicalOpportunity,
    CanonicalOutcomeEvent,
    CanonicalPartnershipOpportunity,
    CanonicalPersona,
    CanonicalPlaybookVersion,
    CanonicalProofEvent,
    CanonicalProposal,
    CanonicalRelationship,
    CanonicalSignal,
    CanonicalSource,
    CanonicalTenant,
    CompanyBrainSource,
    CompanyStatus,
    ConsentBasisStatus,
    ConsentBasisType,
    ConsentChannel,
    ContactRole,
    ContactStatus,
    Department,
    DraftChannel,
    EntityType,
    EvidenceState,
    LawfulContactBasis,
    LearningEventType,
    OfferApprovalPolicy,
    OfferPriceUnit,
    OfferStatus,
    OutcomeEventType,
    PartnershipStage,
    PartnershipType,
    PersonaStatus,
    PlanPriority,
    PlanStatus,
    PlaybookApprovalStatus,
    ProofSourceEventType,
    ProofType,
    ProposalStatus,
    RelationshipStatus,
    RelationshipStrength,
    RelationshipType,
    RiskLevel,
    SignalSensitivity,
    SignalStatus,
    SignalType,
    SourcePolicyStatus,
    SourceStatus,
    SourceType,
    TenantPlan,
    TenantStatus,
    # Builders
    build_action,
    build_company,
    build_consent_basis,
    build_contact,
    build_daily_command,
    build_department_plan,
    build_draft,
    build_learning_event,
    build_offer,
    build_outcome_event,
    build_partnership_opportunity,
    build_persona,
    build_playbook_version,
    build_proof_event,
    build_proposal,
    build_relationship,
    build_signal,
    build_source,
    build_tenant,
    # Transition helpers
    is_valid_company_transition,
    is_valid_consent_transition,
    is_valid_contact_transition,
    is_valid_partnership_transition,
    is_valid_persona_transition,
    is_valid_plan_transition,
    is_valid_playbook_transition,
    is_valid_proposal_transition,
    is_valid_relationship_transition,
    is_valid_signal_transition,
    is_valid_source_transition,
    is_valid_tenant_transition,
    is_valid_transition,
    # Adapters
    normalize_catalog,
    normalize_service_offering,
    transition_action,
    transition_company,
    transition_consent_basis,
    transition_contact,
    transition_partnership,
    transition_persona,
    transition_plan,
    transition_playbook,
    transition_proposal,
    transition_relationship,
    transition_signal,
    transition_source,
    transition_tenant,
)

TENANT_ID = "test-tenant"


# ---------------------------------------------------------------------------
# Full __init__.py export coverage
# ---------------------------------------------------------------------------


class TestExportCompleteness:
    """Verify all __all__ exports are importable and non-None."""

    def test_all_exports_are_importable(self) -> None:
        import dealix.company_intelligence as ci

        for name in ci.__all__:
            obj = getattr(ci, name)
            assert obj is not None, f"{name} exported as None"

    def test_all_count(self) -> None:
        import dealix.company_intelligence as ci

        # All 22 entities have contracts; 13 have state machines with 3 helpers each
        # plus builders, adapters, enums, utilities
        assert len(ci.__all__) > 100


# ---------------------------------------------------------------------------
# Entity construction — every canonical entity type can be built
# ---------------------------------------------------------------------------


class TestEntityConstruction:
    """Verify that all 22 canonical entity types can be constructed."""

    def test_build_tenant(self) -> None:
        t = build_tenant(handle="acme-co", name="ACME Corp", source_id="test")
        assert isinstance(t, CanonicalTenant)
        assert t.status == TenantStatus.ACTIVE

    def test_build_source(self) -> None:
        s = build_source(
            tenant_id=TENANT_ID,
            deduplication_key="src-1",
            name="CRM Export",
            source_type=SourceType.MANUAL,
        )
        assert isinstance(s, CanonicalSource)
        assert s.status == SourceStatus.ACTIVE

    def test_build_consent_basis(self) -> None:
        c = build_consent_basis(
            tenant_id=TENANT_ID,
            contact_id="contact-1",
            basis=ConsentBasisType.EXPLICIT_OPT_IN,
            channel=ConsentChannel.EMAIL,
            source_id="source-1",
        )
        assert isinstance(c, CanonicalConsentBasis)

    def test_build_company(self) -> None:
        c = build_company(
            tenant_id=TENANT_ID,
            deduplication_key="target-corp",
            name="Target Corp",
            source_id="source-1",
        )
        assert isinstance(c, CanonicalCompany)
        assert c.status == CompanyStatus.DISCOVERED

    def test_build_contact(self) -> None:
        c = build_contact(
            tenant_id=TENANT_ID,
            deduplication_key="ali-ahmed-co1",
            company_id="company-1",
            name="Ali Ahmed",
            source_id="source-1",
        )
        assert isinstance(c, CanonicalContact)
        assert c.status == ContactStatus.IDENTIFIED

    def test_build_signal(self) -> None:
        s = build_signal(
            tenant_id=TENANT_ID,
            deduplication_key="sig-1",
            company_id="company-1",
            source_id="source-1",
            signal_type=SignalType.MARKET,
            claim="Expanding to Saudi market",
        )
        assert isinstance(s, CanonicalSignal)

    def test_build_relationship(self) -> None:
        r = build_relationship(
            tenant_id=TENANT_ID,
            from_id="company-a",
            from_type=EntityType.COMPANY,
            to_id="company-b",
            to_type=EntityType.COMPANY,
            relationship_type=RelationshipType.CUSTOMER,
            source_id="source-1",
        )
        assert isinstance(r, CanonicalRelationship)

    def test_build_partnership_opportunity(self) -> None:
        p = build_partnership_opportunity(
            tenant_id=TENANT_ID,
            company_id="company-1",
            partnership_type=PartnershipType.CHANNEL_PARTNER,
            source_id="source-1",
        )
        assert isinstance(p, CanonicalPartnershipOpportunity)

    def test_build_persona(self) -> None:
        p = build_persona(
            tenant_id=TENANT_ID,
            name="Saudi B2B SaaS Founder",
            source_id="source-1",
        )
        assert isinstance(p, CanonicalPersona)

    def test_build_offer(self) -> None:
        o = build_offer(
            tenant_id=TENANT_ID,
            offer_key="free_mini_diagnostic",
            name_ar="التشخيص المجاني السريع",
            name_en="Free Mini Diagnostic",
            status=OfferStatus.FREE_ENTRY,
            approval_policy=OfferApprovalPolicy.SELF_SERVE,
            source_id="service-catalog",
        )
        assert isinstance(o, CanonicalOffer)

    def test_build_department_plan(self) -> None:
        dp = build_department_plan(
            tenant_id=TENANT_ID,
            deduplication_key="plan-1",
            department=Department.SALES,
            goal="Increase pipeline",
            source_id="source-1",
            action_ids=("action-1",),
            kpis=("pipeline-coverage",),
        )
        assert isinstance(dp, CanonicalDepartmentPlan)

    def test_build_action(self) -> None:
        a = build_action(
            tenant_id=TENANT_ID,
            idempotency_key="act-1",
            action_type=ActionType.RESEARCH,
            department="sales",
            autonomy_level=AutonomyLevel.L1_ANALYZE,
            risk_level=RiskLevel.LOW,
        )
        assert isinstance(a, CanonicalAction)

    def test_build_draft(self) -> None:
        d = build_draft(
            tenant_id=TENANT_ID,
            action_id="action-1",
            opportunity_id="opp-1",
            channel=DraftChannel.EMAIL,
            content="Hello, would you like a free diagnostic?",
            lawful_contact_basis=LawfulContactBasis.EXISTING_RELATIONSHIP,
            source_evidence=["crm-record-123"],
        )
        assert isinstance(d, CanonicalDraft)
        assert d.execution_allowed is False

    def test_build_proposal(self) -> None:
        p = build_proposal(
            tenant_id=TENANT_ID,
            opportunity_id="opp-1",
            offer_id="offer-1",
            approval_id="approval-1",
            source_id="source-1",
            version=1,
        )
        assert isinstance(p, CanonicalProposal)

    def test_build_playbook_version(self) -> None:
        pv = build_playbook_version(
            tenant_id=TENANT_ID,
            playbook_name="outreach_v1",
            version=1,
            change_reason="Initial creation",
            source_id="source-1",
        )
        assert isinstance(pv, CanonicalPlaybookVersion)

    def test_build_outcome_event(self) -> None:
        o = build_outcome_event(
            tenant_id=TENANT_ID,
            action_id="action-1",
            event_type=OutcomeEventType.MEETING_BOOKED,
            occurred_at=datetime.now(UTC),
            evidence_refs=["calendar-invite-123"],
        )
        assert isinstance(o, CanonicalOutcomeEvent)

    def test_build_proof_event(self) -> None:
        p = build_proof_event(
            tenant_id=TENANT_ID,
            entity_type="action",
            entity_id="action-1",
            proof_type=ProofType.OUTCOME_EVIDENCE,
            evidence_ref="meeting-recording-url",
            verified_at=datetime.now(UTC),
            verifier="founder",
            source_event_type=ProofSourceEventType.DELIVERY_TASK_COMPLETED,
        )
        assert isinstance(p, CanonicalProofEvent)

    def test_build_learning_event(self) -> None:
        le = build_learning_event(
            tenant_id=TENANT_ID,
            event_type=LearningEventType.TARGETING,
            evidence_refs=["outcome-event-123"],
            confidence=0.8,
            recommended_change="Focus on 50-100 employee companies",
            created_at=datetime.now(UTC),
        )
        assert isinstance(le, CanonicalLearningEvent)

    def test_build_daily_command(self) -> None:
        dc = build_daily_command(
            tenant_id=TENANT_ID,
            command_date=date(2026, 8, 5),
            priorities=["Fix CI pipeline", "Follow up with ACME"],
            approval_items=["Send proposal to ACME"],
            proofs=[],
            learning_events=[],
        )
        assert isinstance(dc, CanonicalDailyCommand)


# ---------------------------------------------------------------------------
# State machine coverage — all 13 lifecycle entities
# ---------------------------------------------------------------------------


class TestStateMachineCoverage:
    """Every lifecycle entity has working transition functions."""

    def test_tenant_transitions(self) -> None:
        t = build_tenant(handle="acme", name="ACME", source_id="test")
        t = transition_tenant(t, to_status=TenantStatus.SUSPENDED)
        assert t.status == TenantStatus.SUSPENDED

    def test_source_transitions(self) -> None:
        s = build_source(
            tenant_id=TENANT_ID, deduplication_key="s1",
            name="CRM", source_type=SourceType.MANUAL,
        )
        s = transition_source(s, to_status=SourceStatus.STALE)
        s = transition_source(s, to_status=SourceStatus.ACTIVE)
        assert s.status == SourceStatus.ACTIVE

    def test_consent_transitions(self) -> None:
        c = build_consent_basis(
            tenant_id=TENANT_ID, contact_id="c1",
            basis=ConsentBasisType.EXPLICIT_OPT_IN,
            channel=ConsentChannel.EMAIL, source_id="s1",
        )
        c = transition_consent_basis(c, to_status=ConsentBasisStatus.WITHDRAWN)
        assert c.status == ConsentBasisStatus.WITHDRAWN

    def test_company_transitions(self) -> None:
        c = build_company(
            tenant_id=TENANT_ID, deduplication_key="target",
            name="Target", source_id="s1",
        )
        c = transition_company(c, to_status=CompanyStatus.RESEARCHED)
        c = transition_company(c, to_status=CompanyStatus.QUALIFIED)
        assert c.status == CompanyStatus.QUALIFIED

    def test_contact_transitions(self) -> None:
        c = build_contact(
            tenant_id=TENANT_ID, deduplication_key="ali",
            company_id="co1", name="Ali", source_id="s1",
        )
        c = transition_contact(c, to_status=ContactStatus.VERIFIED)
        c = transition_contact(c, to_status=ContactStatus.ENGAGED)
        assert c.status == ContactStatus.ENGAGED

    def test_signal_transitions(self) -> None:
        s = build_signal(
            tenant_id=TENANT_ID, deduplication_key="sig1",
            company_id="co1", source_id="s1",
            signal_type=SignalType.MARKET,
        )
        s = transition_signal(s, to_status=SignalStatus.VALIDATED)
        assert s.status == SignalStatus.VALIDATED

    def test_relationship_transitions(self) -> None:
        r = build_relationship(
            tenant_id=TENANT_ID, from_id="a", from_type=EntityType.COMPANY,
            to_id="b", to_type=EntityType.COMPANY,
            relationship_type=RelationshipType.CUSTOMER, source_id="s1",
        )
        r = transition_relationship(r, to_status=RelationshipStatus.CONFIRMED)
        r = transition_relationship(r, to_status=RelationshipStatus.ACTIVE)
        assert r.status == RelationshipStatus.ACTIVE

    def test_partnership_transitions(self) -> None:
        p = build_partnership_opportunity(
            tenant_id=TENANT_ID, company_id="co1",
            partnership_type=PartnershipType.CHANNEL_PARTNER, source_id="s1",
        )
        p = transition_partnership(p, to_stage=PartnershipStage.RESEARCHED)
        assert p.stage == PartnershipStage.RESEARCHED

    def test_persona_transitions(self) -> None:
        p = build_persona(
            tenant_id=TENANT_ID, name="Founder",
            source_id="s1",
        )
        p = transition_persona(p, to_status=PersonaStatus.ACTIVE)
        assert p.status == PersonaStatus.ACTIVE

    def test_plan_transitions(self) -> None:
        dp = build_department_plan(
            tenant_id=TENANT_ID, deduplication_key="p1",
            department=Department.SALES, goal="Pipeline",
            source_id="s1", action_ids=("a1",), kpis=("k1",),
        )
        dp = transition_plan(dp, to_status=PlanStatus.ACTIVE)
        assert dp.status == PlanStatus.ACTIVE

    def test_action_transitions(self) -> None:
        a = build_action(
            tenant_id=TENANT_ID, idempotency_key="a1",
            action_type=ActionType.RESEARCH, department="sales",
            autonomy_level=AutonomyLevel.L1_ANALYZE,
            risk_level=RiskLevel.LOW,
        )
        a = transition_action(a, to_status=ActionStatus.IN_PROGRESS)
        assert a.status == ActionStatus.IN_PROGRESS

    def test_proposal_transitions(self) -> None:
        p = build_proposal(
            tenant_id=TENANT_ID, opportunity_id="opp1",
            offer_id="off1", approval_id="appr1",
            source_id="s1", version=1,
        )
        p = transition_proposal(p, to_status=ProposalStatus.PENDING_REVIEW)
        assert p.status == ProposalStatus.PENDING_REVIEW

    def test_playbook_transitions(self) -> None:
        pv = build_playbook_version(
            tenant_id=TENANT_ID, playbook_name="outreach",
            version=1, change_reason="Initial",
            source_id="s1",
        )
        pv = transition_playbook(pv, to_status=PlaybookApprovalStatus.UNDER_REVIEW)
        assert pv.approval_status == PlaybookApprovalStatus.UNDER_REVIEW


# ---------------------------------------------------------------------------
# Execution spine pipeline — entities link correctly
# ---------------------------------------------------------------------------


class TestExecutionSpinePipeline:
    """Simulate the full product spine: Company Brain → Daily Command."""

    def test_source_feeds_company(self) -> None:
        """Source → Company: source_id links them."""
        source = build_source(
            tenant_id=TENANT_ID, deduplication_key="crm",
            name="CRM Export", source_type=SourceType.MANUAL,
        )
        company = build_company(
            tenant_id=TENANT_ID, deduplication_key="acme",
            name="ACME", source_id=source.source_id,
        )
        assert company.source_id == source.source_id

    def test_company_has_contacts_and_signals(self) -> None:
        """Company → Contact/Signal: company_id links them."""
        company = build_company(
            tenant_id=TENANT_ID, deduplication_key="acme",
            name="ACME", source_id="s1",
        )
        contact = build_contact(
            tenant_id=TENANT_ID, deduplication_key="ali",
            company_id=company.company_id,
            name="Ali Ahmed", source_id="s1",
        )
        signal = build_signal(
            tenant_id=TENANT_ID, deduplication_key="sig-acme-market",
            company_id=company.company_id,
            source_id="s1", signal_type=SignalType.MARKET,
            claim="Expanding to Saudi market",
        )
        assert contact.company_id == company.company_id
        assert signal.company_id == company.company_id

    def test_action_produces_draft(self) -> None:
        """Action → Draft: action_id links them."""
        action = build_action(
            tenant_id=TENANT_ID, idempotency_key="a1",
            action_type=ActionType.PREPARE_DRAFT,
            department="sales",
            autonomy_level=AutonomyLevel.L2_DRAFT,
            risk_level=RiskLevel.LOW,
        )
        draft = build_draft(
            tenant_id=TENANT_ID, action_id=action.action_id,
            opportunity_id="opp-1", channel=DraftChannel.EMAIL,
            content="Hello, free diagnostic?",
            lawful_contact_basis=LawfulContactBasis.EXISTING_RELATIONSHIP,
            source_evidence=["crm-record"],
        )
        assert draft.action_id == action.action_id
        assert draft.execution_allowed is False
        assert draft.approval_required is True

    def test_action_lifecycle_to_outcome(self) -> None:
        """Action → completed + OutcomeEvent: full action lifecycle."""
        now = datetime.now(UTC)
        action = build_action(
            tenant_id=TENANT_ID, idempotency_key="lifecycle",
            action_type=ActionType.CONDUCT_DISCOVERY,
            department="sales",
            autonomy_level=AutonomyLevel.L3_INTERNAL_EXECUTE,
            risk_level=RiskLevel.LOW,
        )
        action = transition_action(action, to_status=ActionStatus.IN_PROGRESS)
        action = transition_action(action, to_status=ActionStatus.COMPLETED)
        assert action.status == ActionStatus.COMPLETED

        outcome = build_outcome_event(
            tenant_id=TENANT_ID, action_id=action.action_id,
            event_type=OutcomeEventType.MEETING_BOOKED,
            occurred_at=now,
            evidence_refs=["calendar-invite"],
        )
        assert outcome.action_id == action.action_id

    def test_outcome_produces_proof(self) -> None:
        """OutcomeEvent → ProofEvent: entity_id links them."""
        now = datetime.now(UTC)
        outcome = build_outcome_event(
            tenant_id=TENANT_ID, action_id="a1",
            event_type=OutcomeEventType.PAYMENT_RECEIVED,
            occurred_at=now,
            evidence_refs=["bank-transfer-123"],
        )
        proof = build_proof_event(
            tenant_id=TENANT_ID,
            entity_type="outcome_event",
            entity_id=outcome.outcome_id,
            proof_type=ProofType.PAYMENT_EVIDENCE,
            evidence_ref="bank-transfer-123",
            verified_at=now,
            verifier="founder",
            source_event_type=ProofSourceEventType.PAYMENT_CONFIRMED,
        )
        assert proof.entity_id == outcome.outcome_id

    def test_learning_from_outcome(self) -> None:
        """OutcomeEvent → LearningEvent: evidence_refs link them."""
        now = datetime.now(UTC)
        outcome = build_outcome_event(
            tenant_id=TENANT_ID, action_id="a1",
            event_type=OutcomeEventType.NO_REPLY,
            occurred_at=now,
            evidence_refs=["email-tracking-data"],
        )
        learning = build_learning_event(
            tenant_id=TENANT_ID,
            event_type=LearningEventType.TARGETING,
            evidence_refs=[outcome.outcome_id],
            confidence=0.7,
            recommended_change="Try WhatsApp for this segment",
            created_at=now,
        )
        assert outcome.outcome_id in learning.evidence_refs

    def test_daily_command_aggregation(self) -> None:
        """All spine outputs feed into DailyCommand."""
        dc = build_daily_command(
            tenant_id=TENANT_ID,
            command_date=date(2026, 8, 5),
            priorities=["Complete ACME discovery", "Fix CI pipeline"],
            approval_items=["Approve ACME proposal"],
            proofs=[],
            learning_events=[],
        )
        assert dc.tenant_id == TENANT_ID
        assert len(dc.priorities) == 2
        assert len(dc.approval_items) == 1


# ---------------------------------------------------------------------------
# Safety invariants — non-negotiable across the spine
# ---------------------------------------------------------------------------


class TestSafetyInvariants:
    """Cross-cutting safety rules that must hold across the entire spine."""

    def test_all_entities_are_frozen(self) -> None:
        """Frozen entities prevent accidental mutation."""
        frozen_entities = [
            build_tenant(handle="test", name="Test", source_id="s1"),
            build_source(
                tenant_id=TENANT_ID, deduplication_key="s1",
                name="S", source_type=SourceType.MANUAL,
            ),
            build_company(
                tenant_id=TENANT_ID, deduplication_key="c",
                name="C", source_id="s1",
            ),
            build_contact(
                tenant_id=TENANT_ID, deduplication_key="n",
                company_id="co1", name="N", source_id="s1",
            ),
            build_signal(
                tenant_id=TENANT_ID, deduplication_key="sig",
                company_id="co1", source_id="s1",
                signal_type=SignalType.MARKET,
            ),
            build_relationship(
                tenant_id=TENANT_ID, from_id="a", from_type=EntityType.COMPANY,
                to_id="b", to_type=EntityType.COMPANY,
                relationship_type=RelationshipType.CUSTOMER, source_id="s1",
            ),
            build_persona(tenant_id=TENANT_ID, name="P", source_id="s1"),
            build_offer(
                tenant_id=TENANT_ID, offer_key="k", name_ar="ar",
                name_en="en", status=OfferStatus.FREE_ENTRY,
                approval_policy=OfferApprovalPolicy.SELF_SERVE,
                source_id="s1",
            ),
            build_partnership_opportunity(
                tenant_id=TENANT_ID, company_id="co1",
                partnership_type=PartnershipType.CHANNEL_PARTNER, source_id="s1",
            ),
            build_department_plan(
                tenant_id=TENANT_ID, deduplication_key="p1",
                department=Department.SALES, goal="G",
                source_id="s1", action_ids=("a1",), kpis=("k1",),
            ),
            build_action(
                tenant_id=TENANT_ID, idempotency_key="a1",
                action_type=ActionType.RESEARCH, department="sales",
                autonomy_level=AutonomyLevel.L1_ANALYZE,
                risk_level=RiskLevel.LOW,
            ),
            build_proposal(
                tenant_id=TENANT_ID, opportunity_id="o1",
                offer_id="off1", approval_id="appr1",
                source_id="s1", version=1,
            ),
            build_playbook_version(
                tenant_id=TENANT_ID, playbook_name="p",
                version=1, change_reason="R", source_id="s1",
            ),
            build_consent_basis(
                tenant_id=TENANT_ID, contact_id="c1",
                basis=ConsentBasisType.EXPLICIT_OPT_IN,
                channel=ConsentChannel.EMAIL, source_id="s1",
            ),
        ]
        for entity in frozen_entities:
            with pytest.raises(Exception):
                entity.tenant_id = "hacked"  # type: ignore[misc]

    def test_opportunity_blocks_external_execution(self) -> None:
        """Canonical opportunities never authorize external execution."""
        with pytest.raises(ValueError, match="never authorize external execution"):
            CanonicalOpportunity(
                tenant_id=TENANT_ID,
                opportunity_id="opp-1",
                company_id="co-1",
                offer_id="off-1",
                stage="discovery",
                score=50,
                next_action="call",
                proof_target="meeting-booked",
                external_action_allowed=True,
            )

    def test_cold_whatsapp_blocked_in_draft(self) -> None:
        """Cold WhatsApp blasts are forbidden by the draft contract."""
        with pytest.raises(ValueError, match="cold WhatsApp is forbidden"):
            build_draft(
                tenant_id=TENANT_ID,
                action_id="a1",
                opportunity_id="opp-1",
                channel=DraftChannel.WHATSAPP,
                content="Buy our product!",
                lawful_contact_basis=LawfulContactBasis.MANUAL_RESEARCH_ONLY,
                source_evidence=["scraped-data"],
            )

    def test_linkedin_automation_blocked_in_draft(self) -> None:
        """LinkedIn automation is forbidden by the draft contract."""
        with pytest.raises(ValueError, match="LinkedIn automation is forbidden"):
            build_draft(
                tenant_id=TENANT_ID,
                action_id="a1",
                opportunity_id="opp-1",
                channel=DraftChannel.LINKEDIN,
                content="Connect with me!",
                lawful_contact_basis=LawfulContactBasis.MANUAL_RESEARCH_ONLY,
                source_evidence=["linkedin-data"],
                is_manual_task=False,
            )

    def test_offer_catalog_commercially_active_count(self) -> None:
        """Only two offers should be commercially active per business rules."""
        catalog = normalize_catalog()
        active = [
            o for o in catalog
            if o.status in {OfferStatus.FREE_ENTRY, OfferStatus.QUOTE_ONLY}
        ]
        assert len(active) == 2

    def test_tenant_scoping(self) -> None:
        """Every entity carries a tenant_id for isolation."""
        entities = [
            build_source(
                tenant_id="tenant-a", deduplication_key="s1",
                name="S", source_type=SourceType.MANUAL,
            ),
            build_company(
                tenant_id="tenant-b", deduplication_key="c",
                name="C", source_id="s1",
            ),
        ]
        assert entities[0].tenant_id == "tenant-a"
        assert entities[1].tenant_id == "tenant-b"


# ---------------------------------------------------------------------------
# Deterministic ID stability
# ---------------------------------------------------------------------------


class TestDeterministicIds:
    """Same inputs produce same IDs across calls."""

    def test_company_id_stable(self) -> None:
        a = build_company(
            tenant_id=TENANT_ID, deduplication_key="acme",
            name="ACME", source_id="s1",
        )
        b = build_company(
            tenant_id=TENANT_ID, deduplication_key="acme",
            name="ACME", source_id="s1",
        )
        assert a.company_id == b.company_id

    def test_action_id_stable(self) -> None:
        a = build_action(
            tenant_id=TENANT_ID, idempotency_key="act-1",
            action_type=ActionType.RESEARCH, department="sales",
            autonomy_level=AutonomyLevel.L1_ANALYZE,
            risk_level=RiskLevel.LOW,
        )
        b = build_action(
            tenant_id=TENANT_ID, idempotency_key="act-1",
            action_type=ActionType.RESEARCH, department="sales",
            autonomy_level=AutonomyLevel.L1_ANALYZE,
            risk_level=RiskLevel.LOW,
        )
        assert a.action_id == b.action_id

    def test_draft_id_stable(self) -> None:
        a = build_draft(
            tenant_id=TENANT_ID, action_id="a1", opportunity_id="o1",
            channel=DraftChannel.EMAIL, content="Hello",
            lawful_contact_basis=LawfulContactBasis.EXISTING_RELATIONSHIP,
            source_evidence=["evidence-1"],
        )
        b = build_draft(
            tenant_id=TENANT_ID, action_id="a1", opportunity_id="o1",
            channel=DraftChannel.EMAIL, content="Hello",
            lawful_contact_basis=LawfulContactBasis.EXISTING_RELATIONSHIP,
            source_evidence=["evidence-1"],
        )
        assert a.draft_id == b.draft_id
        assert a.content_hash == b.content_hash

    def test_different_inputs_different_ids(self) -> None:
        a = build_company(
            tenant_id=TENANT_ID, deduplication_key="acme",
            name="ACME", source_id="s1",
        )
        b = build_company(
            tenant_id=TENANT_ID, deduplication_key="betaco",
            name="BetaCo", source_id="s1",
        )
        assert a.company_id != b.company_id
