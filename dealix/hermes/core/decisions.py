"""
Decision memo store.

Decisions are the bridge between an Opportunity and an Execution. They are
the artifacts Sami reviews when sovereignty requires approval.
"""

from __future__ import annotations

from uuid import uuid4

from dealix.hermes.core.schemas import HermesDecisionMemo


class DecisionStore:
    def __init__(self) -> None:
        self._memos: dict[str, HermesDecisionMemo] = {}

    def add(self, memo: HermesDecisionMemo) -> str:
        did = str(uuid4())
        self._memos[did] = memo
        return did

    def get(self, did: str) -> HermesDecisionMemo | None:
        return self._memos.get(did)

    def pending_approvals(self) -> list[tuple[str, HermesDecisionMemo]]:
        return [(did, m) for did, m in self._memos.items() if m.approval_required]


_default_store = DecisionStore()


def default_store() -> DecisionStore:
    return _default_store
