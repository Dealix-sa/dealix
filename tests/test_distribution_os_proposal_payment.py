"""Distribution OS — proposal factory + payment & delivery handoffs."""

from __future__ import annotations

import pytest

from auto_client_acquisition.distribution_os import (
    delivery_handoff,
    payment_handoff,
    proposal,
)
from auto_client_acquisition.distribution_os.payment_handoff import PaymentHandoffStatus


@pytest.fixture(autouse=True)
def _isolate(tmp_path, monkeypatch):
    monkeypatch.setenv("DEALIX_PROPOSALS_PATH", str(tmp_path / "proposals.jsonl"))
    monkeypatch.setenv("DEALIX_PAYMENT_HANDOFFS_PATH", str(tmp_path / "pay.jsonl"))
    monkeypatch.setenv("DEALIX_DELIVERY_HANDOFFS_PATH", str(tmp_path / "deliv.jsonl"))


# ── proposal ─────────────────────────────────────────────────────────────────


def test_proposal_price_comes_from_catalog() -> None:
    p = proposal.generate_proposal(
        prospect_id="pros_1",
        product_id="prod_data_pack_v1",
        problem="leak",
        proposed_solution="organise",
        out_of_scope=["external sending"],
    )
    assert (p.price_min_sar, p.price_max_sar) == (1500, 1500)
    assert p.approval_status == "pending_approval"


def test_proposal_requires_prospect_product_and_closed_scope() -> None:
    with pytest.raises(ValueError):
        proposal.generate_proposal(prospect_id="", product_id="prod_sprint_v1", out_of_scope=["x"])
    with pytest.raises(ValueError):
        proposal.generate_proposal(prospect_id="p", product_id="prod_unknown", out_of_scope=["x"])
    with pytest.raises(ValueError):
        proposal.generate_proposal(prospect_id="p", product_id="prod_sprint_v1", out_of_scope=[])


def test_proposal_narrative_with_guarantee_is_blocked() -> None:
    with pytest.raises(ValueError):
        proposal.generate_proposal(
            prospect_id="p",
            product_id="prod_sprint_v1",
            problem="نضمن لك مبيعات مضمونة",
            out_of_scope=["x"],
        )


def test_proposal_approve_reject() -> None:
    p = proposal.generate_proposal(prospect_id="p", product_id="prod_sprint_v1", out_of_scope=["x"])
    assert proposal.approve_proposal(p.id).approval_status == "approved"
    p2 = proposal.generate_proposal(
        prospect_id="p", product_id="prod_sprint_v1", out_of_scope=["x"]
    )
    assert proposal.reject_proposal(p2.id).approval_status == "rejected"


# ── payment handoff ──────────────────────────────────────────────────────────


def test_handoff_requires_all_six_approvals() -> None:
    h = payment_handoff.prepare_handoff(
        proposal_id="prop_1", customer_id="Acme", product_id="prod_sprint_v1", amount_sar=499
    )
    assert h.status == PaymentHandoffStatus.PENDING_APPROVAL.value
    assert h.governance_status == "requires_founder_approval"
    keys = [
        "proposal_approved",
        "scope_confirmed",
        "price_confirmed",
        "decision_maker_confirmed",
        "risk_reviewed",
    ]
    for k in keys:
        h = payment_handoff.set_approval(h.id, k, True)
        assert h.status == PaymentHandoffStatus.PENDING_APPROVAL.value  # still missing founder
    h = payment_handoff.set_approval(h.id, "founder_approved", True)
    assert h.status == PaymentHandoffStatus.APPROVED.value
    assert h.governance_status == "approved"


def test_handoff_amount_must_be_in_catalog_band() -> None:
    with pytest.raises(ValueError):
        payment_handoff.prepare_handoff(
            proposal_id="p", customer_id="c", product_id="prod_sprint_v1", amount_sar=99999
        )


def test_handoff_rejects_unknown_product_and_missing_proposal() -> None:
    with pytest.raises(ValueError):
        payment_handoff.prepare_handoff(
            proposal_id="", customer_id="c", product_id="prod_sprint_v1", amount_sar=499
        )
    with pytest.raises(ValueError):
        payment_handoff.prepare_handoff(
            proposal_id="p", customer_id="c", product_id="nope", amount_sar=499
        )


def test_handoff_has_no_charge_capability() -> None:
    # Doctrine: AI never charges. No charge/send/link function may exist.
    public = set(payment_handoff.__all__)
    assert not any(
        w in name.lower() for name in public for w in ("charge", "send", "link", "moyasar")
    )


def test_set_unknown_approval_raises() -> None:
    h = payment_handoff.prepare_handoff(
        proposal_id="p", customer_id="c", product_id="prod_sprint_v1", amount_sar=499
    )
    with pytest.raises(ValueError):
        payment_handoff.set_approval(h.id, "wishful_thinking", True)


# ── delivery handoff ─────────────────────────────────────────────────────────


def test_delivery_handoff_requires_success_metric_and_valid_product() -> None:
    with pytest.raises(ValueError):
        delivery_handoff.create_handoff(
            customer_id="c", product_sold="prod_sprint_v1", success_metric=""
        )
    with pytest.raises(ValueError):
        delivery_handoff.create_handoff(customer_id="c", product_sold="nope", success_metric="x")
    h = delivery_handoff.create_handoff(
        customer_id="c",
        product_sold="prod_sprint_v1",
        success_metric="reply rate up",
        first_workflow="followups",
    )
    assert h.status == "queued"
    assert delivery_handoff.update_status(h.id, "active").status == "active"
