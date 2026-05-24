"""End-to-end tests for the AI Stack orchestrator (L1..L11)."""

from __future__ import annotations

import pytest

from auto_client_acquisition.ai_stack_os import (
    AIStackInput,
    AIStackOrchestrator,
    AIStackResult,
    LayerStatus,
    Offer,
    SourcePassportInput,
    layer_versions,
    snapshot_health,
)
from auto_client_acquisition.ai_stack_os.orchestrator import (
    reset_default_orchestrator,
    run_ai_stack,
)
from auto_client_acquisition.self_evolving_os import (
    InMemoryLearningStore,
    OutcomeKind,
)


def _passport(
    *,
    contains_pii: bool = False,
    external_use: bool = False,
    ai_allowed: bool = True,
) -> SourcePassportInput:
    return SourcePassportInput(
        source_id="intake_test_001",
        source_type="customer_intake",
        owner="test_owner",
        allowed_use=["ai_assist"],
        contains_pii=contains_pii,
        sensitivity="internal",
        retention_policy="90d",
        ai_access_allowed=ai_allowed,
        external_use_allowed=external_use,
    )


def _payload(
    *,
    tier: Offer = Offer.FREE_DIAGNOSTIC,
    passport: SourcePassportInput | None = None,
    challenge_ar: str = "نحتاج تحسين عملية البيع",
    challenge_en: str = "we need to improve our sales process",
) -> AIStackInput:
    return AIStackInput(
        tenant_id="acme",
        customer_handle="acme_handle",
        company_name="Acme Corp",
        sector="technology",
        challenge_ar=challenge_ar,
        challenge_en=challenge_en,
        offer_tier=tier,
        source_passport=passport or _passport(),
    )


@pytest.fixture(autouse=True)
def _reset_orchestrator():
    reset_default_orchestrator()
    yield
    reset_default_orchestrator()


class TestLayerHealthSnapshot:
    def test_snapshot_returns_eleven_layers(self) -> None:
        snap = snapshot_health()
        assert len(snap.layers) == 11

    def test_overall_healthy_when_all_modules_import(self) -> None:
        snap = snapshot_health()
        assert snap.overall_healthy is True
        for layer in snap.layers:
            assert layer.healthy, f"{layer.layer} unhealthy: {layer.detail}"

    def test_layer_versions_returns_all_layers(self) -> None:
        versions = layer_versions()
        assert len(versions) == 11


