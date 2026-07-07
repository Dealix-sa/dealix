"""
Integration Registry — honest catalogue of external tools the Autonomous OS
is *designed to* orchestrate, with truthful wiring status.

This is documentation-as-data, not a claim of live integration. Each entry
records what a tool would be used for and its current status:

  - "reference": we follow its patterns/ideas, nothing to wire.
  - "adapter_planned": a first-class adapter is intended; not built yet.
  - "wired": a real, offline-safe adapter exists in the repo under
    dealix/autonomous_os/adapters/ (Ollama, Twenty, WhatsApp draft, Firecrawl,
    Cal.com). Being "wired" never implies auto-send — all wired adapters are
    draft-only / read-only and still pass through the SafetyGate + ApprovalQueue.

Nothing here sends anything. Adapters, when built, must still pass through the
SafetyGate and ApprovalQueue. Local-first tools (Ollama, self-hosted) are
preferred per the safety doctrine.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Integration:
    name: str
    url: str
    category: str
    role: str
    status: str  # reference | adapter_planned | wired

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "url": self.url,
            "category": self.category,
            "role": self.role,
            "status": self.status,
        }


# Core stack to prioritise first (per the brief): local-first + orchestration.
CORE_STACK = (
    "ollama",
    "n8n",
    "dify",
    "crewai",
    "langgraph",
    "twenty",
    "firecrawl",
    "mem0",
    "evolution_api",
)


REGISTRY: tuple[Integration, ...] = (
    # Core agents & orchestration
    Integration(
        "n8n",
        "https://github.com/n8n-io/n8n",
        "orchestration",
        "self-hosted workflow automation for internal, approval-gated pipelines",
        "adapter_planned",
    ),
    Integration(
        "dify",
        "https://github.com/langgenius/dify",
        "orchestration",
        "LLM app/workflow builder for internal drafting flows",
        "adapter_planned",
    ),
    Integration(
        "ollama",
        "https://github.com/ollama/ollama",
        "models",
        "local-first inference; primary model provider "
        "(dealix/autonomous_os/adapters/ollama_adapter.py)",
        "wired",
    ),
    Integration(
        "open_webui",
        "https://github.com/open-webui/open-webui",
        "models",
        "local chat UI over Ollama for founder review",
        "reference",
    ),
    Integration(
        "crewai",
        "https://github.com/crewAIInc/crewAI",
        "agents",
        "multi-agent role patterns for planners/reviewers",
        "reference",
    ),
    Integration(
        "langflow",
        "https://github.com/langflow-ai/langflow",
        "orchestration",
        "visual flow prototyping for strategies",
        "reference",
    ),
    Integration(
        "autogpt",
        "https://github.com/Significant-Gravitas/AutoGPT",
        "agents",
        "autonomous task patterns (bounded, draft-only here)",
        "reference",
    ),
    Integration(
        "langchain",
        "https://github.com/langchain-ai/langchain",
        "agents",
        "LLM tooling primitives",
        "reference",
    ),
    Integration(
        "langgraph",
        "https://github.com/langchain-ai/langgraph",
        "agents",
        "stateful graph orchestration for the planner",
        "adapter_planned",
    ),
    Integration(
        "firecrawl",
        "https://github.com/firecrawl/firecrawl",
        "research",
        "compliant public web/market research, contact/social scraping refused "
        "(dealix/autonomous_os/adapters/firecrawl_adapter.py)",
        "wired",
    ),
    Integration(
        "mem0",
        "https://github.com/mem0ai/mem0",
        "memory",
        "long-term memory for strategy/learning context",
        "adapter_planned",
    ),
    Integration(
        "ragflow",
        "https://github.com/infiniflow/ragflow",
        "rag",
        "document RAG over company knowledge",
        "reference",
    ),
    Integration(
        "haystack", "https://github.com/deepset-ai/haystack", "rag", "RAG pipelines", "reference"
    ),
    Integration(
        "llamaindex",
        "https://github.com/run-llama/llama_index",
        "rag",
        "indexing/retrieval over company docs",
        "reference",
    ),
    Integration(
        "browser_use",
        "https://github.com/browser-use/browser-use",
        "research",
        "guarded browser automation for research only",
        "reference",
    ),
    # Sales, CRM, WhatsApp & growth
    Integration(
        "twenty",
        "https://github.com/twentyhq/twenty",
        "crm",
        "self-hosted CRM as the pipeline system of record, read-only "
        "(dealix/autonomous_os/adapters/twenty_adapter.py)",
        "wired",
    ),
    Integration(
        "salesgpt",
        "https://github.com/filip-michalsky/SalesGPT",
        "sales",
        "sales conversation patterns (draft-only)",
        "reference",
    ),
    Integration(
        "calcom",
        "https://github.com/calcom/cal.com",
        "scheduling",
        "self-hosted booking-link prep for diagnostics/sprints, read-only "
        "(dealix/autonomous_os/adapters/calcom_adapter.py)",
        "wired",
    ),
    Integration(
        "evolution_api",
        "https://github.com/evolution-foundation/evolution-api",
        "messaging",
        "WhatsApp API — DRAFT PREP ONLY, no send capability "
        "(dealix/autonomous_os/adapters/whatsapp_draft_adapter.py)",
        "wired",
    ),
    Integration(
        "moneyprinterturbo",
        "https://github.com/harry0703/MoneyPrinterTurbo",
        "content",
        "short-form video draft generation",
        "reference",
    ),
    Integration(
        "openmontage",
        "https://github.com/calesthio/OpenMontage",
        "content",
        "video montage drafting",
        "reference",
    ),
    Integration(
        "markitdown",
        "https://github.com/microsoft/markitdown",
        "content",
        "document-to-markdown for proof packs",
        "adapter_planned",
    ),
    Integration(
        "appwrite",
        "https://github.com/appwrite/appwrite",
        "platform",
        "self-hosted backend services",
        "reference",
    ),
    Integration(
        "metabase",
        "https://github.com/metabase/metabase",
        "analytics",
        "commercial dashboards over the OS outputs",
        "adapter_planned",
    ),
    Integration(
        "aider",
        "https://github.com/Aider-AI/aider",
        "engineering",
        "AI pair-programming for internal tooling",
        "reference",
    ),
    Integration(
        "tabby",
        "https://github.com/TabbyML/tabby",
        "engineering",
        "self-hosted code assistant",
        "reference",
    ),
    Integration(
        "codebase_memory_mcp",
        "https://github.com/DeusData/codebase-memory-mcp",
        "memory",
        "codebase memory via MCP",
        "reference",
    ),
    Integration(
        "last30days_skill",
        "https://github.com/mvanhorn/last30days-skill",
        "skills",
        "recency-aware research skill",
        "reference",
    ),
    Integration(
        "agent_reach",
        "https://github.com/Panniantong/Agent-Reach",
        "growth",
        "outreach patterns (draft-only, opt-in only)",
        "reference",
    ),
    Integration(
        "openclaw",
        "https://github.com/openclaw/openclaw",
        "agents",
        "agent framework component",
        "reference",
    ),
    # Advanced, compliance, skills & extras
    Integration(
        "awesome_claude_skills",
        "https://github.com/ComposioHQ/awesome-claude-skills",
        "skills",
        "skill library for the growth engine",
        "reference",
    ),
    Integration(
        "autogen",
        "https://github.com/microsoft/autogen",
        "agents",
        "multi-agent conversation framework",
        "reference",
    ),
    Integration(
        "superagi",
        "https://github.com/TransformerOptimus/SuperAGI",
        "agents",
        "autonomous agent infra patterns",
        "reference",
    ),
    Integration(
        "anythingllm",
        "https://github.com/Mintplex-Labs/anything-llm",
        "rag",
        "self-hosted private RAG workspace",
        "reference",
    ),
    Integration(
        "privategpt",
        "https://github.com/zylon-ai/private-gpt",
        "rag",
        "fully local RAG for private data",
        "reference",
    ),
    Integration(
        "vaultwarden",
        "https://github.com/bitwarden/server",
        "security",
        "self-hosted secrets vault (never in repo)",
        "reference",
    ),
    Integration(
        "developer_roadmap",
        "https://github.com/kamranahmedse/developer-roadmap",
        "knowledge",
        "capability roadmap reference",
        "reference",
    ),
    Integration(
        "system_design_101",
        "https://github.com/ByteByteGoHq/system-design-101",
        "knowledge",
        "architecture reference",
        "reference",
    ),
    Integration(
        "hermes_agent",
        "https://github.com/NousResearch/hermes-agent",
        "agents",
        "agent patterns (aligns with in-repo Hermes)",
        "reference",
    ),
    Integration(
        "pi_mono",
        "https://github.com/earendil-works/pi",
        "agents",
        "agent runtime component",
        "reference",
    ),
)


def core_stack() -> list[Integration]:
    index = {i.name: i for i in REGISTRY}
    return [index[name] for name in CORE_STACK if name in index]


def by_status(status: str) -> list[Integration]:
    return [i for i in REGISTRY if i.status == status]


def summary() -> dict[str, Any]:
    counts: dict[str, int] = {}
    for i in REGISTRY:
        counts[i.status] = counts.get(i.status, 0) + 1
    return {
        "total": len(REGISTRY),
        "by_status": counts,
        "core_stack": list(CORE_STACK),
        "note": (
            "Catalogue only. No tool here auto-sends. Adapters, when built, must "
            "pass the SafetyGate and ApprovalQueue. Custom items 41-50 (WhatsApp+"
            "LangGraph agents, Ragas/Phoenix eval, approval-workflow libs, growth "
            "skills, audit/compliance tooling) are tracked in the OS roadmap doc."
        ),
    }
