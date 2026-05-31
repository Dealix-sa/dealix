"""Hermes Agents — comprehensive multi-agent intelligence layer for Dealix.

Architecture
------------
::

    dealix/hermes/
    ├── engine.py          Anthropic SDK native tool-use agentic loop
    ├── base.py            HermesAgent abstract base class
    ├── orchestrator.py    Supervisor pattern + predefined pipelines
    ├── memory.py          Session-scoped shared context store
    ├── registry.py        Singleton agent registry
    ├── config.py          HermesConfig (Pydantic settings)
    ├── agents/            10 production specialised agents
    ├── tools/             25+ async tool functions across 5 domains
    ├── loops/             4 real recurring execution loops
    └── api/router.py      FastAPI endpoints (9 routes)

Quick start
-----------
::

    from dealix.hermes import HermesRegistry, HermesOrchestrator

    registry = HermesRegistry.instance()
    registry.build_all_agents()

    agent = registry.get("diagnostic_agent")
    result = await agent.run({"company_name": "Acme SA", "records": [...]})
"""

from dealix.hermes.agents.company_brain import CompanyBrainAgent
from dealix.hermes.agents.data_architect import DataArchitectAgent
from dealix.hermes.agents.diagnostic_agent import DiagnosticAgent
from dealix.hermes.agents.governance import GovernanceAgent
from dealix.hermes.agents.lead_intelligence import LeadIntelligenceAgent
from dealix.hermes.agents.managed_ops import ManagedOpsAgent
from dealix.hermes.agents.market_intel import MarketIntelAgent
from dealix.hermes.agents.revenue_intelligence import RevenueIntelligenceAgent
from dealix.hermes.agents.sales_intelligence import SalesIntelligenceAgent
from dealix.hermes.agents.sprint_orchestrator import SprintOrchestratorAgent
from dealix.hermes.base import HermesAgent
from dealix.hermes.config import HermesConfig, get_hermes_config
from dealix.hermes.engine import HermesEngine
from dealix.hermes.loops.lead_loop import LeadLoop
from dealix.hermes.loops.revenue_loop import RevenueLoop
from dealix.hermes.loops.sprint_loop import SprintLoop
from dealix.hermes.loops.watchdog_loop import WatchdogLoop
from dealix.hermes.memory import HermesMemory
from dealix.hermes.orchestrator import HermesOrchestrator
from dealix.hermes.registry import HermesRegistry

__all__ = [
    # Core
    "HermesEngine",
    "HermesAgent",
    "HermesOrchestrator",
    "HermesRegistry",
    "HermesMemory",
    "HermesConfig",
    "get_hermes_config",
    # Agents
    "LeadIntelligenceAgent",
    "RevenueIntelligenceAgent",
    "SprintOrchestratorAgent",
    "DiagnosticAgent",
    "DataArchitectAgent",
    "ManagedOpsAgent",
    "SalesIntelligenceAgent",
    "MarketIntelAgent",
    "CompanyBrainAgent",
    "GovernanceAgent",
    # Loops
    "RevenueLoop",
    "LeadLoop",
    "SprintLoop",
    "WatchdogLoop",
]
