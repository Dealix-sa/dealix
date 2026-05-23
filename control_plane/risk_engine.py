"""RiskEngine: classify operational risks across Dealix systems."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from enum import Enum
from typing import Iterable, List


class RiskArea(str, Enum):
    REVENUE = "Revenue"
    DELIVERY = "Delivery"
    TRUST = "Trust"
    PRODUCT = "Product"
    FOUNDER = "Founder"
    LEGAL = "Legal/Compliance"
    REPUTATION = "Reputation"


class RiskSeverity(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"


@dataclass
class Risk:
    area: RiskArea
    severity: RiskSeverity
    title: str
    detail: str
    mitigation: str
    as_of: str = field(default_factory=lambda: date.today().isoformat())


@dataclass
class RiskSignals:
    payment_fallback_missing: bool = False
    qa_checklist_missing: bool = False
    public_repo_contains_leads: bool = False
    a3_action_attempted: bool = False
    ci_failing_on_main: bool = False
    pending_founder_approvals: int = 0
    public_safety_failures: int = 0
    overdue_client_deliveries: int = 0


class RiskEngine:
    """Maps boolean/numeric signals into a typed Risk list."""

    def evaluate(self, signals: RiskSignals) -> List[Risk]:
        risks: List[Risk] = []

        if signals.payment_fallback_missing:
            risks.append(
                Risk(
                    area=RiskArea.REVENUE,
                    severity=RiskSeverity.HIGH,
                    title="No payment fallback",
                    detail="Single payment provider with no failover.",
                    mitigation="Add a secondary payment path before next paid sprint.",
                )
            )

        if signals.qa_checklist_missing:
            risks.append(
                Risk(
                    area=RiskArea.DELIVERY,
                    severity=RiskSeverity.HIGH,
                    title="No QA checklist",
                    detail="Reports may ship without verification.",
                    mitigation="Lock QA_CHECKLIST.md before next delivery.",
                )
            )

        if signals.public_repo_contains_leads:
            risks.append(
                Risk(
                    area=RiskArea.TRUST,
                    severity=RiskSeverity.CRITICAL,
                    title="Public repo contains lead data",
                    detail="Client or lead data must live in private ops.",
                    mitigation="Purge and move to dealix-ops-private; rotate any leaked tokens.",
                )
            )

        if signals.a3_action_attempted:
            risks.append(
                Risk(
                    area=RiskArea.TRUST,
                    severity=RiskSeverity.CRITICAL,
                    title="A3 action attempted",
                    detail="A prohibited-auto action was attempted by an agent or workflow.",
                    mitigation="Block at approval router; require founder sign-off; audit log.",
                )
            )

        if signals.ci_failing_on_main:
            risks.append(
                Risk(
                    area=RiskArea.PRODUCT,
                    severity=RiskSeverity.HIGH,
                    title="CI failing on main",
                    detail="Broken main blocks safe deployment.",
                    mitigation="Revert offending change or hotfix before next release.",
                )
            )

        if signals.pending_founder_approvals > 15:
            risks.append(
                Risk(
                    area=RiskArea.FOUNDER,
                    severity=RiskSeverity.HIGH,
                    title="Founder approval backlog",
                    detail=f"{signals.pending_founder_approvals} approvals pending.",
                    mitigation="Clear approvals or delegate per APPROVAL_MATRIX.md.",
                )
            )

        if signals.public_safety_failures > 0:
            risks.append(
                Risk(
                    area=RiskArea.REPUTATION,
                    severity=RiskSeverity.HIGH,
                    title="Public safety check failed",
                    detail=f"{signals.public_safety_failures} public safety failures detected.",
                    mitigation="Fix banned-claim or evidence violations before next push.",
                )
            )

        if signals.overdue_client_deliveries > 0:
            risks.append(
                Risk(
                    area=RiskArea.DELIVERY,
                    severity=RiskSeverity.MEDIUM,
                    title="Client delivery overdue",
                    detail=f"{signals.overdue_client_deliveries} active client(s) past due.",
                    mitigation="Escalate to founder; communicate revised ETA with client.",
                )
            )

        return risks

    @staticmethod
    def filter_critical(risks: Iterable[Risk]) -> List[Risk]:
        return [r for r in risks if r.severity == RiskSeverity.CRITICAL]
