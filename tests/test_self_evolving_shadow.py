"""Tests for the Self-Evolving OS (L11) — strict shadow-mode invariants."""

from __future__ import annotations

import pytest

from auto_client_acquisition.self_evolving_os import (
    SELF_EVOLVING_SHADOW_ONLY,
    FeedbackEvent,
    IllegalProposalTransition,
    InMemoryLearningStore,
    InMemoryProposalRepository,
    OutcomeKind,
    ProposalState,
    ShadowModeViolationError,
    assert_shadow_mode,
    derive_suggestions,
    from_doctrine_violation,
    from_friction_log,
    from_governance_block,
    from_value_event,
    make_feedback_event,
    proposal_from_suggestion,
    record_feedback,
)


class TestShadowModeInvariant:
    def test_shadow_mode_constant_is_true(self) -> None:
        assert SELF_EVOLVING_SHADOW_ONLY is True

    def test_assert_shadow_mode_passes_in_shadow(self) -> None:
        # Should not raise.
        assert_shadow_mode()

    def test_shadow_mode_violation_error_exists(self) -> None:
        assert issubclass(ShadowModeViolationError, RuntimeError)


class TestFeedbackEvent:
    def test_make_event_validates_layer(self) -> None:
        with pytest.raises(ValueError, match="unknown layer"):
            make_feedback_event(
                tenant_id="t1",
                run_id="r1",
                layer="L99_fake",
                outcome_kind=OutcomeKind.SUCCESS,
            )

    def test_make_event_validates_outcome_kind(self) -> None:
        with pytest.raises(ValueError, match="unknown outcome_kind"):
            make_feedback_event(
                tenant_id="t1",
                run_id="r1",
                layer="L7_proof_pack",
                outcome_kind="not_a_thing",
            )

    def test_make_event_requires_tenant(self) -> None:
        with pytest.raises(ValueError, match="tenant_id"):
            make_feedback_event(
                tenant_id="",
                run_id="r1",
                layer="L7_proof_pack",
                outcome_kind=OutcomeKind.SUCCESS,
            )

    def test_event_from_value_maps_client_confirmed(self) -> None:
        ev = from_value_event(
            tenant_id="t1",
            run_id="r1",
            value_event={
                "tier": "client_confirmed",
                "amount": 4500,
                "kind": "monthly_retainer",
                "source_ref": "moyasar:pay_123",
            },
        )
        assert ev.outcome_kind == OutcomeKind.CUSTOMER_CONFIRMED.value
        assert ev.outcome_value == 4500.0

    def test_event_from_friction_high_is_failure(self) -> None:
        ev = from_friction_log(
            tenant_id="t1",
            run_id="r1",
            friction_event={"impact": "high", "friction_type": "approval_friction"},
        )
        assert ev.outcome_kind == OutcomeKind.FAILURE.value
        assert ev.doctrine_clean is True

    def test_event_from_governance_block_is_doctrine_dirty(self) -> None:
        ev = from_governance_block(
            tenant_id="t1",
            run_id="r1",
            layer="L6_governance",
            reason="cold_whatsapp_blocked",
        )
        assert ev.outcome_kind == OutcomeKind.BLOCKED_BY_GOVERNANCE.value
        assert ev.doctrine_clean is False

    def test_event_from_doctrine_violation_is_doctrine_dirty(self) -> None:
        ev = from_doctrine_violation(
            tenant_id="t1",
            run_id="r1",
            layer="L6_governance",
            violation="no_guaranteed_claims",
        )
        assert ev.outcome_kind == OutcomeKind.BLOCKED_BY_DOCTRINE.value
        assert ev.doctrine_clean is False


class TestLearningStore:
    def test_append_and_list_round_trip(self) -> None:
        store = InMemoryLearningStore()
        ev = make_feedback_event(
            tenant_id="t1",
            run_id="r1",
            layer="L7_proof_pack",
            outcome_kind=OutcomeKind.SUCCESS,
            outcome_value=80.0,
        )
        store.append(ev)
        rows = store.list_events(tenant_id="t1")
        assert len(rows) == 1
        assert rows[0].event_id == ev.event_id

    def test_summarize_layer_aggregates_outcomes(self) -> None:
        store = InMemoryLearningStore()
        for _ in range(3):
            store.append(make_feedback_event(
                tenant_id="t1", run_id="r",
                layer="L7_proof_pack",
                outcome_kind=OutcomeKind.SUCCESS,
            ))
        store.append(make_feedback_event(
            tenant_id="t1", run_id="r",
            layer="L7_proof_pack",
            outcome_kind=OutcomeKind.FAILURE,
        ))
        summary = store.summarize_layer(tenant_id="t1", layer="L7_proof_pack")
        assert summary.total == 4
        assert summary.by_kind[OutcomeKind.SUCCESS.value] == 3
        assert summary.by_kind[OutcomeKind.FAILURE.value] == 1
        assert 0.74 < summary.success_rate() < 0.76

    def test_summarize_all_layers(self) -> None:
        store = InMemoryLearningStore()
        store.append(make_feedback_event(
            tenant_id="t1", run_id="r",
            layer="L7_proof_pack",
            outcome_kind=OutcomeKind.SUCCESS,
        ))
        store.append(make_feedback_event(
            tenant_id="t1", run_id="r",
            layer="L6_governance",
            outcome_kind=OutcomeKind.BLOCKED_BY_GOVERNANCE,
            doctrine_clean=False,
        ))
        summaries = store.summarize_all_layers(tenant_id="t1")
        assert "L7_proof_pack" in summaries
        assert summaries["L6_governance"].doctrine_violations == 1

    def test_tenant_isolation(self) -> None:
        store = InMemoryLearningStore()
        store.append(make_feedback_event(
            tenant_id="t1", run_id="r",
            layer="L7_proof_pack",
            outcome_kind=OutcomeKind.SUCCESS,
        ))
        store.append(make_feedback_event(
            tenant_id="t2", run_id="r",
            layer="L7_proof_pack",
            outcome_kind=OutcomeKind.SUCCESS,
        ))
        rows1 = store.list_events(tenant_id="t1")
        rows2 = store.list_events(tenant_id="t2")
        assert len(rows1) == 1
        assert len(rows2) == 1
        assert rows1[0].event_id != rows2[0].event_id


