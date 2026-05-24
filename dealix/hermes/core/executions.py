"""
Execution plan store.

An execution plan is what an agent or human would actually do to realise
a decision. Plans are produced by the Orchestrator after sovereignty +
trust checks. The store never *runs* anything — it records intent.
"""

from __future__ import annotations

from uuid import uuid4

from dealix.hermes.core.schemas import HermesExecutionPlan


class ExecutionStore:
    def __init__(self) -> None:
        self._plans: dict[str, HermesExecutionPlan] = {}

    def add(self, plan: HermesExecutionPlan) -> str:
        eid = str(uuid4())
        self._plans[eid] = plan
        return eid

    def get(self, eid: str) -> HermesExecutionPlan | None:
        return self._plans.get(eid)

    def awaiting_approval(self) -> list[tuple[str, HermesExecutionPlan]]:
        return [(eid, p) for eid, p in self._plans.items() if p.requires_approval]


_default_store = ExecutionStore()


def default_store() -> ExecutionStore:
    return _default_store
