"""End-to-end scenario test for the full Company Intelligence spine.

Simulates a realistic Saudi B2B customer journey:
  1. Source passport → CanonicalSource (data provenance)
  2. Lead → CanonicalCompany + CanonicalContact (graph entities)
  3. SignalDetection → CanonicalSignal (market intelligence)
  4. ConsentRecord → CanonicalConsentBasis (privacy)
  5. Pipeline Lead → CanonicalOpportunity (execution)
  6. NextBestAction → CanonicalAction (action queue)
  7. Revenue Graph edge → CanonicalRelationship (graph edges)
  8. All entities are frozen, tenant-scoped, evidence-graded
  9. State machine transitions work end-to-end
 10. Daily Command can be built from accumulated entities

This test does NOT touch databases, networks, or LLMs — it exercises
only the persistence-neutral contract and adapter layers.
"""
from __future__ import annotations

from datetime import UTC, datetime
from types import SimpleNamespace

import pytest

from dealix.company_intelligence import (
    ActionStatus,
    CanonicalAction,
    CanonicalCompany,
    CanonicalConsentBasis,
    CanonicalContact,
    CanonicalDailyCommand,
    CanonicalLearningEvent,
    CanonicalOpportunity,
    CanonicalPlaybookVersion,
    CanonicalProposal,
    CanonicalRelationship,
    CanonicalSignal,
    CanonicalSource,
    CompanyStatus,
    ConsentBasisStatus,
    ContactStatus,
    EntityType,
    LearningEventType,
    OpportunityStage,
    PlaybookApprovalStatus,
    ProposalStatus,
    RelationshipStatus,
    SignalStatus,
    SourceStatus,
    build_daily_command,
    normalize_consent,
    normalize_graph_edge,
    normalize_lead_to_company,
    normalize_lead_to_contact,
    normalize_learning_event,
    normalize_next_best_action,
    normalize_pipeline_lead,
    normalize_proposal,
    normalize_sector_playbook,
    normalize_signal,
    normalize_source_passport,
    normalize_win_loss,
    transition_action,
    transition_company,
    transition_contact,
    transition_opportunity,
    transition_playbook,
    transition_proposal,
    transition_signal,
)

TENANT_ID = "tenant-acme-sa"


