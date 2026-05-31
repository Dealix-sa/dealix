"""Data boundaries — explicit walls between workspaces and sensitivity tiers."""

from __future__ import annotations

from dataclasses import dataclass

from dealix.hermes.data.classification import DataClass


@dataclass(frozen=True)
class DataBoundary:
    """An agent's maximum reachable classification."""

    agent_id: str
    max_classification: DataClass

    def can_read(self, cls: DataClass) -> bool:
        order = [
            DataClass.PUBLIC,
            DataClass.INTERNAL,
            DataClass.CONFIDENTIAL,
            DataClass.RESTRICTED,
            DataClass.SOVEREIGN,
        ]
        return order.index(cls) <= order.index(self.max_classification)


@dataclass(frozen=True)
class WorkspaceBoundary:
    """An agent's reachable workspace set."""

    agent_id: str
    workspace_ids: tuple[str, ...]

    def can_read(self, workspace_id: str) -> bool:
        return workspace_id in self.workspace_ids
