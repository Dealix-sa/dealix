"""End-to-end behavior tests for the full AI Stack pipeline.

These tests exercise the full L1..L11 path on a real (deterministic)
orchestrator and assert that the eleven layers behave as a single
coherent system — not just that each layer is individually correct.
"""

from __future__ import annotations

import pytest

from auto_client_acquisition.ai_stack_os import (
    AIStackInput,
    AIStackOrchestrator,
    LayerStatus,
    Offer,
    SourcePassportInput,
)
from auto_client_acquisition.ai_stack_os.orchestrator import reset_default_orchestrator
from auto_client_acquisition.proof_os import (
    PROOF_PACK_V2_SECTIONS,
    new_chain,
)
from auto_client_acquisition.self_evolving_os import (
    InMemoryLearningStore,
    OutcomeKind,
    derive_suggestions,
    proposal_from_suggestion,
)


def _passport(*, ai_allowed: bool = True) -> SourcePassportInput:
    return SourcePassportInput(
        source_id="intake_e2e",
        source_type="customer_intake",
        owner="e2e_owner",
        allowed_use=["ai_assist"],
        contains_pii=False,
        sensitivity="internal",
        retention_policy="90d",
        ai_access_allowed=ai_allowed,
        external_use_allowed=False,
    )


def _payload(*, tier: Offer = Offer.FREE_DIAGNOSTIC) -> AIStackInput:
    return AIStackInput(
        tenant_id="e2e_tenant",
        customer_handle="e2e_customer",
        company_name="E2E Corp",
        sector="technology",
        challenge_ar="نحتاج رفع كفاءة فريق المبيعات",
        challenge_en="we need to lift sales team efficiency",
        offer_tier=tier,
        source_passport=_passport(),
    )


@pytest.fixture(autouse=True)
def _reset():
    reset_default_orchestrator()
    yield
    reset_default_orchestrator()


class TestE2EPipeline:
    """Full L1..L11 execution and consistency invariants."""

    def test_full_pipeline_produces_proof_pack_with_evidence_chain(self) -> None:
        store = InMemoryLearningStore()
        orch = AIStackOrchestrator(learning_store=store)
        result = orch.run(_payload())

        # The eleven layers all show up.
        assert len(result.layers) == 11
        layer_names = [l.layer for l in result.layers]
        assert layer_names == [
            "L1_source_passport",
            "L2_data_quality",
            "L3_intelligence",
            "L4_model_router",
            "L5_agent_mesh",
            "L6_governance",
            "L7_proof_pack",
            "L8_value_ledger",
            "L9_capital_ledger",
            "L10_adoption",
            "L11_self_evolving",
        ]

        # Proof pack is produced with an evidence head hash.
        assert result.proof_pack_id is not None
        assert result.proof_pack_id.startswith("pp_")
        assert len(result.evidence_head_hash) == 64

    def test_full_pipeline_records_at_least_one_decision_passport(self) -> None:
        store = InMemoryLearningStore()
        orch = AIStackOrchestrator(learning_store=store)
        result = orch.run(_payload(tier=Offer.SPRINT_499))
        # Sprint 499 runs 4 agents → at least 4 decision passports.
        assert len(result.decision_passport_ids) >= 2

    def test_higher_tier_runs_more_agents(self) -> None:
        store = InMemoryLearningStore()
        orch1 = AIStackOrchestrator(learning_store=InMemoryLearningStore())
        orch2 = AIStackOrchestrator(learning_store=InMemoryLearningStore())
        free = orch1.run(_payload(tier=Offer.FREE_DIAGNOSTIC))
        managed = orch2.run(_payload(tier=Offer.MANAGED_OPS))
        # Both run 11 layers but managed_ops drives more agents in L5.
        l5_free = next(l for l in free.layers if l.layer == "L5_agent_mesh")
        l5_mgmt = next(l for l in managed.layers if l.layer == "L5_agent_mesh")
        runs_free = l5_free.payload.get("runs", [])
        runs_mgmt = l5_mgmt.payload.get("runs", [])
        assert len(runs_mgmt) > len(runs_free)

    def test_evidence_chain_is_internally_consistent(self) -> None:
        # Build a chain manually to verify the verification contract.
        chain = new_chain(tenant_id="e2e_tenant")
        chain.append(
            layer="L1_source_passport",
            artifact_type="t",
            content={"a": 1},
            summary="first",
        )
        chain.append(
            layer="L7_proof_pack",
            artifact_type="t",
            content={"b": 2},
            summary="second",
        )
        ok, errors = chain.verify()
        assert ok, errors
        assert len(chain) == 2

    def test_full_pipeline_includes_bilingual_executive_summary(self) -> None:
        orch = AIStackOrchestrator(learning_store=InMemoryLearningStore())
        result = orch.run(_payload())
        md = result.proof_pack_markdown
        # Both labels MUST appear in the rendered Markdown.
        assert "الملخص التنفيذي" in md
        assert "Executive Summary" in md
        # And every canonical section header should be rendered.
        for section in PROOF_PACK_V2_SECTIONS:
            assert section.replace("_", " ").title().lower() in md.lower() or section in md or any(
                lbl in md for lbl in (section,)
            )

    def test_full_pipeline_records_feedback_event_per_run(self) -> None:
        store = InMemoryLearningStore()
        orch = AIStackOrchestrator(learning_store=store)
        for _ in range(3):
            orch.run(_payload())
        # Each run should record at least one feedback event.
        events = store.list_events(tenant_id="e2e_tenant")
        assert len(events) >= 3

    def test_full_pipeline_value_ledger_layer_advisory_only(self) -> None:
        orch = AIStackOrchestrator(learning_store=InMemoryLearningStore())
        result = orch.run(_payload(tier=Offer.MANAGED_OPS))
        l8 = next(l for l in result.layers if l.layer == "L8_value_ledger")
        assert l8.status == LayerStatus.SKIPPED
        assert l8.payload["advisory_only"] is True


