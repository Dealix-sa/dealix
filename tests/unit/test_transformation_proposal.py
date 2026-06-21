"""Unit tests — Transformation OS proposal generator (governed, stateless)."""

from __future__ import annotations

import re

import pytest

from auto_client_acquisition.service_catalog import get_offering
from dealix.commercial.transformation_proposal import (
    TransformationProposalError,
    TransformationProposalGenerator,
    TransformationProposalRequest,
)


def _gen(**kw) -> object:
    req = TransformationProposalRequest(**kw)
    return TransformationProposalGenerator().generate(req)


def test_proposal_is_approval_gated_and_estimate():
    p = _gen(
        company_name="Acme Clinics",
        sector="healthcare_clinic",
        selected_system_ids=["whatsapp_revenue_os", "ai_command_center_os"],
        stakeholders=["CEO", "COO"],
    )
    assert p.approval_status == "approval_required"
    assert p.governance_decision == "pending"
    assert p.is_estimate is True
    assert len(p.line_items) == 2


def test_proposal_reads_prices_from_catalog():
    p = _gen(company_name="X", selected_system_ids=["ai_command_center_os"])
    item = p.line_items[0]
    off = get_offering("ai_command_center_os")
    assert item.setup_sar_min == off.price_sar
    assert item.setup_sar_max == off.price_sar_max
    assert item.monthly_sar_min == off.price_monthly_sar_min
    # Totals echo the single line item
    assert p.total_setup_sar_min == off.price_sar
    assert p.total_setup_sar_max == off.price_sar_max


def test_markdown_is_bilingual_and_has_disclaimer():
    p = _gen(company_name="Beta Co", selected_system_ids=["brand_intelligence_os"])
    md = p.markdown_ar_en
    assert "Dealix Transformation Proposal" in md
    assert "عرض التحول" in md
    assert "approval_required" in md
    assert "Estimated value is not Verified value" in md
    # No guaranteed-outcome language in the rendered proposal
    assert re.search(r"\bguarantee", md, re.IGNORECASE) is None
    assert "نضمن" not in md


def test_unknown_ids_are_tracked_not_billed():
    p = _gen(
        company_name="Y",
        selected_system_ids=["ai_command_center_os", "revenue_proof_sprint_499", "bogus_id"],
    )
    # Only transformation-stage systems are valid line items.
    assert [i.system_id for i in p.line_items] == ["ai_command_center_os"]
    assert "revenue_proof_sprint_499" in p.unknown_system_ids
    assert "bogus_id" in p.unknown_system_ids


def test_empty_selection_raises():
    with pytest.raises(TransformationProposalError):
        _gen(company_name="Z", selected_system_ids=[])


def test_all_invalid_selection_raises():
    with pytest.raises(TransformationProposalError):
        _gen(company_name="Z", selected_system_ids=["not_a_system", "also_not"])


def test_guaranteed_claim_in_notes_is_rejected():
    with pytest.raises(TransformationProposalError):
        _gen(
            company_name="Z",
            selected_system_ids=["whatsapp_revenue_os"],
            notes="We guarantee +300% revenue in 30 days",
        )
    with pytest.raises(TransformationProposalError):
        _gen(
            company_name="Z",
            selected_system_ids=["whatsapp_revenue_os"],
            notes="نضمن لك مضاعفة المبيعات",
        )


def test_custom_enterprise_system_handles_open_ended_pricing():
    p = _gen(company_name="Mega Corp", selected_system_ids=["custom_enterprise_system"])
    item = p.line_items[0]
    assert item.price_unit == "custom"
    assert item.setup_sar_min == 0.0
    # Open-ended ceiling falls back to floor for totals (no crash).
    assert p.total_setup_sar_max == p.total_setup_sar_min
