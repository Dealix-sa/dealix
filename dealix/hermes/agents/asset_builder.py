"""
Asset builder agent — promotes an outcome to a reusable asset.
"""

from __future__ import annotations

from dealix.hermes.core.schemas import HermesAsset, HermesOutcome
from dealix.hermes.orchestrator import HermesOrchestrator

_orchestrator = HermesOrchestrator()


def build(outcome: HermesOutcome) -> HermesAsset | None:
    return _orchestrator.outcome_to_asset(outcome)
