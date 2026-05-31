from __future__ import annotations

from dataclasses import dataclass


@dataclass
class EnablementProgress:
    partner_id: str
    score: float
    completed: list[str]
    pending: list[str]


_REQUIRED_MODULES = (
    "positioning_training",
    "delivery_playbook_walkthrough",
    "approved_claims_quiz",
    "approval_flow_walkthrough",
    "incident_response_drill",
)


def score_enablement(
    partner_id: str, completed_modules: list[str]
) -> EnablementProgress:
    completed = [m for m in _REQUIRED_MODULES if m in completed_modules]
    pending = [m for m in _REQUIRED_MODULES if m not in completed_modules]
    pct = (len(completed) / len(_REQUIRED_MODULES)) * 100
    return EnablementProgress(
        partner_id=partner_id,
        score=round(pct, 2),
        completed=completed,
        pending=pending,
    )
