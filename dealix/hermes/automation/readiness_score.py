"""
AutomationReadinessScore — combine trust pass rate, outcome success
rate, incident rate, human correction rate, data sensitivity, and
external risk into a single decision.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class AutomationDecision(StrEnum):
    DRAFT_ONLY = "draft_only"
    APPROVAL_GATED = "approval_gated"
    LOW_RISK_AUTONOMY = "low_risk_autonomy"
    NEVER_AUTONOMOUS = "never_autonomous"


@dataclass
class AutomationReadinessScore:
    workflow_id: str
    score: float
    decision: AutomationDecision
    reasons: tuple[str, ...]


def score_automation_readiness(
    *,
    workflow_id: str,
    trust_pass_rate: float,
    outcome_success_rate: float,
    incident_rate: float,
    human_correction_rate: float,
    data_sensitivity: str,  # "S0" .. "S3"
    external_risk: str,  # "low" | "medium" | "high"
) -> AutomationReadinessScore:
    reasons: list[str] = []
    if data_sensitivity in ("S3",):
        reasons.append("S3 data — never fully autonomous")
        return AutomationReadinessScore(workflow_id, 0.0, AutomationDecision.NEVER_AUTONOMOUS, tuple(reasons))
    if external_risk == "high":
        reasons.append("external risk high — keep approval-gated")

    score = round(
        0.3 * trust_pass_rate
        + 0.3 * outcome_success_rate
        - 0.2 * incident_rate
        - 0.2 * human_correction_rate,
        4,
    )

    if score >= 0.7 and external_risk == "low":
        decision = AutomationDecision.LOW_RISK_AUTONOMY
    elif score >= 0.5:
        decision = AutomationDecision.APPROVAL_GATED
    else:
        decision = AutomationDecision.DRAFT_ONLY

    return AutomationReadinessScore(workflow_id, score, decision, tuple(reasons))
