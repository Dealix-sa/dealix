"""Single-source-of-truth view of "what is the state of the company today".

The control plane reads from many systems (CRM, ledgers, pipelines,
approval logs, trust queues, CI). Rather than each consumer poking each
system, we materialise the daily state into one typed object so every
downstream loop (CEO Brief, Decision Queue, Action Router, Risk Engine,
Approval Router) reads from the same picture.

The full human-facing description lives in
``docs/control_plane/COMPANY_STATE_SCHEMA.md``.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass
class RevenueState:
    cash_collected: float = 0.0
    cash_expected: float = 0.0
    mrr: float = 0.0
    proposals_pending: int = 0
    pipeline_value: float = 0.0
    best_next_close: str = ""


@dataclass
class SalesState:
    new_leads: int = 0
    qualified_leads: int = 0
    contacted: int = 0
    replies: int = 0
    calls_booked: int = 0
    proposals_sent: int = 0


@dataclass
class DeliveryState:
    active_clients: int = 0
    reports_due: int = 0
    qa_needed: int = 0
    blocked_deliveries: int = 0
    delivery_on_time_rate: float = 0.0


@dataclass
class TrustState:
    approvals_waiting: int = 0
    a3_blocked_actions: int = 0
    opt_outs: int = 0
    claims_needing_review: int = 0
    incidents: int = 0


@dataclass
class ProductState:
    ci_status: str = "unknown"
    bugs_open: int = 0
    release_candidate: str = ""
    customer_requested_features: int = 0
    trust_tests_status: str = "unknown"


@dataclass
class LearningState:
    experiments_running: int = 0
    latest_win_loss: str = ""
    best_message: str = ""
    best_sector: str = ""
    biggest_objection: str = ""
    next_experiment: str = ""


@dataclass
class CompanyState:
    """Frozen snapshot of company state at a point in time."""

    as_of: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    revenue: RevenueState = field(default_factory=RevenueState)
    sales: SalesState = field(default_factory=SalesState)
    delivery: DeliveryState = field(default_factory=DeliveryState)
    trust: TrustState = field(default_factory=TrustState)
    product: ProductState = field(default_factory=ProductState)
    learning: LearningState = field(default_factory=LearningState)

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["as_of"] = self.as_of.isoformat()
        return data

    def red_signals(self) -> list[str]:
        """Conditions that should land in the Escalation Matrix as RED."""

        reasons: list[str] = []
        if self.trust.a3_blocked_actions > 0:
            reasons.append("A3 action attempted")
        if self.trust.incidents > 0:
            reasons.append("trust incident open")
        if self.delivery.blocked_deliveries > 0:
            reasons.append("paid delivery blocked")
        if self.product.ci_status.lower() == "broken":
            reasons.append("CI broken on main")
        return reasons

    def yellow_signals(self) -> list[str]:
        reasons: list[str] = []
        if self.trust.approvals_waiting > 0:
            reasons.append("proposals or approvals waiting")
        if self.delivery.qa_needed > 0:
            reasons.append("delivery QA pending")
        if self.sales.replies > 0 and self.sales.calls_booked == 0:
            reasons.append("replies without follow-up calls")
        return reasons
