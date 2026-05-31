"""Shared FastAPI dependency: a process-wide Hermes orchestrator."""

from __future__ import annotations

from fastapi import Depends

from dealix.hermes.config import seed_tools
from dealix.hermes.orchestrator import HermesOrchestrator, get_orchestrator


_seeded = False


def get_hermes() -> HermesOrchestrator:
    global _seeded
    orch = get_orchestrator()
    if not _seeded:
        seed_tools(orch.tool_registry)
        _seeded = True
    return orch


HermesDep = Depends(get_hermes)
