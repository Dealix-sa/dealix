"""
Hermes Workflows — مجمَّع تعريفات الـ workflows.

كل workflow معرَّف كـ `WorkflowSpec` ثابت في ملف مستقل، ويُسجَّل في
الـ runtime عبر `register_all(runtime)`.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from ..execution.workflow_runtime import WorkflowSpec
from .ai_trust_kit_workflow import SPEC as AI_TRUST_KIT_SPEC
from .customer_value_report_workflow import SPEC as CUSTOMER_VALUE_REPORT_SPEC
from .market_radar_workflow import SPEC as MARKET_RADAR_SPEC
from .partner_pitch_workflow import SPEC as PARTNER_PITCH_SPEC
from .proposal_workflow import SPEC as PROPOSAL_SPEC
from .revenue_hunter_workflow import SPEC as REVENUE_HUNTER_SPEC
from .training_workshop_workflow import SPEC as TRAINING_WORKSHOP_SPEC
from .venture_test_workflow import SPEC as VENTURE_TEST_SPEC

if TYPE_CHECKING:
    from ..execution.workflow_runtime import WorkflowRuntime


ALL_SPECS: tuple[WorkflowSpec, ...] = (
    REVENUE_HUNTER_SPEC,
    PROPOSAL_SPEC,
    AI_TRUST_KIT_SPEC,
    PARTNER_PITCH_SPEC,
    MARKET_RADAR_SPEC,
    CUSTOMER_VALUE_REPORT_SPEC,
    TRAINING_WORKSHOP_SPEC,
    VENTURE_TEST_SPEC,
)


def register_all(runtime: WorkflowRuntime) -> None:
    """تسجيل كل الـ workflows دفعة واحدة."""
    for spec in ALL_SPECS:
        runtime.register_spec(spec)


__all__ = [
    "AI_TRUST_KIT_SPEC",
    "ALL_SPECS",
    "CUSTOMER_VALUE_REPORT_SPEC",
    "MARKET_RADAR_SPEC",
    "PARTNER_PITCH_SPEC",
    "PROPOSAL_SPEC",
    "REVENUE_HUNTER_SPEC",
    "TRAINING_WORKSHOP_SPEC",
    "VENTURE_TEST_SPEC",
    "register_all",
]
