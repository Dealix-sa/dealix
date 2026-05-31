"""Hermes FastAPI router — 9 endpoints for agent execution, pipelines, and health."""

from __future__ import annotations

import time
from typing import Any

import structlog
from fastapi import APIRouter, BackgroundTasks, HTTPException
from pydantic import BaseModel, Field

from dealix.hermes.config import get_hermes_config
from dealix.hermes.memory import HermesMemory
from dealix.hermes.orchestrator import HermesOrchestrator
from dealix.hermes.registry import HermesRegistry

logger = structlog.get_logger(__name__)

hermes_router = APIRouter(prefix="/hermes", tags=["hermes"])

# Shared singletons
_registry = HermesRegistry.instance()
_memory = HermesMemory()
_config = get_hermes_config()
_orchestrator = HermesOrchestrator(registry=_registry, memory=_memory, config=_config)


# ------------------------------------------------------------------
# Request / Response models
# ------------------------------------------------------------------

class HermesResponse(BaseModel):
    success: bool
    data: dict[str, Any] = Field(default_factory=dict)
    agent: str = ""
    duration_ms: int = 0
    tokens_used: int = 0
    error: str | None = None


class AgentRunRequest(BaseModel):
    input_data: dict[str, Any] = Field(default_factory=dict)
    session_id: str | None = None


class PipelineRunRequest(BaseModel):
    input_data: dict[str, Any] = Field(default_factory=dict)
    session_id: str | None = None


class SupervisorRequest(BaseModel):
    goal: str
    agents: list[str] = Field(default_factory=list)
    initial_context: dict[str, Any] = Field(default_factory=dict)
    max_iterations: int = 10


class SprintStartRequest(BaseModel):
    client_data: dict[str, Any]
    sprint_id: str | None = None


class LeadBatchRequest(BaseModel):
    leads: list[dict[str, Any]]


# ------------------------------------------------------------------
# Ensure agents are initialised on first request
# ------------------------------------------------------------------

_agents_initialised = False


def _ensure_agents() -> None:
    global _agents_initialised
    if not _agents_initialised:
        try:
            _registry.build_all_agents(config=_config)
            _agents_initialised = True
            logger.info("hermes_agents_initialised", count=len(_registry.list_agents()))
        except Exception as exc:
            logger.warning("hermes_agents_init_warning", error=str(exc))


# ------------------------------------------------------------------
# Endpoints
# ------------------------------------------------------------------

@hermes_router.get("/health", response_model=HermesResponse)
async def hermes_health() -> HermesResponse:
    """Hermes system health — agents, API key, tool modules."""
    from dealix.hermes.loops.watchdog_loop import WatchdogLoop
    _ensure_agents()
    watchdog = WatchdogLoop(config=_config)
    health = await watchdog.run_once()
    return HermesResponse(
        success=health.get("status") == "healthy",
        data=health,
        agent="watchdog",
    )


@hermes_router.get("/agents", response_model=HermesResponse)
async def list_agents() -> HermesResponse:
    """List all registered Hermes agents."""
    _ensure_agents()
    names = _registry.list_agents()
    agents_info = []
    for name in names:
        try:
            agent = _registry.get(name)
            agents_info.append({"name": agent.name, "description": agent.description})
        except Exception:
            agents_info.append({"name": name, "description": "unknown"})
    return HermesResponse(success=True, data={"agents": agents_info, "count": len(agents_info)})


@hermes_router.get("/agents/{agent_name}", response_model=HermesResponse)
async def get_agent_info(agent_name: str) -> HermesResponse:
    """Get info for a specific agent."""
    _ensure_agents()
    try:
        agent = _registry.get(agent_name)
        return HermesResponse(
            success=True,
            data={
                "name": agent.name,
                "description": agent.description,
                "tools": [t["name"] for t in agent.tools_schema],
            },
            agent=agent_name,
        )
    except KeyError:
        raise HTTPException(status_code=404, detail=f"Agent '{agent_name}' not found")


@hermes_router.post("/agents/{agent_name}/run", response_model=HermesResponse)
async def run_agent(agent_name: str, request: AgentRunRequest) -> HermesResponse:
    """Run a specific Hermes agent with the provided input data."""
    _ensure_agents()
    try:
        agent = _registry.get(agent_name)
    except KeyError:
        raise HTTPException(status_code=404, detail=f"Agent '{agent_name}' not found")

    started = time.monotonic()
    try:
        result = await agent.run(request.input_data)
        duration_ms = int((time.monotonic() - started) * 1000)
        tokens = result.get("usage", {}).get("total_tokens", 0)
        logger.info("hermes_agent_run", agent=agent_name, duration_ms=duration_ms, tokens=tokens)
        return HermesResponse(
            success=True,
            data=result,
            agent=agent_name,
            duration_ms=duration_ms,
            tokens_used=tokens,
        )
    except Exception as exc:
        logger.exception("hermes_agent_run_error", agent=agent_name, error=str(exc))
        raise HTTPException(status_code=500, detail=str(exc))


