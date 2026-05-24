"""
Customer Value Loop — §102.

Every customer has desired outcomes and a monthly value report. The
report has a fixed shape so it can be rendered by any UI consistently.
"""

from __future__ import annotations

import threading
import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any


@dataclass
class CustomerOutcome:
    outcome: str
    value_sar: float
    recorded_at: str

    def to_dict(self) -> dict[str, Any]:
        return {"outcome": self.outcome, "value_sar": self.value_sar,
                "recorded_at": self.recorded_at}


@dataclass
class Customer:
    customer_id: str
    name: str
    desired_outcomes: list[str]
    value_report_due: str
    status: str = "onboarding"
    outcomes: list[CustomerOutcome] = field(default_factory=list)
    activities: list[str] = field(default_factory=list)
    outputs: list[str] = field(default_factory=list)
    assets_created: list[str] = field(default_factory=list)
    risks_reduced: list[str] = field(default_factory=list)
    onboarded_at: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "customer_id": self.customer_id,
            "name": self.name,
            "desired_outcomes": list(self.desired_outcomes),
            "value_report_due": self.value_report_due,
            "status": self.status,
            "outcomes": [o.to_dict() for o in self.outcomes],
            "activities": list(self.activities),
            "outputs": list(self.outputs),
            "assets_created": list(self.assets_created),
            "risks_reduced": list(self.risks_reduced),
            "onboarded_at": self.onboarded_at,
        }


class CustomerValueLoop:
    def __init__(self) -> None:
        self._items: dict[str, Customer] = {}
        self._lock = threading.Lock()

    def onboard(
        self, name: str, desired_outcomes: list[str], value_report_due: str
    ) -> Customer:
        with self._lock:
            c = Customer(
                customer_id=f"cus_{uuid.uuid4().hex[:12]}",
                name=name, desired_outcomes=list(desired_outcomes),
                value_report_due=value_report_due, status="active",
                onboarded_at=datetime.now(UTC).isoformat(),
            )
            self._items[c.customer_id] = c
            return c

    def get(self, customer_id: str) -> Customer | None:
        return self._items.get(customer_id)

    def log_activity(self, customer_id: str, activity: str) -> None:
        c = self._items.get(customer_id)
        if c is not None:
            c.activities.append(activity)

    def log_output(self, customer_id: str, output: str) -> None:
        c = self._items.get(customer_id)
        if c is not None:
            c.outputs.append(output)

    def log_asset(self, customer_id: str, asset_id: str) -> None:
        c = self._items.get(customer_id)
        if c is not None:
            c.assets_created.append(asset_id)

    def log_risk_reduced(self, customer_id: str, risk: str) -> None:
        c = self._items.get(customer_id)
        if c is not None:
            c.risks_reduced.append(risk)

    def log_outcome(
        self, customer_id: str, outcome: str, value_sar: float
    ) -> CustomerOutcome | None:
        c = self._items.get(customer_id)
        if c is None:
            return None
        rec = CustomerOutcome(
            outcome=outcome, value_sar=value_sar,
            recorded_at=datetime.now(UTC).isoformat(),
        )
        c.outcomes.append(rec)
        return rec

    def monthly_value_report(self, customer_id: str) -> dict[str, Any]:
        c = self._items.get(customer_id)
        if c is None:
            raise KeyError(customer_id)
        estimated = round(sum(o.value_sar for o in c.outcomes), 2)
        upsell = self._upsell_recommendation(c, estimated)
        return {
            "customer_id": c.customer_id,
            "name": c.name,
            "activities": list(c.activities),
            "outputs": list(c.outputs),
            "outcomes": [o.to_dict() for o in c.outcomes],
            "estimated_value": estimated,
            "risks_reduced": list(c.risks_reduced),
            "assets_created": list(c.assets_created),
            "next_actions": self._next_actions(c),
            "upsell_recommendation": upsell,
        }

    @staticmethod
    def _next_actions(c: Customer) -> list[str]:
        if not c.outcomes:
            return ["schedule_first_outcome_review"]
        return ["confirm_outcomes_with_customer", "plan_next_quarter"]

    @staticmethod
    def _upsell_recommendation(c: Customer, estimated: float) -> str:
        if estimated >= 100_000:
            return "expansion_tier"
        if estimated >= 25_000:
            return "addon_module"
        return "stay_on_current_plan"
