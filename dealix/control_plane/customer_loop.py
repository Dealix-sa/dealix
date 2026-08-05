"""
Section 71 — Customer Value Loop.

For every customer:
    Onboard → Define desired outcomes → Execute → Log outcomes →
    Monthly value report → Renewal/upsell → Case study.

The monthly Customer Value Report turns ad-hoc deliverables into a
*relationship* the customer renews.
"""

from __future__ import annotations

import uuid
from collections.abc import Iterable
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from typing import Any


class CustomerStage(StrEnum):
    ONBOARD = "onboard"
    DEFINING_OUTCOMES = "defining_outcomes"
    EXECUTING = "executing"
    REPORTING = "reporting"
    RENEWAL = "renewal"
    UPSELL = "upsell"
    CASE_STUDY = "case_study"
    CHURNED = "churned"


@dataclass
class CustomerValueReport:
    report_id: str
    customer_id: str
    period: str
    activities: list[str]
    outputs: list[str]
    outcomes: list[str]
    estimated_value_sar: float
    risks_reduced: list[str]
    assets_created: list[str]
    next_actions: list[str]
    upsell_recommendation: str | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def to_dict(self) -> dict[str, Any]:
        return {
            "report_id": self.report_id,
            "customer_id": self.customer_id,
            "period": self.period,
            "activities": list(self.activities),
            "outputs": list(self.outputs),
            "outcomes": list(self.outcomes),
            "estimated_value_sar": self.estimated_value_sar,
            "risks_reduced": list(self.risks_reduced),
            "assets_created": list(self.assets_created),
            "next_actions": list(self.next_actions),
            "upsell_recommendation": self.upsell_recommendation,
            "created_at": self.created_at.isoformat(),
        }


@dataclass
class Customer:
    customer_id: str
    name: str
    workspace_id: str
    stage: CustomerStage = CustomerStage.ONBOARD
    desired_outcomes: list[str] = field(default_factory=list)
    reports: list[CustomerValueReport] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))


class CustomerValueLoop:
    def __init__(self) -> None:
        self._customers: dict[str, Customer] = {}

    def onboard(self, *, name: str, workspace_id: str) -> Customer:
        customer = Customer(
            customer_id=f"cust_{uuid.uuid4().hex[:12]}",
            name=name,
            workspace_id=workspace_id,
        )
        self._customers[customer.customer_id] = customer
        return customer

    def define_outcomes(self, customer_id: str, *, outcomes: Iterable[str]) -> Customer:
        customer = self.get(customer_id)
        customer.desired_outcomes = list(outcomes)
        customer.stage = CustomerStage.DEFINING_OUTCOMES
        return customer

    def advance(self, customer_id: str, *, stage: CustomerStage) -> Customer:
        customer = self.get(customer_id)
        customer.stage = stage
        return customer

    def file_report(
        self,
        customer_id: str,
        *,
        period: str,
        activities: Iterable[str],
        outputs: Iterable[str],
        outcomes: Iterable[str],
        estimated_value_sar: float,
        risks_reduced: Iterable[str] = (),
        assets_created: Iterable[str] = (),
        next_actions: Iterable[str] = (),
        upsell_recommendation: str | None = None,
    ) -> CustomerValueReport:
        customer = self.get(customer_id)
        report = CustomerValueReport(
            report_id=f"cvr_{uuid.uuid4().hex[:12]}",
            customer_id=customer_id,
            period=period,
            activities=list(activities),
            outputs=list(outputs),
            outcomes=list(outcomes),
            estimated_value_sar=estimated_value_sar,
            risks_reduced=list(risks_reduced),
            assets_created=list(assets_created),
            next_actions=list(next_actions),
            upsell_recommendation=upsell_recommendation,
        )
        customer.reports.append(report)
        customer.stage = CustomerStage.REPORTING
        return report

    def latest_report(self, customer_id: str) -> CustomerValueReport | None:
        customer = self.get(customer_id)
        if not customer.reports:
            return None
        return customer.reports[-1]

    def churn(self, customer_id: str) -> Customer:
        return self.advance(customer_id, stage=CustomerStage.CHURNED)

    def get(self, customer_id: str) -> Customer:
        try:
            return self._customers[customer_id]
        except KeyError as exc:
            raise KeyError(f"unknown customer: {customer_id}") from exc

    def without_value_reports(self, *, max_days: int = 35) -> list[Customer]:
        now = datetime.now(UTC)
        flagged: list[Customer] = []
        for customer in self._customers.values():
            if customer.stage is CustomerStage.CHURNED:
                continue
            if not customer.reports:
                flagged.append(customer)
                continue
            last = customer.reports[-1]
            if (now - last.created_at).days >= max_days:
                flagged.append(customer)
        return flagged

    def all(self) -> list[Customer]:
        return list(self._customers.values())