class TestDecisionImprover:
    def test_suggestions_flag_doctrine_violations_as_act(self) -> None:
        store = InMemoryLearningStore()
        store.append(make_feedback_event(
            tenant_id="t1", run_id="r",
            layer="L6_governance",
            outcome_kind=OutcomeKind.BLOCKED_BY_GOVERNANCE,
            doctrine_clean=False,
        ))
        suggestions = derive_suggestions(tenant_id="t1", store=store)
        gov = [s for s in suggestions if s.target_layer == "L6_governance"]
        assert gov, "expected a suggestion for the doctrine-violation layer"
        assert gov[0].severity == "act"

    def test_suggestions_filter_by_severity(self) -> None:
        store = InMemoryLearningStore()
        for _ in range(20):
            store.append(make_feedback_event(
                tenant_id="t1", run_id="r",
                layer="L5_agent_mesh",
                outcome_kind=OutcomeKind.SUCCESS,
            ))
        # All success → severity stays info; filter to "act" returns nothing.
        suggestions = derive_suggestions(
            tenant_id="t1", store=store, minimum_severity="act",
        )
        assert suggestions == []

    def test_suggestions_returned_for_low_success_rate(self) -> None:
        store = InMemoryLearningStore()
        for _ in range(11):
            store.append(make_feedback_event(
                tenant_id="t1", run_id="r",
                layer="L5_agent_mesh",
                outcome_kind=OutcomeKind.FAILURE,
            ))
        suggestions = derive_suggestions(tenant_id="t1", store=store)
        mesh = [s for s in suggestions if s.target_layer == "L5_agent_mesh"]
        assert mesh and mesh[0].severity == "act"


class TestImprovementProposals:
    def test_proposal_starts_pending(self) -> None:
        store = InMemoryLearningStore()
        for _ in range(11):
            store.append(make_feedback_event(
                tenant_id="t1", run_id="r",
                layer="L7_proof_pack",
                outcome_kind=OutcomeKind.FAILURE,
            ))
        suggestion = derive_suggestions(tenant_id="t1", store=store)[0]
        proposal = proposal_from_suggestion(suggestion)
        assert proposal.state == ProposalState.PENDING.value
        assert proposal.proposal_id.startswith("prop_")
        assert proposal.approved_by is None

    def test_state_machine_enforces_order(self) -> None:
        store = InMemoryLearningStore()
        for _ in range(11):
            store.append(make_feedback_event(
                tenant_id="t1", run_id="r",
                layer="L7_proof_pack",
                outcome_kind=OutcomeKind.FAILURE,
            ))
        suggestion = derive_suggestions(tenant_id="t1", store=store)[0]
        proposal = proposal_from_suggestion(suggestion)
        repo = InMemoryProposalRepository()
        repo.submit(proposal)

        # Cannot apply before approving.
        with pytest.raises(IllegalProposalTransition):
            repo.apply(
                tenant_id="t1",
                proposal_id=proposal.proposal_id,
                applied_by="founder",
            )

        approved = repo.approve(
            tenant_id="t1",
            proposal_id=proposal.proposal_id,
            approved_by="founder",
        )
        assert approved.state == ProposalState.APPROVED.value

        # Cannot re-approve.
        with pytest.raises(IllegalProposalTransition):
            repo.approve(
                tenant_id="t1",
                proposal_id=proposal.proposal_id,
                approved_by="founder",
            )

        applied = repo.apply(
            tenant_id="t1",
            proposal_id=proposal.proposal_id,
            applied_by="founder",
        )
        assert applied.state == ProposalState.APPLIED.value

        # Cannot reject after applied.
        with pytest.raises(IllegalProposalTransition):
            repo.reject(
                tenant_id="t1",
                proposal_id=proposal.proposal_id,
                rejected_by="founder",
            )

    def test_no_auto_apply_path_exists_in_module(self) -> None:
        """Doctrine guard: nothing in the module should expose an `apply_now` path."""
        from auto_client_acquisition.self_evolving_os import decision_improver

        forbidden = ("apply_now", "auto_apply", "force_apply")
        for name in forbidden:
            assert not hasattr(decision_improver, name), (
                f"decision_improver must not expose {name!r}"
            )
