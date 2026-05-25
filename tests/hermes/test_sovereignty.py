"""Sovereignty classifier — S1..S5 routing tests."""

from __future__ import annotations

from dealix.hermes.contracts import (
    Actor,
    ActorKind,
    ContextPacket,
    DataSensitivity,
    OutputKind,
    SovereigntyLevel,
)
from dealix.hermes.sovereignty import classify


def _internal_context(intent: str = "internal.test") -> ContextPacket:
    return ContextPacket(
        actor=Actor(actor_id="u_internal", kind=ActorKind.INTERNAL_USER),
        intent=intent,
        declared_output_kind=OutputKind.DRAFT,
        data_sensitivity=DataSensitivity.INTERNAL,
    )


def _founder_context(intent: str, output: OutputKind = OutputKind.ACTION) -> ContextPacket:
    return ContextPacket(
        actor=Actor(actor_id="founder_1", kind=ActorKind.FOUNDER),
        intent=intent,
        declared_output_kind=output,
        data_sensitivity=DataSensitivity.INTERNAL,
    )


def test_internal_user_internal_intent_is_s1_no_approval() -> None:
    ctx = _internal_context(intent="internal.read.dashboard")
    decision = classify(context=ctx, intent="internal.read.dashboard")
    assert decision.sovereignty_level == SovereigntyLevel.S1_INTERNAL_AUTO
    assert decision.approval_required is False


def test_founder_send_email_is_s2_sami_approval() -> None:
    ctx = _founder_context("external.send.email")
    decision = classify(context=ctx, intent="external.send.email")
    assert decision.sovereignty_level == SovereigntyLevel.S2_SAMI_APPROVAL
    assert decision.approval_required is True


def test_contract_sign_is_s3_legal_approval() -> None:
    ctx = _founder_context("external.contract.sign")
    decision = classify(context=ctx, intent="external.contract.sign")
    assert decision.sovereignty_level == SovereigntyLevel.S3_LEGAL_APPROVAL
    assert decision.approval_required is True


def test_acquisition_commit_is_s4_board_approval() -> None:
    ctx = _founder_context("company.acquisition.commit")
    decision = classify(context=ctx, intent="company.acquisition.commit")
    assert decision.sovereignty_level == SovereigntyLevel.S4_BOARD_APPROVAL
    assert decision.approval_required is True


def test_bulk_unverified_send_is_s5_blocked() -> None:
    ctx = _founder_context("external.send.bulk.unverified")
    decision = classify(context=ctx, intent="external.send.bulk.unverified")
    assert decision.sovereignty_level == SovereigntyLevel.S5_BLOCKED
    # blocked intents short-circuit before approval logic
    assert decision.approval_required is False


def test_bulk_count_50_on_external_action_escalates_to_s2() -> None:
    # Pick an external intent that is NOT itself in founder_only, so the
    # bulk-count branch is the one that fires.
    ctx = ContextPacket(
        actor=Actor(actor_id="founder_1", kind=ActorKind.FOUNDER),
        intent="external.broadcast.update",
        declared_output_kind=OutputKind.ACTION,
        data_sensitivity=DataSensitivity.INTERNAL,
    )
    decision = classify(
        context=ctx,
        intent="external.broadcast.update",
        extra_signals={"bulk_count": 75},
    )
    assert decision.sovereignty_level == SovereigntyLevel.S2_SAMI_APPROVAL
    assert decision.approval_required is True
    assert any("bulk" in r for r in decision.reasons)


def test_regulated_data_sensitivity_is_s3_legal() -> None:
    ctx = ContextPacket(
        actor=Actor(actor_id="u_internal", kind=ActorKind.INTERNAL_USER),
        intent="internal.export.report",
        declared_output_kind=OutputKind.REPORT,
        data_sensitivity=DataSensitivity.REGULATED,
    )
    decision = classify(context=ctx, intent="internal.export.report")
    assert decision.sovereignty_level == SovereigntyLevel.S3_LEGAL_APPROVAL
    assert decision.approval_required is True
