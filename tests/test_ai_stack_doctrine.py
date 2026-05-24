"""Doctrine non-negotiables for the AI Stack — zero compromise.

These tests guard the eleven non-negotiables from
``dealix/commercial_ops/doctrine.py`` at the AI Stack boundary. A
regression here is a Doctrine violation, not a flake — every assertion
is intentional.
"""

from __future__ import annotations

import pytest

from auto_client_acquisition.ai_stack_os import (
    AIStackInput,
    AIStackOrchestrator,
    Offer,
    SourcePassportInput,
)
from auto_client_acquisition.ai_stack_os.orchestrator import reset_default_orchestrator
from auto_client_acquisition.proof_os import (
    ApprovalLevel,
    Reversibility,
    Sensitivity,
    issue_passport,
)
from auto_client_acquisition.self_evolving_os import (
    InMemoryLearningStore,
    OutcomeKind,
    SELF_EVOLVING_SHADOW_ONLY,
)


def _passport() -> SourcePassportInput:
    return SourcePassportInput(
        source_id="doctrine_test",
        source_type="customer_intake",
        owner="founder",
        allowed_use=["ai_assist"],
        contains_pii=False,
        sensitivity="internal",
        retention_policy="90d",
        ai_access_allowed=True,
        external_use_allowed=False,
    )


def _payload(*, challenge_ar: str = "نحتاج تحسين", tier: Offer = Offer.FREE_DIAGNOSTIC) -> AIStackInput:
    return AIStackInput(
        tenant_id="acme",
        customer_handle="acme_handle",
        company_name="Acme Corp",
        sector="technology",
        challenge_ar=challenge_ar,
        challenge_en="we need improvement",
        offer_tier=tier,
        source_passport=_passport(),
    )


@pytest.fixture(autouse=True)
def _reset():
    reset_default_orchestrator()
    yield
    reset_default_orchestrator()


class TestNonNegotiableCommunications:
    """No cold WhatsApp / LinkedIn / Gmail without approval (non-negotiables #1-3)."""

    def test_no_layer_payload_mentions_send_message_directly(self) -> None:
        orch = AIStackOrchestrator(learning_store=InMemoryLearningStore())
        result = orch.run(_payload())
        for layer in result.layers:
            payload_str = str(layer.payload).lower()
            assert "whatsapp.send_message" not in payload_str
            assert "linkedin.publish" not in payload_str
            assert "gmail.send" not in payload_str

    def test_proposal_handler_marks_approval_required(self) -> None:
        orch = AIStackOrchestrator(learning_store=InMemoryLearningStore())
        result = orch.run(_payload(tier=Offer.SPRINT_499))
        l5 = next(l for l in result.layers if l.layer == "L5_agent_mesh")
        # The proposal handler's output must carry approval_required=True.
        runs = l5.payload["runs"]
        proposal_runs = [r for r in runs if "proposal" in r["agent_id"]]
        for run in proposal_runs:
            if run["output"]:
                assert run["output"].get("approval_required") is True


class TestNonNegotiableNoInventedKPIs:
    """Non-negotiable #4: no fabricated CRM/KPI numbers."""

    def test_self_evolving_outcome_kinds_are_a_closed_set(self) -> None:
        valid = {k.value for k in OutcomeKind}
        # The orchestrator records feedback with a known outcome_kind.
        store = InMemoryLearningStore()
        orch = AIStackOrchestrator(learning_store=store)
        orch.run(_payload())
        for event in store.list_events(tenant_id="acme"):
            assert event.outcome_kind in valid


class TestNonNegotiableNoRevenueBeforeInvoicePaid:
    """Non-negotiable #5: no upsell / revenue before invoice_paid."""

    def test_value_ledger_layer_is_skipped(self) -> None:
        from auto_client_acquisition.ai_stack_os import LayerStatus

        orch = AIStackOrchestrator(learning_store=InMemoryLearningStore())
        result = orch.run(_payload(tier=Offer.MANAGED_OPS))
        l8 = next(l for l in result.layers if l.layer == "L8_value_ledger")
        assert l8.status == LayerStatus.SKIPPED
        # Reason MUST mention awaiting invoice_paid signal.
        assert "invoice_paid" in str(l8.payload).lower()

    def test_capital_ledger_does_not_persist(self) -> None:
        orch = AIStackOrchestrator(learning_store=InMemoryLearningStore())
        result = orch.run(_payload(tier=Offer.MANAGED_OPS))
        l9 = next(l for l in result.layers if l.layer == "L9_capital_ledger")
        assert l9.payload["persisted"] is False


