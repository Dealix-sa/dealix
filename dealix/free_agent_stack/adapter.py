"""Approval-first free agent adapter for Dealix.

The source inspiration is the public `build-ai-agents-free` pattern:
model + tools + memory + a plan/act/observe loop. This module does not import
LangChain or Groq directly because Dealix must keep production stable and avoid
adding mandatory runtime dependencies for an optional free-tier path.

Instead, it provides a typed manifest that existing Dealix runners can use to
wire tools safely through the current model router, approval center, and proof
ledger.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

AutonomyLevel = Literal["L0", "L1", "L2", "L3", "L4", "L5"]
RiskLevel = Literal["low", "medium", "high", "blocked"]


@dataclass(frozen=True, slots=True)
class AgentLoopStep:
    """One explicit plan -> act -> observe step.

    Keeping the loop materialized makes Dealix auditable: the system can show
    why a tool was selected, what it observed, and whether the next action must
    be routed to founder/client approval.
    """

    phase: Literal["plan", "act", "observe"]
    instruction: str
    tool_name: str | None = None
    risk_level: RiskLevel = "low"
    autonomy_level: AutonomyLevel = "L2"
    approval_required: bool = False


@dataclass(frozen=True, slots=True)
class ToolManifestEntry:
    """A Dealix-safe tool description for LLM/tool routing."""

    name: str
    purpose: str
    allowed_autonomy_level: AutonomyLevel
    risk_level: RiskLevel
    approval_required: bool
    allowed_outputs: tuple[str, ...]
    blocked_actions: tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True, slots=True)
class DealixFreeAgentProfile:
    """Configuration profile for a free-tier-aware Dealix agent."""

    name: str
    objective: str
    preferred_model_order: tuple[str, ...]
    memory_scope: Literal["thread", "client_workspace", "founder_only"]
    default_mode: Literal["draft-only"] = "draft-only"
    cloud_prompt_safety: tuple[str, ...] = field(default_factory=tuple)
    hard_blocks: tuple[str, ...] = field(default_factory=tuple)
    tools: tuple[ToolManifestEntry, ...] = field(default_factory=tuple)


def build_approval_first_tool_manifest() -> tuple[ToolManifestEntry, ...]:
    """Return the default safe tool manifest for Dealix free-agent loops."""

    return (
        ToolManifestEntry(
            name="company_brain_lookup",
            purpose="Read Dealix/client positioning, offers, personas, restrictions, and tone.",
            allowed_autonomy_level="L1",
            risk_level="low",
            approval_required=False,
            allowed_outputs=("summary", "constraints", "offer_match"),
        ),
        ToolManifestEntry(
            name="opportunity_score_preview",
            purpose="Score candidate companies from provided/allowed sources and explain why.",
            allowed_autonomy_level="L2",
            risk_level="medium",
            approval_required=False,
            allowed_outputs=("score", "reason", "risk", "next_action"),
            blocked_actions=("scrape_prohibited_sources", "invent_contacts", "infer_consent"),
        ),
        ToolManifestEntry(
            name="outreach_draft_builder",
            purpose="Create email/LinkedIn/WhatsApp manual scripts as drafts only.",
            allowed_autonomy_level="L2",
            risk_level="medium",
            approval_required=True,
            allowed_outputs=("draft_message", "subject", "cta", "approval_note"),
            blocked_actions=("send_email", "send_whatsapp", "mass_linkedin", "auto_post"),
        ),
        ToolManifestEntry(
            name="approval_queue_writer",
            purpose="Write reviewable action items to the approval queue.",
            allowed_autonomy_level="L3",
            risk_level="medium",
            approval_required=False,
            allowed_outputs=("approval_item", "risk", "decision_options"),
            blocked_actions=("execute_external_action",),
        ),
        ToolManifestEntry(
            name="proof_log_writer",
            purpose="Record evidence of internal actions and approved outcomes without fake proof.",
            allowed_autonomy_level="L3",
            risk_level="low",
            approval_required=False,
            allowed_outputs=("proof_event", "evidence", "source", "timestamp"),
            blocked_actions=("fake_roi", "fake_client", "guaranteed_claim"),
        ),
        ToolManifestEntry(
            name="free_web_research_draft",
            purpose="Use free/public search only for non-sensitive research drafts; source uncertainty must be shown.",
            allowed_autonomy_level="L2",
            risk_level="medium",
            approval_required=False,
            allowed_outputs=("source_notes", "caveats", "research_summary"),
            blocked_actions=("send_sensitive_data_to_free_tier", "scrape_prohibited_sources"),
        ),
    )


def build_dealix_free_agent_profile() -> DealixFreeAgentProfile:
    """Build the default Dealix profile for applying free-agent patterns."""

    return DealixFreeAgentProfile(
        name="dealix_free_agent_stack_adapter",
        objective=(
            "Use free/local-first agent patterns to produce opportunity research, "
            "scoring, drafts, approval queues, proof logs, and learning notes for Dealix."
        ),
        preferred_model_order=(
            "existing_dealix_local_router",
            "ollama_or_vllm_private_endpoint",
            "groq_free_tier_for_public_non_sensitive_tasks",
            "gemini_free_tier_for_public_non_sensitive_long_context_tasks",
            "human_handoff",
        ),
        memory_scope="client_workspace",
        cloud_prompt_safety=(
            "Do not send founder-only or customer-internal sensitive data to free tiers.",
            "Assume free tiers can change or be rate-limited.",
            "Prefer local/private endpoints for client data.",
            "Show caveats and route low-confidence output to approval.",
        ),
        hard_blocks=(
            "live_outbound",
            "cold_whatsapp_blast",
            "mass_linkedin_automation",
            "auto_posting",
            "payment_capture",
            "production_mutation",
            "public_llm_endpoint",
            "hardcoded_secret",
            "fake_proof",
            "guaranteed_revenue_claim",
            "government_access_claim",
        ),
        tools=build_approval_first_tool_manifest(),
    )


def run_plan_act_observe_preview(task: str) -> tuple[AgentLoopStep, ...]:
    """Generate an auditable preview loop for a Dealix task.

    This is a deterministic preview, not an LLM call. Runners can include it in
    reports before wiring actual model/tool execution.
    """

    task_text = task.strip() or "Build today's Dealix daily opportunity command."
    return (
        AgentLoopStep(
            phase="plan",
            instruction=f"Clarify the safest internal next step for: {task_text}",
            autonomy_level="L1",
        ),
        AgentLoopStep(
            phase="act",
            tool_name="company_brain_lookup",
            instruction="Load Dealix offers, personas, restrictions, and proof requirements.",
            autonomy_level="L1",
        ),
        AgentLoopStep(
            phase="act",
            tool_name="opportunity_score_preview",
            instruction="Rank only allowed/provided opportunities and explain reasons and risks.",
            risk_level="medium",
            autonomy_level="L2",
        ),
        AgentLoopStep(
            phase="act",
            tool_name="outreach_draft_builder",
            instruction="Prepare draft-only messages and negotiation notes for approval.",
            risk_level="medium",
            autonomy_level="L2",
            approval_required=True,
        ),
        AgentLoopStep(
            phase="observe",
            tool_name="approval_queue_writer",
            instruction="Write risky external actions to the approval queue instead of executing them.",
            risk_level="medium",
            autonomy_level="L3",
        ),
        AgentLoopStep(
            phase="observe",
            tool_name="proof_log_writer",
            instruction="Record internal evidence and caveats; never create fake proof.",
            autonomy_level="L3",
        ),
    )
