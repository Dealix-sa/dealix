"""Negotiation Desk can never approve discounts or final/binding terms."""

from __future__ import annotations

from app.commercial import negotiation_desk
from app.commercial.negotiation_desk import FORBIDDEN_COMMITMENTS
from app.commercial.reply_classifier import classify_reply


def test_forbidden_commitments_cover_pricing_and_legal():
    for forbidden in (
        "approve_discount",
        "set_final_price",
        "accept_legal_terms",
        "guarantee_results",
        "sign_or_accept_contract",
    ):
        assert forbidden in FORBIDDEN_COMMITMENTS


def test_price_objection_draft_offers_scope_not_discount():
    draft = negotiation_desk.build_negotiation_draft("c1", "price_objection")
    assert draft.approval_required is True
    assert "approve_discount" in draft.forbidden_commitments
    assert "discount" not in draft.allowed_response.lower() or "do not" in draft.allowed_response.lower()
    assert "smaller_pilot" in draft.scope_adjustment_options


def test_contract_request_escalates_not_accepts():
    draft = negotiation_desk.build_negotiation_draft("c1", "contract_request")
    assert "ESCALATE" in draft.allowed_response
    assert "sign_or_accept_contract" in draft.forbidden_commitments


def test_drafts_built_only_for_negotiable_replies():
    replies = [
        classify_reply("too expensive", "c1"),
        classify_reply("interested!", "c2"),  # not a negotiation trigger
    ]
    drafts = negotiation_desk.build_negotiation_drafts(replies)
    assert all(d.approval_required for d in drafts)
    assert any(d.objection_type == "price_objection" for d in drafts)
