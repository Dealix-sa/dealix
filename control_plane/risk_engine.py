"""
Risk engine.

Inspects company state and produces a ranked list of risks. Used by the
CEO brief, the priority engine, and the system scorecard. Severities map
to the escalation matrix.
"""
from __future__ import annotations

from dataclasses import dataclass

from .company_state import CompanyState


@dataclass(frozen=True, slots=True)
class RiskItem:
    code: str
    title: str
    severity: str  # P0 | P1 | P2 | P3
    detail: str


class RiskEngine:
    def __init__(
        self,
        *,
        runway_p0_months: float = 2.0,
        runway_p1_months: float = 4.0,
        approval_p1_count: int = 5,
        health_p1_threshold: int = 60,
        health_p0_threshold: int = 40,
    ) -> None:
        self.runway_p0_months = runway_p0_months
        self.runway_p1_months = runway_p1_months
        self.approval_p1_count = approval_p1_count
        self.health_p1_threshold = health_p1_threshold
        self.health_p0_threshold = health_p0_threshold

    def assess(self, state: CompanyState) -> list[RiskItem]:
        risks: list[RiskItem] = []

        if state.runway_months and state.runway_months <= self.runway_p0_months:
            risks.append(RiskItem(
                code="RUNWAY_P0",
                title="Runway critical",
                severity="P0",
                detail=f"{state.runway_months:.1f} months remaining",
            ))
        elif state.runway_months and state.runway_months <= self.runway_p1_months:
            risks.append(RiskItem(
                code="RUNWAY_P1",
                title="Runway tight",
                severity="P1",
                detail=f"{state.runway_months:.1f} months remaining",
            ))

        if state.company_health_score <= self.health_p0_threshold:
            risks.append(RiskItem(
                code="HEALTH_P0",
                title="Company health alert",
                severity="P0",
                detail=f"score={state.company_health_score}",
            ))
        elif state.company_health_score <= self.health_p1_threshold:
            risks.append(RiskItem(
                code="HEALTH_P1",
                title="Company health watch",
                severity="P1",
                detail=f"score={state.company_health_score}",
            ))

        if state.pending_approvals >= self.approval_p1_count:
            risks.append(RiskItem(
                code="APPROVAL_BACKLOG",
                title="Approval backlog",
                severity="P1",
                detail=f"{state.pending_approvals} pending",
            ))

        for r in state.open_risks:
            risks.append(RiskItem(
                code="OPEN",
                title=r,
                severity="P2",
                detail="from state.open_risks",
            ))

        severity_order = {"P0": 0, "P1": 1, "P2": 2, "P3": 3}
        return sorted(risks, key=lambda r: severity_order.get(r.severity, 9))
