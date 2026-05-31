"""
End-to-end lifecycle helper: Signal → Opportunity → Decision → Execution →
Outcome → Asset → Scale/Kill.

The Kernel object holds every store and exposes a single fluent API so
business code never has to remember the order of phases.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from dealix.hermes.kernel.assets import AssetStore
from dealix.hermes.kernel.decisions import DecisionStore
from dealix.hermes.kernel.executions import ExecutionStore
from dealix.hermes.kernel.opportunities import OpportunityStore
from dealix.hermes.kernel.outcomes import OutcomeStore
from dealix.hermes.kernel.schemas import LifecycleEvent
from dealix.hermes.kernel.signals import SignalStore


@dataclass
class HermesKernel:
    """Bundle of all seven phase stores plus a unified event log."""

    signals: SignalStore = field(default_factory=SignalStore)
    opportunities: OpportunityStore = field(default_factory=OpportunityStore)
    decisions: DecisionStore = field(default_factory=DecisionStore)
    executions: ExecutionStore = field(default_factory=ExecutionStore)
    outcomes: OutcomeStore = field(default_factory=OutcomeStore)
    assets: AssetStore = field(default_factory=AssetStore)

    def all_events(self) -> list[LifecycleEvent]:
        events: list[LifecycleEvent] = []
        events.extend(self.signals.events())
        events.extend(self.opportunities.events())
        events.extend(self.decisions.events())
        events.extend(self.executions.events())
        events.extend(self.outcomes.events())
        events.extend(self.assets.events())
        events.sort(key=lambda e: e.occurred_at)
        return events


_default_kernel: HermesKernel | None = None


def get_kernel() -> HermesKernel:
    """Process-wide default kernel. Tests build their own."""
    global _default_kernel
    if _default_kernel is None:
        _default_kernel = HermesKernel()
    return _default_kernel


def reset_default_kernel() -> None:
    global _default_kernel
    _default_kernel = None
