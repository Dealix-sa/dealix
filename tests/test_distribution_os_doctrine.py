"""Doctrine guards for the distribution_os layer (the 11 non-negotiables).

These complement the repo-wide guard tests (test_no_cold_whatsapp.py, etc.) by
asserting the new Revenue Execution layer cannot send, cannot charge, cannot
invent prices, and never ships an un-governed or guaranteed-outcome draft.
"""

from __future__ import annotations

import pytest

from auto_client_acquisition.distribution_os import (
    catalog,
    delivery_handoff,
    draft_factory,
    payment_handoff,
    proposal,
    prospect,
)
from auto_client_acquisition.distribution_os.draft_factory import DraftStatus, DraftType

_FORBIDDEN_VERBS = ("send", "charge", "scrape", "automate", "blast", "moyasar", "link")


@pytest.fixture(autouse=True)
def _isolate(tmp_path, monkeypatch):
    for var, name in (
        ("DEALIX_PROSPECTS_PATH", "prospects.jsonl"),
        ("DEALIX_DRAFTS_PATH", "drafts.jsonl"),
        ("DEALIX_PROPOSALS_PATH", "proposals.jsonl"),
        ("DEALIX_PAYMENT_HANDOFFS_PATH", "pay.jsonl"),
        ("DEALIX_DELIVERY_HANDOFFS_PATH", "deliv.jsonl"),
    ):
        monkeypatch.setenv(var, str(tmp_path / name))


def _prospect(**over):
    base = {
        "company": "Acme",
        "sector": "marketing_agencies",
        "pain_hypothesis": "leaks",
        "offer_angle": "prod_sprint_v1",
        "preferred_channel": "email",
        "risk": "low",
    }
    base.update(over)
    return prospect.add_prospect(**base)


def test_no_external_send_capability_in_any_submodule() -> None:
    """NON-NEGOTIABLE: no external send / charge / scrape function exists."""
    for module in (draft_factory, proposal, payment_handoff, delivery_handoff):
        for name in module.__all__:
            lowered = name.lower()
            assert not any(
                verb in lowered for verb in _FORBIDDEN_VERBS
            ), f"{module.__name__}.{name}"


def test_every_generated_draft_carries_a_governance_status() -> None:
    """NON-NEGOTIABLE: output requires governance status."""
    p = _prospect()
    for dtype in DraftType:
        d = draft_factory.generate_draft(prospect=p, draft_type=dtype)
        assert d.governance_status in {"pending_approval", "needs_edit", "blocked"}
        assert d.status == d.governance_status


def test_no_draft_is_ever_auto_sent_on_generation() -> None:
    """NON-NEGOTIABLE: all drafts pending approval — never sent by AI."""
    p = _prospect()
    d = draft_factory.generate_draft(prospect=p, draft_type=DraftType.OUTREACH_FIRST)
    assert d.status != DraftStatus.SENT_VIA_INTEGRATION.value
    assert d.status != DraftStatus.APPROVED.value


def test_guaranteed_claim_draft_cannot_reach_approved() -> None:
    """NON-NEGOTIABLE: no guaranteed claims."""
    bad = _prospect(company="B", pain_hypothesis="نضمن لك نتائج مبيعات مضمونة 100%")
    d = draft_factory.generate_draft(prospect=bad, draft_type=DraftType.DIAGNOSTIC_SUMMARY)
    assert d.governance_status == "blocked"
    with pytest.raises(ValueError):
        draft_factory.approve_draft(d.id)


def test_proposal_and_handoff_prices_only_from_catalog() -> None:
    """NON-NEGOTIABLE: every offer links to a catalog product; no invented price."""
    for product in catalog.all_products():
        prop = proposal.generate_proposal(
            prospect_id="p", product_id=product.id, out_of_scope=["external send"]
        )
        pmin, pmax = catalog.price_band(product.id)
        assert (prop.price_min_sar, prop.price_max_sar) == (pmin, pmax)
    # an off-catalog product can never produce a proposal or handoff
    with pytest.raises(ValueError):
        proposal.generate_proposal(prospect_id="p", product_id="prod_imaginary", out_of_scope=["x"])
    with pytest.raises(ValueError):
        payment_handoff.prepare_handoff(
            proposal_id="x", customer_id="c", product_id="prod_imaginary", amount_sar=10
        )


def test_payment_handoff_defaults_to_requiring_founder_approval() -> None:
    """NON-NEGOTIABLE: AI never charges; founder approval is required."""
    h = payment_handoff.prepare_handoff(
        proposal_id="p", customer_id="c", product_id="prod_sprint_v1", amount_sar=499
    )
    assert h.governance_status == "requires_founder_approval"
    assert h.approvals["founder_approved"] is False
