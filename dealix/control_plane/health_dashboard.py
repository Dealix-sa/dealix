"""
Section 77 — System Health Dashboard.

Tracks the throughput numbers the system must keep an eye on, and a list
of *red flags* (executions without outcomes, external actions without
approval, tools without owners, customers without value reports, etc.).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any


class RedFlag(StrEnum):
    EXECUTIONS_WITHOUT_OUTCOMES = "executions_without_outcomes"
    EXTERNAL_ACTIONS_WITHOUT_APPROVAL = "external_actions_without_approval"
    TOOLS_WITHOUT_OWNER = "tools_without_owner"
    AGENTS_WITHOUT_KPIS = "agents_without_kpis"
    ASSETS_NOT_REUSED = "assets_not_reused"
    CUSTOMERS_WITHOUT_VALUE_REPORTS = "customers_without_value_reports"
    PARTNERS_WITHOUT_REVENUE = "partners_without_revenue"


@dataclass
class HealthMetrics:
    signals_captured: int = 0
    opportunities_created: int = 0
    executions_completed: int = 0
    outcomes_logged: int = 0
    assets_created: int = 0
    approvals_pending: int = 0
    risks_blocked: int = 0
    agent_runs: int = 0
    tool_calls: int = 0
    cost_sar: float = 0.0
    latency_ms_p95: float = 0.0
    revenue_influenced_sar: float = 0.0

    def to_dict(self) -> dict[str, Any]:
        return {
            "signals_captured": self.signals_captured,
            "opportunities_created": self.opportunities_created,
            "executions_completed": self.executions_completed,
            "outcomes_logged": self.outcomes_logged,
            "assets_created": self.assets_created,
            "approvals_pending": self.approvals_pending,
            "risks_blocked": self.risks_blocked,
            "agent_runs": self.agent_runs,
            "tool_calls": self.tool_calls,
            "cost_sar": self.cost_sar,
            "latency_ms_p95": self.latency_ms_p95,
            "revenue_influenced_sar": self.revenue_influenced_sar,
        }


@dataclass
class HealthDashboard:
    metrics: HealthMetrics = field(default_factory=HealthMetrics)
    red_flags: list[RedFlag] = field(default_factory=list)

    def raise_flag(self, flag: RedFlag) -> None:
        if flag not in self.red_flags:
            self.red_flags.append(flag)

    def clear_flag(self, flag: RedFlag) -> None:
        if flag in self.red_flags:
            self.red_flags.remove(flag)

    def increment(self, field: str, *, by: float | int = 1) -> None:
        if not hasattr(self.metrics, field):
            raise ValueError(f"unknown metric field: {field}")
        setattr(self.metrics, field, getattr(self.metrics, field) + by)

    def to_dict(self) -> dict[str, Any]:
        return {
            "metrics": self.metrics.to_dict(),
            "red_flags": [f.value for f in self.red_flags],
        }
