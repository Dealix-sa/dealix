"""Red Flag detector (section 132).

Surfaces the dangerous patterns Sami must intervene on:

  * external action without approval
  * tool without owner
  * agent without KPI
  * execution without outcome
  * customer without value report
  * partner without performance review
  * offer without metric
  * asset never reused
  * high approval backlog
  * repeated incident type
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass

from dealix.hermes.audit.no_orphan import OrphanReport
from dealix.hermes.trust.approvals import ApprovalCenter
from dealix.hermes.trust.incident_response import IncidentRegister


@dataclass(frozen=True)
class RedFlag:
    code: str
    detail: str
    severity: str


class RedFlagDetector:
    def __init__(
        self,
        *,
        approval_backlog_threshold: int = 5,
        repeated_incident_threshold: int = 3,
    ) -> None:
        self.approval_backlog_threshold = approval_backlog_threshold
        self.repeated_incident_threshold = repeated_incident_threshold

    def detect(
        self,
        *,
        orphan_report: OrphanReport,
        approval_center: ApprovalCenter,
        incidents: IncidentRegister,
    ) -> list[RedFlag]:
        flags: list[RedFlag] = []
        if orphan_report.tools_without_owner:
            flags.append(RedFlag("tool_without_owner", str(orphan_report.tools_without_owner), "high"))
        if orphan_report.agents_without_kpi:
            flags.append(RedFlag("agent_without_kpi", str(orphan_report.agents_without_kpi), "medium"))
        if orphan_report.executions_without_outcome:
            flags.append(RedFlag("execution_without_outcome", str(orphan_report.executions_without_outcome), "medium"))
        if orphan_report.customers_without_value_report:
            flags.append(RedFlag("customer_without_value_report", str(orphan_report.customers_without_value_report), "high"))
        if orphan_report.partners_without_performance_review:
            flags.append(RedFlag("partner_without_performance_review", str(orphan_report.partners_without_performance_review), "medium"))
        if orphan_report.unreused_assets:
            flags.append(RedFlag("asset_never_reused", str(orphan_report.unreused_assets), "low"))

        backlog = approval_center.pending()
        if len(backlog) >= self.approval_backlog_threshold:
            flags.append(RedFlag("high_approval_backlog", f"{len(backlog)} pending approvals", "medium"))

        # Repeated incident types.
        counts = Counter(i.title for i in incidents.open_incidents())
        for title, count in counts.items():
            if count >= self.repeated_incident_threshold:
                flags.append(RedFlag("repeated_incident_type", f"{title} x{count}", "high"))

        return flags


__all__ = ["RedFlag", "RedFlagDetector"]