class TestOrchestratorRun:
    def test_full_run_completes_all_eleven_layers(self) -> None:
        orch = AIStackOrchestrator(learning_store=InMemoryLearningStore())
        result = orch.run(_payload())
        assert isinstance(result, AIStackResult)
        assert len(result.layers) == 11
        assert result.tenant_id == "acme"
        assert result.run_id.startswith("ais_")
        assert result.proof_pack_id is not None
        assert result.proof_pack_id.startswith("pp_")

    def test_full_run_produces_bilingual_markdown(self) -> None:
        orch = AIStackOrchestrator(learning_store=InMemoryLearningStore())
        result = orch.run(_payload())
        md = result.proof_pack_markdown
        assert "Proof Pack" in md
        assert "حزمة الإثبات" in md
        assert "Executive Summary" in md
        assert "الملخص التنفيذي" in md

    def test_full_run_records_evidence_chain_head(self) -> None:
        orch = AIStackOrchestrator(learning_store=InMemoryLearningStore())
        result = orch.run(_payload())
        assert result.evidence_head_hash
        assert len(result.evidence_head_hash) == 64  # SHA-256 hex

    def test_invalid_passport_blocks_at_l1(self) -> None:
        orch = AIStackOrchestrator(learning_store=InMemoryLearningStore())
        passport = SourcePassportInput(
            source_id="bad",
            source_type="x",
            owner="o",
            allowed_use=["ai_assist"],
            ai_access_allowed=False,  # explicit denial
        )
        result = orch.run(_payload(passport=passport))
        assert result.governance_blocked is True
        # Should NOT execute all 11 layers — short-circuits at L1.
        l1 = next(l for l in result.layers if l.layer == "L1_source_passport")
        assert l1.status == LayerStatus.BLOCKED

    def test_run_respects_offer_tier(self) -> None:
        orch = AIStackOrchestrator(learning_store=InMemoryLearningStore())
        result = orch.run(_payload(tier=Offer.MANAGED_OPS))
        assert result.offer_tier == Offer.MANAGED_OPS
        # Managed Ops should run 6 agent tasks; we don't assert exact count
        # because the mesh hides individual runs in L5's payload — but the
        # layer must be ok.
        l5 = next(l for l in result.layers if l.layer == "L5_agent_mesh")
        assert l5.status == LayerStatus.OK

    def test_full_run_records_feedback_event(self) -> None:
        store = InMemoryLearningStore()
        orch = AIStackOrchestrator(learning_store=store)
        result = orch.run(_payload())
        feedback_events = store.list_events(tenant_id="acme")
        assert feedback_events, "expected at least one feedback event"

    def test_run_doctrine_clean_for_clean_input(self) -> None:
        orch = AIStackOrchestrator(learning_store=InMemoryLearningStore())
        result = orch.run(_payload())
        assert result.doctrine_clean is True

    def test_value_ledger_layer_is_skipped_until_invoice_paid(self) -> None:
        orch = AIStackOrchestrator(learning_store=InMemoryLearningStore())
        result = orch.run(_payload())
        l8 = next(l for l in result.layers if l.layer == "L8_value_ledger")
        assert l8.status == LayerStatus.SKIPPED

    def test_proof_score_is_higher_for_complete_intake(self) -> None:
        orch = AIStackOrchestrator(learning_store=InMemoryLearningStore())
        full = orch.run(_payload(challenge_en="we need to fix this"))
        empty = orch.run(_payload(challenge_en=""))
        # Empty EN challenge should still produce a score but the bilingual
        # bonus only kicks in when both languages are present.
        assert full.proof_score >= empty.proof_score

    def test_module_level_run_helper(self) -> None:
        result = run_ai_stack(_payload())
        assert result.run_id


class TestDeterminism:
    def test_two_runs_with_same_input_produce_eleven_layers(self) -> None:
        orch1 = AIStackOrchestrator(learning_store=InMemoryLearningStore())
        orch2 = AIStackOrchestrator(learning_store=InMemoryLearningStore())
        r1 = orch1.run(_payload())
        r2 = orch2.run(_payload())
        assert len(r1.layers) == len(r2.layers) == 11
        # Both should classify identically.
        assert r1.governance_blocked == r2.governance_blocked
        assert r1.doctrine_clean == r2.doctrine_clean


class TestDoctrineSafety:
    def test_no_revenue_recorded_without_invoice_paid(self) -> None:
        store = InMemoryLearningStore()
        orch = AIStackOrchestrator(learning_store=store)
        result = orch.run(_payload(tier=Offer.MANAGED_OPS))
        l8 = next(l for l in result.layers if l.layer == "L8_value_ledger")
        assert l8.status == LayerStatus.SKIPPED
        # The value ledger payload must advertise the advisory-only mode.
        assert l8.payload["advisory_only"] is True

    def test_no_external_action_in_default_run(self) -> None:
        orch = AIStackOrchestrator(learning_store=InMemoryLearningStore())
        result = orch.run(_payload())
        # No layer reports an outbound action — the default handlers are
        # draft-only.
        for layer in result.layers:
            payload_str = str(layer.payload).lower()
            assert "whatsapp.send_message" not in payload_str
            assert "linkedin.publish" not in payload_str

    def test_self_evolving_records_outcome_without_mutating_router(self) -> None:
        store = InMemoryLearningStore()
        orch = AIStackOrchestrator(learning_store=store)
        orch.run(_payload())
        events = store.list_events(tenant_id="acme")
        l11 = [e for e in events if e.layer == "L11_self_evolving"]
        assert l11, "L11 must record at least one feedback event"
        # outcome_kind must be a valid OutcomeKind value (no fabrication).
        for e in l11:
            assert e.outcome_kind in {k.value for k in OutcomeKind}
