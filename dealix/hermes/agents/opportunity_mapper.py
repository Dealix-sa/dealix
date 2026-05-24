"""
Opportunity mapper agent — thin wrapper around the orchestrator's
``signal_to_opportunity`` so other code can call an agent-shaped API.
"""

from __future__ import annotations

from dealix.hermes.core.schemas import HermesOpportunity, HermesSignal
from dealix.hermes.orchestrator import HermesOrchestrator

_orchestrator = HermesOrchestrator()


def map_signal(signal: HermesSignal) -> HermesOpportunity:
    return _orchestrator.signal_to_opportunity(signal)
