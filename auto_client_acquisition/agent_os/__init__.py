"""Agent OS — identity, lifecycle, mesh execution for the governed Dealix AI Stack.

This package exposes three concentric layers:

1. **Identity** — :class:`AgentCard`, registry, lifecycle, autonomy levels,
   tool permissions. The unit of *who is allowed to act*.
2. **Execution** — :func:`run_agent`, the agent runner that wraps every
   handler invocation with input hashing, output summarization, error
   capture, and lifecycle gating.
3. **Orchestration** — :class:`AgentMesh` and the task router. Convert an
   AI Stack input into an ordered :class:`TaskPlan`, dispatch through the
   mesh, and produce a stable :class:`MeshTrace` the rest of the stack
   consumes.
"""

from auto_client_acquisition.agent_os.agent_card import (
    AgentCard,
    AgentStatus,
    agent_card_valid,
    new_card,
)
from auto_client_acquisition.agent_os.agent_lifecycle import (
    AgentLifecycleState,
    lifecycle_allows_production_tools,
)
from auto_client_acquisition.agent_os.agent_mesh import AgentMesh, MeshTrace
from auto_client_acquisition.agent_os.agent_registry import (
    clear_agent_registry_for_tests,
    clear_for_test,
    get_agent,
    kill_agent,
    list_agents,
    register_agent,
)
from auto_client_acquisition.agent_os.agent_runner import (
    AgentHandler,
    AgentRun,
    run_agent,
)
from auto_client_acquisition.agent_os.autonomy_levels import (
    MAX_AUTONOMY_LEVEL_MVP,
    AutonomyLevel,
)
from auto_client_acquisition.agent_os.task_router import (
    AGENT_ICP,
    AGENT_OUTREACH_DRAFT,
    AGENT_PAIN,
    AGENT_PROPOSAL,
    AGENT_QUALIFICATION,
    AGENT_RETAINER_RECOMMEND,
    AGENT_SECTOR_INTEL,
    AgentTask,
    TaskPlan,
    agents_required_for_tier,
    plan_for_offer,
    supported_offer_tiers,
)
from auto_client_acquisition.agent_os.tool_permissions import (
    ALLOWED_TOOLS_MVP,
    FORBIDDEN_TOOLS_MVP,
    is_tool_allowed,
    tool_allowed_mvp,
)

__all__ = [
    "AGENT_ICP",
    "AGENT_OUTREACH_DRAFT",
    "AGENT_PAIN",
    "AGENT_PROPOSAL",
    "AGENT_QUALIFICATION",
    "AGENT_RETAINER_RECOMMEND",
    "AGENT_SECTOR_INTEL",
    "ALLOWED_TOOLS_MVP",
    "FORBIDDEN_TOOLS_MVP",
    "MAX_AUTONOMY_LEVEL_MVP",
    "AgentCard",
    "AgentHandler",
    "AgentLifecycleState",
    "AgentMesh",
    "AgentRun",
    "AgentStatus",
    "AgentTask",
    "AutonomyLevel",
    "MeshTrace",
    "TaskPlan",
    "agent_card_valid",
    "agents_required_for_tier",
    "clear_agent_registry_for_tests",
    "clear_for_test",
    "get_agent",
    "is_tool_allowed",
    "kill_agent",
    "list_agents",
    "lifecycle_allows_production_tools",
    "new_card",
    "plan_for_offer",
    "register_agent",
    "run_agent",
    "supported_offer_tiers",
    "tool_allowed_mvp",
]