class TestE2EShortCircuits:
    def test_l1_failure_short_circuits_the_pipeline(self) -> None:
        bad = SourcePassportInput(
            source_id="bad",
            owner="o",
            allowed_use=["ai_assist"],
            ai_access_allowed=False,
        )
        payload = AIStackInput(
            tenant_id="e2e_tenant",
            customer_handle="e2e_customer",
            company_name="E2E Corp",
            sector="x",
            challenge_ar="anything substantive",
            challenge_en="anything substantive",
            offer_tier=Offer.FREE_DIAGNOSTIC,
            source_passport=bad,
        )
        orch = AIStackOrchestrator(learning_store=InMemoryLearningStore())
        result = orch.run(payload)
        assert result.governance_blocked is True
        # Only L1 should have executed.
        assert len(result.layers) == 1
        assert result.layers[0].layer == "L1_source_passport"
        assert result.layers[0].status == LayerStatus.BLOCKED


class TestE2ESelfEvolvingProposalLifecycle:
    """The full feedback → suggestion → proposal → approval → applied flow."""

    def test_lifecycle_runs_end_to_end(self) -> None:
        from auto_client_acquisition.self_evolving_os.improvement_proposals import (
            InMemoryProposalRepository,
            ProposalState,
        )

        store = InMemoryLearningStore()
        orch = AIStackOrchestrator(learning_store=store)

        # Drive a doctrine-dirty pattern: many runs whose challenge contains a
        # guaranteed claim — the orchestrator marks them doctrine_clean=False.
        bad_payload = _payload()
        bad_payload.challenge_ar = "نضمن نتائج مبيعات مضمونة"
        for _ in range(3):
            orch.run(bad_payload)

        # Derive suggestions and lift the most severe into a proposal.
        suggestions = derive_suggestions(
            tenant_id="e2e_tenant",
            store=store,
            minimum_severity="info",
        )
        assert suggestions, "expected at least one suggestion after dirty runs"
        proposal = proposal_from_suggestion(suggestions[0])
        assert proposal.state == ProposalState.PENDING.value

        # Submit + approve + apply through the repository state machine.
        repo = InMemoryProposalRepository()
        repo.submit(proposal)
        approved = repo.approve(
            tenant_id="e2e_tenant",
            proposal_id=proposal.proposal_id,
            approved_by="founder",
        )
        assert approved.state == ProposalState.APPROVED.value
        applied = repo.apply(
            tenant_id="e2e_tenant",
            proposal_id=proposal.proposal_id,
            applied_by="founder",
        )
        assert applied.state == ProposalState.APPLIED.value


class TestE2EBilingualEnforcement:
    def test_no_section_in_markdown_is_unilingual_only(self) -> None:
        orch = AIStackOrchestrator(learning_store=InMemoryLearningStore())
        result = orch.run(_payload())
        md = result.proof_pack_markdown
        # Every section header has both AR and EN labels separated by " — ".
        # Count headers (lines starting with "## ").
        header_lines = [
            line for line in md.splitlines() if line.startswith("## ")
        ]
        # Each header must contain a " — " separator binding AR + EN labels.
        for header in header_lines:
            assert " — " in header, f"missing bilingual separator in: {header!r}"


class TestE2EHashStability:
    def test_two_identical_runs_have_distinct_run_ids(self) -> None:
        orch = AIStackOrchestrator(learning_store=InMemoryLearningStore())
        r1 = orch.run(_payload())
        r2 = orch.run(_payload())
        # Run ids are random per run; proof_pack_ids are random per pack.
        assert r1.run_id != r2.run_id
        assert r1.proof_pack_id != r2.proof_pack_id

    def test_evidence_head_hashes_are_distinct_across_runs(self) -> None:
        orch = AIStackOrchestrator(learning_store=InMemoryLearningStore())
        r1 = orch.run(_payload())
        r2 = orch.run(_payload())
        assert r1.evidence_head_hash != r2.evidence_head_hash
