"""Delivery Handoff — bridge a won deal into delivery.

Produces a handoff stub: required inputs from the client, a kickoff agenda,
acceptance criteria and a proof-pack plan. Status starts at
``pending_approval`` — a handoff is an approval-gated pipeline stage.
"""

from __future__ import annotations

from typing import Any, Mapping

from app.commercial.schemas import DeliveryHandoff


def build_delivery_handoff(
    account_id: str,
    proposal_id: str = "",
    handoff_index: int = 0,
) -> DeliveryHandoff:
    return DeliveryHandoff(
        handoff_id=f"handoff_{account_id}_{handoff_index:03d}",
        account_id=account_id,
        proposal_id=proposal_id,
        required_inputs=[
            "Signed scope document (founder-approved)",
            "Data / source access per kickoff checklist",
            "Named client point-of-contact",
            "Defined success metrics",
        ],
        kickoff_agenda=[
            "Confirm scope, timeline & success metrics",
            "Walk through data handling & safety doctrine",
            "Agree weekly cadence & command-room access",
        ],
        acceptance_criteria=[
            "Client confirms scope & out-of-scope",
            "Baseline metrics captured before work starts",
            "Proof-pack plan agreed",
        ],
        proof_pack_plan=[
            "Before/after metrics (truthful, sourced)",
            "Sample Growth Cards & drafts produced",
            "Command-room snapshot at milestone",
        ],
        status="pending_approval",
    )


def build_delivery_handoffs(
    proposals: list[Any],
    card_to_account: Mapping[str, str] | None = None,
) -> list[DeliveryHandoff]:
    """Stub a handoff per proposal brief (pending approval — never auto-active)."""
    card_to_account = card_to_account or {}
    out: list[DeliveryHandoff] = []
    for i, prop in enumerate(proposals):
        card_id = _get(prop, "card_id") or ""
        proposal_id = _get(prop, "proposal_id") or ""
        account_id = card_to_account.get(card_id, card_id)
        out.append(build_delivery_handoff(account_id, proposal_id, i))
    return out


def _get(obj: Any, key: str) -> Any:
    if isinstance(obj, Mapping):
        return obj.get(key)
    return getattr(obj, key, None)
