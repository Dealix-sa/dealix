"""Free-agent-stack adapter for Dealix.

This package translates the public `Moh4696/build-ai-agents-free` pattern into
Dealix-safe primitives:

- plan -> act -> observe loops
- explicit tool manifests
- thread/memory labels
- local-first / free-tier-aware model policy
- approval-first safety gates

It intentionally does not enable live outbound, auto-posting, payments, production
mutation, or public LLM endpoints.
"""

from dealix.free_agent_stack.adapter import (
    AgentLoopStep,
    DealixFreeAgentProfile,
    build_approval_first_tool_manifest,
    build_dealix_free_agent_profile,
    run_plan_act_observe_preview,
)

__all__ = [
    "AgentLoopStep",
    "DealixFreeAgentProfile",
    "build_approval_first_tool_manifest",
    "build_dealix_free_agent_profile",
    "run_plan_act_observe_preview",
]