class TestNonNegotiableNoGuaranteedClaims:
    """Implicit non-negotiable from governance_os: no 100% guaranteed outcomes."""

    def test_guarantee_in_challenge_does_not_leak_to_proof_pack(self) -> None:
        orch = AIStackOrchestrator(learning_store=InMemoryLearningStore())
        # If a customer types "guaranteed sales" the doctrine scan should catch it.
        payload = _payload(challenge_ar="نضمن نتائج مبيعات مضمونة 100٪")
        result = orch.run(payload)
        # The orchestrator marks doctrine_clean=False; downstream callers see
        # the flag and refuse to publish.
        # NB: governance_os also flags this at L6, so governance_blocked may
        # be true too.
        assert result.doctrine_clean is False or result.governance_blocked is True


class TestNonNegotiableSourcePassportGate:
    """All AI use must pass a Source Passport check (data sovereignty)."""

    def test_no_ai_access_blocks_run(self) -> None:
        bad_passport = SourcePassportInput(
            source_id="bad_passport",
            source_type="x",
            owner="o",
            allowed_use=["ai_assist"],
            ai_access_allowed=False,
        )
        payload = AIStackInput(
            tenant_id="acme",
            customer_handle="acme_handle",
            company_name="Acme",
            sector="x",
            challenge_ar="anything",
            challenge_en="anything",
            offer_tier=Offer.FREE_DIAGNOSTIC,
            source_passport=bad_passport,
        )
        orch = AIStackOrchestrator(learning_store=InMemoryLearningStore())
        result = orch.run(payload)
        assert result.governance_blocked is True


class TestNonNegotiableBilingualOutput:
    """Every customer-facing artifact must be bilingual (AR + EN)."""

    def test_proof_pack_markdown_has_both_languages(self) -> None:
        orch = AIStackOrchestrator(learning_store=InMemoryLearningStore())
        result = orch.run(_payload())
        # Must include Arabic
        assert "ال" in result.proof_pack_markdown
        # Must include English
        assert "summary" in result.proof_pack_markdown.lower() or "english" in result.proof_pack_markdown.lower()

    def test_decision_passports_require_bilingual_summaries(self) -> None:
        # Constructor-level guard.
        with pytest.raises(ValueError, match="summary_ar"):
            issue_passport(
                tenant_id="t1",
                decision_type="icp_classification",
                summary_ar="",
                summary_en="english only",
                content={},
            )


class TestNonNegotiableSelfEvolvingShadowMode:
    """Self-Evolving must never auto-apply changes."""

    def test_shadow_mode_constant_is_locked_true(self) -> None:
        assert SELF_EVOLVING_SHADOW_ONLY is True

    def test_no_apply_now_function_exists(self) -> None:
        from auto_client_acquisition.self_evolving_os import (
            decision_improver,
            improvement_proposals,
        )

        for module in (decision_improver, improvement_proposals):
            assert not hasattr(module, "apply_now")
            assert not hasattr(module, "auto_apply")
            assert not hasattr(module, "force_apply_proposal")


class TestNonNegotiableDecisionPassportApprovalLadder:
    """Critical decisions must escalate per approval ladder."""

    def test_irreversible_action_forces_founder_approval(self) -> None:
        p = issue_passport(
            tenant_id="t1",
            decision_type="capital_register",
            summary_ar="ع",
            summary_en="e",
            content={},
            reversibility=Reversibility.R3_IRREVERSIBLE,
        )
        assert p.approval_level == ApprovalLevel.A2_FOUNDER

    def test_regulated_pii_external_forces_founder_approval(self) -> None:
        p = issue_passport(
            tenant_id="t1",
            decision_type="outreach_draft",
            summary_ar="ع",
            summary_en="e",
            content={},
            sensitivity=Sensitivity.S3_REGULATED_PII,
            external_action=True,
        )
        assert p.approval_level == ApprovalLevel.A2_FOUNDER
