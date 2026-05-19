"""Executive OS — the autonomous top of the agent pyramid.

One orchestrator convenes the 7 role briefs every tick, synthesizes a
single executive brief, queues every external action for founder
approval, prepares internal jobs, and audits every decision. It queues
and prepares — it never sends and never charges.
"""

from auto_client_acquisition.executive_os.aggregator import (
    aggregator_degraded_roles,
    build_all_role_briefs,
)
from auto_client_acquisition.executive_os.brief_store import (
    clear_for_test as _clear_briefs,
)
from auto_client_acquisition.executive_os.brief_store import (
    load_latest_brief,
    save_brief,
)
from auto_client_acquisition.executive_os.identity import (
    EXECUTIVE_AGENT_ID,
    build_executive_agent_card,
    ensure_registered,
)
from auto_client_acquisition.executive_os.orchestrator import (
    run_executive_tick,
    spawn_internal_jobs,
)
from auto_client_acquisition.executive_os.schemas import (
    GUARDRAILS,
    ExecutiveBrief,
    ExecutiveTickResult,
    QueuedApproval,
    RankedDecision,
)


def clear_for_test() -> None:
    """Reset persisted briefs (test helper)."""
    _clear_briefs()


__all__ = [
    "EXECUTIVE_AGENT_ID",
    "GUARDRAILS",
    "ExecutiveBrief",
    "ExecutiveTickResult",
    "QueuedApproval",
    "RankedDecision",
    "aggregator_degraded_roles",
    "build_all_role_briefs",
    "build_executive_agent_card",
    "clear_for_test",
    "ensure_registered",
    "load_latest_brief",
    "run_executive_tick",
    "save_brief",
    "spawn_internal_jobs",
]
