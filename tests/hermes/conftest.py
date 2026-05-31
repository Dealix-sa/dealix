"""Shared fixtures for Hermes tests."""

from __future__ import annotations

import pytest

from dealix.hermes.config import seed_tools
from dealix.hermes.orchestrator import HermesOrchestrator


@pytest.fixture()
def orch() -> HermesOrchestrator:
    o = HermesOrchestrator().bootstrap()
    seed_tools(o.tool_registry)
    return o
