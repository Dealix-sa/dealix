"""
Agent risk scoring.

Risk is computed from the *declared scope*, not from runtime behavior.
The score is a 0–1 float; the band drives the minimum lifecycle stage
the agent is allowed to occupy before approval gating.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

# Capability → base risk weight. Anything not listed defaults to 0.05.
_CAPABILITY_RISK: dict[str, float] = {
    # read-only — cheap
    "read_approved_opportunity": 0.02,
    "read_public_data": 0.01,
    "read_internal_doc": 0.03,
    # drafting — moderate
    "draft_proposal": 0.10,
    "draft_message": 0.10,
    "summarize_call": 0.05,
    "flag_risk": 0.05,
    # writing internal state — higher
    "update_crm_internal": 0.20,
    "create_workflow_internal": 0.20,
    # external & monetary — top tier
    "send_external": 0.40,
    "approve_price": 0.40,
    "sign_contract": 0.60,
    "export_data": 0.45,
    "issue_refund": 0.50,
    "modify_production_config": 0.55,
}

_FORBIDDEN_DAMPENER = 0.05  # every forbidden capability lowers risk slightly


class RiskBand(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class AgentRiskScore:
    score: float
    band: RiskBand
    contributors: list[tuple[str, float]]
    notes: list[str]

    def requires_human_approval(self) -> bool:
        return self.band in (RiskBand.HIGH, RiskBand.CRITICAL)


def _band(score: float) -> RiskBand:
    if score >= 0.6:
        return RiskBand.CRITICAL
    if score >= 0.4:
        return RiskBand.HIGH
    if score >= 0.2:
        return RiskBand.MEDIUM
    return RiskBand.LOW


def score_agent_risk(
    capability_scope: list[str] | tuple[str, ...],
    forbidden_capabilities: list[str] | tuple[str, ...] = (),
    *,
    workspace_scope: list[str] | tuple[str, ...] = (),
    handles_personal_data: bool = False,
    can_initiate_external_send: bool = False,
) -> AgentRiskScore:
    contributors: list[tuple[str, float]] = []
    total = 0.0
    for cap in capability_scope:
        w = _CAPABILITY_RISK.get(cap, 0.05)
        contributors.append((cap, w))
        total += w

    if handles_personal_data:
        contributors.append(("handles_personal_data", 0.10))
        total += 0.10
    if can_initiate_external_send:
        contributors.append(("can_initiate_external_send", 0.20))
        total += 0.20
    if not workspace_scope:
        contributors.append(("no_workspace_scope", 0.05))
        total += 0.05

    dampener = _FORBIDDEN_DAMPENER * len(forbidden_capabilities)
    if dampener:
        contributors.append(("forbidden_capabilities", -dampener))
        total -= dampener

    score = max(0.0, min(1.0, total))
    notes = []
    if score >= 0.6:
        notes.append("CRITICAL risk: never promote past APPROVAL_GATED without S4 review")
    elif score >= 0.4:
        notes.append("HIGH risk: keep at APPROVAL_GATED until 200+ clean runs")
    elif score >= 0.2:
        notes.append("MEDIUM risk: standard promotion thresholds apply")
    else:
        notes.append("LOW risk: standard promotion thresholds apply")
    return AgentRiskScore(
        score=round(score, 4),
        band=_band(score),
        contributors=contributors,
        notes=notes,
    )