@hermes_router.post("/pipeline/{pipeline_name}", response_model=HermesResponse)
async def run_pipeline(pipeline_name: str, request: PipelineRunRequest) -> HermesResponse:
    """Execute a predefined multi-agent pipeline.

    Available pipelines: ``revenue_sprint``, ``lead_qualification``,
    ``free_diagnostic``, ``managed_ops_weekly``, ``data_pack_build``.
    """
    _ensure_agents()
    started = time.monotonic()
    try:
        result = await _orchestrator.run_pipeline(
            pipeline_name=pipeline_name,
            input_data=request.input_data,
            session_id=request.session_id,
        )
        duration_ms = int((time.monotonic() - started) * 1000)
        return HermesResponse(
            success=True,
            data=result,
            agent=f"pipeline:{pipeline_name}",
            duration_ms=duration_ms,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception as exc:
        logger.exception("hermes_pipeline_error", pipeline=pipeline_name, error=str(exc))
        raise HTTPException(status_code=500, detail=str(exc))


@hermes_router.post("/orchestrate", response_model=HermesResponse)
async def orchestrate(request: SupervisorRequest) -> HermesResponse:
    """Run the supervisor loop: an LLM-driven meta-agent achieves a goal using available agents."""
    _ensure_agents()
    agents_to_use = request.agents or _registry.list_agents()
    started = time.monotonic()
    try:
        result = await _orchestrator.run_supervisor_loop(
            goal=request.goal,
            available_agents=agents_to_use,
            initial_context=request.initial_context,
            max_iterations=request.max_iterations,
        )
        duration_ms = int((time.monotonic() - started) * 1000)
        return HermesResponse(
            success=True,
            data=result,
            agent="supervisor",
            duration_ms=duration_ms,
        )
    except Exception as exc:
        logger.exception("hermes_orchestrate_error", error=str(exc))
        raise HTTPException(status_code=500, detail=str(exc))


@hermes_router.post("/loops/revenue/start", response_model=HermesResponse)
async def start_revenue_loop(
    tenant_id: str,
    background_tasks: BackgroundTasks,
) -> HermesResponse:
    """Start the revenue intelligence loop as a background task."""
    _ensure_agents()
    from dealix.hermes.loops.revenue_loop import RevenueLoop

    loop = RevenueLoop(orchestrator=_orchestrator, config=_config)

    async def _run() -> None:
        await loop.run_once(tenant_id=tenant_id)

    background_tasks.add_task(_run)
    return HermesResponse(
        success=True,
        data={"status": "started", "tenant_id": tenant_id, "mode": "background_once"},
        agent="revenue_loop",
    )


@hermes_router.post("/loops/lead/batch", response_model=HermesResponse)
async def process_lead_batch(request: LeadBatchRequest) -> HermesResponse:
    """Process a batch of leads through the LeadIntelligenceAgent."""
    _ensure_agents()
    from dealix.hermes.loops.lead_loop import LeadLoop

    started = time.monotonic()
    loop = LeadLoop(config=_config, orchestrator=_orchestrator)
    result = await loop.run_once(leads=request.leads)
    duration_ms = int((time.monotonic() - started) * 1000)

    return HermesResponse(
        success=result.get("status") == "complete",
        data=result,
        agent="lead_loop",
        duration_ms=duration_ms,
    )


@hermes_router.post("/sprint/start", response_model=HermesResponse)
async def start_sprint(request: SprintStartRequest) -> HermesResponse:
    """Start a new 7-day Revenue Intelligence Sprint."""
    _ensure_agents()
    from dealix.hermes.loops.sprint_loop import SprintLoop

    started = time.monotonic()
    sprint_loop = SprintLoop(config=_config)
    result = await sprint_loop.run_sprint(
        client_data=request.client_data,
        sprint_id=request.sprint_id,
    )
    duration_ms = int((time.monotonic() - started) * 1000)
    tokens = result.get("usage", {}).get("total_tokens", 0)

    return HermesResponse(
        success=result.get("status") == "complete",
        data=result,
        agent="sprint_loop",
        duration_ms=duration_ms,
        tokens_used=tokens,
    )
