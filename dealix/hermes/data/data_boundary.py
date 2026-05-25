"""
DataBoundary — the per-workspace contract describing exactly which
agents may access it, which capabilities are forbidden, and whether
external output requires Sami approval.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class DataBoundary:
    workspace_id: str
    data_boundary: str = "customer_workspace_only"
    allowed_agents: tuple[str, ...] = field(default_factory=tuple)
    forbidden_exports: tuple[str, ...] = field(default_factory=tuple)
    external_output_requires_approval: bool = True


BOUNDARIES: dict[str, DataBoundary] = {}


def register_boundary(boundary: DataBoundary) -> DataBoundary:
    BOUNDARIES[boundary.workspace_id] = boundary
    return boundary


def get_boundary(workspace_id: str) -> DataBoundary | None:
    return BOUNDARIES.get(workspace_id)


register_boundary(
    DataBoundary(
        workspace_id="dealix_internal",
        data_boundary="dealix_internal_only",
        allowed_agents=("revenue_hunter", "proposal_factory", "trust_checker", "growth_engine", "value_reporter"),
        forbidden_exports=("read_sovereign_memory", "execute_sovereign_strategy"),
        external_output_requires_approval=True,
    )
)
