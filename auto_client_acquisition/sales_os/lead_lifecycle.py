"""Lead lifecycle state machine (M8) — the canonical sales spine.

The repo had three divergent stage vocabularies: the intake ``LeadStatus``
(8 values), the revenue-ops ``LeadStage`` (15), and ``WarRoomOutreachStatus``
(15). None enforced transitions. This module defines ONE canonical,
ordered lifecycle and a forward-only state machine; the other vocabularies
map into it via :func:`from_intake_status` / :func:`from_revenue_stage`.

Pure logic — no DB, no I/O — so it is trivially testable. Persistence is
the ``LeadRecord.lifecycle_stage`` column plus the append-only
``lead_stage_transitions`` table; callers write a transition row using the
:class:`TransitionResult` this module returns.

Forward-only invariant: a lead may only advance to a later stage, or to the
terminal ``lost`` stage from anywhere. It can never silently move backward —
that would erase pipeline truth.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from enum import StrEnum


class LeadLifecycleStage(StrEnum):
    """Canonical, ordered lead lifecycle. ``lost`` is the only terminal."""

    CAPTURED = "captured"            # lead is in the system
    QUALIFIED = "qualified"          # passed qualification
    ENGAGED = "engaged"              # outreach drafted/approved, reply seen
    MEETING = "meeting"              # meeting booked or held
    PROPOSAL = "proposal"            # scope / proposal sent
    INVOICED = "invoiced"            # invoice sent
    PAID = "paid"                    # invoice_paid — revenue only counts here
    DELIVERING = "delivering"        # delivery started
    PROOF_DELIVERED = "proof_delivered"  # proof pack delivered
    RETAINED = "retained"            # sprint / retainer secured
    LOST = "lost"                    # terminal failure


# Ordinal order for the forward-only rule. ``lost`` is excluded — it is
# reachable from any non-terminal stage and has no successor.
STAGE_ORDER: tuple[LeadLifecycleStage, ...] = (
    LeadLifecycleStage.CAPTURED,
    LeadLifecycleStage.QUALIFIED,
    LeadLifecycleStage.ENGAGED,
    LeadLifecycleStage.MEETING,
    LeadLifecycleStage.PROPOSAL,
    LeadLifecycleStage.INVOICED,
    LeadLifecycleStage.PAID,
    LeadLifecycleStage.DELIVERING,
    LeadLifecycleStage.PROOF_DELIVERED,
    LeadLifecycleStage.RETAINED,
)

_ORDINAL: dict[LeadLifecycleStage, int] = {s: i for i, s in enumerate(STAGE_ORDER)}

# ── Mappings from the legacy vocabularies ─────────────────────────

_INTAKE_MAP: dict[str, LeadLifecycleStage] = {
    "new": LeadLifecycleStage.CAPTURED,
    "qualified": LeadLifecycleStage.QUALIFIED,
    "discovery": LeadLifecycleStage.ENGAGED,
    "proposal": LeadLifecycleStage.PROPOSAL,
    "negotiation": LeadLifecycleStage.PROPOSAL,
    "won": LeadLifecycleStage.RETAINED,
    "lost": LeadLifecycleStage.LOST,
    "disqualified": LeadLifecycleStage.LOST,
}

_REVENUE_MAP: dict[str, LeadLifecycleStage] = {
    "new_lead": LeadLifecycleStage.CAPTURED,
    "qualified_A": LeadLifecycleStage.QUALIFIED,
    "qualified_B": LeadLifecycleStage.QUALIFIED,
    "nurture": LeadLifecycleStage.ENGAGED,
    "partner_candidate": LeadLifecycleStage.ENGAGED,
    "meeting_booked": LeadLifecycleStage.MEETING,
    "meeting_done": LeadLifecycleStage.MEETING,
    "scope_requested": LeadLifecycleStage.PROPOSAL,
    "scope_sent": LeadLifecycleStage.PROPOSAL,
    "invoice_sent": LeadLifecycleStage.INVOICED,
    "invoice_paid": LeadLifecycleStage.PAID,
    "delivery_started": LeadLifecycleStage.DELIVERING,
    "proof_pack_sent": LeadLifecycleStage.PROOF_DELIVERED,
    "sprint_candidate": LeadLifecycleStage.RETAINED,
    "retainer_candidate": LeadLifecycleStage.RETAINED,
    "closed_lost": LeadLifecycleStage.LOST,
}


def from_intake_status(status: str) -> LeadLifecycleStage:
    """Map an intake ``LeadStatus`` value to the canonical lifecycle."""
    return _INTAKE_MAP.get(str(status), LeadLifecycleStage.CAPTURED)


def from_revenue_stage(stage: str) -> LeadLifecycleStage:
    """Map a revenue-ops ``LeadStage`` value to the canonical lifecycle."""
    return _REVENUE_MAP.get(str(stage), LeadLifecycleStage.CAPTURED)


# ── State machine ─────────────────────────────────────────────────

def is_terminal(stage: LeadLifecycleStage) -> bool:
    return stage == LeadLifecycleStage.LOST


def can_transition(
    current: LeadLifecycleStage, target: LeadLifecycleStage
) -> tuple[bool, str]:
    """Is ``current → target`` legal? Returns (allowed, reason)."""
    if is_terminal(current):
        return False, f"lead is terminal ({current.value}); no transitions allowed"
    if target == current:
        return False, "target stage equals current stage (no-op)"
    if target == LeadLifecycleStage.LOST:
        return True, "marked lost"
    if current not in _ORDINAL or target not in _ORDINAL:
        return False, "unknown stage"
    if _ORDINAL[target] <= _ORDINAL[current]:
        return False, (
            f"backward transition blocked: {current.value} → {target.value} "
            "(lifecycle is forward-only)"
        )
    return True, "forward transition"


def next_stages(current: LeadLifecycleStage) -> list[LeadLifecycleStage]:
    """Every stage legally reachable from ``current``."""
    if is_terminal(current):
        return []
    out = [s for s in STAGE_ORDER if can_transition(current, s)[0]]
    out.append(LeadLifecycleStage.LOST)
    return out


@dataclass
class TransitionResult:
    """The outcome of an attempted transition. Callers persist this as a
    ``lead_stage_transitions`` row when ``allowed`` is True."""

    allowed: bool
    lead_id: str
    from_stage: str
    to_stage: str
    reason: str
    actor: str
    occurred_at: str


def advance(
    *,
    lead_id: str,
    current: LeadLifecycleStage,
    target: LeadLifecycleStage,
    actor: str = "system",
    note: str = "",
) -> TransitionResult:
    """Validate a transition and return a :class:`TransitionResult`.

    Pure: does not write to the DB and does not raise — the caller inspects
    ``allowed`` and persists the transition row + updates the lead.
    """
    allowed, reason = can_transition(current, target)
    return TransitionResult(
        allowed=allowed,
        lead_id=lead_id,
        from_stage=current.value,
        to_stage=target.value,
        reason=f"{reason}: {note}" if note else reason,
        actor=actor,
        occurred_at=datetime.now(UTC).isoformat(),
    )


__all__ = [
    "LeadLifecycleStage",
    "STAGE_ORDER",
    "TransitionResult",
    "from_intake_status",
    "from_revenue_stage",
    "is_terminal",
    "can_transition",
    "next_stages",
    "advance",
]