class TestSaudiBtoEndToEnd:
    """Full customer journey from raw data → Daily Command."""

    def _build_source(self) -> CanonicalSource:
        """Step 1: Register a data source."""
        passport = SimpleNamespace(
            source_id="SRC-CRM-ACME",
            source_type="crm",
            owner="acme_sa",
            allowed_use=["internal_analysis", "draft_only"],
            contains_pii=True,
            sensitivity="medium",
            relationship_status="existing_relationship",
            retention_policy="1_year",
            ai_access_allowed=True,
            external_use_allowed=False,
        )
        source = normalize_source_passport(passport, tenant_id=TENANT_ID)
        assert isinstance(source, CanonicalSource)
        assert source.status == SourceStatus.ACTIVE
        return source

    def _build_company_and_contact(
        self, source: CanonicalSource
    ) -> tuple[CanonicalCompany, CanonicalContact]:
        """Step 2: Ingest a lead → Company + Contact."""
        lead = SimpleNamespace(
            id="lead-acme-001",
            source="warm_intro",
            company_name="شركة أكمي السعودية",
            contact_name="أحمد الراشد",
            contact_email="ahmed@acme.sa",
            contact_phone="+966512345678",
            contact_channel="whatsapp",
            sector="B2B SaaS",
            company_size="80",
            region="Riyadh",
            budget=15000.0,
            message="نبحث عن نظام لإدارة العمليات التجارية",
            urgency_score=0.8,
            fit_score=0.85,
            status="new",
            pain_points=["no CRM", "manual follow-up"],
            locale="ar",
            created_at=datetime(2026, 8, 1, 12, 0, 0),
            dedup_hash="acme_sa_hash_001",
        )

        company = normalize_lead_to_company(
            lead, tenant_id=TENANT_ID, source_id=source.source_id
        )
        assert isinstance(company, CanonicalCompany)
        assert company.name == "شركة أكمي السعودية"
        assert company.icp_fit_score == 0.85
        assert company.employee_count_estimate == 80
        assert company.status == CompanyStatus.DISCOVERED

        contact = normalize_lead_to_contact(
            lead,
            tenant_id=TENANT_ID,
            source_id=source.source_id,
            company_id=company.company_id,
        )
        assert isinstance(contact, CanonicalContact)
        assert contact.name == "أحمد الراشد"
        assert contact.company_id == company.company_id
        assert contact.consent_status == "unknown"

        return company, contact

    def _build_signal(self, company: CanonicalCompany) -> CanonicalSignal:
        """Step 3: Detect a market signal."""
        detection = SimpleNamespace(
            company_id=company.company_id,
            signal_type="hiring_sales_rep",
            detected_at=datetime(2026, 8, 2, 9, 0, 0),
            source="linkedin_jobs",
            confidence=0.9,
            evidence_url="https://linkedin.com/jobs/acme-sa-sales-rep",
            payload={"title": "Senior Sales Rep", "location": "Riyadh"},
        )
        signal = normalize_signal(detection, tenant_id=TENANT_ID)
        assert isinstance(signal, CanonicalSignal)
        assert signal.status == SignalStatus.RAW
        return signal

    def _build_consent(self, contact: CanonicalContact) -> CanonicalConsentBasis:
        """Step 4: Record consent basis."""
        record = SimpleNamespace(
            record_id="cons-acme-001",
            customer_id=TENANT_ID,
            contact_id=contact.contact_id,
            record_type="consent_granted",
            lawful_basis="consent",
            purpose="outreach",
            channel="whatsapp",
            source="explicit_whatsapp",
            occurred_at=datetime(2026, 8, 2, 10, 0, 0),
            expires_at=None,
            proof_url="https://proof.dealix.me/consent/acme-001",
            metadata={"contact_name": "أحمد الراشد"},
        )
        consent = normalize_consent(record, tenant_id=TENANT_ID)
        assert isinstance(consent, CanonicalConsentBasis)
        assert consent.status == ConsentBasisStatus.ACTIVE
        return consent

    def _build_opportunity(
        self, company: CanonicalCompany
    ) -> CanonicalOpportunity:
        """Step 5: Create opportunity from pipeline lead."""
        pipeline_lead = SimpleNamespace(
            id="pipe-acme-001",
            slot_id="slot-acme",
            sector="B2B SaaS",
            region="Riyadh",
            stage="diagnostic_delivered",
            commitment_evidence="",
            payment_evidence="",
            created_at=datetime(2026, 8, 5, 14, 0, 0, tzinfo=UTC),
        )
        opp = normalize_pipeline_lead(
            pipeline_lead,
            tenant_id=TENANT_ID,
            company_id=company.company_id,
            offer_id="offer-revenue-pilot",
        )
        assert isinstance(opp, CanonicalOpportunity)
        assert opp.stage == OpportunityStage.APPROVAL
        assert opp.external_action_allowed is False
        return opp

    def _build_action(
        self, opportunity: CanonicalOpportunity
    ) -> CanonicalAction:
        """Step 6: Generate next-best-action."""
        nba = SimpleNamespace(
            action="open_whatsapp_with_arabic_personalization",
            channel="whatsapp",
            rationale=(
                "الشركة تستخدم WhatsApp Business — فتح المحادثة برسالة "
                "عربية مخصصة يرفع معدل الرد بنسبة 3× مقارنة بالإيميل البارد."
            ),
            expected_reply_lift=2.4,
            confidence=0.7,
            playbook_id=None,
        )
        action = normalize_next_best_action(
            nba,
            tenant_id=TENANT_ID,
            opportunity_id=opportunity.opportunity_id,
            company_id=opportunity.company_id,
        )
        assert isinstance(action, CanonicalAction)
        assert action.external_effect is True
        assert action.approval_required is True
        assert action.status == ActionStatus.QUEUED
        return action

    def _build_relationship(
        self, company: CanonicalCompany
    ) -> CanonicalRelationship:
        """Step 7: Bridge a Revenue Graph edge."""
        edge = SimpleNamespace(
            src_id=company.company_id,
            dst_id="company-dealix-internal",
            edge_type="decides_at",
            weight=0.6,
            properties={"description": "Warm intro via founder network"},
            last_updated=None,
        )
        rel = normalize_graph_edge(
            edge,
            tenant_id=TENANT_ID,
            source_id="revenue_graph",
            from_type=EntityType.COMPANY,
            to_type=EntityType.COMPANY,
        )
        assert isinstance(rel, CanonicalRelationship)
        assert rel.status == RelationshipStatus.DISCOVERED
        assert rel.strength == "warm"
        return rel

    def _build_proposal(
        self, opportunity: CanonicalOpportunity
    ) -> CanonicalProposal:
        """Step 8: Generate a proposal from the opportunity."""
        proposal_data = SimpleNamespace(
            id="prop_acme_001",
            prospect_id=opportunity.company_id,
            product_id="revenue_command_pilot",
            sector="B2B SaaS",
            problem="لا يوجد نظام CRM — كل المتابعة يدوية",
            proposed_solution="Revenue Command Pilot لمدة 30 يوم",
            scope=["جودة البيانات", "تصنيف الحسابات", "مسودات ثنائية اللغة"],
            out_of_scope=["no_scraping", "no_cold_whatsapp"],
            timeline="30 يوم",
            price_min_sar=0,
            price_max_sar=0,
            assumptions=["وصول مباشر للمؤسس", "بيانات متاحة"],
            evidence_level=65,
            risks=["جودة البيانات غير معروفة"],
            payment_terms="quote after discovery",
            next_step="جدولة مكالمة الاكتشاف",
            approval_status="pending_approval",
            quality_issues=[],
        )
        proposal = normalize_proposal(
            proposal_data,
            tenant_id=TENANT_ID,
            opportunity_id=opportunity.opportunity_id,
            approval_id="approval-acme-001",
        )
        assert isinstance(proposal, CanonicalProposal)
        assert proposal.status == ProposalStatus.PENDING_REVIEW
        assert proposal.offer_id == "revenue_command_pilot"
        assert proposal.company_id == opportunity.company_id
        return proposal

    def _build_playbook(self) -> CanonicalPlaybookVersion:
        """Step 9: Register a sector playbook."""
        playbook_data = SimpleNamespace(
            sector_id="b2b_saas",
            sector_ar="برمجيات B2B",
            sector_en="B2B SaaS",
            pain_points_ar=(
                "صعوبة جلب عملاء بدون فريق مبيعات",
                "عدم وجود نظام CRM فعّال",
                "متابعة يدوية للعملاء المحتملين",
            ),
            top_objections=("OBJ_TRUST_001", "OBJ_PRICE_001"),
            opening_lines_ar=(
                "لاحظنا أنكم تبحثون عن حلول لإدارة العمليات التجارية",
            ),
            best_offer_angle_ar="نظام يدير العمليات التجارية بالكامل",
            buying_committee=("CEO", "VP Sales"),
            seasonal_peaks_ar=("Q1", "Q3"),
            benchmarks={
                "reply_rate_p50": 0.074,
                "meeting_rate_p50": 0.32,
                "win_rate_p50": 0.18,
                "cycle_days_p50": 45,
            },
            recommended_channel_mix={
                "whatsapp": 0.55,
                "email": 0.25,
                "linkedin": 0.10,
                "phone": 0.10,
            },
            whatsapp_tone="warm",
            case_study_template_ar="شركة {brand} استخدمت Dealix لمدة {months} شهر",
            avg_deal_value_sar=50_000,
            avg_cycle_days=45,
        )
        playbook = normalize_sector_playbook(
            playbook_data, tenant_id=TENANT_ID
        )
        assert isinstance(playbook, CanonicalPlaybookVersion)
        assert playbook.approval_status == PlaybookApprovalStatus.PROPOSED
        assert playbook.confidence >= 0.8
        return playbook

    def _build_learning_from_flywheel(self) -> CanonicalLearningEvent:
        """Step 10: Normalize a flywheel learning event."""
        event = SimpleNamespace(
            kind="reply_received",
            customer_handle="alpha-tech-sa",
            timestamp=datetime(2026, 8, 5, 14, 0, tzinfo=UTC),
            sector="b2b_saas",
            channel="whatsapp",
            offer="revenue_command_pilot",
            succeeded=True,
            notes_en="Customer replied positively to pilot proposal",
            notes_ar="العميل رد بإيجابية على عرض الباقة التجريبية",
        )
        learning = normalize_learning_event(event, tenant_id=TENANT_ID)
        assert isinstance(learning, CanonicalLearningEvent)
        assert learning.event_type == LearningEventType.MESSAGE
        assert learning.confidence == 0.7  # succeeded=True
        assert learning.hypothesis_only is True
        assert learning.applied is False
        return learning

    def _build_learning_from_win_loss(self) -> CanonicalLearningEvent:
        """Step 11: Normalize a win/loss retrospective."""
        record = SimpleNamespace(
            outcome="won",
            company="Alpha Tech SA",
            lesson="العميل اقتنع بسبب التشخيص المجاني",
            next_change="تقديم تشخيص أسرع في أول يومين",
            sector="b2b_saas",
            channel="whatsapp",
            offer="revenue_command_pilot",
            reason="value_demonstrated",
            objection="initial_price_concern",
            created_at=datetime(2026, 8, 6, 10, 0, tzinfo=UTC),
        )
        learning = normalize_win_loss(record, tenant_id=TENANT_ID)
        assert isinstance(learning, CanonicalLearningEvent)
        assert learning.event_type == LearningEventType.NEGOTIATION
        assert learning.confidence == 0.7  # won
        assert "العميل اقتنع" in learning.recommended_change
        assert learning.applied is False
        return learning

    # ------------------------------------------------------------------
    # Full end-to-end test
    # ------------------------------------------------------------------

    def test_full_customer_journey(self) -> None:
        """Walk through the entire spine from raw data to entity graph."""
        # Step 1: Source
        source = self._build_source()

        # Step 2: Company + Contact
        company, contact = self._build_company_and_contact(source)

        # Step 3: Signal
        signal = self._build_signal(company)

        # Step 4: Consent
        consent = self._build_consent(contact)

        # Step 5: Opportunity
        opportunity = self._build_opportunity(company)

        # Step 6: Action
        action = self._build_action(opportunity)

        # Step 7: Relationship
        relationship = self._build_relationship(company)

        # Step 8: Proposal
        proposal = self._build_proposal(opportunity)

        # Step 9: Playbook
        playbook = self._build_playbook()

        # Step 10: Flywheel learning event
        learning_flywheel = self._build_learning_from_flywheel()

        # Step 11: Win/loss learning event
        learning_win_loss = self._build_learning_from_win_loss()

        # Verify all entities share the same tenant
        all_entities = [
            source, company, contact, signal, consent,
            opportunity, action, relationship, proposal, playbook,
            learning_flywheel, learning_win_loss,
        ]
        for entity in all_entities:
            assert entity.tenant_id == TENANT_ID

        # Verify all entities are frozen
        for entity in all_entities:
            with pytest.raises(Exception):
                entity.tenant_id = "tampered"  # type: ignore[misc]

    def test_state_machine_progression(self) -> None:
        """Verify state machine transitions work across entities."""
        source = self._build_source()
        company, contact = self._build_company_and_contact(source)
        signal = self._build_signal(company)
        opportunity = self._build_opportunity(company)
        action = self._build_action(opportunity)

        # Company: DISCOVERED → RESEARCHED → QUALIFIED
        company = transition_company(company, to_status=CompanyStatus.RESEARCHED)
        company = transition_company(company, to_status=CompanyStatus.QUALIFIED)
        assert company.status == CompanyStatus.QUALIFIED

        # Contact: IDENTIFIED → VERIFIED → ENGAGED
        contact = transition_contact(contact, to_status=ContactStatus.VERIFIED)
        contact = transition_contact(contact, to_status=ContactStatus.ENGAGED)
        assert contact.status == ContactStatus.ENGAGED

        # Signal: RAW → VALIDATED → LINKED
        signal = transition_signal(signal, to_status=SignalStatus.VALIDATED)
        signal = transition_signal(signal, to_status=SignalStatus.LINKED)
        assert signal.status == SignalStatus.LINKED

        # Opportunity: APPROVAL → CONVERSATION → PILOT
        opportunity = transition_opportunity(
            opportunity, to_stage=OpportunityStage.CONVERSATION
        )
        opportunity = transition_opportunity(
            opportunity, to_stage=OpportunityStage.PILOT
        )
        assert opportunity.stage == OpportunityStage.PILOT

        # Action: QUEUED → IN_PROGRESS → AWAITING_APPROVAL → APPROVED
        action = transition_action(action, to_status=ActionStatus.IN_PROGRESS)
        action = transition_action(
            action, to_status=ActionStatus.AWAITING_APPROVAL
        )
        assert action.status == ActionStatus.AWAITING_APPROVAL

        # Proposal: PENDING_REVIEW → APPROVED
        proposal = self._build_proposal(opportunity)
        proposal = transition_proposal(
            proposal, to_status=ProposalStatus.APPROVED
        )
        assert proposal.status == ProposalStatus.APPROVED

        # Playbook: PROPOSED → UNDER_REVIEW → APPROVED
        playbook = self._build_playbook()
        playbook = transition_playbook(
            playbook, to_status=PlaybookApprovalStatus.UNDER_REVIEW
        )
        playbook = transition_playbook(
            playbook, to_status=PlaybookApprovalStatus.APPROVED
        )
        assert playbook.approval_status == PlaybookApprovalStatus.APPROVED

    def test_daily_command_from_entities(self) -> None:
        """Build a Daily Command from accumulated spine entities."""
        from datetime import date

        source = self._build_source()
        company, contact = self._build_company_and_contact(source)
        signal = self._build_signal(company)
        opportunity = self._build_opportunity(company)
        action = self._build_action(opportunity)
        learning_flywheel = self._build_learning_from_flywheel()
        learning_win_loss = self._build_learning_from_win_loss()

        # Build a Daily Command incorporating all entities
        command = build_daily_command(
            tenant_id=TENANT_ID,
            command_date=date(2026, 8, 6),
            priorities=[
                action.action_id,
                opportunity.opportunity_id,
                signal.signal_id,
            ],
            approval_items=[],
            proofs=[],
            learning_events=[learning_flywheel, learning_win_loss],
        )
        assert isinstance(command, CanonicalDailyCommand)
        assert command.tenant_id == TENANT_ID
        assert action.action_id in command.priorities
        assert opportunity.opportunity_id in command.priorities
        assert learning_flywheel.learning_id in command.learning_ids
        assert learning_win_loss.learning_id in command.learning_ids

    def test_invalid_state_transitions_blocked(self) -> None:
        """Verify invalid transitions are rejected across entities."""
        source = self._build_source()
        company, contact = self._build_company_and_contact(source)
        opportunity = self._build_opportunity(company)

        # Cannot skip from DISCOVERED to ACTIVE
        with pytest.raises(ValueError, match="invalid"):
            transition_company(company, to_status=CompanyStatus.ACTIVE)

        # Cannot go from IDENTIFIED to ENGAGED (must verify first)
        with pytest.raises(ValueError, match="invalid"):
            transition_contact(contact, to_status=ContactStatus.ENGAGED)

        # Cannot go from APPROVAL to WON directly
        with pytest.raises(ValueError, match="invalid"):
            transition_opportunity(
                opportunity, to_stage=OpportunityStage.WON
            )

        # Cannot go from PENDING_REVIEW to ACCEPTED (must approve + send)
        proposal = self._build_proposal(opportunity)
        with pytest.raises(ValueError, match="invalid"):
            transition_proposal(
                proposal, to_status=ProposalStatus.ACCEPTED
            )

        # Cannot go from PROPOSED to APPROVED directly (must review first)
        playbook = self._build_playbook()
        with pytest.raises(ValueError, match="invalid"):
            transition_playbook(
                playbook, to_status=PlaybookApprovalStatus.APPROVED
            )

    def test_adapter_cross_referencing(self) -> None:
        """Verify entities can be cross-referenced via IDs."""
        source = self._build_source()
        company, contact = self._build_company_and_contact(source)
        signal = self._build_signal(company)
        opportunity = self._build_opportunity(company)

        # Contact → Company linkage
        assert contact.company_id == company.company_id

        # Signal → Company linkage (via company_id field on signal)
        assert signal.company_id == company.company_id

        # Opportunity → Company linkage
        assert opportunity.company_id == company.company_id

        # Proposal → Opportunity + Company linkage
        proposal = self._build_proposal(opportunity)
        assert proposal.opportunity_id == opportunity.opportunity_id
        assert proposal.company_id == opportunity.company_id

        # Source ← Company provenance
        assert company.source_id == source.source_id
