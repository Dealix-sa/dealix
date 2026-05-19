"""Full Ops Sales System — autonomous sell-deliver-expand orchestration.

Wires the existing sales / revenue / delivery modules into the 12-stage
golden chain. Internal-safe (A0) actions auto-execute; every external action
is routed to ``approval_center``. See ``docs/full_ops_sales_os/``.
"""

from __future__ import annotations

from auto_client_acquisition.full_ops_os.gate import (
    GateDecision,
    auto_exec_allowed,
    evaluate_gate,
)
from auto_client_acquisition.full_ops_os.orchestrator import (
    WORKFLOW_ID,
    FullOpsOrchestrator,
    StageResult,
)
from auto_client_acquisition.full_ops_os.stages import (
    STAGES,
    Stage,
    StageSpec,
    stage_spec,
)

__all__ = [
    "FullOpsOrchestrator",
    "StageResult",
    "WORKFLOW_ID",
    "GateDecision",
    "evaluate_gate",
    "auto_exec_allowed",
    "Stage",
    "StageSpec",
    "STAGES",
    "stage_spec",
]
