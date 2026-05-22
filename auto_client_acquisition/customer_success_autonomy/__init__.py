"""Customer Success Autonomy Layer — daily per-customer retention cycle.

Runs in parallel to the operational Full Ops lead-acquisition cycle and
under the Strategic Autonomy Layer. For every active customer it:
  - aggregates 5 scores + value + proof signals,
  - detects opportunities (renewal, expansion, churn, detractor, friction),
  - drafts bilingual messages (approval-gated, never auto-sent),
  - creates ApprovalRequests + emits WorkItems,
  - produces a bilingual CycleReport.

Doctrine: AI explores, recommends. Humans approve every external action.
"""
from __future__ import annotations

from auto_client_acquisition.customer_success_autonomy.cs_cycle import (
    CustomerSuccessCycleReport,
    latest_cs_report,
    run_customer_success_cycle,
)
from auto_client_acquisition.customer_success_autonomy.opportunity_detector import (
    Opportunity,
    detect_opportunities,
)
from auto_client_acquisition.customer_success_autonomy.signal_aggregator import (
    CustomerSignalSnapshot,
    aggregate_customer_signals,
)

__all__ = [
    "CustomerSignalSnapshot",
    "CustomerSuccessCycleReport",
    "Opportunity",
    "aggregate_customer_signals",
    "detect_opportunities",
    "latest_cs_report",
    "run_customer_success_cycle",
]
