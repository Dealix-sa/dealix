"""
Company OS Approval Matrix.

Canonical mapping from action class to approval tier (A0–A4) as defined in
`docs/trust/APPROVAL_MATRIX.md`. This is intentionally a separate, small,
auditable module from the broader `approval.py` queue — it encodes *which*
tier an action requires; `approval.py` runs the queue that enforces it.

Tier semantics:
    A0  — internal-only artifact, no approval needed
    A1  — external action to a specific recipient; founder per-item
    A2  — external action to defined audience; founder per-batch
    A3  — public claim; founder + evidence pack
    A4  — prohibited from automation; founder + advisor only

If an action class is not in the matrix, the safe default is A4. Refusing
the unknown is a feature of this design.
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from enum import StrEnum


class ApprovalTier(StrEnum):
    A0 = "A0"
    A1 = "A1"
    A2 = "A2"
    A3 = "A3"
    A4 = "A4"


class ApprovalRequired(Exception):  # noqa: N818
    """Raised when an action attempts to execute without the required approval.

    Named without an `Error` suffix on purpose: the name mirrors the
    `Approval Required` row in `docs/trust/APPROVAL_MATRIX.md` so the
    code reads like the policy doc.
    """


class ProhibitedAction(Exception):  # noqa: N818
    """Raised when an A4 (prohibited from automation) action is attempted.

    Named without an `Error` suffix on purpose: matches the A4 row label
    in `docs/trust/APPROVAL_MATRIX.md`.
    """


@dataclass(frozen=True)
class MatrixEntry:
    action_class: str
    tier: ApprovalTier
    founder_required: bool
    advisor_required: bool
    note: str = ""


_MATRIX: dict[str, MatrixEntry] = {
    "internal_lead_scoring": MatrixEntry(
        "internal_lead_scoring", ApprovalTier.A0, False, False
    ),
    "lead_enrichment": MatrixEntry("lead_enrichment", ApprovalTier.A0, False, False),
    "message_draft_generation": MatrixEntry(
        "message_draft_generation", ApprovalTier.A0, False, False
    ),
    "sending_first_outreach": MatrixEntry(
        "sending_first_outreach", ApprovalTier.A1, True, False
    ),
    "sending_followup": MatrixEntry(
        "sending_followup", ApprovalTier.A2, True, False, "batch-approvable"
    ),
    "sending_proposal": MatrixEntry(
        "sending_proposal", ApprovalTier.A1, True, False, "per-item always"
    ),
    "sending_invoice": MatrixEntry(
        "sending_invoice", ApprovalTier.A1, True, False, "per-item always"
    ),
    "pricing_change": MatrixEntry(
        "pricing_change", ApprovalTier.A2, True, False, "log in pricing_experiments"
    ),
    "refund_or_credit": MatrixEntry(
        "refund_or_credit", ApprovalTier.A4, True, True, "never auto"
    ),
    "contract_change": MatrixEntry(
        "contract_change", ApprovalTier.A4, True, True, "never auto"
    ),
    "public_claim_post": MatrixEntry(
        "public_claim_post", ApprovalTier.A3, True, False, "claim_guard + founder"
    ),
    "public_claim_case_study": MatrixEntry(
        "public_claim_case_study",
        ApprovalTier.A3,
        True,
        True,
        "+ client signoff",
    ),
    "compliance_claim": MatrixEntry(
        "compliance_claim", ApprovalTier.A4, True, True, "prohibited from automation"
    ),
    "share_client_data_externally": MatrixEntry(
        "share_client_data_externally",
        ApprovalTier.A4,
        True,
        True,
        "DPA + client consent",
    ),
    "onboard_contractor_with_data_access": MatrixEntry(
        "onboard_contractor_with_data_access",
        ApprovalTier.A4,
        True,
        True,
        "NDA + scoped",
    ),
    "remove_from_suppression_list": MatrixEntry(
        "remove_from_suppression_list",
        ApprovalTier.A4,
        True,
        True,
        "almost never",
    ),
    "outreach_to_suppression_contact": MatrixEntry(
        "outreach_to_suppression_contact",
        ApprovalTier.A4,
        True,
        True,
        "blocked in code",
    ),
    "send_on_saudi_public_holiday": MatrixEntry(
        "send_on_saudi_public_holiday",
        ApprovalTier.A4,
        True,
        True,
        "blocked in code",
    ),
    "cold_whatsapp": MatrixEntry(
        "cold_whatsapp", ApprovalTier.A4, True, True, "blocked in code"
    ),
}


def tier_for(action_class: str) -> ApprovalTier:
    """Return the required approval tier for an action class.

    Unknown action classes default to A4 (prohibited) — refusing unknown
    actions is the safe default per `DEALIX_DECISION_RULES.md`.
    """
    entry = _MATRIX.get(action_class)
    if entry is None:
        return ApprovalTier.A4
    return entry.tier


def entry_for(action_class: str) -> MatrixEntry:
    """Return the full matrix entry for an action class; default A4."""
    return _MATRIX.get(
        action_class,
        MatrixEntry(
            action_class=action_class,
            tier=ApprovalTier.A4,
            founder_required=True,
            advisor_required=True,
            note="unknown action — defaulting to A4 (prohibited)",
        ),
    )


def all_actions() -> Iterable[str]:
    """Iterate over all registered action classes."""
    return _MATRIX.keys()


def require_approval(
    action_class: str,
    *,
    approvals: list[str] | None = None,
    has_evidence_pack: bool = False,
) -> None:
    """Raise if the action cannot proceed with the supplied approvals.

    `approvals` is the set of approver identifiers that have signed off
    (e.g. ``["founder"]``, ``["founder", "advisor"]``). `has_evidence_pack`
    is required for A3 actions.

    A0 always passes; A4 always raises (prohibited from automation).
    """
    approvals = approvals or []
    entry = entry_for(action_class)
    tier = entry.tier

    if tier == ApprovalTier.A4:
        raise ProhibitedAction(
            f"Action {action_class!r} is A4 (prohibited from automation). "
            "Founder + advisor must execute manually."
        )
    if tier == ApprovalTier.A0:
        return
    if entry.founder_required and "founder" not in approvals:
        raise ApprovalRequired(
            f"Action {action_class!r} requires founder approval (tier {tier.value})."
        )
    if entry.advisor_required and "advisor" not in approvals:
        raise ApprovalRequired(
            f"Action {action_class!r} requires advisor approval (tier {tier.value})."
        )
    if tier == ApprovalTier.A3 and not has_evidence_pack:
        raise ApprovalRequired(
            f"Action {action_class!r} is A3 (public claim) and requires an evidence pack."
        )


__all__ = [
    "ApprovalRequired",
    "ApprovalTier",
    "MatrixEntry",
    "ProhibitedAction",
    "all_actions",
    "entry_for",
    "require_approval",
    "tier_for",
]
