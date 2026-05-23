"""CompanyState: the single operational truth across Dealix systems."""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from datetime import date
from typing import Dict, List, Optional


@dataclass
class RevenueState:
    cash_collected: float = 0.0
    cash_expected: float = 0.0
    mrr: float = 0.0
    proposals_pending: int = 0
    pipeline_value: float = 0.0
    best_next_close: Optional[str] = None


@dataclass
class SalesState:
    leads_new: int = 0
    dms_due: int = 0
    followups_due: int = 0
    replies: int = 0
    calls_booked: int = 0


@dataclass
class DeliveryState:
    active_clients: int = 0
    reports_due: int = 0
    blocked_deliveries: int = 0
    qa_needed: int = 0


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
    customer_requested_features: int = 0
    release_candidate: Optional[str] = None


@dataclass
class FinanceState:
    runway_months: Optional[float] = None
    refunds_open: int = 0
    invoices_overdue: int = 0


@dataclass
class ClientSuccessState:
    health_below_60: int = 0
    retainer_ready: int = 0
    feedback_collected: int = 0


@dataclass
class CompanyState:
    as_of: str = field(default_factory=lambda: date.today().isoformat())
    revenue: RevenueState = field(default_factory=RevenueState)
    sales: SalesState = field(default_factory=SalesState)
    delivery: DeliveryState = field(default_factory=DeliveryState)
    trust: TrustState = field(default_factory=TrustState)
    product: ProductState = field(default_factory=ProductState)
    finance: FinanceState = field(default_factory=FinanceState)
    client_success: ClientSuccessState = field(default_factory=ClientSuccessState)
    decisions_required: List[Dict] = field(default_factory=list)
    alerts: List[Dict] = field(default_factory=list)

    def to_dict(self) -> Dict:
        return asdict(self)
