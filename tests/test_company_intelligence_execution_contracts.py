from __future__ import annotations

from types import SimpleNamespace

import pytest

from auto_client_acquisition.approval_center.schemas import ApprovalRequest
from dealix.company_intelligence import (
    DraftChannel,
    LawfulContactBasis,
    build_draft,
    normalize_approval,
    normalize_opportunity,
)


def _opportunity_record(**overrides: object) -> SimpleNamespace:
    values: dict[str, object] = {
        "tenant_id": "tenant-a",
        "id": "opp-1",
        "account_id": "company-1",
        "company_name": "Acme Saudi",
        "offer_id": "revenue_command_pilot_30d",
        "stage": "qualify",
        "score": 82,
        "score_components_json": {"pain": 30, "access": 22, "evidence": 30},
        "source_signal_ids_json": ["sig-1", "sig-2"],
        "confidence_band": "high",
        "blockers_json": ["baseline_missing"],
        "next_action": "prepare discovery brief",
        "proof_target": "approved discovery outcome",
        "approval_required": True,
        "external_action_allowed": False,
    }
    values.update(overrides)
    return SimpleNamespace(**values)


def test_opportunity_adapter_preserves_tenant_evidence_and_default_block() -> None:
    opportunity = normalize_opportunity(_opportunity_record())

    assert opportunity.tenant_id == "tenant-a"
    assert opportunity.company_id == "company-1"
    assert opportunity.score_reasons["evidence"] == 30
    assert opportunity.signal_ids == ["sig-1", "sig-2"]
    assert opportunity.external_action_allowed is False


def test_opportunity_never_grants_external_execution_authority() -> None:
    record = _opportunity_record(
        approval_required=False,
        external_action_allowed=True,
    )

    with pytest.raises(ValueError, match="never authorize external execution"):
        normalize_opportunity(record)


def test_draft_builder_is_deterministic_and_execution_disabled() -> None:
    kwargs = dict(
        tenant_id="tenant-a",
        action_id="action-1",
        opportunity_id="opp-1",
        channel=DraftChannel.EMAIL,
        content="Draft only message",
        lawful_contact_basis=LawfulContactBasis.EXISTING_RELATIONSHIP,
        source_evidence=["source-2", "source-1", "source-1"],
    )

    first = build_draft(**kwargs)
    second = build_draft(
        **{
            **kwargs,
            "source_evidence": ["source-1", "source-2"],
        }
    )

    assert first.draft_id == second.draft_id
    assert first.content_hash == second.content_hash
    assert first.source_evidence == ["source-1", "source-2"]
    assert first.approval_required is True
    assert first.execution_allowed is False


def test_draft_identity_includes_compliance_context() -> None:
    base = dict(
        tenant_id="tenant-a",
        action_id="action-1",
        opportunity_id="opp-1",
        channel=DraftChannel.EMAIL,
        content="Draft only message",
        source_evidence=["source-1"],
    )

    existing_relationship = build_draft(
        **base,
        lawful_contact_basis=LawfulContactBasis.EXISTING_RELATIONSHIP,
    )
    explicit_opt_in = build_draft(
        **base,
        lawful_contact_basis=LawfulContactBasis.EXPLICIT_OPT_IN,
    )
    different_evidence = build_draft(
        **{
            **base,
            "source_evidence": ["source-2"],
            "lawful_contact_basis": LawfulContactBasis.EXISTING_RELATIONSHIP,
        }
    )

    assert existing_relationship.draft_id != explicit_opt_in.draft_id
    assert existing_relationship.content_hash != explicit_opt_in.content_hash
    assert existing_relationship.draft_id != different_evidence.draft_id


def test_draft_requires_non_empty_evidence() -> None:
    with pytest.raises(ValueError, match="source_evidence"):
        build_draft(
            tenant_id="tenant-a",
            action_id="action-1",
            opportunity_id="opp-1",
            channel=DraftChannel.EMAIL,
            content="Draft only message",
            lawful_contact_basis=LawfulContactBasis.EXISTING_RELATIONSHIP,
            source_evidence=[],
        )


def test_cold_whatsapp_is_rejected() -> None:
    with pytest.raises(ValueError, match="cold WhatsApp"):
        build_draft(
            tenant_id="tenant-a",
            action_id="action-1",
            opportunity_id="opp-1",
            channel=DraftChannel.WHATSAPP,
            content="Hello",
            lawful_contact_basis=LawfulContactBasis.MANUAL_RESEARCH_ONLY,
            source_evidence=["source-1"],
        )


def test_linkedin_requires_manual_task_and_never_executes() -> None:
    with pytest.raises(ValueError, match="LinkedIn automation"):
        build_draft(
            tenant_id="tenant-a",
            action_id="action-1",
            opportunity_id="opp-1",
            channel=DraftChannel.LINKEDIN,
            content="Personalized draft",
            lawful_contact_basis=LawfulContactBasis.MANUAL_RESEARCH_ONLY,
            source_evidence=["source-1"],
            is_manual_task=False,
        )

    draft = build_draft(
        tenant_id="tenant-a",
        action_id="action-1",
        opportunity_id="opp-1",
        channel=DraftChannel.LINKEDIN,
        content="Personalized draft",
        lawful_contact_basis=LawfulContactBasis.MANUAL_RESEARCH_ONLY,
        source_evidence=["source-1"],
        is_manual_task=True,
    )
    assert draft.execution_allowed is False


def test_approval_adapter_requires_tenant_action_and_proof() -> None:
    request = ApprovalRequest(
        object_type="draft",
        object_id="draft-1",
        action_type="draft_email",
        customer_id="tenant-a",
        action_id="action-1",
        proof_target="approved manual outcome",
    )

    approval = normalize_approval(request)

    assert approval.tenant_id == "tenant-a"
    assert approval.action_id == "action-1"
    assert approval.proof_target == "approved manual outcome"
    assert approval.execution_allowed is False


def test_approval_adapter_rejects_missing_tenant_or_proof() -> None:
    request = ApprovalRequest(
        object_type="draft",
        object_id="draft-1",
        action_type="draft_email",
        action_id="action-1",
    )

    with pytest.raises(ValueError, match="tenant_id"):
        normalize_approval(request)

    request.customer_id = "tenant-a"
    with pytest.raises(ValueError, match="proof_target"):
        normalize_approval(request)
