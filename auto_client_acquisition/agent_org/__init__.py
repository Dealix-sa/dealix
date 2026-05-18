"""Dealix Agent Organization — governed autonomous agent hierarchy.

A pyramid of 25 agent roles (1 Chief of Staff, 6 Directors, 18 Operators)
that runs a daily executive cycle. Governed autonomy: the cycle does the
work automatically; every external output is draft-only and approval-gated.

منظمة وكلاء ديلكس — هرم محكوم من الوكلاء يدير دورة تنفيذية يومية.
"""

from __future__ import annotations

from auto_client_acquisition.agent_org.orchestrator import (
    DailyOrgReport,
    WorkItem,
    run_daily_cycle,
)
from auto_client_acquisition.agent_org.org_chart import (
    AgentRole,
    all_roles,
    chief,
    directors,
    get_role,
    operators,
    org_chart_dict,
    validate_org,
)

__all__ = [
    "AgentRole",
    "DailyOrgReport",
    "WorkItem",
    "all_roles",
    "chief",
    "directors",
    "get_role",
    "operators",
    "org_chart_dict",
    "run_daily_cycle",
    "validate_org",
]
