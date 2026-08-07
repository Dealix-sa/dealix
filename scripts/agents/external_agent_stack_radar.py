#!/usr/bin/env python3
"""Dealix external agent stack radar.

This dependency-free script records which external AI-agent repositories and
framework patterns Dealix should learn from, adopt, defer, or avoid.

It does not install dependencies, call external APIs, clone repositories, enable
MCP, or enable outbound actions. It only writes reviewable reports.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path

DEFAULT_OUTPUT_DIR = Path("reports/agents")


@dataclass(frozen=True)
class ExternalRepoSignal:
    name: str
    url: str
    category: str
    value_for_dealix: str
    adopt_now: str
    defer: str
    risk: str
    decision: str
    dealix_surface: str


REPO_SIGNALS: tuple[ExternalRepoSignal, ...] = (
    ExternalRepoSignal(
        name="LangGraph",
        url="https://github.com/langchain-ai/langgraph",
        category="long_running_stateful_workflows",
        value_for_dealix="Durable loops, human-in-the-loop checkpoints, stateful workflows, and production-grade orchestration patterns for Revenue, Brain, Delivery, Trust, and Market Watch loops.",
        adopt_now="Adopt the architecture pattern: explicit loop state, checkpoints, resumability, reports, and verifier gates.",
        defer="Do not add the runtime dependency until Dealix has one production loop that needs resumable graph execution.",
        risk="Dependency creep and complex debugging if imported before the internal loop contract is stable.",
        decision="pattern_now_runtime_later",
        dealix_surface="Loop Operating System / Company Brain / Revenue Command Room",
    ),
    ExternalRepoSignal(
        name="OpenAI Agents SDK",
        url="https://github.com/openai/openai-agents-python",
        category="multi_agent_harness",
        value_for_dealix="Provider-agnostic multi-agent workflow concepts, tool guardrails, handoffs, tracing, and sandbox-oriented agent execution.",
        adopt_now="Adopt the handoff/guardrail vocabulary and sandbox-run design for coding and research agents.",
        defer="Do not force Dealix runtime to depend on the SDK until agent execution needs a formal Python harness.",
        risk="Provider coupling if treated as the only agent runtime instead of one adapter among many.",
        decision="adapter_ready_pattern_now",
        dealix_surface="Agent Workbench / Founder Engineer / Research Agent",
    ),
    ExternalRepoSignal(
        name="Model Context Protocol",
        url="https://github.com/modelcontextprotocol",
        category="tool_and_data_connector_standard",
        value_for_dealix="Standard interface for connecting agents to data sources, tools, and external systems across SDKs and server registries.",
        adopt_now="Define a Dealix MCP Gateway policy: approved tools only, signed manifests, tool-call logging, network boundaries, and human approval before external actions.",
        defer="Do not expose production Postgres, email, WhatsApp, or shell tools through MCP before the gateway and audit policy exist.",
        risk="Tool poisoning, prompt injection, over-permissive tools, and localhost/control-plane attacks if connected directly.",
        decision="gateway_first_no_direct_mcp",
        dealix_surface="Data Connectors / Trust OS / Agent Safety Runtime",
    ),
    ExternalRepoSignal(
        name="NVIDIA NeMo Agent Toolkit",
        url="https://github.com/NVIDIA/NeMo-Agent-Toolkit",
        category="enterprise_agent_teams_evaluation_telemetry",
        value_for_dealix="Enterprise reference for connecting, optimizing, evaluating, and instrumenting teams of AI agents across frameworks.",
        adopt_now="Use as an enterprise architecture reference for evaluation, telemetry, framework neutrality, and multi-agent runtime discipline.",
        defer="Do not import until Dealix needs heavier enterprise-scale agent optimization.",
        risk="Overengineering if adopted before Dealix has stable revenue/delivery loops.",
        decision="reference_architecture_now_runtime_later",
        dealix_surface="Enterprise Agent Stack / Observability / Evaluation",
    ),
    ExternalRepoSignal(
        name="CrewAI",
        url="https://github.com/crewAIInc/crewAI",
        category="role_based_agent_collaboration",
        value_for_dealix="Clear role/task/crew patterns and controlled flows for collaborative agents.",
        adopt_now="Use the role/task/flow mental model for Dealix agent skills: Research, Scoring, Draft, Trust Review, Proposal, Delivery, Proof.",
        defer="Avoid direct runtime import until Dealix needs autonomous agent teams beyond deterministic scripts.",
        risk="Autonomy without enough gates can create noisy outputs and hidden costs.",
        decision="pattern_now_runtime_later",
        dealix_surface="Agent Skills / Revenue Team / Delivery Team",
    ),
    ExternalRepoSignal(
        name="Microsoft AutoGen / Agent Framework lineage",
        url="https://github.com/microsoft/autogen",
        category="multi_agent_conversation_and_human_in_loop",
        value_for_dealix="Multi-agent conversation patterns, human checkpoints, direct agent-to-agent collaboration, and workflow debugging ideas.",
        adopt_now="Adopt the idea of specialized agents with explicit roles and review checkpoints.",
        defer="Do not expose browser/local control planes or shell-like tools without isolation/authentication.",
        risk="Recent agent security lessons show localhost/control-plane boundaries must be authenticated, authorized, and isolated.",
        decision="security_lessons_and_patterns_only",
        dealix_surface="Agent Workbench / CI Fix Agents / PR Agents",
    ),
    ExternalRepoSignal(
        name="PydanticAI",
        url="https://github.com/pydantic/pydantic-ai",
        category="typed_agent_outputs",
        value_for_dealix="Typed outputs, structured validation, and Python-friendly agent contracts.",
        adopt_now="Use the pattern: every agent output must map to a schema before entering ledgers, reports, or approval cards.",
        defer="Runtime dependency can wait because Dealix already has dependency-free generators and Pydantic available through backend code.",
        risk="Schema sprawl if every artifact invents its own incompatible fields.",
        decision="typed_contracts_now_runtime_optional",
        dealix_surface="Proof Pack / Revenue Ledgers / Design Artifacts / Approval Cards",
    ),
    ExternalRepoSignal(
        name="LlamaIndex",
        url="https://github.com/run-llama/llama_index",
        category="knowledge_and_rag_workflows",
        value_for_dealix="RAG, document indexing, data connectors, and knowledge workflows for Company Brain and Client Delivery.",
        adopt_now="Use the indexing/RAG architecture concept for Company Brain, client docs, proof packs, and internal knowledge.",
        defer="Do not add vector databases until there is a real client/data volume requirement.",
        risk="Premature RAG can become a dumping ground without source attribution and freshness controls.",
        decision="knowledge_architecture_now_runtime_later",
        dealix_surface="Company Brain / Client Proof Pack / Knowledge Base",
    ),
    ExternalRepoSignal(
        name="LiteLLM",
        url="https://github.com/BerriAI/litellm",
        category="model_gateway_routing_fallback",
        value_for_dealix="Provider abstraction, routing, fallback, budgets, and multi-model operational control.",
        adopt_now="Design Dealix AI Router around provider neutrality, budgets, fallback, and local/cloud split.",
        defer="Do not add proxy runtime unless multiple live providers are causing operational pain.",
        risk="A central proxy becomes critical infrastructure; must protect keys, logs, and rate limits.",
        decision="router_design_now_proxy_later",
        dealix_surface="AI Router / Cost Control / Local + Cloud Models",
    ),
    ExternalRepoSignal(
        name="Langfuse / Phoenix / Weave-style observability",
        url="https://github.com/langfuse/langfuse",
        category="llm_observability_traces_evals",
        value_for_dealix="Traces, evals, prompt/version tracking, and production visibility for agent outputs.",
        adopt_now="Create Dealix run logs and provenance reports first; keep every action traceable to source, prompt, model, and reviewer.",
        defer="Do not self-host observability before core loops are stable.",
        risk="Logging prompts and customer data can create privacy risk if not redacted.",
        decision="provenance_schema_now_tool_later",
        dealix_surface="Trust OS / Proof Pack / Audit Logs",
    ),
    ExternalRepoSignal(
        name="Firecrawl / Crawl4AI-style web ingestion",
        url="https://github.com/mendableai/firecrawl",
        category="web_research_ingestion",
        value_for_dealix="Website-to-markdown extraction and research ingestion for prospecting, market watch, and offer intelligence.",
        adopt_now="Define a Data Connector interface with source_url, retrieval_time, evidence_hash, and confidence fields.",
        defer="Do not crawl aggressively or bypass site protections; start with manual/public allowed sources and rate limits.",
        risk="Scraping, robots/ToS, stale evidence, and unsafe automation if not controlled.",
        decision="connector_contract_now_tool_later",
        dealix_surface="Market Watch / Prospect Research / Offer Intelligence",
    ),
)


def build_report() -> dict[str, object]:
    return {
        "generated_at": datetime.now(UTC).isoformat(),
        "safety_posture": {
            "external_send_enabled": False,
            "runtime_dependencies_added": False,
            "repositories_vendored": False,
            "mcp_enabled": False,
            "outbound_mode": "draft_only",
        },
        "recommended_next_builds": [
            "Dealix Loop Registry and loop runner contract",
            "Dealix MCP Gateway policy and tool manifest schema",
            "Dealix Data Connector interface with source/provenance fields",
            "Dealix Agent Workbench role map and handoff rules",
            "Dealix run provenance schema for audit/proof packs",
        ],
        "signals": [asdict(signal) for signal in REPO_SIGNALS],
    }


def render_markdown(payload: dict[str, object]) -> str:
    lines = [
        "# Dealix External Agent Stack Radar",
        "",
        "```text",
        f"Generated at: {payload['generated_at']}",
        "Runtime dependencies added: false",
        "Repositories vendored: false",
        "MCP enabled: false",
        "Outbound mode: draft_only",
        "```",
        "",
        "## Executive decision",
        "",
        "Dealix should not copy or vendor external AI-agent repositories. The correct move is to absorb their operating patterns into Dealix-native loops, connectors, agent skills, approval gates, and proof reports.",
        "",
        "## Priority adoption matrix",
        "",
        "| Repo / framework | Decision | Dealix surface | Why |",
        "|---|---|---|---|",
    ]
    for item in payload["signals"]:  # type: ignore[index]
        lines.append(
            "| "
            + " | ".join(
                [
                    f"[{item['name']}]({item['url']})",
                    item["decision"],
                    item["dealix_surface"],
                    item["value_for_dealix"],
                ]
            )
            + " |"
        )
    lines.extend(["", "## What to implement next", ""])
    for build in payload["recommended_next_builds"]:  # type: ignore[index]
        lines.append(f"- {build}")
    lines.extend(
        [
            "",
            "## Safety rule",
            "",
            "No external runtime should be imported into Dealix until it passes license review, security review, data-handling review, CI compatibility, and a narrow commercial use case.",
        ]
    )
    return "\n".join(lines) + "\n"


def write_outputs(output_dir: Path) -> tuple[Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    payload = build_report()
    json_path = output_dir / "external_agent_stack_radar.json"
    md_path = output_dir / "external_agent_stack_radar.md"
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    md_path.write_text(render_markdown(payload), encoding="utf-8")
    return md_path, json_path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate Dealix external agent stack radar.")
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR))
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    md_path, json_path = write_outputs(Path(args.output_dir))
    print(f"external agent stack radar: {md_path}")
    print(f"external agent stack radar json: {json_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
