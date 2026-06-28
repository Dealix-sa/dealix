"""Negotiation Desk — guardrailed objection handling.

The desk proposes *response strategies* and *scope adjustments*. It is hard
constrained: it can never approve a discount, set a final price, accept legal
terms, promise guaranteed results, or commit a delivery date without a
capacity check. Those are A3-restricted and require founder approval.
"""

from __future__ import annotations

from typing import Any, Mapping

from app.commercial.schemas import NegotiationDraft

# Things the desk may NEVER do. Surfaced on every draft for auditability.
FORBIDDEN_COMMITMENTS = (
    "approve_discount",
    "set_final_price",
    "accept_legal_terms",
    "guarantee_results",
    "commit_delivery_date_without_capacity_check",
    "sign_or_accept_contract",
    "commit_payment_terms",
    "promise_refund",
)

# Allowed levers — all reversible, all non-binding.
_PLAYBOOK: dict[str, dict[str, Any]] = {
    "price_objection": {
        "response": (
            "Acknowledge budget. Offer a smaller paid pilot or diagnostic-first "
            "sprint to prove value before scaling. Do NOT offer a discount or a "
            "final price — propose a scope that fits the budget instead."
        ),
        "scope_options": [
            "smaller_pilot",
            "diagnostic_first",
            "phased_scope",
            "lower_retainer_tier",
            "proof_first_sprint",
        ],
    },
    "not_now": {
        "response": (
            "Respect timing. Propose a lightweight proof-first sprint or a "
            "scheduled check-in. Keep the door open without pressure."
        ),
        "scope_options": ["proof_first_sprint", "alternative_timeline", "diagnostic_first"],
    },
    "contract_request": {
        "response": (
            "ESCALATE to founder. Legal terms, contract acceptance and payment "
            "commitments are A3-restricted. Prepare a proposal brief only."
        ),
        "scope_options": ["phased_scope"],
    },
    "partnership_interest": {
        "response": (
            "Propose a partner model with a defined pilot scope. No revenue-share "
            "or exclusivity commitment without founder approval."
        ),
        "scope_options": ["partner_model", "phased_scope", "diagnostic_first"],
    },
    "send_details": {
        "response": (
            "Send a scoped brief with pricing *range* (not a final price) and "
            "clear out-of-scope. Keep draft-only until approved."
        ),
        "scope_options": ["diagnostic_first", "phased_scope"],
    },
}

_DEFAULT = {
    "response": (
        "Clarify the objection, restate value, and propose a low-risk next step "
        "(diagnostic-first). Never commit price, terms or guaranteed results."
    ),
    "scope_options": ["diagnostic_first", "smaller_pilot"],
}


def build_negotiation_draft(
    card_id: str,
    objection_type: str,
    negotiation_index: int = 0,
) -> NegotiationDraft:
    play = _PLAYBOOK.get(objection_type, _DEFAULT)
    return NegotiationDraft(
        negotiation_id=f"nego_{card_id}_{negotiation_index:03d}",
        card_id=card_id,
        objection_type=objection_type,
        allowed_response=play["response"],
        forbidden_commitments=list(FORBIDDEN_COMMITMENTS),
        scope_adjustment_options=list(play["scope_options"]),
        approval_required=True,
    )


def build_negotiation_drafts(
    replies: list[Any],
) -> list[NegotiationDraft]:
    """Build negotiation drafts for replies that warrant negotiation."""
    negotiable = {
        "price_objection",
        "not_now",
        "contract_request",
        "partnership_interest",
        "send_details",
    }
    drafts: list[NegotiationDraft] = []
    idx = 0
    for reply in replies:
        rtype = _get(reply, "reply_type")
        if rtype in negotiable:
            drafts.append(build_negotiation_draft(_get(reply, "card_id"), rtype, idx))
            idx += 1
    return drafts


def _get(obj: Any, key: str) -> Any:
    if isinstance(obj, Mapping):
        return obj.get(key)
    return getattr(obj, key, None)
