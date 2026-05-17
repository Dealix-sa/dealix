"""Tests for public funnel auto-routing."""
from __future__ import annotations

from auto_client_acquisition.approval_center.approval_store import ApprovalStore
from auto_client_acquisition.content_os.funnel_routing import route_and_draft_proposal
from auto_client_acquisition.sales_os.qualification import qualify


def test_clean_high_fit_lead_queues_proposal():
    store = ApprovalStore()
    qr = qualify(
        pain_clear=True, owner_present=True, data_available=True,
        accepts_governance=True, has_budget=True, wants_safe_methods=True,
        proof_path_visible=True, retainer_path_visible=True,
    )
    assert qr.decision == "accept"

    result = route_and_draft_proposal(
        qr, lead_id="L1", company="Acme RE", sector="real_estate",
        email="owner@acme.example", store=store,
    )
    assert result["status"] == "queued"
    assert result["offer"] == "growth_starter_pilot"
    assert result["approval_id"]

    pending = store.list_pending()
    assert len(pending) == 1
    assert pending[0].action_mode == "approval_required"
    assert pending[0].lead_id == "L1"


def test_doctrine_violation_is_declined_with_no_proposal():
    store = ApprovalStore()
    qr = qualify(
        raw_request_text="we want a cold whatsapp blast to leads",
        accepts_governance=True, owner_present=True, pain_clear=True,
    )
    assert qr.decision == "reject"

    result = route_and_draft_proposal(
        qr, lead_id="L2", company="X", sector="x",
        email="x@x.example", store=store,
    )
    assert result["status"] == "declined"
    assert store.list_pending() == []


def test_low_fit_lead_is_referred_out_without_proposal():
    store = ApprovalStore()
    qr = qualify(accepts_governance=True)  # score too low to engage
    result = route_and_draft_proposal(
        qr, lead_id="L3", company="X", sector="x",
        email="x@x.example", store=store,
    )
    assert result["status"] == "refer_out"
    assert store.list_pending() == []


def test_routed_offer_matches_qualification():
    store = ApprovalStore()
    qr = qualify(pain_clear=True, owner_present=True, accepts_governance=True)
    assert qr.recommended_offer == "capability_diagnostic"

    result = route_and_draft_proposal(
        qr, lead_id="L4", company="X", sector="b2b_services",
        email="x@x.example", store=store,
    )
    assert result["status"] == "queued"
    assert result["offer"] == "diagnostic"
