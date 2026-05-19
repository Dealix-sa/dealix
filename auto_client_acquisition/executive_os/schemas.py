"""Typed records for the Executive Orchestrator.

Frozen, slotted dataclasses — bilingual (Arabic primary, English
secondary). The orchestrator queues and prepares; it never sends or
charges. ``GUARDRAILS`` is the structural promise, every value True.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

# The 11 non-negotiables, asserted True for every executive tick.
GUARDRAILS: dict[str, bool] = {
    "no_live_send": True,
    "no_live_charge": True,
    "no_cold_whatsapp": True,
    "no_linkedin_automation": True,
    "no_scraping": True,
    "no_fake_proof": True,
    "no_fake_revenue": True,
    "no_unapproved_testimonial": True,
    "approval_required_for_external_actions": True,
    "queues_never_sends": True,
    "every_decision_audited": True,
}


@dataclass(frozen=True, slots=True)
class RankedDecision:
    """One role decision, ranked into the executive queue."""

    role: str
    rank: int
    title_ar: str
    title_en: str
    risk_level: str
    approval_required: bool
    rationale_ar: str = ""
    rationale_en: str = ""
    proof_event: str | None = None
    action_type: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class QueuedApproval:
    """An approval the orchestrator placed in the founder's queue."""

    approval_id: str
    role: str
    action_type: str
    action_mode: str
    risk_level: str
    status: str
    summary_ar: str
    summary_en: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class ExecutiveBrief:
    """The unified executive brief — one tick of the top of the pyramid."""

    generated_at: str
    one_number_that_matters: int
    headline_ar: str
    headline_en: str
    ranked_decisions: list[RankedDecision]
    queued_approvals: list[QueuedApproval]
    cross_role_risks: list[str]
    degraded_roles: list[str]
    spawned_jobs: list[dict[str, Any]]
    autonomy_level: int = 3
    guardrails: dict[str, bool] = field(default_factory=lambda: dict(GUARDRAILS))

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class ExecutiveTickResult:
    """Outcome of one ``run_executive_tick`` call. Never raises."""

    ok: bool
    reason: str
    brief: ExecutiveBrief | None = None
    aborted_at: str = ""
    intended_jobs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


__all__ = [
    "GUARDRAILS",
    "ExecutiveBrief",
    "ExecutiveTickResult",
    "QueuedApproval",
    "RankedDecision",
]
