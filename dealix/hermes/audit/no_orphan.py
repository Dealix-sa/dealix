"""No-Orphan auditor (section 129).

Forbidden states:

  * Signal stuck in NEW/CLASSIFIED past the cutoff.
  * Opportunity with no score.
  * Execution that completed with no outcome.
  * Tool with no owner.
  * Agent with no KPI.
  * Customer with no value report.
  * Partner with no performance review.

Returns a structured report; callers decide whether to fail loud.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import timedelta

from dealix.hermes.core.assets import AssetRegistry
from dealix.hermes.core.executions import ExecutionPlanner
from dealix.hermes.core.opportunities import OpportunityBook
from dealix.hermes.core.outcomes import OutcomeLedger
from dealix.hermes.core.signals import SignalInbox
from dealix.hermes.trust.agent_registry import AgentRegistry
from dealix.hermes.trust.tool_registry import ToolRegistry


@dataclass
class OrphanReport:
    orphan_signals: list[str] = field(default_factory=list)
    unscored_opportunities: list[str] = field(default_factory=list)
    executions_without_outcome: list[str] = field(default_factory=list)
    tools_without_owner: list[str] = field(default_factory=list)
    agents_without_kpi: list[str] = field(default_factory=list)
    customers_without_value_report: list[str] = field(default_factory=list)
    partners_without_performance_review: list[str] = field(default_factory=list)
    unreused_assets: list[str] = field(default_factory=list)

    @property
    def clean(self) -> bool:
        return not any(
            (
                self.orphan_signals,
                self.unscored_opportunities,
                self.executions_without_outcome,
                self.tools_without_owner,
                self.agents_without_kpi,
                self.customers_without_value_report,
                self.partners_without_performance_review,
            )
        )


@dataclass
class NoOrphanAudit:
    signals: SignalInbox
    opportunities: OpportunityBook
    executions: ExecutionPlanner
    outcomes: OutcomeLedger
    tools: ToolRegistry
    agents: AgentRegistry
    assets: AssetRegistry
    signal_age_cutoff: timedelta = timedelta(hours=24)

    def run(
        self,
        *,
        active_customers: list[str] | None = None,
        customer_value_reports: dict[str, bool] | None = None,
        active_partners: list[str] | None = None,
        partner_reviews: dict[str, bool] | None = None,
    ) -> OrphanReport:
        report = OrphanReport()
        report.orphan_signals = [s.id for s in self.signals.orphans(older_than=self.signal_age_cutoff)]
        report.unscored_opportunities = [o.id for o in self.opportunities.unscored()]
        report.executions_without_outcome = [
            e.id for e in self.outcomes.orphan_executions(self.executions.all())
        ]
        report.tools_without_owner = [t.tool_id for t in self.tools.all() if not t.owner]
        report.agents_without_kpi = [a.agent_id for a in self.agents.all() if not a.kpis]
        report.unreused_assets = [a.id for a in self.assets.unreused()]

        for c in (active_customers or []):
            if not (customer_value_reports or {}).get(c, False):
                report.customers_without_value_report.append(c)
        for p in (active_partners or []):
            if not (partner_reviews or {}).get(p, False):
                report.partners_without_performance_review.append(p)

        return report


__all__ = ["NoOrphanAudit", "OrphanReport"]
