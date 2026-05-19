"""Strategic Autonomy Layer — CEO/board-tier autonomous loop.

Sits ABOVE the Full Ops operational cycle. Aggregates company signals,
evaluates codified strategic decision gates, produces CEO-level
decisions, records them to a code-backed decision ledger, routes
irreversible decisions to the founder approval queue, and on approval
delegates execution to the Full Ops orchestrator.

Doctrine: "AI explores, analyzes, recommends. Deterministic workflows
execute. Humans approve critical moves." Irreversible decisions are
never auto-executed.
"""

from __future__ import annotations

from auto_client_acquisition.strategy_autonomy.board_report import (
    render_board_report_markdown,
)
from auto_client_acquisition.strategy_autonomy.decision_gates import (
    GateEvaluation,
    evaluate_strategic_gates,
)
from auto_client_acquisition.strategy_autonomy.decision_ledger import (
    StrategicDecision,
    clear_for_test,
    get_decision,
    latest_decisions,
    query_decisions,
    record_decision,
)
from auto_client_acquisition.strategy_autonomy.decision_types import (
    IRREVERSIBLE,
    StrategicDecisionType,
    from_compounding,
    is_irreversible,
)
from auto_client_acquisition.strategy_autonomy.gate_catalog import (
    STRATEGIC_GATE_CATALOG,
    GateRule,
    get_gate,
    list_gates,
)
from auto_client_acquisition.strategy_autonomy.signal_aggregator import (
    LAUNCH_DATE,
    StrategicSignalSnapshot,
    aggregate_strategic_signals,
)
from auto_client_acquisition.strategy_autonomy.strategic_cycle import (
    StrategicCycleReport,
    latest_strategic_report,
    run_strategic_cycle,
)
from auto_client_acquisition.strategy_autonomy.strategic_hierarchy import (
    OPERATIONAL_ORCHESTRATOR_ID,
    STRATEGIC_MAX_AUTONOMY_LEVEL,
    StrategicHierarchyNode,
    all_strategic_nodes,
    get_strategic_tier,
    seed_strategic_tier,
    strategic_tier_status,
)

__all__ = [
    "IRREVERSIBLE",
    "LAUNCH_DATE",
    "OPERATIONAL_ORCHESTRATOR_ID",
    "STRATEGIC_GATE_CATALOG",
    "STRATEGIC_MAX_AUTONOMY_LEVEL",
    "GateEvaluation",
    "GateRule",
    "StrategicCycleReport",
    "StrategicDecision",
    "StrategicDecisionType",
    "StrategicHierarchyNode",
    "StrategicSignalSnapshot",
    "aggregate_strategic_signals",
    "all_strategic_nodes",
    "clear_for_test",
    "evaluate_strategic_gates",
    "from_compounding",
    "get_decision",
    "get_gate",
    "get_strategic_tier",
    "is_irreversible",
    "latest_decisions",
    "latest_strategic_report",
    "list_gates",
    "query_decisions",
    "record_decision",
    "render_board_report_markdown",
    "run_strategic_cycle",
    "seed_strategic_tier",
    "strategic_tier_status",
]
