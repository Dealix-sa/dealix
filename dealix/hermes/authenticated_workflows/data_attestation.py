"""Verify data scope is within the declared boundary."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class DataBoundary:
    workspace_id: str
    allowed_scopes: frozenset[str]
    allowed_classifications: frozenset[str] = field(default_factory=lambda: frozenset({"public", "internal"}))


@dataclass(frozen=True)
class DataAttestation:
    workspace_id: str
    scope: str
    classification: str
    approved: bool
    reason: str = ""


def attest_data(boundary: DataBoundary, scope: str, classification: str) -> DataAttestation:
    """Return DataAttestation indicating if (scope, classification) lies inside the boundary."""
    if scope not in boundary.allowed_scopes:
        return DataAttestation(
            workspace_id=boundary.workspace_id,
            scope=scope,
            classification=classification,
            approved=False,
            reason=f"scope '{scope}' not in declared boundary",
        )
    if classification not in boundary.allowed_classifications:
        return DataAttestation(
            workspace_id=boundary.workspace_id,
            scope=scope,
            classification=classification,
            approved=False,
            reason=f"classification '{classification}' exceeds boundary",
        )
    return DataAttestation(
        workspace_id=boundary.workspace_id,
        scope=scope,
        classification=classification,
        approved=True,
    )
